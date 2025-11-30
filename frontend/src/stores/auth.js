import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '../api/client'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('auth_token'))
  const user = ref(JSON.parse(localStorage.getItem('user_data') || 'null'))
  const router = useRouter()

  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || null)

  const login = async (credentials) => {
    try {
      const formData = new FormData()
      formData.append('username', credentials.email)
      formData.append('password', credentials.password)
      
      const response = await apiClient.post('/api/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      
      const { access_token } = response.data
      token.value = access_token
      localStorage.setItem('auth_token', access_token)
      
      // Получаем данные пользователя
      const userResponse = await apiClient.get('/api/auth/me')
      user.value = userResponse.data
      localStorage.setItem('user_data', JSON.stringify(userResponse.data))
      
      return userResponse.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const register = async (userData) => {
    try {
      const response = await apiClient.post('/api/auth/register', userData)
      return response.data
    } catch (err) {
      // Более детальная обработка ошибок
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          throw new Error(err.response.data.detail[0]?.msg || 'Ошибка валидации')
        } else {
          throw new Error(err.response.data.detail)
        }
      } else if (err.response?.data?.message) {
        throw new Error(err.response.data.message)
      } else {
        throw new Error('Ошибка соединения с сервером')
      }
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
    router.push('/login')
  }

  const checkAuth = async () => {
    if (!token.value) return false
    
    try {
      const response = await apiClient.get('/api/auth/me')
      user.value = response.data
      return true
    } catch (error) {
      logout()
      return false
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    userRole,
    login,
    register,
    logout,
    checkAuth
  }
})