import request from '@/utils/request'

export interface KnowledgeBase {
  id: number
  name: string
  description?: string
  chroma_collection_name: string
  created_at: string
}

export interface KnowledgeBaseCreate {
  name: string
  description?: string
}

export interface KnowledgeBaseUpdate {
  name?: string
  description?: string
}

export interface KnowledgeDocument {
  id: number
  knowledge_base_id: number
  filename: string
  file_type: string
  chunk_count: number
  uploaded_at: string
}

// 获取知识库列表
export const getKnowledgeBases = () => {
  return request.get<KnowledgeBase[]>('/knowledge-bases/')
}

// 创建知识库
export const createKnowledgeBase = (data: KnowledgeBaseCreate) => {
  return request.post<KnowledgeBase>('/knowledge-bases/', data)
}

// 更新知识库
export const updateKnowledgeBase = (id: number, data: KnowledgeBaseUpdate) => {
  return request.put<KnowledgeBase>(`/knowledge-bases/${id}`, data)
}

// 删除知识库
export const deleteKnowledgeBase = (id: number) => {
  return request.delete(`/knowledge-bases/${id}`)
}

// 获取知识库文档列表
export const getKnowledgeBaseDocuments = (kbId: number) => {
  return request.get<KnowledgeDocument[]>(`/knowledge-bases/${kbId}/documents`)
}

// 上传知识库文档
export const uploadKnowledgeBaseDocument = (kbId: number, file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post(`/knowledge-bases/${kbId}/documents/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
