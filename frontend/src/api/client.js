import axios from 'axios'

const API_BASE_URL = 'https://hotel-booking-system-07d2.onrender.com' // Убедитесь, что это правильный URL вашего бэкенда

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: false // Важно для CORS
})

// Интерцептор для добавления токена
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Интерцептор для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_data')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient