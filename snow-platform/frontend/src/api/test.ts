import request from '@/utils/request'

export interface TestPoint {
  id: number
  project_id: number
  document_id?: number
  title: string
  description?: string
  priority: string
  category?: string
  is_verified: boolean
  verified_by?: string
  verified_at?: string
  created_at: string
}

export interface TestCase {
  id: number
  project_id: number
  test_point_id: number
  case_number?: string
  title: string
  precondition?: string
  steps?: Array<{ step: string; expected_result: string }>
  expected_result?: string
  priority: string
  case_type?: string
  created_at: string
}

export interface TaskBatch {
  id: number
  project_id: number
  task_type: string
  status: string
  progress: number
  total_count: number
  completed_count: number
  error_message?: string
  started_at?: string
  completed_at?: string
  created_at: string
}

// 提取测试点
export const extractTestPoints = (documentIds: number[], knowledgeBaseIds?: number[]) => {
  return request.post('/test-points/extract', {
    document_ids: documentIds,
    knowledge_base_ids: knowledgeBaseIds
  })
}

// 获取测试点列表
export const getTestPoints = (projectId: number) => {
  return request.get<TestPoint[]>(`/test-points/project/${projectId}`)
}

export interface TestPointCreate {
  title: string
  description?: string
  priority?: string
  category?: string
}

export interface TestCaseCreate {
  test_point_id: number
  title: string
  precondition?: string
  steps?: Array<{ step: string; expected_result: string }>
  expected_result?: string
  priority?: string
  case_type?: string
}

export interface TestCaseUpdate {
  title?: string
  precondition?: string
  steps?: Array<{ step: string; expected_result: string }>
  expected_result?: string
  priority?: string
  case_type?: string
}

// 手动创建测试点
export const createTestPoint = (projectId: number, data: TestPointCreate) => {
  return request.post<TestPoint>(`/test-points/?project_id=${projectId}`, data)
}

// 更新测试点
export const updateTestPoint = (id: number, data: any) => {
  return request.put<TestPoint>(`/test-points/${id}`, data)
}

// 删除测试点
export const deleteTestPoint = (id: number) => {
  return request.delete(`/test-points/${id}`)
}

// 生成测试用例
export const generateTestCases = (testPointIds: number[], knowledgeBaseIds?: number[]) => {
  return request.post('/test-cases/generate', {
    test_point_ids: testPointIds,
    knowledge_base_ids: knowledgeBaseIds
  })
}

// 获取测试用例列表
export const getTestCases = (projectId: number) => {
  return request.get<TestCase[]>(`/test-cases/project/${projectId}`)
}

// 获取测试用例详情
export const getTestCase = (id: number) => {
  return request.get<TestCase>(`/test-cases/${id}`)
}

// 手动创建测试用例
export const createTestCase = (projectId: number, data: TestCaseCreate) => {
  return request.post<TestCase>(`/test-cases/?project_id=${projectId}`, data)
}

// 更新测试用例
export const updateTestCase = (id: number, data: TestCaseUpdate) => {
  return request.put<TestCase>(`/test-cases/${id}`, data)
}

// 删除测试用例
export const deleteTestCase = (id: number) => {
  return request.delete(`/test-cases/${id}`)
}

// 导出测试用例
export const exportTestCases = (projectId: number) => {
  return request.get(`/test-cases/export/${projectId}`, {
    responseType: 'blob'
  })
}

// 获取任务批次
export const getTaskBatch = (batchId: number) => {
  return request.get<TaskBatch>(`/batches/${batchId}`)
}

// 获取项目任务批次
export const getProjectBatches = (projectId: number) => {
  return request.get<TaskBatch[]>(`/batches/project/${projectId}`)
}

// 取消任务批次
export const cancelBatch = (batchId: number) => {
  return request.put(`/batches/${batchId}/cancel`)
}
