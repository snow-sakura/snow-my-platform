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
      <el-table-column prop="uploaded_at" label="上传时间" width="180">
        <template #default="{ row }">
          {{ formatTime(row.uploaded_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="handleView(row)">查看</el-button>
          <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 查看文档对话框 -->
    <el-dialog v-model="showViewDialog" title="文档内容" width="700px" top="5vh">
      <div class="document-content" v-html="viewContent"></div>
    </el-dialog>

    <!-- AI提取测试点对话框 -->
    <el-dialog v-model="showExtractDialog" title="AI 提取测试点" width="500px">
      <div class="extract-info">
        <p>已选文档 {{ selectedDocs.length }} 个文档</p>
      </div>
      <div class="form-item">
        <label>关联知识库</label>
        <el-select v-model="selectedKnowledgeBases" multiple placeholder="请选择知识库（可选）" style="width: 100%; margin-top: 8px;">
          <el-option
            v-for="kb in knowledgeBases"
            :key="kb.id"
            :label="kb.name"
            :value="kb.id"
          />
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
import { getDocuments, deleteDocument, getDocument } from '@/api/project'
import { extractTestPoints } from '@/api/test'
import { getKnowledgeBases } from '@/api/knowledgeBase'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const documents = ref<any[]>([])
const loading = ref(false)
const selectedDocs = ref<any[]>([])
const showExtractDialog = ref(false)
const showViewDialog = ref(false)
const viewContent = ref('')
const selectedKnowledgeBases = ref<number[]>([])
const knowledgeBases = ref<any[]>([])

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

const loadKnowledgeBases = async () => {
  try {
    knowledgeBases.value = await getKnowledgeBases()
  } catch (error) {
    console.error('加载知识库列表失败:', error)
  }
}

const handleSelectionChange = (selection: any[]) => {
  selectedDocs.value = selection
}

const handleUploadSuccess = () => {
  ElMessage.success('上传成功')
  loadDocuments()
}

const handleView = async (doc: any) => {
  try {
    const detail = await getDocument(projectId.value, doc.id)
    viewContent.value = (detail.content || '暂无内容').replace(/\n/g, '<br>')
    showViewDialog.value = true
  } catch (error) {
    ElMessage.error('加载文档内容失败')
  }
}

const handleDelete = async (doc: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该文档吗？', '提示', { type: 'warning' })
    await deleteDocument(projectId.value, doc.id)
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
    const kbIds = selectedKnowledgeBases.value.length > 0 ? selectedKnowledgeBases.value : undefined
    await extractTestPoints(ids, kbIds)
    ElMessage.success('测试点提取任务已启动')
    showExtractDialog.value = false
    router.push(`/project/${projectId.value}/test-points`)
  } catch (error) {
    console.error('提取测试点失败:', error)
  }
}

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

onMounted(() => {
  loadDocuments()
  loadKnowledgeBases()
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

.document-content {
  max-height: 60vh;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
  background: #f5f7fa;
  padding: 16px;
  border-radius: 4px;
  line-height: 1.6;
}
</style>
