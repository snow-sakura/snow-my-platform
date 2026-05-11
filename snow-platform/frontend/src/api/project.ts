import request from '@/utils/request'

export interface Project {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
  doc_count?: number
  test_point_count?: number
  test_case_count?: number
}

export interface ProjectCreate {
  name: string
  description?: string
}

// 获取项目列表
export const getProjects = () => {
  return request.get<Project[]>('/projects/')
}

// 创建项目
export const createProject = (data: ProjectCreate) => {
  return request.post<Project>('/projects/', data)
}

// 获取项目详情
export const getProject = (id: number) => {
  return request.get<Project>(`/projects/${id}`)
}

// 更新项目
export const updateProject = (id: number, data: Partial<ProjectCreate>) => {
  return request.put<Project>(`/projects/${id}`, data)
}

// 删除项目
export const deleteProject = (id: number) => {
  return request.delete(`/projects/${id}`)
}

// 上传文档
export const uploadDocument = (projectId: number, file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post(`/projects/${projectId}/documents/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export interface DocumentDetail {
  id: number
  project_id: number
  filename: string
  file_type: string
  content?: string
  uploaded_at: string
}

// 获取文档列表
export const getDocuments = (projectId: number) => {
  return request.get<DocumentDetail[]>(`/projects/${projectId}/documents`)
}

// 获取文档详情
export const getDocument = (projectId: number, documentId: number) => {
  return request.get<DocumentDetail>(`/projects/${projectId}/documents/${documentId}`)
}

// 删除文档
export const deleteDocument = (projectId: number, documentId: number) => {
  return request.delete(`/projects/${projectId}/documents/${documentId}`)
}
