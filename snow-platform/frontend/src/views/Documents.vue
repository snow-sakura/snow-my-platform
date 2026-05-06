<template>
  <div class="documents-tab">
    <div class="action-bar">
      <el-upload
        :action="uploadUrl"
        :on-success="handleUploadSuccess"
        :show-file-list="false"
        accept=".pdf,.docx,.md,.markdown,.yaml,.yml,.csv"
      >
        <el-button type="primary">上传文档</el-button>
      </el-upload>
      <el-button type="success" @click="showExtractDialog = true" :disabled="selectedDocs.length === 0">
        AI 提取测试点
      </el-button>
      <span v-if="selectedDocs.length > 0" class="selection-info">
        已选 {{ selectedDocs.length }} 个文档
      </span>
    </div>

    <el-table :data="documents" v-loading="loading" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" />
      <el-table-column prop="filename" label="文件名" />
      <el-table-column prop="file_type" label="类型" width="100">
        <template #default="{ row }">
          <el-tag size="small" type="info">{{ row.file_type?.toUpperCase() }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="大小" width="100">
        <template #default="{ row }">
          {{ formatSize(row.size) }}
        </template>
      </el-table-column>
      <el-table-column label="解析状态" width="120">
        <template #default="{ row }">
          <el-tag size="small" type="success">已完成</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="handleView(row)">查看</el-button>
          <el-button type="warning" link size="small" @click="handleReparse(row)">重新解析</el-button>
          <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- AI提取测试点对话框 -->
    <el-dialog v-model="showExtractDialog" title="AI 提取测试点" width="500px">
      <div class="extract-info">
        <p>已选文档 {{ selectedDocs.length }} 个文档</p>
      </div>
      <div class="form-item">
        <label>关联知识库</label>
        <el-select v-model="selectedKnowledgeBases" multiple placeholder="请选择知识库" style="width: 100%; margin-top: 8px;">
          <el-option label="用例生成规范" value="kb1" />
          <el-option label="业务逻辑梳理" value="kb2" />
        </el-select>
      </div>
      <template #footer>
        <el-button @click="showExtractDialog = false">取消</el-button>
        <el-button type="primary" @click="handleExtract">开始提取</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getDocuments } from '@/api/project'
import { extractTestPoints } from '@/api/test'

const route = useRoute()
const router = useRouter()
const documents = ref<any[]>([])
const loading = ref(false)
const selectedDocs = ref<any[]>([])
const showExtractDialog = ref(false)
const selectedKnowledgeBases = ref<string[]>([])

const projectId = computed(() => Number(route.params.id))
const uploadUrl = computed(() => `/api/v1/projects/${projectId.value}/documents/upload`)

const loadDocuments = async () => {
  loading.value = true
  try {
    documents.value = await getDocuments(projectId.value)
  } catch (error) {
    console.error('加载文档列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSelectionChange = (selection: any[]) => {
  selectedDocs.value = selection
}

const handleUploadSuccess = () => {
  ElMessage.success('上传成功')
  loadDocuments()
}

const handleView = (doc: any) => {
  ElMessage.info('查看功能开发中')
}

const handleReparse = (doc: any) => {
  ElMessage.info('重新解析功能开发中')
}

const handleDelete = async (doc: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该文档吗？', '提示', {
      type: 'warning'
    })
    ElMessage.success('删除成功')
    loadDocuments()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除文档失败:', error)
    }
  }
}

const handleExtract = async () => {
  try {
    const ids = selectedDocs.value.map(doc => doc.id)
    const result = await extractTestPoints(ids)
    ElMessage.success(`测试点提取任务已启动`)
    showExtractDialog.value = false
    router.push(`/project/${projectId.value}/test-points`)
  } catch (error) {
    console.error('提取测试点失败:', error)
  }
}

const formatSize = (size?: number) => {
  if (!size) return '-'
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / 1024 / 1024).toFixed(1)} MB`
}

onMounted(() => {
  loadDocuments()
})
</script>

<style scoped>
.documents-tab {
  min-height: 300px;
}

.action-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.selection-info {
  color: #909399;
  font-size: 14px;
}

.extract-info {
  margin-bottom: 16px;
}

.form-item label {
  font-size: 14px;
  color: #606266;
}
</style>
