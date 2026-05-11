<template>
  <div class="settings-page">
    <div class="page-header">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span> / </span>
        <span>系统设置</span>
      </div>
      <div class="page-title">
        <h2>系统设置</h2>
      </div>
    </div>

    <el-card class="content-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="LLM配置" name="llm">
          <el-form :model="llmConfig" label-width="120px" style="max-width: 600px;">
            <el-form-item label="API Key">
              <el-input v-model="llmConfig.apiKey" type="password" show-password placeholder="请输入API Key" />
            </el-form-item>
            <el-form-item label="模型名称">
              <el-input v-model="llmConfig.model" placeholder="例如: gpt-4, deepseek-chat" />
            </el-form-item>
            <el-form-item label="API地址">
              <el-input v-model="llmConfig.baseUrl" placeholder="第三方平台地址（可选，留空使用官方地址）" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveLLMConfig" :loading="savingLLM">保存配置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="飞书通知配置" name="feishu">
          <el-form :model="feishuConfig" label-width="120px" style="max-width: 600px;">
            <el-form-item label="Webhook地址">
              <el-input v-model="feishuConfig.webhookUrl" placeholder="请输入飞书机器人Webhook地址" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveFeishuConfig" :loading="savingFeishu">保存配置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getSettings, saveSetting } from '@/api/settings'

const activeTab = ref('llm')
const savingLLM = ref(false)
const savingFeishu = ref(false)

const llmConfig = reactive({
  apiKey: '',
  model: 'gpt-4',
  baseUrl: ''
})

const feishuConfig = reactive({
  webhookUrl: ''
})

const loadSettings = async () => {
  try {
    const settings = await getSettings()
    for (const s of settings) {
      switch (s.key) {
        case 'LLM_API_KEY':
          llmConfig.apiKey = s.value
          break
        case 'LLM_MODEL':
          llmConfig.model = s.value
          break
        case 'LLM_BASE_URL':
          llmConfig.baseUrl = s.value
          break
        case 'FEISHU_WEBHOOK_URL':
          feishuConfig.webhookUrl = s.value
          break
      }
    }
  } catch (error) {
    console.error('加载系统设置失败:', error)
  }
}

const saveLLMConfig = async () => {
  savingLLM.value = true
  try {
    await saveSetting({ key: 'LLM_API_KEY', value: llmConfig.apiKey, description: 'LLM API密钥' })
    await saveSetting({ key: 'LLM_MODEL', value: llmConfig.model, description: 'LLM 模型名称' })
    await saveSetting({ key: 'LLM_BASE_URL', value: llmConfig.baseUrl, description: 'LLM API 代理地址' })
    ElMessage.success('LLM 配置保存成功')
  } catch (error) {
    console.error('保存LLM配置失败:', error)
  } finally {
    savingLLM.value = false
  }
}

const saveFeishuConfig = async () => {
  savingFeishu.value = true
  try {
    await saveSetting({ key: 'FEISHU_WEBHOOK_URL', value: feishuConfig.webhookUrl, description: '飞书机器人 Webhook 地址' })
    ElMessage.success('飞书配置保存成功')
  } catch (error) {
    console.error('保存飞书配置失败:', error)
  } finally {
    savingFeishu.value = false
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.settings-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.breadcrumb {
  color: #909399;
  font-size: 14px;
  margin-bottom: 10px;
}

.breadcrumb a {
  color: #909399;
  text-decoration: none;
}

.breadcrumb a:hover {
  color: #409eff;
}

.page-title h2 {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}

.content-card {
  border-radius: 4px;
}
</style>
