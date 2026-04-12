<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Создание типа номера</h2>
        <button @click="close" class="close-btn">×</button>
      </div>

      <form @submit.prevent="submitForm" class="room-type-form">
        <div class="form-group">
          <label>Название типа *</label>
          <input 
            v-model="form.name"
            type="text" 
            required
            placeholder="Например: Стандарт, Люкс, Семейный"
            class="form-input"
          >
        </div>

        <div class="form-group">
          <label>Описание</label>
          <textarea 
            v-model="form.description"
            placeholder="Опишите особенности этого типа номера"
            class="form-input textarea"
            rows="3"
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Базовая цена за ночь *</label>
            <input 
              v-model="form.base_price"
              type="number" 
              required
              min="0"
              step="0.01"
              placeholder="0.00"
              class="form-input"
            >
          </div>
          
          <div class="form-group">
            <label>Вместимость (гостей) *</label>
            <input 
              v-model="form.capacity"
              type="number" 
              required
              min="1"
              placeholder="2"
              class="form-input"
            >
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Площадь (м²)</label>
            <input 
              v-model="form.size_sqm"
              type="number" 
              min="1"
              placeholder="20"
              class="form-input"
            >
          </div>
          
          <div class="form-group">
            <label>Тип кровати</label>
            <input 
              v-model="form.bed_type"
              type="text" 
              placeholder="Например: Двуспальная, Две односпальные"
              class="form-input"
            >
          </div>
        </div>

        <div class="form-group">
          <label>Удобства номера</label>
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

        <div class="form-actions">
          <button type="button" @click="close" class="cancel-btn">
            Отмена
          </button>
          <button type="submit" :disabled="loading" class="submit-btn">
            {{ loading ? 'Создание...' : 'Создать тип номера' }}
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
import { ref } from 'vue'
import { useManagerStore } from '../../stores/manager'

export default {
  name: 'RoomTypeFormModal',
  emits: ['save', 'close'],
  setup(props, { emit }) {
    const managerStore = useManagerStore()
    
    const loading = ref(false)
    const error = ref('')
    
    const form = ref({
      name: '',
      description: '',
      base_price: '',
      capacity: '',
      size_sqm: null,
      bed_type: '',
      amenities: []
    })

    const commonAmenities = [
      'Кондиционер',
      'Отопление',
      'Телевизор',
      'Wi-Fi',
      'Мини-бар',
      'Сейф',
      'Фен',
      'Утюг',
      'Кофеварка',
      'Чайник',
      'Балкон',
      'Вид на море',
      'Вид на город',
      'Кухня',
      'Гостиная зона',
      'Рабочий стол',
      'Гардероб',
      'Ванная комната',
      'Душ',
      'Ванна',
      'Тапочки',
      'Халаты',
      'Туалетные принадлежности'
    ]

    const submitForm = async () => {
      loading.value = true
      error.value = ''
      
      try {
        await managerStore.createRoomType(form.value)
        emit('save')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка создания типа номера'
      } finally {
        loading.value = false
      }
    }

    const close = () => {
      emit('close')
    }

    return {
      form,
      loading,
      error,
      commonAmenities,
      submitForm,
      close
    }
  }
}
</script>

<style scoped>
.amenities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.5rem;
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
  font-size: 0.9rem;
}

.amenity-checkbox:hover {
  background: #f8f9fa;
}

.amenity-checkbox input[type="checkbox"] {
  margin: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.3);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #7f8c8d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #e74c3c;
}

.room-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-input {
  width: 100%;
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
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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
  padding-top: 1.5rem;
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
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .modal-content {
    margin: 1rem;
  }
}
</style>