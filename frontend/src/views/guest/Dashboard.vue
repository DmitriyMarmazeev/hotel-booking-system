<template>
  <div class="dashboard">
    <div class="hero-section">
      <h1>Найдите идеальный отель для отдыха</h1>
      <p>Откройте для себя лучшие отели по всему миру</p>
      
      <div class="search-widget">
        <HotelSearchWidget @search="handleSearch" />
      </div>
    </div>

    <div class="popular-destinations" v-if="popularDestinations.length > 0">
      <h2>Популярные направления</h2>
      <div class="destinations-grid">
        <div 
          v-for="destination in popularDestinations" 
          :key="`${destination.city}-${destination.country}`"
          class="destination-card"
          @click="searchByDestination(destination)"
        >
          <h3>{{ destination.city }}</h3>
          <p>{{ destination.country }}</p>
          <span class="popularity">🔥 {{ destination.popularity }} бронирований</span>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>Быстрые действия</h2>
      <div class="actions-grid">
        <router-link to="/search" class="action-card">
          <div class="action-icon">🔍</div>
          <h3>Поиск отелей</h3>
          <p>Найдите отель по вашим критериям</p>
        </router-link>
        
        <router-link to="/my-bookings" class="action-card">
          <div class="action-icon">📋</div>
          <h3>Мои бронирования</h3>
          <p>Управляйте вашими бронированиями</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useHotelsStore } from '../../stores/hotels'
import HotelSearchWidget from '../../components/hotels/HotelSearchWidget.vue'

export default {
  name: 'GuestDashboard',
  components: {
    HotelSearchWidget
  },
  setup() {
    const router = useRouter()
    const hotelsStore = useHotelsStore()
    const popularDestinations = ref([])

    const loadPopularDestinations = async () => {
      try {
        popularDestinations.value = await hotelsStore.getPopularDestinations(6)
      } catch (error) {
        console.error('Error loading popular destinations:', error)
      }
    }

    const handleSearch = (searchParams) => {
      router.push({
        path: '/search',
        query: searchParams
      })
    }

    const searchByDestination = (destination) => {
      router.push({
        path: '/search',
        query: {
          city: destination.city,
          country: destination.country
        }
      })
    }

    onMounted(() => {
      loadPopularDestinations()
    })

    return {
      popularDestinations,
      handleSearch,
      searchByDestination
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.hero-section {
  text-align: center;
  margin-bottom: 4rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  border-radius: 15px;
  margin-top: -1rem;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero-section p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.search-widget {
  max-width: 800px;
  margin: 0 auto;
}

.popular-destinations {
  margin-bottom: 4rem;
}

.popular-destinations h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.destinations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.destination-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.destination-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.destination-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.destination-card p {
  margin: 0 0 1rem 0;
  color: #7f8c8d;
}

.popularity {
  background: #e74c3c;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
}

.quick-actions h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.action-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s, box-shadow 0.3s;
}

.action-card:hover {
  transform: translateY(-5px);
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
</style>