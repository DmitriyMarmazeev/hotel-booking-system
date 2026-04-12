<template>
  <div class="manager-dashboard">
    <div class="dashboard-header">
      <h1>Панель управления отелем</h1>
      <p>Управляйте вашими отелями и бронированиями</p>
    </div>

    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon">🏨</div>
        <div class="stat-info">
          <h3>{{ myHotels.length }}</h3>
          <p>Отелей</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
          <h3>{{ totalBookings }}</h3>
          <p>Всего бронирований</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">⏳</div>
        <div class="stat-info">
          <h3>{{ pendingBookings }}</h3>
          <p>Ожидают подтверждения</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <h3>{{ activeHotels }}</h3>
          <p>Активных отелей</p>
        </div>
      </div>
    </div>

    <div class="dashboard-actions">
      <div class="action-grid">
        <router-link to="/manager/hotels" class="action-card">
          <div class="action-icon">🏨</div>
          <h3>Мои отели</h3>
          <p>Управление вашими отелями</p>
        </router-link>
        
        <router-link to="/manager/hotels/new" class="action-card">
          <div class="action-icon">➕</div>
          <h3>Добавить отель</h3>
          <p>Создать новый отель</p>
        </router-link>
        
        <div class="action-card" @click="loadRecentBookings">
          <div class="action-icon">📋</div>
          <h3>Последние бронирования</h3>
          <p>Просмотр новых заказов</p>
        </div>
      </div>
    </div>

    <div class="recent-bookings" v-if="recentBookings.length > 0">
      <h2>Последние бронирования</h2>
      <div class="bookings-list">
        <div 
          v-for="booking in recentBookings" 
          :key="booking.id"
          class="booking-item"
        >
          <div class="booking-info">
            <h4>Бронирование #{{ booking.id.slice(-8) }}</h4>
            <p><strong>Отель:</strong> {{ booking.room?.hotel?.name }}</p>
            <p><strong>Номер:</strong> {{ booking.room?.room_number }}</p>
            <p><strong>Даты:</strong> {{ formatDate(booking.check_in_date) }} - {{ formatDate(booking.check_out_date) }}</p>
          </div>
          <div class="booking-status">
            <span class="status-badge" :class="`status-${booking.status}`">
              {{ getStatusText(booking.status) }}
            </span>
            <router-link 
              :to="`/manager/hotels/${booking.room?.hotel?.id}/bookings`"
              class="view-btn"
            >
              Подробнее
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <div class="loading-state" v-if="loading">
      <LoadingSpinner message="Загружаем данные..." />
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useManagerStore } from '../../stores/manager'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'ManagerDashboard',
  components: {
    LoadingSpinner
  },
  setup() {
    const managerStore = useManagerStore()
    const recentBookings = ref([])
    const loading = ref(false)

    const myHotels = computed(() => managerStore.myHotels)
    const totalBookings = computed(() => recentBookings.value.length)
    const pendingBookings = computed(() => 
      recentBookings.value.filter(b => b.status === 'pending').length
    )
    const activeHotels = computed(() => 
      myHotels.value.filter(h => h.is_active).length
    )

    const loadDashboardData = async () => {
      loading.value = true
      try {
        await managerStore.getMyHotels()
        // Загружаем бронирования для первого отеля (если есть)
        if (myHotels.value.length > 0) {
          await loadRecentBookings()
        }
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      } finally {
        loading.value = false
      }
    }

    const loadRecentBookings = async () => {
      if (myHotels.value.length === 0) return
      
      try {
        // Загружаем бронирования для первого отеля
        const firstHotel = myHotels.value[0]
        const bookings = await managerStore.getHotelBookings(firstHotel.id)
        recentBookings.value = bookings.slice(0, 5) // Последние 5 бронирований
      } catch (error) {
        console.error('Error loading recent bookings:', error)
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU')
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

    onMounted(() => {
      loadDashboardData()
    })

    return {
      myHotels,
      recentBookings,
      loading,
      totalBookings,
      pendingBookings,
      activeHotels,
      loadRecentBookings,
      formatDate,
      getStatusText
    }
  }
}
</script>

<style scoped>
.manager-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-info h3 {
  margin: 0;
  font-size: 2rem;
  color: #2c3e50;
}

.stat-info p {
  margin: 0;
  color: #7f8c8d;
}

.dashboard-actions {
  margin-bottom: 3rem;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
  cursor: pointer;
  text-align: center;
}

.action-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.action-card h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.action-card p {
  margin: 0;
  color: #7f8c8d;
}

.recent-bookings h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.booking-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.booking-info h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.booking-info p {
  margin: 0.25rem 0;
  color: #5d6d7e;
  font-size: 0.9rem;
}

.booking-status {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
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

.view-btn {
  background: #3498db;
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.view-btn:hover {
  background: #2980b9;
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

@media (max-width: 768px) {
  .stats-overview {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
  
  .booking-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .booking-status {
    align-items: flex-start;
  }
}
</style>