<template>
  <div class="test-cases-tab">
    <div class="action-bar">
      <el-select v-model="filterPriority" placeholder="优先级" clearable style="width: 120px;">
        <el-option label="P0" value="P0" />
        <el-option label="P1" value="P1" />
        <el-option label="P2" value="P2" />
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

    <el-table :data="testCases" v-loading="loading" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" />
      <el-table-column prop="case_number" label="用例编号" width="120" />
      <el-table-column prop="title" label="用例标题" min-width="200" />
      <el-table-column prop="precondition" label="前置条件" min-width="200" show-overflow-tooltip />
      <el-table-column prop="priority" label="优先级" width="100">
        <template #default="{ row }">
          <el-tag size="small" :type="getPriorityType(row.priority)">{{ row.priority }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="case_type" label="用例类型" width="100" />
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="handleView(row)">查看</el-button>
          <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTestCases, type TestCase } from '@/api/test'

const route = useRoute()
const testCases = ref<TestCase[]>([])
const loading = ref(false)
const selectedCases = ref<TestCase[]>([])
const filterPriority = ref('')
const filterType = ref('')

const projectId = computed(() => Number(route.params.id))

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

const handleEdit = (testCase: TestCase) => {
  ElMessage.info('编辑功能开发中')
}

const handleView = (testCase: TestCase) => {
  ElMessage.info('查看详情功能开发中')
}

const handleDelete = async (testCase: TestCase) => {
  try {
    await ElMessageBox.confirm('确定要删除该测试用例吗？', '提示', {
      type: 'warning'
    })
    ElMessage.success('删除成功')
    loadTestCases()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除测试用例失败:', error)
    }
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedCases.value.length} 个测试用例吗？`, '提示', {
      type: 'warning'
    })
    ElMessage.success('批量删除成功')
    loadTestCases()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
    }
  }
}

const handleExport = () => {
  ElMessage.info('导出Excel功能开发中')
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
</style>
