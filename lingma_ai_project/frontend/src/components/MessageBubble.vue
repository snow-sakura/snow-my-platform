<template>
  <div class="message-container" :class="{ 'user-message': isUser }">
    <!-- AI消息的时间轴线 -->
    <div class="timeline-line" v-if="!isUser"></div>
    <div class="timeline-dot" v-if="!isUser" :style="{ background: agentColor }"></div>
    
    <div class="message-bubble">
      <!-- 用户消息：简化头部 -->
      <div class="message-header" v-if="isUser">
        <span class="message-time">{{ formatTime(message.timestamp) }}</span>
      </div>
      
      <!-- AI 消息：智能体标签 + 时间 -->
      <div class="agent-label" v-if="!isUser" :style="{ borderLeftColor: agentColor }">
        <span class="agent-icon" :style="{ background: agentColor }">{{ agentIcon }}</span>
        <span class="agent-name">{{ getAgentLabel(message) }}</span>
        <span class="message-time">{{ formatTime(message.timestamp) }}</span>
      </div>
      
      <!-- 消息内容 -->
      <div class="message-body" :class="{ 'collapsible': isLongContent }">
        <!-- 用户消息直接显示内容 -->
        <div v-if="isUser" class="user-content">{{ message.content }}</div>
        
        <!-- AI 消息 -->
        <div v-else>
          <!-- 短内容直接显示 -->
          <div v-if="!isLongContent">{{ message.content }}</div>
          
          <!-- 长内容可折叠 -->
          <div v-else>
            <div :class="{ 'collapsed': isCollapsed }">{{ message.content }}</div>
            <button class="toggle-btn" @click="toggleCollapse">
              {{ isCollapsed ? '展开全部' : '收起' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

const isUser = computed(() => props.message.source === 'user')
const isCollapsed = ref(false) // 默认展开

// 智能体配置
const agentConfig = {
  'test_writer': { label: '测试用例编写员', icon: '✍️', color: '#52c41a' },
  'test_reviewer': { label: '测试用例评审员', icon: '🔍', color: '#fa8c16' },
  'coordinator': { label: '流程协调员', icon: '🎯', color: '#722ed1' },
  'assistant': { label: 'AI助手', icon: '🤖', color: '#1677ff' },
  'user_proxy': { label: '用户代理', icon: '👤', color: '#1677ff' }
}

const agentInfo = computed(() => agentConfig[props.message.source] || agentConfig['assistant'])
const agentColor = computed(() => agentInfo.value.color)
const agentIcon = computed(() => agentInfo.value.icon)

// 判断是否为长内容（超过500字符）
const isLongContent = computed(() => {
  return !isUser.value && props.message.content && props.message.content.length > 500
})

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

// 获取智能体标签（友好显示）
const getAgentLabel = (msg) => {
  const source = msg.source || 'assistant'
  return agentConfig[source]?.label || source
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.message-container {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 20px;
  position: relative;
  animation: slideUp 0.3s ease;
}

.user-message {
  justify-content: flex-end;
}

/* 时间轴线 */
.timeline-line {
  width: 2px;
  background: #e8eaed;
  position: absolute;
  left: 15px;
  top: 30px;
  bottom: -20px;
}

/* 时间轴点 */
.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 20px;
  z-index: 1;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.8);
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 16px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.user-message .message-bubble {
  background: linear-gradient(135deg, #1677ff 0%, #4096ff 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.ai-message .message-bubble {
  background: #ffffff;
  color: #202124;
  border: 1px solid #e8eaed;
  border-bottom-left-radius: 4px;
}

.message-bubble:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-size: 12px;
}

/* 智能体标签 */
.agent-label {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-left: 12px;
  margin-bottom: 8px;
  border-left: 3px solid;
}

.agent-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: white;
  flex-shrink: 0;
}

.agent-name {
  font-weight: 600;
  color: #202124;
  font-size: 14px;
}

.message-time {
  color: #9aa0a6;
  font-size: 11px;
  margin-left: auto;
}

.message-body {
  line-height: 1.6;
  word-wrap: break-word;
  white-space: pre-wrap;
  transition: max-height 0.3s ease, opacity 0.3s ease;
}

.user-content {
  white-space: pre-wrap;
}

/* 折叠按钮 */
.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #1677ff;
  font-size: 12px;
  padding: 4px 8px;
  margin-top: 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.toggle-btn:hover {
  background: #f1f3f4;
}

.message-body.collapsed {
  max-height: 150px;
  overflow: hidden;
  opacity: 0.8;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
