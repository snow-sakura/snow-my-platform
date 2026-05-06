<template>
  <div class="test-points-tab">
    <div class="action-bar">
      <el-select v-model="filterPriority" placeholder="优先级" clearable style="width: 120px;">
        <el-option label="P0" value="P0" />
        <el-option label="P1" value="P1" />
        <el-option label="P2" value="P2" />
      </el-select>
      <el-select v-model="filterCategory" placeholder="分类" clearable style="width: 120px;">
        <el-option label="功能" value="功能" />
        <el-option label="边界" value="边界" />
        <el-option label="性能" value="性能" />
      </el-select>
      <el-button type="primary" @click="handleAdd">手动新增</el-button>
      <el-button type="success" @click="handleGenerateCases">一键生成用例</el-button>
      <el-button type="danger" :disabled="selectedPoints.length === 0" @click="handleBatchDelete">批量删除</el-button>
    </div>

    <el-table :data="testPoints" v-loading="loading" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" />
      <el-table-column prop="title" label="测试点标题" min-width="200" />
      <el-table-column prop="description" label="描述" min-width="300" show-overflow-tooltip />
      <el-table-column prop="priority" label="优先级" width="100">
        <template #default="{ row }">
          <el-tag size="small" :type="getPriorityType(row.priority)">{{ row.priority }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="category" label="分类" width="100" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag size="small" type="success">{{ row.is_verified ? '已就绪' : '待确认' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="用例数" width="100">
        <template #default="{ row }">
          {{ row.test_cases?.length || 0 }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTestPoints, generateTestCases, type TestPoint } from '@/api/test'

const route = useRoute()
const router = useRouter()
const testPoints = ref<TestPoint[]>([])
const loading = ref(false)
const selectedPoints = ref<TestPoint[]>([])
const filterPriority = ref('')
const filterCategory = ref('')

const projectId = computed(() => Number(route.params.id))

const loadTestPoints = async () => {
  loading.value = true
  try {
    testPoints.value = await getTestPoints(projectId.value)
  } catch (error) {
    console.error('加载测试点失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSelectionChange = (selection: TestPoint[]) => {
  selectedPoints.value = selection
}

const getPriorityType = (priority: string) => {
  const types: Record<string, any> = {
    'P0': 'danger',
    'P1': 'warning',
    'P2': 'info'
  }
  return types[priority] || 'info'
}

const handleAdd = () => {
  ElMessage.info('手动新增功能开发中')
}

const handleEdit = (point: TestPoint) => {
  ElMessage.info('编辑功能开发中')
}

const handleDelete = async (point: TestPoint) => {
  try {
    await ElMessageBox.confirm('确定要删除该测试点吗？', '提示', {
      type: 'warning'
    })
    ElMessage.success('删除成功')
    loadTestPoints()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除测试点失败:', error)
    }
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedPoints.value.length} 个测试点吗？`, '提示', {
      type: 'warning'
    })
    ElMessage.success('批量删除成功')
    loadTestPoints()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
    }
  }
}

const handleGenerateCases = async () => {
  try {
    const ids = selectedPoints.value.map(p => p.id)
    await generateTestCases(ids)
    ElMessage.success('测试用例生成任务已启动')
    router.push(`/project/${projectId.value}/test-cases`)
  } catch (error) {
    console.error('生成测试用例失败:', error)
  }
}

onMounted(() => {
  loadTestPoints()
})
</script>

<style scoped>
.test-points-tab {
  min-height: 300px;
}

.action-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
</style>
