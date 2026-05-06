import React from 'react'
import ReactMarkdown from 'react-markdown'

function MessageList({ messages, streamingContent, isLoading, messagesEndRef, currentAgent }) {
  // 解析多智能体协作的内容
  const parseAgentContent = (content) => {
    const sections = []
    const lines = content.split('\n')
    let currentSection = null
    
    for (const line of lines) {
      const designerMatch = line.match(/^【测试用例设计师】$/)
      const reviewerMatch = line.match(/^【测试用例评审师】$/)
      const userMatch = line.match(/^【用户评审】$/)
      
      if (designerMatch) {
        if (currentSection) sections.push(currentSection)
        currentSection = { role: '测试用例设计师', content: '', color: '#4F8EF7' }
      } else if (reviewerMatch) {
        if (currentSection) sections.push(currentSection)
        currentSection = { role: '测试用例评审师', content: '', color: '#FF9800' }
      } else if (userMatch) {
        if (currentSection) sections.push(currentSection)
        currentSection = { role: '用户评审', content: '', color: '#4CAF50' }
      } else if (currentSection) {
        currentSection.content += line + '\n'
      }
    }
    
    if (currentSection) sections.push(currentSection)
    return sections
  }

  return (
    <div className="message-list">
      {messages.length === 0 && !isLoading ? (
        <div className="empty-state">
          <div className="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="#4F8EF7" strokeWidth="2" fill="none"/>
              <path d="M8 10H16M8 14H13" stroke="#4F8EF7" strokeWidth="2" strokeLinecap="round"/>
            </svg>
          </div>
          <h2>欢迎来到 AI 测试用例协作助手</h2>
          <p>通过多智能体协作，帮助你设计、评审和优化测试用例</p>
          <div className="suggestions">
            <div className="suggestion-item">设计登录功能的测试用例</div>
            <div className="suggestion-item">编写购物车测试用例</div>
            <div className="suggestion-item">用户注册流程测试</div>
          </div>
        </div>
      ) : (
        <>
          {messages.map((message, index) => (
            <div key={index} className="message-group">
              {message.role === 'user' ? (
                <div className="message message-user">
                  <div className="message-avatar">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <circle cx="12" cy="8" r="4" fill="#666"/>
                      <path d="M4 20C4 16.6863 6.68629 14 10 14H14C17.3137 14 20 16.6863 20 20V21H4V20Z" fill="#666"/>
                    </svg>
                  </div>
                  <div className="message-content">
                    <div className="message-role">你</div>
                    <div className="message-text">{message.content}</div>
                  </div>
                </div>
              ) : (
                <div className="message message-assistant">
                  <div className="message-avatar">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <circle cx="12" cy="12" r="10" fill="#4F8EF7"/>
                      <path d="M7 9H17M7 12H17M7 15H13" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                  </div>
                  <div className="message-content">
                    <div className="message-role">AI 协作团队</div>
                    <div className="agent-sections">
                      {parseAgentContent(message.content).map((section, idx) => (
                        <div key={idx} className="agent-section">
                          <div className="agent-badge" style={{ backgroundColor: section.color }}>
                            {section.role}
                          </div>
                          <div className="agent-content markdown-content">
                            <ReactMarkdown>{section.content.trim()}</ReactMarkdown>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="message message-assistant">
              <div className="message-avatar">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="10" fill="#4F8EF7"/>
                  <path d="M7 9H17M7 12H17M7 15H13" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </div>
              <div className="message-content">
                <div className="message-role">
                  AI 协作团队
                  {currentAgent && <span className="current-agent-badge" style={{ backgroundColor: 
                    currentAgent === '测试用例设计师' ? '#4F8EF7' : 
                    currentAgent === '测试用例评审师' ? '#FF9800' : '#4CAF50'
                  }}>正在输出: {currentAgent}</span>}
                </div>
                <div className="message-text">
                  {streamingContent ? (
                    <div className="agent-sections">
                      {parseAgentContent(streamingContent).map((section, idx) => (
                        <div key={idx} className="agent-section">
                          <div className="agent-badge" style={{ backgroundColor: section.color }}>
                            {section.role}
                          </div>
                          <div className="agent-content markdown-content">
                            <ReactMarkdown>{section.content.trim()}</ReactMarkdown>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  )
}

export default MessageList
