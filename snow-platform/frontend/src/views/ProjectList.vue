<template>
  <div class="project-list-page">
    <div class="page-header">
      <div class="breadcrumb">首页</div>
      <div class="page-title">项目列表</div>
      <el-button type="primary" @click="showCreateDialog = true">+ 新建项目</el-button>
    </div>
    
    <div class="project-grid">
      <div class="project-card" v-for="project in projects" :key="project.id" @click="goToProject(project.id)">
        <div class="card-header">
          <span class="project-name">{{ project.name }}</span>
          <el-dropdown @click.stop>
            <span class="more-icon">...</span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click.stop="handleEdit(project)">编辑</el-dropdown-item>
                <el-dropdown-item @click.stop="handleDelete(project.id)">删除</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        
        <div class="card-description">
          {{ project.description || '暂无描述' }}
        </div>
        
        <div class="card-stats">
          <div class="stat-item">
            <div class="stat-value" style="color: #3498db;">{{ project.doc_count || 0 }}</div>
            <div class="stat-label">文档</div>
          </div>
          <div class="stat-item">
            <div class="stat-value" style="color: #2ecc71;">{{ project.test_point_count || 0 }}</div>
            <div class="stat-label">测试点</div>
          </div>
          <div class="stat-item">
            <div class="stat-value" style="color: #f39c12;">{{ project.test_case_count || 0 }}</div>
            <div class="stat-label">用例</div>
          </div>
        </div>
      </div>
      
      <el-empty v-if="projects.length === 0" description="暂无项目，点击右上角新建项目" />
    </div>

    <!-- 创建项目对话框 -->
    <el-dialog v-model="showCreateDialog" title="新建项目" width="500px">
      <el-form :model="createForm" label-width="80px">
        <el-form-item label="项目名称" required>
          <el-input v-model="createForm.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目描述">
          <el-input 
            v-model="createForm.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入项目描述" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate" :loading="creating">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getProjects, createProject, deleteProject, type ProjectCreate } from '@/api/project'

const router = useRouter()
const projects = ref<any[]>([])
const showCreateDialog = ref(false)
const creating = ref(false)
const createForm = ref<ProjectCreate>({
  name: '',
  description: ''
})

const loadProjects = async () => {
  try {
    projects.value = await getProjects()
  } catch (error) {
    console.error('加载项目列表失败:', error)
  }
}

const handleCreate = async () => {
  if (!createForm.value.name) {
    ElMessage.warning('请输入项目名称')
    return
  }
  
  creating.value = true
  try {
    await createProject(createForm.value)
    ElMessage.success('项目创建成功')
    showCreateDialog.value = false
    createForm.value = { name: '', description: '' }
    await loadProjects()
  } catch (error) {
    console.error('创建项目失败:', error)
  } finally {
    creating.value = false
  }
}

const handleEdit = (project: any) => {
  ElMessage.info('编辑功能开发中')
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', {
      type: 'warning'
    })
    await deleteProject(id)
    ElMessage.success('删除成功')
    await loadProjects()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除项目失败:', error)
    }
  }
}

const goToProject = (id: number) => {
  router.push(`/project/${id}/documents`)
}

onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.project-list-page {
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.breadcrumb {
  color: #909399;
  font-size: 14px;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
  margin-left: 15px;
  flex: 1;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.project-card {
  background: #fff;
  border-radius: 4px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.project-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.project-name {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.more-icon {
  color: #909399;
  cursor: pointer;
  padding: 4px 8px;
}

.card-description {
  color: #606266;
  font-size: 14px;
  min-height: 40px;
  margin-bottom: 16px;
  word-break: break-all;
}

.card-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}
</style>
