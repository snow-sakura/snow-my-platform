import { useState, useRef, useCallback } from 'react'
import { 
  Upload, Button, Steps, Card, Typography, Input, 
  Table, Tag, Space, message, Spin, Empty, Tooltip,
  Modal, Descriptions, Popconfirm
} from 'antd'
import { 
  UploadOutlined, FileImageOutlined, FileExcelOutlined,
  EyeOutlined, DownloadOutlined, DeleteOutlined, 
  SendOutlined, ReloadOutlined, CheckCircleOutlined,
  RobotOutlined, FileTextOutlined, ExperimentOutlined,
  LoadingOutlined, ThunderboltOutlined
} from '@ant-design/icons'
import { XStream } from '@ant-design/x'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const { Title, Text, Paragraph } = Typography
const { TextArea } = Input

// API 基础 URL
const API_BASE = '/api'

function App() {
  // 状态管理
  const [currentStep, setCurrentStep] = useState(0)
  const [uploadedFile, setUploadedFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [context, setContext] = useState('')
  const [requirements, setRequirements] = useState('')
  const [analysisResult, setAnalysisResult] = useState('')
  const [testcases, setTestcases] = useState([])
  const [streamingContent, setStreamingContent] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentStage, setCurrentStage] = useState('')
  const [selectedTestcase, setSelectedTestcase] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  
  const abortRef = useRef(null)

  // 步骤配置
  const steps = [
    { title: '上传图片', icon: <FileImageOutlined /> },
    { title: '需求分析', icon: <ExperimentOutlined /> },
    { title: '生成用例', icon: <RobotOutlined /> },
    { title: '导出结果', icon: <FileExcelOutlined /> },
  ]

  // 处理文件上传
  const handleUpload = useCallback((file) => {
    const isImage = file.type.startsWith('image/')
    if (!isImage) {
      message.error('请上传图片文件！')
      return false
    }
    
    const isLt10M = file.size / 1024 / 1024 < 10
    if (!isLt10M) {
      message.error('图片大小不能超过 10MB！')
      return false
    }

    setUploadedFile(file)
    
    // 生成预览
    const reader = new FileReader()
    reader.onload = (e) => {
      setImagePreview(e.target.result)
      setCurrentStep(1)
    }
    reader.readAsDataURL(file)
    
    return false
  }, [])

  // 清除上传
  const handleClear = useCallback(() => {
    setUploadedFile(null)
    setImagePreview(null)
    setAnalysisResult('')
    setTestcases([])
    setStreamingContent('')
    setCurrentStep(0)
    setCurrentStage('')
  }, [])

  // 开始生成（分析+生成）
  const handleGenerate = useCallback(async () => {
    if (!uploadedFile) {
      message.error('请先上传图片')
      return
    }

    setIsProcessing(true)
    setStreamingContent('')
    setAnalysisResult('')
    setTestcases([])
    
    const controller = new AbortController()
    abortRef.current = controller

    try {
      const formData = new FormData()
      formData.append('file', uploadedFile)
      formData.append('context', context)
      formData.append('requirements', requirements)

      const response = await fetch(`${API_BASE}/generate-all`, {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      })

      if (!response.ok || !response.body) {
        throw new Error(`HTTP ${response.status}`)
      }

      let tempAnalysis = ''
      let tempTestcase = ''

      for await (const chunk of XStream({ readableStream: response.body })) {
        if (!chunk?.data) continue
        
        const data = JSON.parse(chunk.data)
        
        if (data.type === 'stage') {
          setCurrentStage(data.message)
          if (data.stage === 'analysis_start') {
            setCurrentStep(1)
          } else if (data.stage === 'generation_start') {
            setCurrentStep(2)
          }
        } else if (data.type === 'analysis') {
          tempAnalysis += data.content
          setStreamingContent(tempAnalysis)
          setAnalysisResult(tempAnalysis)
        } else if (data.type === 'testcase') {
          tempTestcase += data.content
          setStreamingContent(tempTestcase)
        } else if (data.type === 'complete') {
          if (data.data) {
            setTestcases(Array.isArray(data.data) ? data.data : [data.data])
          }
          setCurrentStep(3)
        } else if (data.type === 'done') {
          setCurrentStep(3)
        } else if (data.type === 'error') {
          message.error(data.error)
        }
      }

      // 尝试解析测试用例
      try {
        const jsonMatch = tempTestcase.match(/\[[\s\S]*\]/)
        if (jsonMatch) {
          const parsed = JSON.parse(jsonMatch[0])
          setTestcases(Array.isArray(parsed) ? parsed : [parsed])
        }
      } catch (e) {
        console.log('解析测试用例失败，显示原始内容')
      }

    } catch (error) {
      if (error.name === 'AbortError') {
        message.info('已取消生成')
      } else {
        message.error(`生成失败: ${error.message}`)
      }
    } finally {
      setIsProcessing(false)
      abortRef.current = null
    }
  }, [uploadedFile, context, requirements])

  // 停止生成
  const handleStop = useCallback(() => {
    if (abortRef.current) {
      abortRef.current.abort()
      abortRef.current = null
    }
  }, [])

  // 导出 Excel
  const handleExport = useCallback(async () => {
    if (testcases.length === 0) {
      message.error('没有可导出的测试用例')
      return
    }

    try {
      const response = await fetch(`${API_BASE}/export-excel`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ testcases }),
      })

      if (!response.ok) {
        throw new Error('导出失败')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `测试用例_${new Date().toISOString().slice(0, 10)}.xlsx`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      message.success('导出成功！')
    } catch (error) {
      message.error(`导出失败: ${error.message}`)
    }
  }, [testcases])

  // 下载模板
  const handleDownloadTemplate = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/download-template`)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = '测试用例模板.xlsx'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      message.error('模板下载失败')
    }
  }, [])

  // 查看用例详情
  const handleViewDetail = useCallback((record) => {
    setSelectedTestcase(record)
    setIsModalOpen(true)
  }, [])

  // 表格列定义
  const columns = [
    {
      title: '编号',
      dataIndex: 'id',
      key: 'id',
      width: 100,
      fixed: 'left',
    },
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      width: 300,
      ellipsis: true,
    },
    {
      title: '模块',
      dataIndex: 'module',
      key: 'module',
      width: 120,
    },
    {
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
      width: 100,
      render: (priority) => (
        <Tag className={`priority-badge priority-${priority?.toLowerCase()}`}>
          {priority}
        </Tag>
      ),
    },
    {
      title: '类型',
      dataIndex: 'test_type',
      key: 'test_type',
      width: 100,
      render: (type) => (
        <span className="type-badge">{type}</span>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 100,
      fixed: 'right',
      render: (_, record) => (
        <Button 
          type="text" 
          icon={<EyeOutlined />}
          onClick={() => handleViewDetail(record)}
        >
          查看
        </Button>
      ),
    },
  ]

  return (
    <div className="app-container">
      {/* 头部 */}
      <header className="header">
        <div className="header-logo">
          <div className="header-logo-icon">
            <ThunderboltOutlined />
          </div>
          <span className="header-logo-text">TestCase AI</span>
        </div>
        <Space>
          <Button 
            icon={<FileExcelOutlined />}
            onClick={handleDownloadTemplate}
          >
            下载模板
          </Button>
          {testcases.length > 0 && (
            <Button 
              type="primary"
              icon={<DownloadOutlined />}
              onClick={handleExport}
            >
              导出 Excel
            </Button>
          )}
        </Space>
      </header>

      {/* 主内容 */}
      <main className="main-content">
        {/* 步骤条 */}
        <Card style={{ marginBottom: 24 }}>
          <Steps current={currentStep} items={steps} />
        </Card>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
          {/* 左侧：上传和配置 */}
          <div>
            {/* 图片上传 */}
            <Card 
              title="上传需求图片" 
              className="gemini-card"
              style={{ marginBottom: 24 }}
            >
              {!imagePreview ? (
                <Upload.Dragger
                  accept="image/*"
                  beforeUpload={handleUpload}
                  showUploadList={false}
                  disabled={isProcessing}
                >
                  <div className="upload-area">
                    <p className="upload-icon">
                      <FileImageOutlined />
                    </p>
                    <p className="upload-text">
                      点击或拖拽上传图片
                    </p>
                    <p className="upload-hint">
                      支持思维导图、流程图、界面截图等（最大 10MB）
                    </p>
                  </div>
                </Upload.Dragger>
              ) : (
                <div className="image-preview">
                  <img src={imagePreview} alt="预览" />
                  <button 
                    className="image-preview-remove"
                    onClick={handleClear}
                    disabled={isProcessing}
                  >
                    <DeleteOutlined />
                  </button>
                </div>
              )}
            </Card>

            {/* 配置信息 */}
            <Card title="配置信息" className="gemini-card">
              <div style={{ marginBottom: 16 }}>
                <Text strong>项目背景</Text>
                <TextArea
                  placeholder="描述项目背景、业务场景等信息..."
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                  rows={3}
                  style={{ marginTop: 8 }}
                  disabled={isProcessing}
                />
              </div>
              <div>
                <Text strong>具体要求</Text>
                <TextArea
                  placeholder="描述具体的测试需求、重点关注的功能点..."
                  value={requirements}
                  onChange={(e) => setRequirements(e.target.value)}
                  rows={3}
                  style={{ marginTop: 8 }}
                  disabled={isProcessing}
                />
              </div>
              
              <div style={{ marginTop: 24, textAlign: 'center' }}>
                {!isProcessing ? (
                  <Button
                    type="primary"
                    size="large"
                    icon={<SendOutlined />}
                    onClick={handleGenerate}
                    disabled={!uploadedFile}
                    style={{ 
                      background: 'var(--primary-gradient)',
                      border: 'none',
                      height: 48,
                      padding: '0 48px',
                    }}
                  >
                    开始生成
                  </Button>
                ) : (
                  <Button
                    danger
                    size="large"
                    icon={<ReloadOutlined spin />}
                    onClick={handleStop}
                    style={{ height: 48, padding: '0 48px' }}
                  >
                    停止生成
                  </Button>
                )}
              </div>
            </Card>
          </div>

          {/* 右侧：结果展示 */}
          <div>
            {/* 流式输出 */}
            {isProcessing && (
              <Card 
                title={
                  <Space>
                    <Spin indicator={<LoadingOutlined spin />} />
                    <span>{currentStage || '处理中...'}</span>
                  </Space>
                }
                className="gemini-card"
                style={{ marginBottom: 24 }}
              >
                <div className="streaming-content">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {streamingContent || '等待输出...'}
                  </ReactMarkdown>
                </div>
              </Card>
            )}

            {/* 测试用例列表 */}
            {testcases.length > 0 && !isProcessing && (
              <Card 
                title={`测试用例列表 (${testcases.length} 条)`}
                className="gemini-card"
              >
                <Table
                  columns={columns}
                  dataSource={testcases}
                  rowKey="id"
                  pagination={{ pageSize: 10 }}
                  scroll={{ x: 800 }}
                  size="small"
                />
              </Card>
            )}

            {/* 空状态 */}
            {!isProcessing && testcases.length === 0 && !streamingContent && (
              <Card className="gemini-card">
                <Empty
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                  description={
                    <div className="empty-state">
                      <p className="empty-state-title">开始生成测试用例</p>
                      <p className="empty-state-desc">
                        上传需求图片，AI 将自动分析并生成专业测试用例
                      </p>
                    </div>
                  }
                />
              </Card>
            )}
          </div>
        </div>
      </main>

      {/* 用例详情弹窗 */}
      <Modal
        title="测试用例详情"
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
        width={700}
      >
        {selectedTestcase && (
          <Descriptions bordered column={1}>
            <Descriptions.Item label="用例编号">
              {selectedTestcase.id}
            </Descriptions.Item>
            <Descriptions.Item label="用例标题">
              {selectedTestcase.title}
            </Descriptions.Item>
            <Descriptions.Item label="所属模块">
              {selectedTestcase.module}
            </Descriptions.Item>
            <Descriptions.Item label="前置条件">
              {selectedTestcase.precondition}
            </Descriptions.Item>
            <Descriptions.Item label="测试步骤">
              <ol>
                {Array.isArray(selectedTestcase.steps) ? (
                  selectedTestcase.steps.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))
                ) : (
                  <li>{selectedTestcase.steps}</li>
                )}
              </ol>
            </Descriptions.Item>
            <Descriptions.Item label="预期结果">
              {selectedTestcase.expected_result}
            </Descriptions.Item>
            <Descriptions.Item label="优先级">
              <Tag className={`priority-badge priority-${selectedTestcase.priority?.toLowerCase()}`}>
                {selectedTestcase.priority}
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="测试类型">
              <span className="type-badge">{selectedTestcase.test_type}</span>
            </Descriptions.Item>
          </Descriptions>
        )}
      </Modal>
    </div>
  )
}

export default App
