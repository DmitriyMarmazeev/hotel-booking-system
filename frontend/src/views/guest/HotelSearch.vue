<template>
  <div class="hotel-search">
    <div class="search-header">
      <h1>Поиск отелей</h1>
      
      <div class="search-filters">
        <div class="filter-card">
          <h3>Параметры поиска</h3>
          <form @submit.prevent="performSearch" class="filters-form">
            <div class="filter-row">
              <div class="filter-group">
                <label>Город</label>
                <input 
                  v-model="filters.city"
                  type="text" 
                  placeholder="Например: Москва"
                >
              </div>
              
              <div class="filter-group">
                <label>Страна</label>
                <input 
                  v-model="filters.country"
                  type="text" 
                  placeholder="Например: Россия"
                >
              </div>
            </div>
            
            <div class="filter-row">
              <div class="filter-group">
                <label>Дата заезда</label>
                <input 
                  v-model="filters.check_in"
                  type="date" 
                  :min="today"
                >
              </div>
              
              <div class="filter-group">
                <label>Дата выезда</label>
                <input 
                  v-model="filters.check_out"
                  type="date" 
                  :min="minCheckoutDate"
                >
              </div>
              
              <div class="filter-group">
                <label>Количество гостей</label>
                <input 
                  v-model="filters.guests"
                  type="number" 
                  min="1"
                  placeholder="1"
                >
              </div>
            </div>
            
            <div class="filter-row">
              <div class="filter-group">
                <label>Минимальная цена</label>
                <input 
                  v-model="filters.min_price"
                  type="number" 
                  min="0"
                  placeholder="0"
                >
              </div>
              
              <div class="filter-group">
                <label>Максимальная цена</label>
                <input 
                  v-model="filters.max_price"
                  type="number" 
                  min="0"
                  placeholder="100000"
                >
              </div>
            </div>
            
            <div class="filter-actions">
              <button type="submit" class="search-btn" :disabled="loading">
                {{ loading ? 'Поиск...' : 'Найти отели' }}
              </button>
              <button type="button" @click="clearFilters" class="clear-btn">
                Очистить
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="search-results">
      <div v-if="loading" class="loading-state">
        <LoadingSpinner message="Ищем отели..." />
      </div>
      
      <div v-else-if="error" class="error-state">
        <div class="error-message">
          {{ error }}
        </div>
      </div>
      
      <div v-else-if="hotels.length === 0 && hasSearched" class="no-results">
        <h3>Отели не найдены</h3>
        <p>Попробуйте изменить параметры поиска</p>
      </div>
      
      <div v-else-if="hotels.length > 0" class="results-grid">
        <h2>Найдено отелей: {{ hotels.length }}</h2>
        <HotelCard 
          v-for="hotel in hotels" 
          :key="hotel.id" 
          :hotel="hotel" 
        />
      </div>
      
      <div v-else class="initial-state">
        <div class="welcome-message">
          <h2>Начните поиск отелей</h2>
          <p>Заполните параметры поиска и найдите идеальный отель для вашего отдыха</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHotelsStore } from '../../stores/hotels'
import HotelCard from '../../components/hotels/HotelCard.vue'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'HotelSearch',
  components: {
    HotelCard,
    LoadingSpinner
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const hotelsStore = useHotelsStore()
    
    const filters = ref({
      city: '',
      country: '',
      check_in: '',
      check_out: '',
      guests: 1,
      min_price: null,
      max_price: null,
      amenities: ''
    })
    
    const hasSearched = ref(false)
    const loading = computed(() => hotelsStore.loading)
    const error = computed(() => hotelsStore.error)
    const hotels = computed(() => hotelsStore.hotels)

    const today = computed(() => {
      return new Date().toISOString().split('T')[0]
    })

    const minCheckoutDate = computed(() => {
      return filters.value.check_in || today.value
    })

    // Загружаем параметры из URL при загрузке
    const loadFiltersFromQuery = () => {
      const query = route.query
      Object.keys(filters.value).forEach(key => {
        if (query[key] !== undefined) {
          if (key === 'guests' || key === 'min_price' || key === 'max_price') {
            filters.value[key] = parseInt(query[key]) || null
          } else {
            filters.value[key] = query[key]
          }
        }
      })
    }

    const performSearch = async () => {
      hasSearched.value = true
      
      // Очищаем пустые поля
      const searchParams = {}
      Object.keys(filters.value).forEach(key => {
        const value = filters.value[key]
        if (value !== '' && value !== null && value !== undefined) {
          searchParams[key] = value
        }
      })

      // Обновляем URL
      router.replace({ 
        path: '/search', 
        query: searchParams 
      })

      try {
        await hotelsStore.searchHotels(searchParams)
      } catch (err) {
        console.error('Search error:', err)
      }
    }

    const clearFilters = () => {
      Object.keys(filters.value).forEach(key => {
        if (key === 'guests') {
          filters.value[key] = 1
        } else {
          filters.value[key] = ''
        }
      })
      hasSearched.value = false
      hotelsStore.clearHotels()
      router.replace({ path: '/search', query: {} })
    }

    onMounted(() => {
      loadFiltersFromQuery()
      
      // Если в URL есть параметры, выполняем поиск
      if (Object.keys(route.query).length > 0) {
        performSearch()
      }
    })

    return {
      filters,
      hasSearched,
      loading,
      error,
      hotels,
      today,
      minCheckoutDate,
      performSearch,
      clearFilters
    }
  }
}
</script>

<style scoped>
.hotel-search {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.search-header {
  margin-bottom: 2rem;
}

.search-header h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.search-filters {
  max-width: 800px;
  margin: 0 auto 3rem auto;
}

.filter-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.filter-card h3 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
}

.filters-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.filter-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
}

.filter-group input {
  padding: 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.filter-group input:focus {
  outline: none;
  border-color: #3498db;
}

.filter-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.search-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-btn:hover:not(:disabled) {
  background: #2980b9;
}

.search-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.clear-btn {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.clear-btn:hover {
  background: #7f8c8d;
}

.search-results {
  min-height: 400px;
}

.loading-state, .error-state, .no-results, .initial-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.error-message {
  background: #e74c3c;
  color: white;
  padding: 1rem 2rem;
  border-radius: 5px;
  text-align: center;
}

.no-results {
  text-align: center;
  color: #7f8c8d;
}

.no-results h3 {
  margin-bottom: 1rem;
}

.welcome-message {
  text-align: center;
  color: #7f8c8d;
}

.welcome-message h2 {
  margin-bottom: 1rem;
}

.results-grid h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}
</style>