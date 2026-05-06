export async function sendMessage(message, onChunk) {
  try {
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      
      // 按 SSE 消息边界分割（\n\n）
      const messages = buffer.split('\n\n')
      buffer = messages.pop() || ''

      for (const msg of messages) {
        if (!msg.trim()) continue
        
        const lines = msg.split('\n')
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue
            
            try {
              const parsed = JSON.parse(data)
              if (parsed.content) {
                onChunk(parsed.content)
              } else if (parsed.error) {
                console.error('Backend error:', parsed.error)
                onChunk(`[错误] ${parsed.error}`)
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e, 'Raw data:', data)
            }
          }
        }
      }
    }
  } catch (error) {
    console.error('Error in sendMessage:', error)
    throw error
  }
}
