<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Вход в систему</h2>
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>Email:</label>
          <input 
            v-model="form.email"
            type="email" 
            required
            placeholder="Введите ваш email"
          >
        </div>
        
        <div class="form-group">
          <label>Пароль:</label>
          <input 
            v-model="form.password"
            type="password" 
            required
            placeholder="Введите пароль"
          >
        </div>
        
        <button type="submit" :disabled="loading" class="submit-btn">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
      
      <p class="auth-link">
        Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

export default {
  name: 'Login',
  setup() {
    const form = ref({
      email: '',
      password: ''
    })
    
    const loading = ref(false)
    const error = ref('')
    const router = useRouter()
    const authStore = useAuthStore()
    
    const handleLogin = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const user = await authStore.login(form.value)
        
        // Редирект в зависимости от роли
        if (user.role === 'admin') {
          router.push('/admin')
        } else if (user.role === 'hotel_manager') {
          router.push('/manager')
        } else {
          router.push('/')
        }
      } catch (err) {
        error.value = err.detail?.[0]?.msg || 'Ошибка входа. Проверьте данные.'
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      loading,
      error,
      handleLogin
    }
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  width: 100%;
  max-width: 400px;
}

.auth-card h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
}

.submit-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background: #2980b9;
}

.submit-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.error-message {
  background: #e74c3c;
  color: white;
  padding: 0.75rem;
  border-radius: 5px;
  text-align: center;
}

.auth-link {
  text-align: center;
  margin-top: 1.5rem;
}

.auth-link a {
  color: #3498db;
  text-decoration: none;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>