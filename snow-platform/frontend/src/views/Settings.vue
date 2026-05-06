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
              <el-input v-model="llmConfig.model" placeholder="例如: gpt-4" />
            </el-form-item>
            <el-form-item label="API地址">
              <el-input v-model="llmConfig.baseUrl" placeholder="第三方平台地址 (可选)" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveLLMConfig">保存配置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="飞书通知配置" name="feishu">
          <el-form :model="feishuConfig" label-width="120px" style="max-width: 600px;">
            <el-form-item label="Webhook地址">
              <el-input v-model="feishuConfig.webhookUrl" placeholder="请输入飞书机器人Webhook地址" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveFeishuConfig">保存配置</el-button>
              <el-button @click="testNotification">发送测试通知</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('llm')

const llmConfig = ref({
  apiKey: '',
  model: 'gpt-4',
  baseUrl: ''
})

const feishuConfig = ref({
  webhookUrl: ''
})

const saveLLMConfig = () => {
  ElMessage.success('配置保存成功（功能开发中）')
}

const saveFeishuConfig = () => {
  ElMessage.success('配置保存成功（功能开发中）')
}

const testNotification = () => {
  ElMessage.info('测试通知发送成功（功能开发中）')
}

onMounted(() => {
  // TODO: 加载配置
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
