import request from '@/utils/request'

export interface SystemSetting {
  id: number
  key: string
  value: string
  description?: string
  updated_at: string
}

// 获取所有系统设置
export const getSettings = () => {
  return request.get<SystemSetting[]>('/settings/')
}

// 获取单个设置
export const getSetting = (key: string) => {
  return request.get<SystemSetting>(`/settings/${key}`)
}

// 创建或更新设置
export const saveSetting = (data: { key: string; value: string; description?: string }) => {
  return request.post<SystemSetting>('/settings/', data)
}

// 更新设置
export const updateSetting = (key: string, value: string) => {
  return request.put<SystemSetting>(`/settings/${key}`, { value })
}
