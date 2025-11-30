<template>
  <div class="hotel-form-page">
    <div class="form-container">
      <div class="form-header">
        <h1>{{ isEdit ? 'Редактирование отеля' : 'Создание отеля' }}</h1>
        <router-link to="/manager/hotels" class="back-link">
          ← Назад к списку отелей
        </router-link>
      </div>

      <form @submit.prevent="submitForm" class="hotel-form">
        <div class="form-section">
          <h2>Основная информация</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label>Название отеля *</label>
              <input 
                v-model="form.name"
                type="text" 
                required
                placeholder="Введите название отеля"
                class="form-input"
                :class="{ error: errors.name }"
              >
              <span v-if="errors.name" class="error-text">{{ errors.name }}</span>
            </div>
          </div>

          <div class="form-group">
            <label>Описание</label>
            <textarea 
              v-model="form.description"
              placeholder="Опишите ваш отель, его особенности и преимущества"
              class="form-input textarea"
              rows="4"
            ></textarea>
          </div>
        </div>

        <div class="form-section">
          <h2>Контакты</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label>Контактный email</label>
              <input 
                v-model="form.contact_email"
                type="email" 
                placeholder="email@example.com"
                class="form-input"
              >
            </div>
            
            <div class="form-group">
              <label>Контактный телефон</label>
              <input 
                v-model="form.contact_phone"
                type="tel" 
                placeholder="+7 (XXX) XXX-XX-XX"
                class="form-input"
              >
            </div>
          </div>
        </div>

        <div class="form-section">
          <h2>Адрес</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label>Адрес *</label>
              <input 
                v-model="form.address"
                type="text" 
                required
                placeholder="Полный адрес отеля"
                class="form-input"
                :class="{ error: errors.address }"
              >
              <span v-if="errors.address" class="error-text">{{ errors.address }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Город *</label>
              <input 
                v-model="form.city"
                type="text" 
                required
                placeholder="Город"
                class="form-input"
                :class="{ error: errors.city }"
              >
              <span v-if="errors.city" class="error-text">{{ errors.city }}</span>
            </div>
            
            <div class="form-group">
              <label>Страна *</label>
              <input 
                v-model="form.country"
                type="text" 
                required
                placeholder="Страна"
                class="form-input"
                :class="{ error: errors.country }"
              >
              <span v-if="errors.country" class="error-text">{{ errors.country }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Широта</label>
              <input 
                v-model="form.latitude"
                type="number" 
                step="any"
                placeholder="55.7558"
                class="form-input"
              >
            </div>
            
            <div class="form-group">
              <label>Долгота</label>
              <input 
                v-model="form.longitude"
                type="number" 
                step="any"
                placeholder="37.6173"
                class="form-input"
              >
            </div>
          </div>
        </div>

        <div class="form-section">
          <h2>Дополнительная информация</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label>Количество звезд</label>
              <select v-model="form.star_rating" class="form-input">
                <option :value="null">Не указано</option>
                <option v-for="n in 5" :key="n" :value="n">{{ n }} ⭐</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Удобства отеля</label>
            <div class="amenities-grid">
              <label 
                v-for="amenity in commonAmenities" 
                :key="amenity"
                class="amenity-checkbox"
              >
                <input 
                  type="checkbox" 
                  :value="amenity"
                  v-model="form.amenities"
                >
                <span class="checkmark"></span>
                {{ amenity }}
              </label>
            </div>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input 
                type="checkbox" 
                v-model="form.is_active"
              >
              <span class="checkmark"></span>
              Отель активен и принимает бронирования
            </label>
          </div>
        </div>

        <div class="form-actions">
          <button 
            type="button" 
            @click="$router.push('/manager/hotels')"
            class="cancel-btn"
          >
            Отмена
          </button>
          <button 
            type="submit" 
            :disabled="loading"
            class="submit-btn"
          >
            {{ loading ? 'Сохранение...' : (isEdit ? 'Обновить отель' : 'Создать отель') }}
          </button>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useManagerStore } from '../../stores/manager'

export default {
  name: 'HotelForm',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const managerStore = useManagerStore()
    
    const isEdit = computed(() => route.params.id !== undefined)
    const loading = ref(false)
    const error = ref('')
    
    const form = ref({
      name: '',
      description: '',
      address: '',
      city: '',
      country: '',
      latitude: null,
      longitude: null,
      star_rating: null,
      contact_email: '',
      contact_phone: '',
      amenities: [],
      images: [],
      is_active: true
    })
    
    const errors = ref({})
    
    const commonAmenities = [
      'Wi-Fi',
      'Бассейн',
      'Спа',
      'Фитнес-центр',
      'Ресторан',
      'Бар',
      'Парковка',
      'Кондиционер',
      'Отопление',
      'Лифт',
      'Для людей с ограниченными возможностями',
      'Трансфер',
      'Экскурсии',
      'Прачечная',
      'Химчистка'
    ]

    const validateForm = () => {
      errors.value = {}
      
      if (!form.value.name.trim()) {
        errors.value.name = 'Название отеля обязательно'
      }
      if (!form.value.address.trim()) {
        errors.value.address = 'Адрес обязателен'
      }
      if (!form.value.city.trim()) {
        errors.value.city = 'Город обязателен'
      }
      if (!form.value.country.trim()) {
        errors.value.country = 'Страна обязательна'
      }
      
      return Object.keys(errors.value).length === 0
    }

    const submitForm = async () => {
      if (!validateForm()) return
      
      loading.value = true
      error.value = ''
      
      try {
        // Очищаем пустые значения
        const submitData = { ...form.value }
        Object.keys(submitData).forEach(key => {
          if (submitData[key] === '' || submitData[key] === null) {
            delete submitData[key]
          }
        })
        
        if (isEdit.value) {
          await managerStore.updateHotel(route.params.id, submitData)
        } else {
          await managerStore.createHotel(submitData)
        }
        
        router.push('/manager/hotels')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка сохранения отеля'
      } finally {
        loading.value = false
      }
    }

    const loadHotelData = async () => {
      if (!isEdit.value) return
      
      loading.value = true
      try {
        await managerStore.getMyHotels()
        const hotel = managerStore.myHotels.find(h => h.id === route.params.id)
        if (hotel) {
          form.value = { ...form.value, ...hotel }
        } else {
          throw new Error('Отель не найден')
        }
      } catch (err) {
        error.value = 'Ошибка загрузки данных отеля'
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      if (isEdit.value) {
        loadHotelData()
      }
    })

    return {
      form,
      errors,
      loading,
      error,
      isEdit,
      commonAmenities,
      submitForm
    }
  }
}
</script>

<style scoped>
.hotel-form-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.form-header h1 {
  color: #2c3e50;
  margin: 0;
}

.back-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.back-link:hover {
  text-decoration: underline;
}

.hotel-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.form-section {
  margin-bottom: 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
}

.form-section h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-input {
  padding: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
  background: #f8f9fa;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  background: white;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-input.error {
  border-color: #e74c3c;
}

.form-input.textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.error-text {
  color: #e74c3c;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.amenities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.amenity-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.amenity-checkbox:hover {
  background: #f8f9fa;
}

.amenity-checkbox input[type="checkbox"] {
  margin: 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: normal;
}

.checkbox-label input[type="checkbox"] {
  margin: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

.cancel-btn {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-btn:hover {
  background: #7f8c8d;
}

.submit-btn {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
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
  border-radius: 6px;
  text-align: center;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .form-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .amenities-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .hotel-form {
    padding: 1.5rem;
  }
}
</style>