<template>
  <div class="my-hotels">
    <div class="page-header">
      <div class="header-content">
        <h1>Мои отели</h1>
        <router-link to="/manager/hotels/new" class="create-btn">
          ➕ Добавить отель
        </router-link>
      </div>
      <p>Управляйте вашими отелями и их номерами</p>
    </div>

    <div v-if="loading" class="loading-state">
      <LoadingSpinner message="Загружаем ваши отели..." />
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-message">
        {{ error }}
      </div>
      <button @click="loadHotels" class="retry-btn">Попробовать снова</button>
    </div>

    <div v-else-if="hotels.length === 0" class="no-hotels">
      <div class="empty-state">
        <div class="empty-icon">🏨</div>
        <h3>У вас пока нет отелей</h3>
        <p>Добавьте ваш первый отель чтобы начать принимать бронирования</p>
        <router-link to="/manager/hotels/new" class="create-link">
          Создать первый отель
        </router-link>
      </div>
    </div>

    <div v-else class="hotels-list">
      <div class="hotels-stats">
        <div class="stat">
          <span class="stat-number">{{ hotels.length }}</span>
          <span class="stat-label">всего отелей</span>
        </div>
        <div class="stat">
          <span class="stat-number">{{ activeHotelsCount }}</span>
          <span class="stat-label">активных</span>
        </div>
        <div class="stat">
          <span class="stat-number">{{ totalRooms }}</span>
          <span class="stat-label">номеров</span>
        </div>
      </div>

      <div class="hotels-grid">
        <HotelCardManager 
          v-for="hotel in hotels" 
          :key="hotel.id" 
          :hotel="hotel" 
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useManagerStore } from '../../stores/manager'
import HotelCardManager from '../../components/manager/HotelCardManager.vue'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'MyHotels',
  components: {
    HotelCardManager,
    LoadingSpinner
  },
  setup() {
    const managerStore = useManagerStore()
    const loading = ref(false)

    const hotels = computed(() => managerStore.myHotels)
    const error = computed(() => managerStore.error)

    const activeHotelsCount = computed(() => 
      hotels.value.filter(hotel => hotel.is_active).length
    )

    const totalRooms = computed(() => 
      hotels.value.reduce((total, hotel) => total + (hotel.rooms?.length || 0), 0)
    )

    const loadHotels = async () => {
      loading.value = true
      try {
        await managerStore.getMyHotels()
      } catch (err) {
        console.error('Error loading hotels:', err)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadHotels()
    })

    return {
      hotels,
      loading,
      error,
      activeHotelsCount,
      totalRooms,
      loadHotels
    }
  }
}
</script>

<style scoped>
.my-hotels {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.page-header {
  margin-bottom: 3rem;
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

.create-btn {
  background: linear-gradient(135deg, #27ae60 0%, #219a52 100%);
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(39, 174, 96, 0.3);
}

.page-header p {
  color: #7f8c8d;
  margin: 0;
  font-size: 1.1rem;
}

.hotels-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
  transition: transform 0.2s;
}

.stat:hover {
  transform: translateY(-2px);
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  color: #3498db;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.hotels-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.loading-state, .error-state, .no-hotels {
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

.retry-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.retry-btn:hover {
  background: #2980b9;
}

.empty-state {
  max-width: 400px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.empty-state p {
  color: #7f8c8d;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.create-link {
  background: #3498db;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.create-link:hover {
  background: #2980b9;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .create-btn {
    align-self: stretch;
    text-align: center;
  }
  
  .hotels-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>