<template>
  <div class="project-detail-page">
    <div class="page-header">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span> / </span>
        <span>项目详情</span>
      </div>
      <div class="page-title">
        <h2>{{ projectName }}</h2>
        <el-button @click="$router.back()">返回列表</el-button>
      </div>
    </div>

    <el-card class="content-card" :body-style="{ padding: '0' }">
      <el-tabs v-model="activeTab" @tab-click="handleTabChange">
        <el-tab-pane name="documents">
          <template #label>文档管理</template>
        </el-tab-pane>
        <el-tab-pane name="test-points">
          <template #label>测试点</template>
        </el-tab-pane>
        <el-tab-pane name="knowledge-bases">
          <template #label>知识库</template>
        </el-tab-pane>
        <el-tab-pane name="test-cases">
          <template #label>测试用例</template>
        </el-tab-pane>
        <el-tab-pane name="batches">
          <template #label>
            任务批次
            <el-badge v-if="runningCount > 0" :value="runningCount" style="margin-left: 6px;" />
          </template>
        </el-tab-pane>
      </el-tabs>

      <div class="tab-content">
        <router-view v-if="activeTab !== 'batches'" />
        <BatchTracker v-else :projectId="projectId" />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getProject } from '@/api/project'
import { getProjectBatches, type TaskBatch } from '@/api/test'
import BatchTracker from './BatchTracker.vue'

const route = useRoute()
const router = useRouter()
const activeTab = ref('documents')
const projectName = ref('')
const runningCount = ref(0)

const projectId = computed(() => Number(route.params.id))

const loadProject = async () => {
  try {
    const project = await getProject(projectId.value)
    projectName.value = project.name
  } catch (error) {
    console.error('加载项目信息失败:', error)
  }
}

const loadRunningCount = async () => {
  try {
    const batches = await getProjectBatches(projectId.value)
    runningCount.value = batches.filter(b => b.status === 'RUNNING' || b.status === 'PENDING').length
  } catch { /* 静默失败 */ }
}

const handleTabChange = (tab: any) => {
  const name = tab.props.name
  if (name === 'batches') {
    router.push(`/project/${projectId.value}/batches`)
    loadRunningCount()
  } else {
    router.push(`/project/${projectId.value}/${name}`)
  }
}

const syncTabWithRoute = () => {
  const routeName = route.name as string
  if (routeName && ['documents', 'test-points', 'knowledge-bases', 'test-cases', 'batches'].includes(routeName)) {
    activeTab.value = routeName
  }
}

watch(() => route.name, syncTabWithRoute)
watch(activeTab, () => {
  if (activeTab.value !== 'batches') loadRunningCount()
})

onMounted(() => {
  loadProject()
  loadRunningCount()
  syncTabWithRoute()
})
</script>

<style scoped>
.project-detail-page {
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

.page-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title h2 {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}

.content-card {
  border-radius: 4px;
}

:deep(.el-tabs__header) {
  margin: 0;
  padding: 0 20px;
  background-color: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.tab-content {
  padding: 20px;
}
</style>
