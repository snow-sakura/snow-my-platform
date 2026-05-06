import { useState, useRef, useEffect } from 'react'
import ChatContainer from './components/ChatContainer'
import MessageList from './components/MessageList'
import InputArea from './components/InputArea'
import { sendMessage } from './services/chatService'

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [streamingContent, setStreamingContent] = useState('')
  const [currentAgent, setCurrentAgent] = useState('') // 当前正在输出的智能体
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, streamingContent])

  const handleSendMessage = async (content) => {
    if (!content.trim() || isLoading) return

    const userMessage = { role: 'user', content }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setStreamingContent('')
    setCurrentAgent('')

    try {
      // 存储流式内容
      let fullResponse = ''
      let agentResponse = ''
      let lastAgent = ''
      
      await sendMessage(content, (chunk) => {
        // 检测智能体角色切换
        if (chunk.includes('【测试用例设计师】')) {
          if (lastAgent && agentResponse) {
            fullResponse += `\n\n【测试用例设计师】\n${agentResponse}`
          }
          lastAgent = '测试用例设计师'
          agentResponse = ''
          setCurrentAgent('测试用例设计师')
        } else if (chunk.includes('【测试用例评审师】')) {
          if (lastAgent && agentResponse) {
            fullResponse += `\n\n【测试用例评审师】\n${agentResponse}`
          }
          lastAgent = '测试用例评审师'
          agentResponse = ''
          setCurrentAgent('测试用例评审师')
        } else if (chunk.includes('【用户评审】')) {
          if (lastAgent && agentResponse) {
            fullResponse += `\n\n【用户评审】\n${agentResponse}`
          }
          lastAgent = '用户评审'
          agentResponse = ''
          setCurrentAgent('用户评审')
        } else if (chunk.includes('--- 用户评审完成 ---')) {
          // 用户评审完成，标记为结束
          if (agentResponse) {
            fullResponse += `\n\n${agentResponse}`
          }
          agentResponse = ''
        } else {
          // 普通内容
          agentResponse += chunk
        }
        
        setStreamingContent(fullResponse + (agentResponse ? `\n\n${lastAgent ? '【' + lastAgent + '】' : ''}\n${agentResponse}` : ''))
      })

      // 流式完成后，将完整内容添加到消息列表
      const finalResponse = fullResponse + (agentResponse ? `\n\n${lastAgent ? '【' + lastAgent + '】' : ''}\n${agentResponse}` : '')
      setMessages(prev => [...prev, { role: 'assistant', content: finalResponse }])
      setStreamingContent('')
      setCurrentAgent('')
    } catch (error) {
      console.error('Error sending message:', error)
      setMessages(prev => [...prev, { role: 'assistant', content: '抱歉，发生了错误，请稍后再试。' }])
      setStreamingContent('')
      setCurrentAgent('')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app">
      <ChatContainer>
        <MessageList 
          messages={messages}
          streamingContent={streamingContent}
          isLoading={isLoading}
          messagesEndRef={messagesEndRef}
          currentAgent={currentAgent}
        />
        <InputArea onSendMessage={handleSendMessage} isLoading={isLoading} />
      </ChatContainer>
    </div>
  )
}

export default App
