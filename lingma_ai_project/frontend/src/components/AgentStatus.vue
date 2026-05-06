<template>
  <div class="agent-status" v-if="isConnected || isProcessing">
    <div class="status-content">
      <a-spin v-if="isProcessing" size="small" />
      <div v-else class="status-indicator connected"></div>
      <span class="status-text">{{ statusText }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  isConnected: {
    type: Boolean,
    default: false
  },
  isProcessing: {
    type: Boolean,
    default: false
  }
})

const statusText = computed(() => {
  if (props.isProcessing) {
    return 'AI 正在思考...'
  }
  if (props.isConnected) {
    return '已连接'
  }
  return '未连接'
})
</script>

<style scoped>
.agent-status {
  padding: 12px 20px;
  background: #ffffff;
  border-bottom: 1px solid #e8eaed;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-content {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #5f6368;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #34a853;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.status-text {
  font-weight: 400;
}
</style>
