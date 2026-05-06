import React from 'react'

function ChatContainer({ children }) {
  return (
    <div className="chat-container">
      <header className="chat-header">
        <div className="logo">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="#4F8EF7"/>
            <path d="M7 9H17M7 12H17M7 15H13" stroke="white" strokeWidth="2" strokeLinecap="round"/>
          </svg>
          <span>AI Assistant</span>
        </div>
      </header>
      <main className="chat-main">
        {children}
      </main>
    </div>
  )
}

export default ChatContainer
