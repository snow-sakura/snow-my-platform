import { ref } from 'vue'
import { message } from 'ant-design-vue'

export function useSSE() {
  const eventSource = ref(null)
  const messages = ref([])
  const isConnected = ref(false)
  const isProcessing = ref(false)
  const isWaitingForInput = ref(false)
  const sessionId = ref(null)
  const reconnectTimer = ref(null)
  const maxReconnectAttempts = 5
  const reconnectAttempts = ref(0)

  // API基础URL
  const getBaseUrl = () => {
    return import.meta.env.DEV ? 'http://localhost:8000' : ''
  }

  // 创建会话
  const createSession = async () => {
    try {
      const response = await fetch(`${getBaseUrl()}/api/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to create session')
      }
      
      const data = await response.json()
      sessionId.value = data.session_id
      console.log('Session created:', sessionId.value)
      return data.session_id
    } catch (error) {
      console.error('Error creating session:', error)
      message.error('创建会话失败')
      throw error
    }
  }

  // 连接SSE
  const connect = async () => {
    return new Promise(async (resolve, reject) => {
      try {
        // 先创建会话
        if (!sessionId.value) {
          await createSession()
        }

        // 关闭之前的连接
        if (eventSource.value) {
          eventSource.value.close()
        }

        // 建立SSE连接
        const sseUrl = `${getBaseUrl()}/api/stream/${sessionId.value}`
        console.log('[DEBUG] Connecting to SSE:', sseUrl)
        eventSource.value = new EventSource(sseUrl)

        eventSource.value.onopen = () => {
          console.log('SSE connected')
          isConnected.value = true
          reconnectAttempts.value = 0
          message.success('已连接到服务器')
          resolve()
        }

        eventSource.value.addEventListener('connected', (event) => {
          console.log('[DEBUG] SSE connection confirmed:', event.data)
        })

        eventSource.value.addEventListener('message', (event) => {
          try {
            const data = JSON.parse(event.data)
            console.log('[DEBUG] Received generic message event:', data)
            handleEvent(data)
          } catch (error) {
            console.error('Failed to parse SSE message:', error)
          }
        })

        eventSource.value.addEventListener('processing', (event) => {
          const data = JSON.parse(event.data)
          console.log('[DEBUG] Processing event received:', data)
          isProcessing.value = true
          isWaitingForInput.value = false
        })

        eventSource.value.addEventListener('AgentResponse', (event) => {
          try {
            const data = JSON.parse(event.data)
            console.log('[DEBUG] AgentResponse event received:', data)
            handleAgentResponse(data)
          } catch (error) {
            console.error('Failed to parse AgentResponse:', error)
          }
        })

        eventSource.value.addEventListener('done', (event) => {
          const data = JSON.parse(event.data)
          console.log('[DEBUG] Done event received:', data)
          console.log('Conversation completed')
          isProcessing.value = false
          isWaitingForInput.value = false
        })

        eventSource.value.addEventListener('error', (event) => {
          console.log('[DEBUG] Error event received:', event.data)
          try {
            const data = JSON.parse(event.data)
            message.error(data.content || '发生错误')
          } catch (e) {
            message.error('SSE连接错误')
          }
          isProcessing.value = false
        })

        eventSource.value.onerror = (error) => {
          console.error('[ERROR] SSE onerror triggered')
          console.error('[ERROR] readyState:', eventSource.value?.readyState)
          
          // SSE的onerror在以下情况会被触发：
          // 1. 正常连接关闭（浏览器重连机制）
          // 2. 真正的连接错误
          // readyState: 0=CONNECTING, 1=OPEN, 2=CLOSED
          
          if (eventSource.value?.readyState === EventSource.CLOSED) {
            console.log('[DEBUG] SSE connection closed by server or network issue')
            isConnected.value = false
            
            // 尝试重连
            if (reconnectAttempts.value < maxReconnectAttempts) {
              reconnectAttempts.value++
              console.log(`Attempting to reconnect (${reconnectAttempts.value}/${maxReconnectAttempts})...`)
              
              if (reconnectTimer.value) {
                clearTimeout(reconnectTimer.value)
              }
              
              reconnectTimer.value = setTimeout(() => {
                // 重新创建会话并连接
                sessionId.value = null
                connect().catch(() => {})
              }, 3000)
            } else {
              message.error('连接断开,请刷新页面重试')
              reject(error)
            }
          } else if (eventSource.value?.readyState === EventSource.CONNECTING) {
            // 浏览器正在自动重连，不需要额外处理
            console.log('[DEBUG] Browser is auto-reconnecting SSE...')
          }
        }
      } catch (error) {
        console.error('Failed to create SSE connection:', error)
        reject(error)
      }
    })
  }

  // 处理通用事件
  const handleEvent = (data) => {
    console.log('Received event:', data)

    // 处理系统消息
    if (data.type === 'UserInputRequest') {
      // 标记正在等待用户输入
      isWaitingForInput.value = true
      console.log('[DEBUG] AI is waiting for user input')
      return
    }

    if (data.type === 'error') {
      message.error(data.content || '发生错误')
      isProcessing.value = false
      isWaitingForInput.value = false
      return
    }
  }

  // 处理Agent响应
  const handleAgentResponse = (data) => {
    // 过滤掉 user_proxy 的中间消息
    if (data.source === 'user_proxy') {
      return
    }

    const newMessage = {
      id: Date.now() + Math.random(),
      content: data.content || '',
      source: data.source || 'assistant',
      timestamp: data.timestamp || new Date().toISOString(),
      type: 'AgentResponse'
    }

    messages.value.push(newMessage)
    // 收到 AgentResponse 表示对话结束，停止 processing
    isProcessing.value = false
    isWaitingForInput.value = false
  }

  // 发送消息（HTTP POST）
  const sendMessage = async ({ content, attachment }) => {
    if (!sessionId.value) {
      message.error('未连接到服务器')
      return false
    }

    try {
      const payload = {
        session_id: sessionId.value,
        content: content,
        attachment: attachment || null
      }
      
      const response = await fetch(`${getBaseUrl()}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })

      if (!response.ok) {
        throw new Error('Failed to send message')
      }

      // 添加用户消息到列表
      messages.value.push({
        id: Date.now(),
        content: content,
        source: 'user',
        timestamp: new Date().toISOString(),
        type: 'TextMessage'
      })

      isProcessing.value = true
      return true
    } catch (error) {
      console.error('Failed to send message:', error)
      message.error('发送失败')
      return false
    }
  }

  // 断开连接
  const disconnect = () => {
    if (eventSource.value) {
      eventSource.value.close()
      eventSource.value = null
      isConnected.value = false
      isProcessing.value = false
    }
    
    if (reconnectTimer.value) {
      clearTimeout(reconnectTimer.value)
      reconnectTimer.value = null
    }
  }

  // 清空消息
  const clearMessages = () => {
    messages.value = []
  }

  return {
    connect,
    disconnect,
    sendMessage,
    messages,
    isConnected,
    isProcessing,
    isWaitingForInput,
    clearMessages
  }
}
