<template>
  <div class="chat-window">
    <!-- 代理状态栏 -->
    <AgentStatus :isConnected="isConnected" :isProcessing="isProcessing" />

    <!-- 消息列表 -->
    <div class="messages-container" ref="messagesContainer">
      <div v-if="messages.length === 0" class="empty-state">
        <div class="empty-icon">💬</div>
        <h2>开始对话</h2>
        <p>发送消息开始与 AI 助手交流</p>
      </div>

      <TransitionGroup name="slide-up">
        <MessageBubble
          v-for="msg in messages"
          :key="msg.id"
          :message="msg"
        />
      </TransitionGroup>

      <!-- 加载指示器 -->
      <div v-if="isProcessing && messages.length > 0" class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    </div>

    <!-- 输入区域 -->
    <InputArea
      :disabled="!isConnected"
      :isProcessing="isProcessing"
      :isWaitingForInput="isWaitingForInput"
      @send="handleSendMessage"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { message } from 'ant-design-vue'
import { useSSE } from '../composables/useSSE'
import MessageBubble from './MessageBubble.vue'
import InputArea from './InputArea.vue'
import AgentStatus from './AgentStatus.vue'

const { connect, sendMessage, messages, isConnected, isProcessing, isWaitingForInput } = useSSE()
const messagesContainer = ref(null)

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 监听消息变化,自动滚动
watch(() => messages.value.length, () => {
  scrollToBottom()
})

// 处理发送消息
const handleSendMessage = ({ content, attachment }) => {
  const success = sendMessage({ content, attachment })
  if (success) {
    scrollToBottom()
  }
}

// 组件挂载时连接 WebSocket
onMounted(async () => {
  try {
    await connect()
  } catch (error) {
    message.error('连接服务器失败')
  }
})
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 900px;
  margin: 0 auto;
  background: #ffffff;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.08);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #5f6368;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-state h2 {
  font-size: 24px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #202124;
}

.empty-state p {
  font-size: 14px;
  color: #9aa0a6;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  margin-bottom: 16px;
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #dadce0;
  animation: typing 1.4s infinite;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}
</style>
