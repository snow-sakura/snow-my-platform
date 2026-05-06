<template>
  <div class="knowledge-bases-tab">
    <div class="action-bar">
      <el-button type="primary" @click="showCreateKbDialog = true">新建知识库</el-button>
    </div>

    <div v-for="kb in knowledgeBases" :key="kb.id" class="knowledge-base-card">
      <div class="kb-header">
        <div class="kb-title">
          <span class="kb-name">{{ kb.name }}</span>
          <el-tag size="small">{{ kb.document_count }} 文档</el-tag>
          <el-tag size="small">{{ kb.chunk_count }} 分块</el-tag>
          <el-tag size="small" type="success">正常</el-tag>
        </div>
        <el-button type="text" @click="kb.expanded = !kb.expanded">
          <el-icon><ArrowDown v-if="!kb.expanded" /><ArrowUp v-else /></el-icon>
        </el-button>
      </div>
      
      <div class="kb-description">{{ kb.description || '暂无描述' }}</div>
      
      <div v-if="kb.expanded" class="kb-content">
        <div class="kb-actions">
          <el-upload
            :action="getUploadUrl(kb.id)"
            :on-success="() => handleUploadSuccess(kb.id)"
            :show-file-list="false"
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
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag size="small" type="success">已完成</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80">
            <template #default="{ row }">
              <el-button type="danger" link size="small" @click="handleDeleteDoc(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <el-empty v-if="knowledgeBases.length === 0" description="暂无知识库，点击新建知识库" />

    <!-- 创建知识库对话框 -->
    <el-dialog v-model="showCreateKbDialog" title="新建知识库" width="500px">
      <el-form :model="createForm" label-width="100px">
        <el-form-item label="知识库名称" required>
          <el-input v-model="createForm.name" placeholder="请输入知识库名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="createForm.description" type="textarea" :rows="3" placeholder="请输入知识库描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateKbDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreateKb">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowDown, ArrowUp } from '@element-plus/icons-vue'

const route = useRoute()
const knowledgeBases = ref<any[]>([])
const loading = ref(false)
const showCreateKbDialog = ref(false)
const createForm = ref({ name: '', description: '' })

const projectId = computed(() => Number(route.params.id))

const loadKnowledgeBases = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取知识库列表
    knowledgeBases.value = []
  } catch (error) {
    console.error('加载知识库失败:', error)
  } finally {
    loading.value = false
  }
}

const getUploadUrl = (kbId: number) => {
  return `/api/v1/knowledge-bases/${kbId}/documents/upload`
}

const handleUploadSuccess = (kbId: number) => {
  ElMessage.success('上传成功')
  loadKnowledgeBases()
}

const handleCreateKb = () => {
  if (!createForm.value.name) {
    ElMessage.warning('请输入知识库名称')
    return
  }
  ElMessage.success('创建成功')
  showCreateKbDialog.value = false
  loadKnowledgeBases()
}

const handleEditKb = (kb: any) => {
  ElMessage.info('编辑功能开发中')
}

const handleDeleteKb = async (kbId: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该知识库吗？', '提示', {
      type: 'warning'
    })
    ElMessage.success('删除成功')
    loadKnowledgeBases()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除知识库失败:', error)
    }
  }
}

const handleDeleteDoc = (doc: any) => {
  ElMessage.info('删除功能开发中')
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
</style>
