<template>
  <div class="hotel-bookings">
    <div class="page-header">
      <div class="header-content">
        <h1>Бронирования отеля</h1>
        <router-link to="/manager/hotels" class="back-link">
          ← Назад к отелям
        </router-link>
      </div>
      <p v-if="hotel">{{ hotel.name }}, {{ hotel.city }}</p>
    </div>

    <div v-if="loading" class="loading-state">
      <LoadingSpinner message="Загружаем бронирования..." />
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-message">
        {{ error }}
      </div>
    </div>

    <div v-else class="bookings-content">
      <!-- Фильтры и статистика -->
      <div class="bookings-header">
        <div class="filters">
          <select v-model="statusFilter" @change="loadBookings" class="filter-select">
            <option value="">Все статусы</option>
            <option value="pending">Ожидание</option>
            <option value="confirmed">Подтверждено</option>
            <option value="cancelled">Отменено</option>
            <option value="completed">Завершено</option>
          </select>
        </div>
        
        <div class="stats">
          <div class="stat">
            <span class="stat-number">{{ bookings.length }}</span>
            <span class="stat-label">всего</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ pendingCount }}</span>
            <span class="stat-label">ожидают</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ confirmedCount }}</span>
            <span class="stat-label">подтверждено</span>
          </div>
        </div>
      </div>

      <!-- Список бронирований -->
      <div v-if="bookings.length === 0" class="no-bookings">
        <div class="empty-state">
          <div class="empty-icon">📋</div>
          <h3>Бронирований нет</h3>
          <p>На выбранные критерии бронирования не найдены</p>
        </div>
      </div>

      <div v-else class="bookings-list">
        <div 
          v-for="booking in bookings" 
          :key="booking.id"
          class="booking-card"
          :class="`status-${booking.status}`"
        >
          <div class="booking-main">
            <div class="booking-info">
              <h4>Бронирование #{{ booking.id.slice(-8) }}</h4>
              <div class="guest-info">
                <strong>Гость:</strong> {{ booking.guest?.first_name }} {{ booking.guest?.last_name }}
                <br>
                <strong>Email:</strong> {{ booking.guest?.email }}
              </div>
              <div class="room-info">
                <strong>Номер:</strong> {{ booking.room?.room_number }} ({{ booking.room?.room_type?.name }})
              </div>
              <div class="dates-info">
                <strong>Даты:</strong> {{ formatDate(booking.check_in_date) }} - {{ formatDate(booking.check_out_date) }}
                <br>
                <strong>Ночей:</strong> {{ calculateNights(booking.check_in_date, booking.check_out_date) }}
                <strong>Гостей:</strong> {{ booking.number_of_guests }}
              </div>
              <div class="price-info">
                <strong>Стоимость:</strong> {{ formatPrice(booking.total_price) }} ₽
              </div>
              <div v-if="booking.special_requests" class="special-requests">
                <strong>Особые пожелания:</strong> {{ booking.special_requests }}
              </div>
            </div>

            <div class="booking-actions">
              <div class="status-display">
                <span class="status-badge" :class="`status-${booking.status}`">
                  {{ getStatusText(booking.status) }}
                </span>
              </div>
              
              <div class="action-buttons">
                <select 
                  v-if="booking.status === 'pending' || booking.status === 'confirmed'"
                  v-model="statusUpdates[booking.id]"
                  @change="updateBookingStatus(booking.id)"
                  class="status-select"
                  :disabled="updatingStatus === booking.id"
                >
                  <option value="">Изменить статус</option>
                  <option value="confirmed">Подтвердить</option>
                  <option value="cancelled">Отменить</option>
                  <option value="completed">Завершить</option>
                </select>
                
                <router-link 
                  :to="`/booking/${booking.id}`"
                  class="view-btn"
                >
                  Подробнее
                </router-link>
              </div>
            </div>
          </div>

          <div class="booking-meta">
            <span class="booking-date">
              Создано: {{ formatDateTime(booking.created_at) }}
            </span>
            <span v-if="booking.cancelled_at" class="cancelled-date">
              Отменено: {{ formatDateTime(booking.cancelled_at) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useManagerStore } from '../../stores/manager'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'HotelBookings',
  components: {
    LoadingSpinner
  },
  setup() {
    const route = useRoute()
    const managerStore = useManagerStore()
    
    const loading = ref(false)
    const error = ref('')
    const statusFilter = ref('')
    const updatingStatus = ref(null)
    const statusUpdates = ref({})

    const hotel = computed(() => 
      managerStore.myHotels.find(h => h.id === route.params.id) || {}
    )
    
    const bookings = computed(() => managerStore.hotelBookings)

    const pendingCount = computed(() => 
      bookings.value.filter(b => b.status === 'pending').length
    )
    
    const confirmedCount = computed(() => 
      bookings.value.filter(b => b.status === 'confirmed').length
    )

    const loadBookings = async () => {
      loading.value = true
      error.value = ''
      
      try {
        await managerStore.getHotelBookings(route.params.id, statusFilter.value || null)
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка загрузки бронирований'
      } finally {
        loading.value = false
      }
    }

    const updateBookingStatus = async (bookingId) => {
      const newStatus = statusUpdates.value[bookingId]
      if (!newStatus) return

      updatingStatus.value = bookingId
      
      try {
        await managerStore.updateBookingStatus(bookingId, { status: newStatus })
        statusUpdates.value[bookingId] = ''
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка обновления статуса'
      } finally {
        updatingStatus.value = null
      }
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

    const getStatusText = (status) => {
      const statusMap = {
        'pending': 'Ожидание',
        'confirmed': 'Подтверждено',
        'cancelled': 'Отменено',
        'completed': 'Завершено'
      }
      return statusMap[status] || status
    }

    onMounted(async () => {
      // Сначала загружаем отели, чтобы получить информацию об отеле
      try {
        await managerStore.getMyHotels()
        await loadBookings()
      } catch (err) {
        error.value = 'Ошибка загрузки данных'
      }
    })

    return {
      hotel,
      bookings,
      loading,
      error,
      statusFilter,
      updatingStatus,
      statusUpdates,
      pendingCount,
      confirmedCount,
      loadBookings,
      updateBookingStatus,
      formatDate,
      formatDateTime,
      formatPrice,
      calculateNights,
      getStatusText
    }
  }
}
</script>

<style scoped>
.hotel-bookings {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.page-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-content h1 {
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

.page-header p {
  color: #7f8c8d;
  margin: 0;
  font-size: 1.1rem;
}

.bookings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.filters {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.filter-select {
  padding: 0.5rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  background: white;
  font-size: 0.9rem;
}

.stats {
  display: flex;
  gap: 1.5rem;
}

.stat {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #3498db;
}

.stat-label {
  font-size: 0.8rem;
  color: #7f8c8d;
  text-transform: uppercase;
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

.booking-main {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 2rem;
  margin-bottom: 1rem;
}

.booking-info h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.guest-info, .room-info, .dates-info, .price-info, .special-requests {
  margin-bottom: 0.75rem;
  color: #5d6d7e;
}

.special-requests {
  background: #f8f9fa;
  padding: 0.75rem;
  border-radius: 6px;
  border-left: 3px solid #3498db;
}

.booking-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 200px;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  text-align: center;
}

.status-badge.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.status-confirmed {
  background: #d1ecf1;
  color: #0c5460;
}

.status-badge.status-cancelled {
  background: #f8d7da;
  color: #721c24;
}

.status-badge.status-completed {
  background: #d4edda;
  color: #155724;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.status-select {
  padding: 0.5rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 0.9rem;
  background: white;
}

.status-select:disabled {
  background: #ecf0f1;
  cursor: not-allowed;
}

.view-btn {
  background: #3498db;
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-align: center;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.view-btn:hover {
  background: #2980b9;
}

.booking-meta {
  border-top: 1px solid #ecf0f1;
  padding-top: 1rem;
  display: flex;
  justify-content: space-between;
  color: #7f8c8d;
  font-size: 0.8rem;
}

.cancelled-date {
  color: #e74c3c;
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
  border-radius: 8px;
  text-align: center;
}

.empty-state {
  text-align: center;
  color: #7f8c8d;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .bookings-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .stats {
    align-self: stretch;
    justify-content: space-around;
  }
  
  .booking-main {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .booking-actions {
    min-width: auto;
  }
  
  .booking-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>