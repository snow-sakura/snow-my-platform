<template>
  <div class="batch-tracker">
    <div class="tracker-header">
      <h4 class="tracker-title">任务批次</h4>
      <el-button type="primary" link size="small" @click="refresh" :loading="loading">刷新</el-button>
    </div>

    <el-empty v-if="batches.length === 0" description="暂无任务批次" :image-size="60" />

    <div v-for="batch in batches" :key="batch.id" class="batch-item">
      <div class="batch-row">
        <span class="batch-label">{{ getTaskLabel(batch.task_type) }}</span>
        <el-tag size="small" :type="getStatusType(batch.status)">{{ getStatusText(batch.status) }}</el-tag>
      </div>

      <el-progress
        v-if="batch.status === 'RUNNING' || batch.status === 'PENDING'"
        :percentage="batch.progress"
        :stroke-width="8"
        style="margin: 8px 0;"
      />

      <div class="batch-meta">
        <span>{{ batch.completed_count }} / {{ batch.total_count }}</span>
        <span class="time-text">{{ formatTime(batch.created_at) }}</span>
      </div>

      <div v-if="batch.error_message" class="error-msg">{{ batch.error_message }}</div>

      <div class="batch-actions">
        <el-button type="primary" link size="small" @click="showDetail(batch)">详情</el-button>
        <el-button
          v-if="batch.status === 'PENDING' || batch.status === 'RUNNING'"
          type="danger" link size="small"
          @click="handleCancel(batch.id)"
        >取消</el-button>
      </div>
    </div>

    <!-- 批次详情对话框 -->
    <el-dialog v-model="detailVisible" title="批次详情" width="500px">
      <div v-if="detailBatch" class="detail-content">
        <div class="detail-row"><span class="label">任务类型：</span>{{ getTaskLabel(detailBatch.task_type) }}</div>
        <div class="detail-row"><span class="label">状态：</span>
          <el-tag size="small" :type="getStatusType(detailBatch.status)">{{ getStatusText(detailBatch.status) }}</el-tag>
        </div>
        <div class="detail-row"><span class="label">进度：</span>{{ detailBatch.completed_count }} / {{ detailBatch.total_count }}</div>
        <div class="detail-row"><span class="label">创建时间：</span>{{ formatTime(detailBatch.created_at) }}</div>
        <div class="detail-row" v-if="detailBatch.started_at"><span class="label">开始时间：</span>{{ formatTime(detailBatch.started_at) }}</div>
        <div class="detail-row" v-if="detailBatch.completed_at"><span class="label">完成时间：</span>{{ formatTime(detailBatch.completed_at) }}</div>
        <div class="detail-row" v-if="detailBatch.error_message"><span class="label">错误信息：</span>
          <span class="error-text">{{ detailBatch.error_message }}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import { getProjectBatches, cancelBatch, type TaskBatch } from '@/api/test'
import dayjs from 'dayjs'

const props = defineProps<{ projectId: number }>()
const batches = ref<TaskBatch[]>([])
const loading = ref(false)
const detailVisible = ref(false)
const detailBatch = ref<TaskBatch | null>(null)
// 追踪上一轮批次状态，用于检测变化
const prevStates = ref<Record<number, string>>({})
let timer: ReturnType<typeof setInterval> | null = null

const loadBatches = async () => {
  loading.value = true
  try {
    batches.value = await getProjectBatches(props.projectId)
    checkCompletion()
  } catch (error) {
    console.error('加载任务批次失败:', error)
  } finally {
    loading.value = false
  }
}

const refresh = () => loadBatches()

const checkCompletion = () => {
  for (const batch of batches.value) {
    const prev = prevStates.value[batch.id]
    // 检测任务刚完成
    if (prev && (prev === 'RUNNING' || prev === 'PENDING')) {
      if (batch.status === 'COMPLETED') {
        ElNotification({ title: '任务完成', message: `${getTaskLabel(batch.task_type)} 已完成`, type: 'success' })
      } else if (batch.status === 'FAILED') {
        ElNotification({ title: '任务失败', message: batch.error_message || '未知错误', type: 'error' })
      }
    }
    prevStates.value[batch.id] = batch.status
  }
}

const hasRunning = () => batches.value.some(b => b.status === 'RUNNING' || b.status === 'PENDING')

const handleCancel = async (batchId: number) => {
  try {
    await ElMessageBox.confirm('确定要取消该任务吗？', '提示', { type: 'warning' })
    await cancelBatch(batchId)
    ElMessage.success('任务已取消')
    refresh()
  } catch (error) {
    if (error !== 'cancel') console.error('取消任务失败:', error)
  }
}

const showDetail = (batch: TaskBatch) => {
  detailBatch.value = batch
  detailVisible.value = true
}

const getTaskLabel = (type: string) => {
  const labels: Record<string, string> = {
    extract_test_points: '提取测试点',
    generate_test_cases: '生成测试用例'
  }
  return labels[type] || type
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    PENDING: '等待中', RUNNING: '运行中', COMPLETED: '已完成', FAILED: '失败'
  }
  return texts[status] || status
}

const getStatusType = (status: string) => {
  const types: Record<string, any> = {
    PENDING: 'info', RUNNING: 'warning', COMPLETED: 'success', FAILED: 'danger'
  }
  return types[status] || 'info'
}

const formatTime = (time?: string) => {
  if (!time) return '-'
  return dayjs(time).format('MM-DD HH:mm:ss')
}

watch(() => props.projectId, () => {
  loadBatches()
})

onMounted(() => {
  loadBatches()
  timer = setInterval(() => {
    if (hasRunning()) loadBatches()
  }, 3000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.batch-tracker {
  min-height: 100px;
}

.tracker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.tracker-title {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
  margin: 0;
}

.batch-item {
  background: #fafafa;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  padding: 12px 16px;
  margin-bottom: 10px;
}

.batch-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.batch-label {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.batch-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.time-text {
  color: #c0c4cc;
}

.error-msg {
  margin-top: 6px;
  font-size: 12px;
  color: #f56c6c;
  background: #fef0f0;
  padding: 4px 8px;
  border-radius: 4px;
}

.batch-actions {
  margin-top: 8px;
  display: flex;
  gap: 12px;
}

.detail-content {
  line-height: 2;
}

.detail-row .label {
  font-weight: bold;
  color: #303133;
}

.error-text {
  color: #f56c6c;
}
</style>
