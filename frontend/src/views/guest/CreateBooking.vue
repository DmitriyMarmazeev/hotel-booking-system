<template>
  <div class="create-booking">
    <div class="booking-container">
      <div v-if="loading" class="loading-state">
        <LoadingSpinner message="Создаём бронирование..." />
      </div>

      <div v-else-if="error" class="error-state">
        <div class="error-message">
          {{ error }}
        </div>
        <router-link to="/search" class="back-link">← Вернуться к поиску</router-link>
      </div>

      <div v-else class="booking-content">
        <div class="booking-header">
          <h1>Подтверждение бронирования</h1>
          <router-link to="/search" class="back-link">← Назад к поиску</router-link>
        </div>

        <div class="booking-details">
          <div class="section">
            <h2>Информация о номере</h2>
            <div class="detail-card">
              <div class="room-info">
                <h3>{{ room.room_number }} - {{ room.room_type.name }}</h3>
                <p><strong>Отель:</strong> {{ hotel.name }}</p>
                <p><strong>Адрес:</strong> {{ hotel.address }}, {{ hotel.city }}, {{ hotel.country }}</p>
                <p><strong>Вместимость:</strong> до {{ room.room_type.capacity }} гостей</p>
                <p><strong>Цена за ночь:</strong> {{ formatPrice(room.room_type.base_price) }} ₽</p>
              </div>
            </div>
          </div>

          <div class="section">
            <h2>Даты проживания</h2>
            <div class="detail-card">
              <div class="date-info">
                <p><strong>Заезд:</strong> {{ formatDate(bookingData.check_in_date) }}</p>
                <p><strong>Выезд:</strong> {{ formatDate(bookingData.check_out_date) }}</p>
                <p><strong>Количество ночей:</strong> {{ calculateNights() }}</p>
                <p><strong>Общая стоимость:</strong> {{ formatPrice(totalPrice) }} ₽</p>
              </div>
            </div>
          </div>

          <div class="section">
            <h2>Информация о гостях</h2>
            <div class="detail-card">
              <form @submit.prevent="createBooking" class="guest-form">
                <div class="form-group">
                  <label>Количество гостей *</label>
                  <select v-model="bookingData.number_of_guests" class="form-input" required>
                    <option v-for="n in room.room_type.capacity" :key="n" :value="n">
                      {{ n }} {{ n === 1 ? 'гость' : 'гостей' }}
                    </option>
                  </select>
                </div>

                <div class="form-group">
                  <label>Особые пожелания</label>
                  <textarea 
                    v-model="bookingData.special_requests"
                    class="form-input textarea"
                    placeholder="Укажите дополнительные пожелания (необязательно)"
                    rows="4"
                  ></textarea>
                </div>

                <div class="booking-summary">
                  <div class="summary-item">
                    <span>Стоимость за {{ calculateNights() }} ночей:</span>
                    <span>{{ formatPrice(totalPrice) }} ₽</span>
                  </div>
                  <div class="summary-total">
                    <strong>Итого к оплате:</strong>
                    <strong>{{ formatPrice(totalPrice) }} ₽</strong>
                  </div>
                </div>

                <button 
                  type="submit" 
                  :disabled="creatingBooking" 
                  class="submit-booking-btn"
                >
                  {{ creatingBooking ? 'Бронируем...' : 'Подтвердить бронирование' }}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHotelsStore } from '../../stores/hotels'
import { bookingsApi } from '../../api/bookings'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'CreateBooking',
  components: {
    LoadingSpinner
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const hotelsStore = useHotelsStore()
    
    const room = ref({})
    const hotel = ref({})
    const loading = ref(true)
    const error = ref('')
    const creatingBooking = ref(false)
    
    const bookingData = ref({
      room_id: route.params.roomId,
      check_in_date: route.query.check_in,
      check_out_date: route.query.check_out,
      number_of_guests: parseInt(route.query.guests) || 1,
      special_requests: ''
    })

    const totalPrice = computed(() => {
      if (!room.value.room_type?.base_price) return 0
      const nights = calculateNights()
      return room.value.room_type.base_price * nights
    })

    const loadRoomDetails = async () => {
      try {
        // Здесь нужно получить информацию о номере и отеле
        // Пока используем данные из availability
        const availability = hotelsStore.availability
        if (availability && availability.available_rooms) {
          const foundRoom = availability.available_rooms.find(
            r => r.room_id === route.params.roomId
          )
          if (foundRoom) {
            room.value = foundRoom
            hotel.value = availability.hotel
          } else {
            throw new Error('Номер не найден')
          }
        } else {
          throw new Error('Информация о доступности не загружена')
        }
      } catch (err) {
        error.value = err.message || 'Ошибка загрузки информации о номере'
      } finally {
        loading.value = false
      }
    }

    const createBooking = async () => {
      creatingBooking.value = true
      error.value = ''

      try {
        const bookingPayload = {
          ...bookingData.value,
          room_id: route.params.roomId
        }

        const response = await bookingsApi.createBooking(bookingPayload)
        
        // Перенаправляем на страницу успешного бронирования
        router.push({
          path: `/booking/${response.data.id}`,
          query: { success: 'true' }
        })
      } catch (err) {
        console.error('Booking creation error:', err)
        error.value = err.response?.data?.detail?.[0]?.msg || 
                     err.response?.data?.detail || 
                     'Ошибка создания бронирования. Попробуйте снова.'
      } finally {
        creatingBooking.value = false
      }
    }

    const calculateNights = () => {
      const checkIn = new Date(bookingData.value.check_in_date)
      const checkOut = new Date(bookingData.value.check_out_date)
      const diffTime = Math.abs(checkOut - checkIn)
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const formatPrice = (price) => {
      return new Intl.NumberFormat('ru-RU').format(price)
    }

    onMounted(() => {
      if (!route.params.roomId || !route.query.check_in || !route.query.check_out) {
        error.value = 'Недостаточно данных для бронирования'
        loading.value = false
        return
      }
      loadRoomDetails()
    })

    return {
      room,
      hotel,
      loading,
      error,
      creatingBooking,
      bookingData,
      totalPrice,
      createBooking,
      calculateNights,
      formatDate,
      formatPrice
    }
  }
}
</script>

<style scoped>
.create-booking {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.booking-header h1 {
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

.booking-details {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.detail-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.room-info h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.25rem;
}

.room-info p {
  margin: 0.5rem 0;
  color: #5d6d7e;
}

.date-info p {
  margin: 0.5rem 0;
  color: #5d6d7e;
  font-size: 1.1rem;
}

.guest-form {
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

.form-input {
  padding: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
  background: #f8f9fa;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  background: white;
}

.textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.booking-summary {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  color: #5d6d7e;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 2px solid #dee2e6;
  font-size: 1.2rem;
  color: #2c3e50;
}

.submit-booking-btn {
  background: linear-gradient(135deg, #27ae60 0%, #219a52 100%);
  color: white;
  border: none;
  padding: 1.25rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.submit-booking-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(39, 174, 96, 0.3);
}

.submit-booking-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.loading-state, .error-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  text-align: center;
}

.error-message {
  background: #e74c3c;
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  max-width: 500px;
}

@media (max-width: 768px) {
  .booking-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .create-booking {
    padding: 1rem;
  }
  
  .detail-card {
    padding: 1rem;
  }
}
</style>