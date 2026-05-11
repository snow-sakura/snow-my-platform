<template>
  <div class="test-points-tab">
    <div class="action-bar">
      <el-select v-model="filterPriority" placeholder="优先级" clearable style="width: 120px;" @change="applyFilter">
        <el-option label="HIGH" value="HIGH" />
        <el-option label="MEDIUM" value="MEDIUM" />
        <el-option label="LOW" value="LOW" />
      </el-select>
      <el-select v-model="filterCategory" placeholder="分类" clearable style="width: 120px;" @change="applyFilter">
        <el-option label="功能" value="功能" />
        <el-option label="性能" value="性能" />
        <el-option label="安全" value="安全" />
        <el-option label="兼容性" value="兼容性" />
        <el-option label="UI" value="UI" />
      </el-select>
      <el-button type="primary" @click="showCreateDialog = true">手动新增</el-button>
      <el-button type="success" @click="handleGenerateCases" :disabled="selectedPoints.length === 0">
        一键生成用例
      </el-button>
      <el-button type="danger" :disabled="selectedPoints.length === 0" @click="handleBatchDelete">批量删除</el-button>
    </div>

    <el-table :data="filteredTestPoints" v-loading="loading" @selection-change="handleSelectionChange">
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
          <el-tag size="small" :type="row.is_verified ? 'success' : 'warning'">
            {{ row.is_verified ? '已确认' : '待确认' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="success" link size="small" @click="handleVerify(row)">确认</el-button>
          <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑测试点对话框 -->
    <el-dialog v-model="showDialog" :title="isEditing ? '编辑测试点' : '新增测试点'" width="550px">
      <el-form :model="formData" label-width="80px">
        <el-form-item label="标题" required>
          <el-input v-model="formData.title" placeholder="请输入测试点标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入测试点描述" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="formData.priority" style="width: 100%;">
            <el-option label="HIGH" value="HIGH" />
            <el-option label="MEDIUM" value="MEDIUM" />
            <el-option label="LOW" value="LOW" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="formData.category" style="width: 100%;" placeholder="请选择分类">
            <el-option label="功能" value="功能" />
            <el-option label="性能" value="性能" />
            <el-option label="安全" value="安全" />
            <el-option label="兼容性" value="兼容性" />
            <el-option label="UI" value="UI" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTestPoints, createTestPoint, updateTestPoint, deleteTestPoint, generateTestCases, type TestPoint, type TestPointCreate } from '@/api/test'

const route = useRoute()
const router = useRouter()
const testPoints = ref<TestPoint[]>([])
const loading = ref(false)
const selectedPoints = ref<TestPoint[]>([])
const filterPriority = ref('')
const filterCategory = ref('')
const showDialog = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const editingId = ref<number | null>(null)

const formData = ref<TestPointCreate>({
  title: '',
  description: '',
  priority: 'MEDIUM',
  category: ''
})

const projectId = computed(() => Number(route.params.id))

const filteredTestPoints = computed(() => {
  return testPoints.value.filter(tp => {
    if (filterPriority.value && tp.priority !== filterPriority.value) return false
    if (filterCategory.value && tp.category !== filterCategory.value) return false
    return true
  })
})

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

const applyFilter = () => {}

const handleSelectionChange = (selection: TestPoint[]) => {
  selectedPoints.value = selection
}

const getPriorityType = (priority: string) => {
  const types: Record<string, any> = { HIGH: 'danger', MEDIUM: 'warning', LOW: 'info' }
  return types[priority] || 'info'
}

const resetForm = () => {
  formData.value = { title: '', description: '', priority: 'MEDIUM', category: '' }
  editingId.value = null
}

const handleEdit = (point: TestPoint) => {
  isEditing.value = true
  editingId.value = point.id
  formData.value = {
    title: point.title,
    description: point.description || '',
    priority: point.priority,
    category: point.category || ''
  }
  showDialog.value = true
}

const handleVerify = async (point: TestPoint) => {
  try {
    await updateTestPoint(point.id, { is_verified: true })
    ElMessage.success('已确认')
    loadTestPoints()
  } catch (error) {
    console.error('确认失败:', error)
  }
}

const handleDelete = async (point: TestPoint) => {
  try {
    await ElMessageBox.confirm('确定要删除该测试点吗？', '提示', { type: 'warning' })
    await deleteTestPoint(point.id)
    ElMessage.success('删除成功')
    loadTestPoints()
  } catch (error) {
    if (error !== 'cancel') console.error('删除失败:', error)
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedPoints.value.length} 个测试点吗？`, '提示', { type: 'warning' })
    for (const point of selectedPoints.value) {
      await deleteTestPoint(point.id)
    }
    ElMessage.success('批量删除成功')
    selectedPoints.value = []
    loadTestPoints()
  } catch (error) {
    if (error !== 'cancel') console.error('批量删除失败:', error)
  }
}

const handleSave = async () => {
  if (!formData.value.title) {
    ElMessage.warning('请输入测试点标题')
    return
  }
  saving.value = true
  try {
    if (isEditing.value && editingId.value) {
      await updateTestPoint(editingId.value, formData.value)
      ElMessage.success('更新成功')
    } else {
      await createTestPoint(projectId.value, formData.value)
      ElMessage.success('创建成功')
    }
    showDialog.value = false
    resetForm()
    loadTestPoints()
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    saving.value = false
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
