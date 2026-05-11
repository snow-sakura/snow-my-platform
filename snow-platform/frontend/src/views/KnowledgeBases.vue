<template>
  <div class="knowledge-bases-tab">
    <div class="action-bar">
      <el-button type="primary" @click="handleCreate">新建知识库</el-button>
    </div>

    <div v-for="kb in knowledgeBases" :key="kb.id" class="knowledge-base-card">
      <div class="kb-header">
        <div class="kb-title">
          <span class="kb-name">{{ kb.name }}</span>
          <el-tag size="small">{{ kb.documents?.length || 0 }} 文档</el-tag>
        </div>
        <el-button type="text" @click="toggleExpand(kb.id)">
          <el-icon><ArrowDown v-if="!expandedMap[kb.id]" /><ArrowUp v-else /></el-icon>
        </el-button>
      </div>

      <div class="kb-description">{{ kb.description || '暂无描述' }}</div>

      <div v-if="expandedMap[kb.id]" class="kb-content">
        <div class="kb-actions">
          <el-upload
            :action="getUploadUrl(kb.id)"
            :on-success="() => handleUploadSuccess(kb.id)"
            :show-file-list="false"
            accept=".pdf,.docx,.md,.markdown,.yaml,.yml,.csv,.txt"
          >
            <el-button type="primary" size="small">上传文档</el-button>
          </el-upload>
          <el-button size="small" @click="handleEditKb(kb)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDeleteKb(kb.id)">删除</el-button>
        </div>

        <el-table :data="kb.documents" v-loading="kb.loading" size="small">
          <el-table-column prop="filename" label="文件名" />
          <el-table-column prop="file_type" label="类型" width="80">
            <template #default="{ row }">
              <el-tag size="small" type="info">{{ row.file_type?.toUpperCase() }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="chunk_count" label="分块数" width="100" />
          <el-table-column prop="uploaded_at" label="上传时间" width="160">
            <template #default="{ row }">
              {{ formatTime(row.uploaded_at) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <el-empty v-if="knowledgeBases.length === 0" description="暂无知识库，点击新建知识库" />

    <!-- 创建/编辑知识库对话框 -->
    <el-dialog v-model="showDialog" :title="isEditing ? '编辑知识库' : '新建知识库'" width="500px">
      <el-form :model="formData" label-width="100px">
        <el-form-item label="知识库名称" required>
          <el-input v-model="formData.name" placeholder="请输入知识库名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入知识库描述" />
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowDown, ArrowUp } from '@element-plus/icons-vue'
import { getKnowledgeBases, createKnowledgeBase, updateKnowledgeBase, deleteKnowledgeBase, getKnowledgeBaseDocuments } from '@/api/knowledgeBase'
import dayjs from 'dayjs'

const knowledgeBases = ref<any[]>([])
const loading = ref(false)
const showDialog = ref(false)
const isEditing = ref(false)
const editingId = ref<number | null>(null)
const saving = ref(false)
const expandedMap = reactive<Record<number, boolean>>({})

const formData = ref({ name: '', description: '' })

const loadKnowledgeBases = async () => {
  loading.value = true
  try {
    knowledgeBases.value = await getKnowledgeBases()
    for (const kb of knowledgeBases.value) {
      kb.documents = []
      kb.loading = false
    }
  } catch (error) {
    console.error('加载知识库失败:', error)
  } finally {
    loading.value = false
  }
}

const getUploadUrl = (kbId: number) => {
  return `/api/v1/knowledge-bases/${kbId}/documents/upload`
}

const toggleExpand = async (kbId: number) => {
  expandedMap[kbId] = !expandedMap[kbId]
  if (expandedMap[kbId]) {
    const kb = knowledgeBases.value.find(k => k.id === kbId)
    if (kb && kb.documents.length === 0) {
      kb.loading = true
      try {
        kb.documents = await getKnowledgeBaseDocuments(kbId)
      } catch (error) {
        console.error('加载文档失败:', error)
      } finally {
        kb.loading = false
      }
    }
  }
}

const handleUploadSuccess = async (kbId: number) => {
  ElMessage.success('上传成功')
  const kb = knowledgeBases.value.find(k => k.id === kbId)
  if (kb) {
    kb.documents = await getKnowledgeBaseDocuments(kbId)
  }
}

const resetForm = () => {
  formData.value = { name: '', description: '' }
  editingId.value = null
}

const handleCreate = () => {
  isEditing.value = false
  resetForm()
  showDialog.value = true
}

const handleEditKb = (kb: any) => {
  isEditing.value = true
  editingId.value = kb.id
  formData.value = { name: kb.name, description: kb.description || '' }
  showDialog.value = true
}

const handleSave = async () => {
  if (!formData.value.name) {
    ElMessage.warning('请输入知识库名称')
    return
  }
  saving.value = true
  try {
    if (isEditing.value && editingId.value) {
      await updateKnowledgeBase(editingId.value, formData.value)
      ElMessage.success('更新成功')
    } else {
      await createKnowledgeBase(formData.value)
      ElMessage.success('创建成功')
    }
    showDialog.value = false
    resetForm()
    loadKnowledgeBases()
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    saving.value = false
  }
}

const handleDeleteKb = async (kbId: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该知识库吗？所有关联文档将被删除。', '提示', { type: 'warning' })
    await deleteKnowledgeBase(kbId)
    ElMessage.success('删除成功')
    delete expandedMap[kbId]
    loadKnowledgeBases()
  } catch (error) {
    if (error !== 'cancel') console.error('删除失败:', error)
  }
}

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

onMounted(() => {
  loadKnowledgeBases()
})
</script>

<style scoped>
.knowledge-bases-tab {
  min-height: 300px;
}

.action-bar {
  margin-bottom: 20px;
}

.knowledge-base-card {
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 16px;
}

.kb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.kb-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.kb-name {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.kb-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 16px;
}

.kb-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.kb-content {
  border-top: 1px solid #ebeef5;
  padding-top: 16px;
}
</style>
