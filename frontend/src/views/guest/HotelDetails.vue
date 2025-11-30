<template>
  <div class="hotel-details">
    <div v-if="loading" class="loading-state">
      <LoadingSpinner message="Загружаем информацию об отеле..." />
    </div>
    
    <div v-else-if="error" class="error-state">
      <div class="error-message">
        {{ error }}
      </div>
      <router-link to="/search" class="back-link">← Вернуться к поиску</router-link>
    </div>
    
    <div v-else-if="hotel" class="hotel-content">
      <!-- Хлебные крошки -->
      <div class="breadcrumbs">
        <router-link to="/">Главная</router-link> /
        <router-link to="/search">Поиск отелей</router-link> /
        <span>{{ hotel.name }}</span>
      </div>

      <!-- Галерея изображений -->
      <div class="hotel-gallery" v-if="hotel.images && hotel.images.length > 0">
        <img 
          :src="hotel.images[0]" 
          :alt="hotel.name" 
          class="main-image"
        >
        <div class="thumbnail-grid" v-if="hotel.images.length > 1">
          <img 
            v-for="(image, index) in hotel.images.slice(1, 5)" 
            :key="index"
            :src="image" 
            :alt="`${hotel.name} - фото ${index + 2}`"
            class="thumbnail"
          >
        </div>
      </div>
      
      <div v-else class="no-images">
        <div class="no-image-placeholder">Нет фотографий</div>
      </div>

      <!-- Основная информация -->
      <div class="hotel-main-info">
        <div class="info-left">
          <h1 class="hotel-title">{{ hotel.name }}</h1>
          <p class="hotel-location">📍 {{ hotel.address }}, {{ hotel.city }}, {{ hotel.country }}</p>
          
          <div class="hotel-rating" v-if="hotel.star_rating">
            <span class="stars">⭐ {{ hotel.star_rating }} звезд(ы)</span>
          </div>
          
          <div class="hotel-description" v-if="hotel.description">
            <h3>Описание</h3>
            <p>{{ hotel.description }}</p>
          </div>

          <div class="hotel-amenities" v-if="hotel.amenities && hotel.amenities.length > 0">
            <h3>Удобства</h3>
            <div class="amenities-grid">
              <span 
                v-for="amenity in hotel.amenities" 
                :key="amenity" 
                class="amenity-tag"
              >
                {{ amenity }}
              </span>
            </div>
          </div>
        </div>

        <div class="info-right">
          <!-- Виджет бронирования -->
          <div class="booking-widget">
            <h3>Проверить доступность</h3>
            <form @submit.prevent="checkAvailability" class="availability-form">
              <div class="form-group">
                <label>Дата заезда</label>
                <input 
                  v-model="availabilityForm.check_in"
                  type="date" 
                  :min="today"
                  required
                >
              </div>
              
              <div class="form-group">
                <label>Дата выезда</label>
                <input 
                  v-model="availabilityForm.check_out"
                  type="date" 
                  :min="minCheckoutDate"
                  required
                >
              </div>
              
              <div class="form-group">
                <label>Количество гостей</label>
                <input 
                  v-model="availabilityForm.guests"
                  type="number" 
                  min="1"
                  required
                >
              </div>
              
              <button 
                type="submit" 
                :disabled="availabilityLoading" 
                class="check-availability-btn"
              >
                {{ availabilityLoading ? 'Проверяем...' : 'Проверить доступность' }}
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- Доступные номера -->
      <div class="available-rooms" v-if="availability && availability.available_rooms.length > 0">
        <h2>Доступные номера</h2>
        <div class="rooms-list">
          <div 
            v-for="room in availability.available_rooms" 
            :key="room.room_id"
            class="room-card"
          >
            <div class="room-info">
              <h4>Номер {{ room.room_number }}</h4>
              <p class="room-type">{{ room.room_type.name }}</p>
              <p class="room-capacity">Вмещает: {{ room.room_type.capacity }} гостей</p>
              <p class="room-price">
                {{ formatPrice(room.price_per_night) }} ₽ / ночь
              </p>
              <p class="total-price">
                Итого за {{ room.nights }} ночей: 
                <strong>{{ formatPrice(room.total_price) }} ₽</strong>
              </p>
            </div>
            <button 
              @click="bookRoom(room)"
              class="book-btn"
            >
              Забронировать
            </button>
          </div>
        </div>
      </div>

      <div v-else-if="availability && availability.available_rooms.length === 0" class="no-rooms">
        <h3>Нет доступных номеров на выбранные даты</h3>
        <p>Попробуйте изменить даты или количество гостей</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHotelsStore } from '../../stores/hotels'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'HotelDetails',
  components: {
    LoadingSpinner
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const hotelsStore = useHotelsStore()
    
    const hotel = computed(() => hotelsStore.currentHotel)
    const availability = computed(() => hotelsStore.availability)
    const loading = computed(() => hotelsStore.loading)
    const error = computed(() => hotelsStore.error)
    
    const availabilityForm = ref({
      check_in: '',
      check_out: '',
      guests: 1
    })
    
    const availabilityLoading = ref(false)

    const today = computed(() => {
      return new Date().toISOString().split('T')[0]
    })

    const minCheckoutDate = computed(() => {
      return availabilityForm.value.check_in || today.value
    })

    const loadHotelDetails = async () => {
      try {
        await hotelsStore.getHotelDetails(route.params.id)
      } catch (err) {
        console.error('Error loading hotel details:', err)
      }
    }

    const checkAvailability = async () => {
      availabilityLoading.value = true
      try {
        await hotelsStore.getHotelAvailability(route.params.id, availabilityForm.value)
      } catch (err) {
        console.error('Error checking availability:', err)
      } finally {
        availabilityLoading.value = false
      }
    }

    const bookRoom = (room) => {
      router.push({
        path: `/booking/create/${room.room_id}`,
        query: {
          check_in: availabilityForm.value.check_in,
          check_out: availabilityForm.value.check_out,
          guests: availabilityForm.value.guests
        }
      })
    }

    const formatPrice = (price) => {
      return new Intl.NumberFormat('ru-RU').format(price)
    }

    onMounted(() => {
      loadHotelDetails()
    })

    return {
      hotel,
      availability,
      loading,
      error,
      availabilityForm,
      availabilityLoading,
      today,
      minCheckoutDate,
      checkAvailability,
      bookRoom,
      formatPrice
    }
  }
}
</script>

<style scoped>
.hotel-details {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.breadcrumbs {
  margin-bottom: 2rem;
  color: #7f8c8d;
}

.breadcrumbs a {
  color: #3498db;
  text-decoration: none;
}

.breadcrumbs a:hover {
  text-decoration: underline;
}

.hotel-gallery {
  margin-bottom: 2rem;
}

.main-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.thumbnail-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.thumbnail {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 5px;
  cursor: pointer;
}

.no-images {
  margin-bottom: 2rem;
}

.no-image-placeholder {
  width: 100%;
  height: 300px;
  background: #ecf0f1;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7f8c8d;
  font-size: 1.1rem;
}

.hotel-main-info {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  margin-bottom: 3rem;
}

.hotel-title {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 2rem;
}

.hotel-location {
  margin: 0 0 1rem 0;
  color: #7f8c8d;
  font-size: 1.1rem;
}

.hotel-rating {
  margin-bottom: 2rem;
}

.stars {
  background: #f39c12;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 500;
}

.hotel-description {
  margin-bottom: 2rem;
}

.hotel-description h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.hotel-amenities h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.amenities-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.amenity-tag {
  background: #3498db;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.booking-widget {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: sticky;
  top: 100px;
}

.booking-widget h3 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  text-align: center;
}

.availability-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 5px;
  font-size: 1rem;
}

.check-availability-btn {
  background: #27ae60;
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 0.5rem;
}

.check-availability-btn:hover:not(:disabled) {
  background: #219a52;
}

.check-availability-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.available-rooms {
  margin-top: 3rem;
}

.available-rooms h2 {
  margin-bottom: 2rem;
  color: #2c3e50;
}

.rooms-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.room-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.room-info h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.room-type {
  margin: 0 0 0.5rem 0;
  color: #3498db;
  font-weight: 500;
}

.room-capacity {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
}

.room-price {
  margin: 0 0 0.5rem 0;
  color: #27ae60;
  font-size: 1.1rem;
}

.total-price {
  margin: 0;
  color: #2c3e50;
}

.book-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 1rem;
}

.book-btn:hover {
  background: #c0392b;
}

.no-rooms {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}

.no-rooms h3 {
  margin-bottom: 1rem;
}

.loading-state, .error-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.back-link {
  margin-top: 1rem;
  color: #3498db;
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}
</style>