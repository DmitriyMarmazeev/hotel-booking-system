<template>
  <div class="admin-dashboard">
    <div class="dashboard-header">
      <h1>Панель администратора</h1>
      <p>Управление системой бронирования отелей</p>
    </div>

    <!-- Статистика системы -->
    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <h3>{{ stats.total_users || 0 }}</h3>
          <p>Пользователей</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🏨</div>
        <div class="stat-info">
          <h3>{{ stats.total_hotels || 0 }}</h3>
          <p>Отелей</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
          <h3>{{ stats.total_bookings || 0 }}</h3>
          <p>Бронирований</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-info">
          <h3>{{ formatPrice(stats.revenue || 0) }}</h3>
          <p>Общий доход</p>
        </div>
      </div>
    </div>

    <!-- Быстрые действия -->
    <div class="dashboard-actions">
      <h2>Быстрые действия</h2>
      <div class="action-grid">
        <router-link to="/admin/users" class="action-card">
          <div class="action-icon">👥</div>
          <h3>Управление пользователями</h3>
          <p>Просмотр и управление всеми пользователями системы</p>
        </router-link>
        
        <div class="action-card" @click="loadSystemStats">
          <div class="action-icon">📊</div>
          <h3>Обновить статистику</h3>
          <p>Обновить системную статистику и отчеты</p>
        </div>
        
        <div class="action-card" @click="exportData">
          <div class="action-icon">📤</div>
          <h3>Экспорт данных</h3>
          <p>Экспорт данных системы в различных форматах</p>
        </div>
      </div>
    </div>

    <!-- Популярные направления -->
    <div class="popular-destinations" v-if="stats.popular_destinations && stats.popular_destinations.length > 0">
      <h2>Популярные направления</h2>
      <div class="destinations-list">
        <div 
          v-for="destination in stats.popular_destinations" 
          :key="destination.city"
          class="destination-item"
        >
          <div class="destination-name">
            <span class="city">{{ destination.city }}</span>
          </div>
          <div class="destination-stats">
            <span class="bookings-count">{{ destination.bookings }} бронирований</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Последние действия -->
    <div class="recent-activity">
      <h2>Последние действия</h2>
      <div class="activity-list">
        <div class="activity-item">
          <div class="activity-icon">➕</div>
          <div class="activity-details">
            <p><strong>Новый пользователь</strong> зарегистрирован в системе</p>
            <span class="activity-time">2 минуты назад</span>
          </div>
        </div>
        <div class="activity-item">
          <div class="activity-icon">🏨</div>
          <div class="activity-details">
            <p><strong>Новый отель</strong> добавлен менеджером</p>
            <span class="activity-time">15 минут назад</span>
          </div>
        </div>
        <div class="activity-item">
          <div class="activity-icon">📋</div>
          <div class="activity-details">
            <p><strong>Новое бронирование</strong> создано пользователем</p>
            <span class="activity-time">1 час назад</span>
          </div>
        </div>
      </div>
    </div>

    <div class="loading-state" v-if="loading">
      <LoadingSpinner message="Загружаем данные системы..." />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'AdminDashboard',
  components: {
    LoadingSpinner
  },
  setup() {
    const adminStore = useAdminStore()
    const loading = ref(false)
    const stats = ref({})

    const loadSystemStats = async () => {
      loading.value = true
      try {
        stats.value = await adminStore.getSystemStats()
      } catch (error) {
        console.error('Error loading system stats:', error)
      } finally {
        loading.value = false
      }
    }

    const exportData = () => {
      alert('Функция экспорта данных будет реализована позже')
    }

    const formatPrice = (price) => {
      return new Intl.NumberFormat('ru-RU').format(price) + ' ₽'
    }

    onMounted(() => {
      loadSystemStats()
    })

    return {
      stats,
      loading,
      loadSystemStats,
      exportData,
      formatPrice
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
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
  font-size: 2.5rem;
}

.dashboard-header p {
  color: #7f8c8d;
  font-size: 1.2rem;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 3rem;
}

.stat-info h3 {
  margin: 0;
  font-size: 2.5rem;
  color: #2c3e50;
  font-weight: bold;
}

.stat-info p {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dashboard-actions {
  margin-bottom: 3rem;
}

.dashboard-actions h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
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
  line-height: 1.5;
}

.popular-destinations {
  margin-bottom: 3rem;
}

.popular-destinations h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.destinations-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.destination-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.destination-name .city {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.1rem;
}

.bookings-count {
  background: #3498db;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.recent-activity h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.activity-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 8px;
  flex-shrink: 0;
}

.activity-details {
  flex: 1;
}

.activity-details p {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.activity-time {
  color: #7f8c8d;
  font-size: 0.8rem;
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

@media (max-width: 768px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 1.5rem;
  }
  
  .stat-icon {
    font-size: 2rem;
  }
  
  .stat-info h3 {
    font-size: 2rem;
  }
}
</style>