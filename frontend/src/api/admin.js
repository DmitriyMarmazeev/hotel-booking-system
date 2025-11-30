import apiClient from './client'

export const adminApi = {
  // Получить всех пользователей
  getUsers(skip = 0, limit = 100) {
    return apiClient.get('/api/users/', {
      params: { skip, limit }
    })
  },

  // Обновить роль пользователя
  updateUserRole(userId, roleData) {
    return apiClient.put(`/api/users/${userId}/role`, roleData)
  },

  // Удалить пользователя
  deleteUser(userId) {
    return apiClient.delete(`/api/users/${userId}`)
  },

  // Получить статистику системы
  getSystemStats() {
    // Эндпоинт для статистики (может потребоваться создать на бэкенде)
    return apiClient.get('/api/admin/stats')
  }
}