import { defineStore } from 'pinia'
import { ref } from 'vue'
import { adminApi } from '../api/admin'

export const useAdminStore = defineStore('admin', () => {
  const users = ref([])
  const systemStats = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const getUsers = async (skip = 0, limit = 100) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await adminApi.getUsers(skip, limit)
      users.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки пользователей'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateUserRole = async (userId, role) => {
    try {
      const response = await adminApi.updateUserRole(userId, { role })
      
      // Обновляем роль пользователя в локальном списке
      const userIndex = users.value.findIndex(u => u.id === userId)
      if (userIndex !== -1) {
        users.value[userIndex].role = role
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка обновления роли'
      throw err
    }
  }

  const deleteUser = async (userId) => {
    try {
      await adminApi.deleteUser(userId)
      
      // Удаляем пользователя из локального списка
      users.value = users.value.filter(u => u.id !== userId)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка удаления пользователя'
      throw err
    }
  }

  const getSystemStats = async () => {
    try {
      // Если эндпоинта для статистики нет, создадим mock данные
      // const response = await adminApi.getSystemStats()
      // systemStats.value = response.data
      
      // Mock данные для демонстрации
      systemStats.value = {
        total_users: users.value.length,
        total_hotels: 45,
        total_bookings: 1234,
        active_bookings: 89,
        revenue: 4567890,
        popular_destinations: [
          { city: 'Москва', bookings: 234 },
          { city: 'Санкт-Петербург', bookings: 189 },
          { city: 'Сочи', bookings: 156 }
        ]
      }
      
      return systemStats.value
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки статистики'
      throw err
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    users,
    systemStats,
    loading,
    error,
    getUsers,
    updateUserRole,
    deleteUser,
    getSystemStats,
    clearError
  }
})