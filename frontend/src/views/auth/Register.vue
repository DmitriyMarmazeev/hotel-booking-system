<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Регистрация</h2>
      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label>Имя:</label>
          <input 
            v-model="form.first_name"
            type="text" 
            required
            placeholder="Введите ваше имя"
            class="form-input"
          >
        </div>
        
        <div class="form-group">
          <label>Фамилия:</label>
          <input 
            v-model="form.last_name"
            type="text" 
            required
            placeholder="Введите вашу фамилию"
            class="form-input"
          >
        </div>
        
        <div class="form-group">
          <label>Email:</label>
          <input 
            v-model="form.email"
            type="email" 
            required
            placeholder="Введите ваш email"
            class="form-input"
          >
        </div>
        
        <div class="form-group">
          <label>Телефон:</label>
          <input 
            v-model="form.phone"
            type="tel" 
            placeholder="Введите ваш телефон"
            class="form-input"
          >
        </div>
        
        <div class="form-group">
          <label>Пароль:</label>
          <input 
            v-model="form.password"
            type="password" 
            required
            placeholder="Придумайте пароль"
            class="form-input"
          >
        </div>
        
        <button type="submit" :disabled="loading" class="submit-btn">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div v-if="success" class="success-message">
          Регистрация успешна! <router-link to="/login">Войдите в систему</router-link>
        </div>
      </form>
      
      <p class="auth-link">
        Уже есть аккаунт? <router-link to="/login">Войти</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '../../stores/auth'

export default {
  name: 'Register',
  setup() {
    const form = ref({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      password: ''
    })
    
    const loading = ref(false)
    const error = ref('')
    const success = ref(false)
    const authStore = useAuthStore()
    
    const handleRegister = async () => {
      loading.value = true
      error.value = ''
      success.value = false
      
      try {
        await authStore.register(form.value)
        success.value = true
        // Очищаем форму после успешной регистрации
        form.value = {
          first_name: '',
          last_name: '',
          email: '',
          phone: '',
          password: ''
        }
      } catch (err) {
        console.error('Registration error:', err)
        error.value = err.detail?.[0]?.msg || err.message || 'Ошибка регистрации. Попробуйте снова.'
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      loading,
      error,
      success,
      handleRegister
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
  padding: 2rem;
}

.auth-card {
  background: white;
  padding: 3rem;
  border-radius: 15px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 500px;
}

.auth-card h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 600;
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
  font-size: 0.9rem;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  background: white;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-input::placeholder {
  color: #adb5bd;
}

.submit-btn {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(52, 152, 219, 0.3);
}

.submit-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.error-message {
  background: #e74c3c;
  color: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  font-size: 0.9rem;
  margin-top: 1rem;
}

.success-message {
  background: #27ae60;
  color: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  font-size: 0.9rem;
  margin-top: 1rem;
}

.success-message a {
  color: white;
  text-decoration: underline;
  font-weight: 600;
}

.auth-link {
  text-align: center;
  margin-top: 2rem;
  color: #6c757d;
}

.auth-link a {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.auth-link a:hover {
  color: #2980b9;
  text-decoration: underline;
}

/* Адаптивность */
@media (max-width: 768px) {
  .auth-container {
    padding: 1rem;
  }
  
  .auth-card {
    padding: 2rem;
  }
  
  .auth-card h2 {
    font-size: 1.5rem;
  }
}
</style>