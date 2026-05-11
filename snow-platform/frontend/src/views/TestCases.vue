<template>
  <div class="test-cases-tab">
    <div class="action-bar">
      <el-select v-model="filterPriority" placeholder="优先级" clearable style="width: 120px;">
        <el-option label="HIGH" value="HIGH" />
        <el-option label="MEDIUM" value="MEDIUM" />
        <el-option label="LOW" value="LOW" />
      </el-select>
      <el-select v-model="filterType" placeholder="用例类型" clearable style="width: 120px;">
        <el-option label="功能" value="功能" />
        <el-option label="性能" value="性能" />
        <el-option label="安全" value="安全" />
      </el-select>
      <el-button type="primary" @click="handleAdd">手动新增</el-button>
      <el-button type="success" @click="handleExport">导出Excel</el-button>
      <el-button type="danger" :disabled="selectedCases.length === 0" @click="handleBatchDelete">批量删除</el-button>
    </div>

    <el-table :data="filteredTestCases" v-loading="loading" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" />
      <el-table-column prop="case_number" label="用例编号" width="140" />
      <el-table-column prop="title" label="用例标题" min-width="200" />
      <el-table-column prop="precondition" label="前置条件" min-width="200" show-overflow-tooltip />
      <el-table-column prop="priority" label="优先级" width="100">
        <template #default="{ row }">
          <el-tag size="small" :type="getPriorityType(row.priority)">{{ row.priority }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="case_type" label="用例类型" width="100" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="handleView(row)">查看</el-button>
          <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑测试用例对话框 -->
    <el-dialog v-model="showDialog" :title="isEditing ? '编辑测试用例' : '新增测试用例'" width="650px" top="3vh">
      <el-form :model="formData" label-width="100px">
        <el-form-item label="用例标题" required>
          <el-input v-model="formData.title" placeholder="请输入用例标题" />
        </el-form-item>
        <el-form-item label="关联测试点" required>
          <el-input-number v-model="formData.test_point_id" :min="1" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="前置条件">
          <el-input v-model="formData.precondition" type="textarea" :rows="2" placeholder="请输入前置条件" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="formData.priority" style="width: 100%;">
            <el-option label="HIGH" value="HIGH" />
            <el-option label="MEDIUM" value="MEDIUM" />
            <el-option label="LOW" value="LOW" />
          </el-select>
        </el-form-item>
        <el-form-item label="用例类型">
          <el-select v-model="formData.case_type" style="width: 100%;">
            <el-option label="功能" value="功能" />
            <el-option label="性能" value="性能" />
            <el-option label="安全" value="安全" />
            <el-option label="兼容性" value="兼容性" />
            <el-option label="UI" value="UI" />
          </el-select>
        </el-form-item>
        <el-form-item label="预期结果">
          <el-input v-model="formData.expected_result" type="textarea" :rows="2" placeholder="请输入预期结果" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看详情对话框 -->
    <el-dialog v-model="showViewDialog" title="测试用例详情" width="650px" top="3vh">
      <div v-if="viewCase" class="case-detail">
        <div class="detail-row"><span class="label">用例编号：</span>{{ viewCase.case_number }}</div>
        <div class="detail-row"><span class="label">标题：</span>{{ viewCase.title }}</div>
        <div class="detail-row"><span class="label">前置条件：</span>{{ viewCase.precondition || '无' }}</div>
        <div class="detail-row"><span class="label">优先级：</span>
          <el-tag size="small" :type="getPriorityType(viewCase.priority)">{{ viewCase.priority }}</el-tag>
        </div>
        <div class="detail-row"><span class="label">用例类型：</span>{{ viewCase.case_type || '-' }}</div>
        <div class="detail-row">
          <span class="label">测试步骤：</span>
          <div v-if="viewCase.steps?.length" class="steps-list">
            <div v-for="(step, idx) in viewCase.steps" :key="idx" class="step-item">
              {{ idx + 1 }}. {{ step.step }}<br>
              <span class="expected">预期：{{ step.expected_result }}</span>
            </div>
          </div>
          <span v-else>无</span>
        </div>
        <div class="detail-row"><span class="label">预期结果：</span>{{ viewCase.expected_result || '无' }}</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTestCases, getTestCase, createTestCase, updateTestCase, deleteTestCase, exportTestCases, type TestCase, type TestCaseCreate, type TestCaseUpdate } from '@/api/test'

const route = useRoute()
const testCases = ref<TestCase[]>([])
const loading = ref(false)
const selectedCases = ref<TestCase[]>([])
const filterPriority = ref('')
const filterType = ref('')
const showDialog = ref(false)
const showViewDialog = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const editingId = ref<number | null>(null)
const viewCase = ref<TestCase | null>(null)

const formData = ref<TestCaseCreate & { expected_result?: string; case_type?: string }>({
  test_point_id: 0,
  title: '',
  precondition: '',
  steps: [],
  expected_result: '',
  priority: 'MEDIUM',
  case_type: ''
})

const projectId = computed(() => Number(route.params.id))

const filteredTestCases = computed(() => {
  return testCases.value.filter(tc => {
    if (filterPriority.value && tc.priority !== filterPriority.value) return false
    if (filterType.value && tc.case_type !== filterType.value) return false
    return true
  })
})

const loadTestCases = async () => {
  loading.value = true
  try {
    testCases.value = await getTestCases(projectId.value)
  } catch (error) {
    console.error('加载测试用例失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSelectionChange = (selection: TestCase[]) => {
  selectedCases.value = selection
}

const getPriorityType = (priority: string) => {
  const types: Record<string, any> = { HIGH: 'danger', MEDIUM: 'warning', LOW: 'info' }
  return types[priority] || 'info'
}

const resetForm = () => {
  formData.value = { test_point_id: 0, title: '', precondition: '', steps: [], expected_result: '', priority: 'MEDIUM', case_type: '' }
  editingId.value = null
}

const handleView = async (testCase: TestCase) => {
  try {
    viewCase.value = await getTestCase(testCase.id)
    showViewDialog.value = true
  } catch (error) {
    ElMessage.error('加载用例详情失败')
  }
}

const handleAdd = () => {
  isEditing.value = false
  resetForm()
  showDialog.value = true
}

const handleEdit = (testCase: TestCase) => {
  isEditing.value = true
  editingId.value = testCase.id
  formData.value = {
    test_point_id: testCase.test_point_id,
    title: testCase.title,
    precondition: testCase.precondition || '',
    steps: testCase.steps || [],
    expected_result: testCase.expected_result || '',
    priority: testCase.priority,
    case_type: testCase.case_type || ''
  }
  showDialog.value = true
}

const handleDelete = async (testCase: TestCase) => {
  try {
    await ElMessageBox.confirm('确定要删除该测试用例吗？', '提示', { type: 'warning' })
    await deleteTestCase(testCase.id)
    ElMessage.success('删除成功')
    loadTestCases()
  } catch (error) {
    if (error !== 'cancel') console.error('删除失败:', error)
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedCases.value.length} 个测试用例吗？`, '提示', { type: 'warning' })
    for (const tc of selectedCases.value) {
      await deleteTestCase(tc.id)
    }
    ElMessage.success('批量删除成功')
    selectedCases.value = []
    loadTestCases()
  } catch (error) {
    if (error !== 'cancel') console.error('批量删除失败:', error)
  }
}

const handleSave = async () => {
  if (!formData.value.title) {
    ElMessage.warning('请输入用例标题')
    return
  }
  saving.value = true
  try {
    if (isEditing.value && editingId.value) {
      const updateData: TestCaseUpdate = {
        title: formData.value.title,
        precondition: formData.value.precondition,
        expected_result: formData.value.expected_result,
        priority: formData.value.priority,
        case_type: formData.value.case_type
      }
      await updateTestCase(editingId.value, updateData)
      ElMessage.success('更新成功')
    } else {
      await createTestCase(projectId.value, formData.value as any)
      ElMessage.success('创建成功')
    }
    showDialog.value = false
    resetForm()
    loadTestCases()
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    saving.value = false
  }
}

const handleExport = async () => {
  try {
    const blob = await exportTestCases(projectId.value) as any
    const url = window.URL.createObjectURL(new Blob([blob]))
    const link = document.createElement('a')
    link.href = url
    link.download = `test_cases_${projectId.value}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
  }
}

onMounted(() => {
  loadTestCases()
})
</script>

<style scoped>
.test-cases-tab {
  min-height: 300px;
}

.action-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.case-detail {
  max-height: 55vh;
  overflow-y: auto;
}

.detail-row {
  margin-bottom: 12px;
  line-height: 1.6;
}

.detail-row .label {
  font-weight: bold;
  color: #303133;
}

.steps-list {
  margin-top: 4px;
}

.step-item {
  padding: 6px 0;
  border-bottom: 1px dashed #ebeef5;
}

.step-item .expected {
  color: #909399;
  font-size: 13px;
  margin-left: 16px;
}
</style>
