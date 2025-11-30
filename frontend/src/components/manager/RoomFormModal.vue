<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ isEdit ? 'Редактирование номера' : 'Создание номера' }}</h2>
        <button @click="close" class="close-btn">×</button>
      </div>

      <form @submit.prevent="submitForm" class="room-form">
        <div class="form-group">
          <label>Номер комнаты *</label>
          <input 
            v-model="form.room_number"
            type="text" 
            required
            placeholder="Например: 101, A1"
            class="form-input"
          >
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Этаж</label>
            <input 
              v-model="form.floor"
              type="number" 
              min="0"
              placeholder="0"
              class="form-input"
            >
          </div>
          
          <div class="form-group">
            <label>Тип номера *</label>
            <select v-model="form.room_type_id" required class="form-input">
              <option value="">Выберите тип номера</option>
              <option 
                v-for="roomType in roomTypes" 
                :key="roomType.id" 
                :value="roomType.id"
              >
                {{ roomType.name }} ({{ roomType.capacity }} гостей, {{ formatPrice(roomType.base_price) }} ₽)
              </option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input 
              type="checkbox" 
              v-model="form.is_available"
            >
            <span class="checkmark"></span>
            Номер доступен для бронирования
          </label>
        </div>

        <div class="form-actions">
          <button type="button" @click="close" class="cancel-btn">
            Отмена
          </button>
          <button type="submit" :disabled="loading" class="submit-btn">
            {{ loading ? 'Сохранение...' : (isEdit ? 'Обновить' : 'Создать') }}
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
import { useManagerStore } from '../../stores/manager'

export default {
  name: 'RoomFormModal',
  props: {
    hotelId: {
      type: String,
      required: true
    },
    room: {
      type: Object,
      default: null
    },
    roomTypes: {
      type: Array,
      default: () => []
    }
  },
  emits: ['save', 'close'],
  setup(props, { emit }) {
    const managerStore = useManagerStore()
    
    const loading = ref(false)
    const error = ref('')
    
    const form = ref({
      room_number: '',
      floor: null,
      room_type_id: '',
      is_available: true
    })

    const isEdit = computed(() => props.room !== null)

    const submitForm = async () => {
      loading.value = true
      error.value = ''
      
      try {
        if (isEdit.value) {
          await managerStore.updateRoom(props.room.id, form.value)
        } else {
          await managerStore.createRoom(props.hotelId, form.value)
        }
        
        emit('save')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка сохранения номера'
      } finally {
        loading.value = false
      }
    }

    const close = () => {
      emit('close')
    }

    const formatPrice = (price) => {
      return new Intl.NumberFormat('ru-RU').format(price)
    }

    onMounted(() => {
      if (isEdit.value) {
        form.value = {
          room_number: props.room.room_number,
          floor: props.room.floor,
          room_type_id: props.room.room_type_id,
          is_available: props.room.is_available
        }
      }
    })

    return {
      form,
      loading,
      error,
      isEdit,
      submitForm,
      close,
      formatPrice
    }
  }
}
</script>

<style scoped>
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