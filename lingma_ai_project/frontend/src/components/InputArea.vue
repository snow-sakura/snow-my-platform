<template>
  <div class="input-area">
    <!-- 附件预览区域 -->
    <div v-if="attachedFile" class="attachment-preview">
      <a-tag color="blue" closable @close="removeAttachment">
        <PaperClipOutlined /> {{ attachedFile.name }}
      </a-tag>
    </div>
    
    <a-input
      v-model:value="inputValue"
      :placeholder="isWaitingForInput ? 'AI 正在等待您的输入...' : '输入消息...'"
      :disabled="disabled"
      @pressEnter="handleSend"
      class="message-input"
      size="large"
    >
      <template #prefix>
        <!-- 上传按钮 -->
        <a-upload
          :beforeUpload="handleFileUpload"
          :showUploadList="false"
          accept=".pdf,.txt"
        >
          <a-button type="text" :disabled="disabled" class="upload-btn">
            <PaperClipOutlined />
          </a-button>
        </a-upload>
      </template>
      <template #suffix>
        <a-button
          type="primary"
          :disabled="!canSend"
          @click="handleSend"
          :loading="isProcessing"
          class="send-button"
        >
          <template #icon>
            <SendOutlined />
          </template>
        </a-button>
      </template>
    </a-input>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { SendOutlined, PaperClipOutlined } from '@ant-design/icons-vue'
import { parseFile } from '../utils/fileParser'
import { message } from 'ant-design-vue'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  },
  isProcessing: {
    type: Boolean,
    default: false
  },
  isWaitingForInput: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['send'])

const inputValue = ref('')
const attachedFile = ref(null)
const attachedContent = ref(null)

// 处理文件上传
const handleFileUpload = async (file) => {
  try {
    const text = await parseFile(file)
    attachedFile.value = file
    attachedContent.value = text
    message.success(`文件 "${file.name}" 已附加`)
  } catch (error) {
    message.error(error.message)
  }
  return false // 阻止默认上传
}

// 移除附件
const removeAttachment = () => {
  attachedFile.value = null
  attachedContent.value = null
}

// 是否可以发送
const canSend = computed(() => {
  return inputValue.value.trim() && !props.disabled && !props.isProcessing
})

const handleSend = () => {
  const content = inputValue.value.trim()
  if (!canSend.value) return

  emit('send', {
    content: content,
    attachment: attachedContent.value
  })
  
  inputValue.value = ''
  removeAttachment()
}

// 监听 processing 状态,完成后聚焦输入框
watch(() => props.isProcessing, (newVal) => {
  if (!newVal) {
    setTimeout(() => {
      const input = document.querySelector('.message-input input')
      if (input) input.focus()
    }, 100)
  }
})
</script>

<style scoped>
.input-area {
  padding: 16px 20px;
  background: #ffffff;
  border-top: 1px solid #e8eaed;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.04);
}

/* 附件预览区域 */
.attachment-preview {
  margin-bottom: 8px;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.message-input {
  border-radius: 24px;
  border: 1px solid #dadce0;
  transition: all 0.3s ease;
}

.message-input:hover {
  border-color: #1677ff;
}

.message-input:focus-within {
  border-color: #1677ff;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
}

.upload-btn {
  color: #5f6368;
  transition: color 0.2s;
}

.upload-btn:hover {
  color: #1677ff;
}

.send-button {
  border-radius: 20px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-button:not(:disabled):hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(22, 119, 255, 0.3);
}
</style>
