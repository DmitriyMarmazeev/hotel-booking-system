<template>
  <div class="my-bookings">
    <div class="page-header">
      <h1>Мои бронирования</h1>
    </div>

    <div v-if="loading" class="loading-state">
      <LoadingSpinner message="Загружаем ваши бронирования..." />
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-message">
        {{ error }}
      </div>
    </div>

    <div v-else-if="bookings.length === 0" class="no-bookings">
      <div class="empty-state">
        <h3>У вас пока нет бронирований</h3>
        <p>Найдите идеальный отель для вашего отдыха</p>
        <router-link to="/search" class="search-link">
          Начать поиск отелей
        </router-link>
      </div>
    </div>

    <div v-else class="bookings-list">
      <div 
        v-for="booking in bookings" 
        :key="booking.id"
        class="booking-card"
        :class="`status-${booking.status}`"
      >
        <div class="booking-header">
          <h3>Бронирование #{{ booking.id.slice(-8) }}</h3>
          <span class="booking-status" :class="`status-${booking.status}`">
            {{ getStatusText(booking.status) }}
          </span>
        </div>

        <div class="booking-details">
          <div class="detail-section">
            <h4>Информация о номере</h4>
            <p><strong>Отель:</strong> {{ booking.room?.hotel?.name || 'Не указан' }}</p>
            <p><strong>Номер:</strong> {{ booking.room?.room_number || 'Не указан' }}</p>
            <p><strong>Тип номера:</strong> {{ booking.room?.room_type?.name || 'Не указан' }}</p>
          </div>

          <div class="detail-section">
            <h4>Даты проживания</h4>
            <p><strong>Заезд:</strong> {{ formatDate(booking.check_in_date) }}</p>
            <p><strong>Выезд:</strong> {{ formatDate(booking.check_out_date) }}</p>
            <p><strong>Ночей:</strong> {{ calculateNights(booking.check_in_date, booking.check_out_date) }}</p>
          </div>

          <div class="detail-section">
            <h4>Стоимость</h4>
            <p><strong>Общая стоимость:</strong> {{ formatPrice(booking.total_price) }} ₽</p>
            <p><strong>Гости:</strong> {{ booking.number_of_guests }} человек</p>
          </div>
        </div>

        <div class="booking-actions">
          <button 
            v-if="booking.status === 'pending' || booking.status === 'confirmed'"
            @click="cancelBooking(booking.id)"
            :disabled="cancellingBooking === booking.id"
            class="cancel-btn"
          >
            {{ cancellingBooking === booking.id ? 'Отмена...' : 'Отменить бронирование' }}
          </button>
          
          <router-link 
            :to="`/booking/${booking.id}`"
            class="details-btn"
          >
            Подробнее
          </router-link>
        </div>

        <div class="booking-footer">
          <p class="booking-date">
            Создано: {{ formatDateTime(booking.created_at) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { bookingsApi } from '../../api/bookings'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'MyBookings',
  components: {
    LoadingSpinner
  },
  setup() {
    const bookings = ref([])
    const loading = ref(false)
    const error = ref('')
    const cancellingBooking = ref(null)
    const debugInfo = ref(true) // Временно включим отладку

    const loadBookings = async () => {
      console.log('Начало загрузки бронирований...')
      loading.value = true
      error.value = ''
      
      try {
        const response = await bookingsApi.getMyBookings()
        console.log('Ответ от API:', response)
        console.log('Данные бронирований:', response.data)
        bookings.value = response.data
        console.log('bookings после присвоения:', bookings.value)
      } catch (err) {
        console.error('Ошибка загрузки бронирований:', err)
        error.value = err.response?.data?.detail || 
                     err.response?.data?.message || 
                     err.message || 
                     'Ошибка загрузки бронирований'
      } finally {
        loading.value = false
        console.log('Загрузка завершена, loading:', loading.value)
      }
    }

    const cancelBooking = async (bookingId) => {
      if (!confirm('Вы уверены, что хотите отменить это бронирование?')) {
        return
      }

      cancellingBooking.value = bookingId
      
      try {
        await bookingsApi.cancelBooking(bookingId)
        // Обновляем статус бронирования локально
        const booking = bookings.value.find(b => b.id === bookingId)
        if (booking) {
          booking.status = 'cancelled'
        }
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка отмены бронирования'
      } finally {
        cancellingBooking.value = null
      }
    }

    const getStatusText = (status) => {
      const statusMap = {
        'pending': 'Ожидание',
        'confirmed': 'Подтверждено',
        'cancelled': 'Отменено',
        'completed': 'Завершено'
      }
      return statusMap[status] || status
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU')
    }

    const formatDateTime = (dateString) => {
      return new Date(dateString).toLocaleString('ru-RU')
    }

    const formatPrice = (price) => {
      return new Intl.NumberFormat('ru-RU').format(price)
    }

    const calculateNights = (checkIn, checkOut) => {
      const start = new Date(checkIn)
      const end = new Date(checkOut)
      const diffTime = Math.abs(end - start)
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    }

    onMounted(() => {
      console.log('Компонент MyBookings mounted')
      loadBookings()
    })

    return {
      bookings,
      loading,
      error,
      cancellingBooking,
      debugInfo,
      cancelBooking,
      getStatusText,
      formatDate,
      formatDateTime,
      formatPrice,
      calculateNights
    }
  }
}
</script>

<style scoped>
.debug-info {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 5px;
  font-size: 0.9rem;
}

.debug-info pre {
  background: white;
  padding: 0.5rem;
  border-radius: 3px;
  overflow-x: auto;
  font-size: 0.8rem;
}

/* Остальные стили остаются без изменений */
.my-bookings {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.page-header {
  margin-bottom: 2rem;
  text-align: center;
}

.page-header h1 {
  color: #2c3e50;
}

.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.booking-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 1.5rem;
  border-left: 4px solid #3498db;
}

.booking-card.status-pending {
  border-left-color: #f39c12;
}

.booking-card.status-confirmed {
  border-left-color: #27ae60;
}

.booking-card.status-cancelled {
  border-left-color: #e74c3c;
}

.booking-card.status-completed {
  border-left-color: #7f8c8d;
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ecf0f1;
}

.booking-header h3 {
  margin: 0;
  color: #2c3e50;
}

.booking-status {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.booking-status.status-pending {
  background: #f39c12;
  color: white;
}

.booking-status.status-confirmed {
  background: #27ae60;
  color: white;
}

.booking-status.status-cancelled {
  background: #e74c3c;
  color: white;
}

.booking-status.status-completed {
  background: #7f8c8d;
  color: white;
}

.booking-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.detail-section h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1rem;
}

.detail-section p {
  margin: 0.25rem 0;
  color: #5d6d7e;
}

.booking-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.cancel-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-btn:hover:not(:disabled) {
  background: #c0392b;
}

.cancel-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.details-btn {
  background: #3498db;
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.details-btn:hover {
  background: #2980b9;
}

.booking-footer {
  border-top: 1px solid #ecf0f1;
  padding-top: 1rem;
}

.booking-date {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.loading-state, .error-state, .no-bookings {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.error-message {
  background: #e74c3c;
  color: white;
  padding: 1rem 2rem;
  border-radius: 5px;
  text-align: center;
}

.empty-state {
  text-align: center;
  color: #7f8c8d;
}

.empty-state h3 {
  margin-bottom: 1rem;
}

.empty-state p {
  margin-bottom: 2rem;
}

.search-link {
  background: #3498db;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.search-link:hover {
  background: #2980b9;
}
</style>