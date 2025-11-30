<template>
  <div class="booking-details-page">
    <div class="container">
      <div class="booking-header">
        <h1>Детали бронирования</h1>
        <router-link to="/my-bookings" class="back-link">← Мои бронирования</router-link>
      </div>

      <div v-if="loading" class="loading-state">
        <LoadingSpinner message="Загружаем информацию о бронировании..." />
      </div>

      <div v-else-if="error" class="error-state">
        <div class="error-message">
          {{ error }}
        </div>
      </div>

      <div v-else-if="booking" class="booking-content">
        <div class="status-banner" :class="`status-${booking.status}`">
          <h3>Статус: {{ getStatusText(booking.status) }}</h3>
          <p v-if="booking.status === 'confirmed'">Ваше бронирование подтверждено!</p>
          <p v-else-if="booking.status === 'pending'">Ожидание подтверждения</p>
          <p v-else-if="booking.status === 'cancelled'">Бронирование отменено</p>
          <p v-else-if="booking.status === 'completed'">Бронирование завершено</p>
        </div>

        <div class="booking-sections">
          <!-- Информация о номере -->
          <div class="section">
            <h2>Информация о номере</h2>
            <div class="info-card">
              <div class="room-info">
                <h3>Номер {{ booking.room.room_number }}</h3>
                <p class="room-type">{{ booking.room.room_type.name }}</p>
                <p><strong>Отель:</strong> {{ booking.room.hotel?.name || 'Не указан' }}</p>
                <p><strong>Адрес:</strong> {{ booking.room.hotel?.address }}, {{ booking.room.hotel?.city }}</p>
              </div>
            </div>
          </div>

          <!-- Даты и гости -->
          <div class="section">
            <h2>Даты проживания</h2>
            <div class="info-card">
              <div class="date-info">
                <p><strong>Заезд:</strong> {{ formatDate(booking.check_in_date) }}</p>
                <p><strong>Выезд:</strong> {{ formatDate(booking.check_out_date) }}</p>
                <p><strong>Ночей:</strong> {{ calculateNights(booking.check_in_date, booking.check_out_date) }}</p>
                <p><strong>Гостей:</strong> {{ booking.number_of_guests }}</p>
              </div>
            </div>
          </div>

          <!-- Стоимость -->
          <div class="section">
            <h2>Стоимость</h2>
            <div class="info-card">
              <div class="price-info">
                <p><strong>Общая стоимость:</strong> {{ formatPrice(booking.total_price) }} ₽</p>
                <p v-if="booking.special_requests"><strong>Особые пожелания:</strong> {{ booking.special_requests }}</p>
              </div>
            </div>
          </div>

          <!-- Платежи -->
          <div class="section" v-if="booking.payments && booking.payments.length > 0">
            <h2>Платежи</h2>
            <div class="payments-list">
              <div 
                v-for="payment in booking.payments" 
                :key="payment.id"
                class="payment-card"
              >
                <div class="payment-info">
                  <p><strong>Сумма:</strong> {{ formatPrice(payment.amount) }} ₽</p>
                  <p><strong>Статус:</strong> {{ getPaymentStatusText(payment.payment_status) }}</p>
                  <p><strong>Метод:</strong> {{ payment.payment_method }}</p>
                  <p v-if="payment.payment_date">
                    <strong>Дата оплаты:</strong> {{ formatDateTime(payment.payment_date) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Действия -->
        <div class="booking-actions" v-if="booking.status === 'pending' || booking.status === 'confirmed'">
          <button 
            @click="cancelBooking"
            :disabled="cancelling"
            class="cancel-btn"
          >
            {{ cancelling ? 'Отмена...' : 'Отменить бронирование' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { bookingsApi } from '../../api/bookings'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'BookingDetails',
  components: {
    LoadingSpinner
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const booking = ref(null)
    const loading = ref(true)
    const error = ref('')
    const cancelling = ref(false)

    const loadBookingDetails = async () => {
      try {
        const response = await bookingsApi.getBooking(route.params.id)
        booking.value = response.data
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка загрузки информации о бронировании'
      } finally {
        loading.value = false
      }
    }

    const cancelBooking = async () => {
      if (!confirm('Вы уверены, что хотите отменить это бронирование?')) {
        return
      }

      cancelling.value = true
      try {
        await bookingsApi.cancelBooking(route.params.id)
        // Обновляем статус
        booking.value.status = 'cancelled'
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка отмены бронирования'
      } finally {
        cancelling.value = false
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

    const getPaymentStatusText = (status) => {
      const statusMap = {
        'pending': 'Ожидание',
        'completed': 'Оплачено',
        'failed': 'Ошибка',
        'refunded': 'Возврат'
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
      loadBookingDetails()
    })

    return {
      booking,
      loading,
      error,
      cancelling,
      cancelBooking,
      getStatusText,
      getPaymentStatusText,
      formatDate,
      formatDateTime,
      formatPrice,
      calculateNights
    }
  }
}
</script>

<style scoped>
.booking-details-page {
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

.status-banner {
  padding: 1.5rem;
  border-radius: 10px;
  margin-bottom: 2rem;
  text-align: center;
}

.status-banner.status-pending {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  color: #856404;
}

.status-banner.status-confirmed {
  background: #d1ecf1;
  border: 1px solid #bee5eb;
  color: #0c5460;
}

.status-banner.status-cancelled {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.status-banner.status-completed {
  background: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.booking-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.info-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.room-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.room-type {
  color: #3498db;
  font-weight: 500;
  margin-bottom: 1rem;
}

.room-info p, .date-info p, .price-info p {
  margin: 0.5rem 0;
  color: #5d6d7e;
}

.payments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.payment-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.booking-actions {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
  text-align: center;
}

.cancel-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
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

.loading-state, .error-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.error-message {
  background: #e74c3c;
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-align: center;
}

@media (max-width: 768px) {
  .booking-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .booking-details-page {
    padding: 1rem;
  }
}
</style>