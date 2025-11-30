<template>
  <div class="hotel-card">
    <div class="hotel-images">
      <img 
        v-if="hotel.images && hotel.images.length > 0" 
        :src="hotel.images[0]" 
        :alt="hotel.name"
        class="hotel-image"
      >
      <div v-else class="no-image">Нет фото</div>
    </div>
    
    <div class="hotel-info">
      <h3 class="hotel-name">{{ hotel.name }}</h3>
      <p class="hotel-location">
        📍 {{ hotel.city }}, {{ hotel.country }}
      </p>
      
      <div class="hotel-rating" v-if="hotel.star_rating">
        ⭐ {{ hotel.star_rating }} звезд(ы)
      </div>
      
      <div class="hotel-amenities">
        <span 
          v-for="amenity in hotel.amenities.slice(0, 3)" 
          :key="amenity" 
          class="amenity-tag"
        >
          {{ amenity }}
        </span>
        <span v-if="hotel.amenities.length > 3" class="amenity-more">
          +{{ hotel.amenities.length - 3 }}
        </span>
      </div>
      
      <p class="hotel-description" v-if="hotel.description">
        {{ truncateDescription(hotel.description) }}
      </p>
    </div>
    
    <div class="hotel-pricing">
      <div class="price">от {{ formatPrice(hotel.min_price) }} ₽</div>
      <div class="available-rooms">
        Доступно номеров: {{ hotel.available_rooms }}
      </div>
      <router-link 
        :to="`/hotel/${hotel.id}`" 
        class="view-details-btn"
      >
        Подробнее
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HotelCard',
  props: {
    hotel: {
      type: Object,
      required: true
    }
  },
  methods: {
    truncateDescription(description) {
      return description.length > 100 
        ? description.substring(0, 100) + '...' 
        : description
    },
    
    formatPrice(price) {
      return new Intl.NumberFormat('ru-RU').format(price)
    }
  }
}
</script>

<style scoped>
.hotel-card {
  display: flex;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
  margin-bottom: 1.5rem;
  transition: transform 0.3s, box-shadow 0.3s;
}

.hotel-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.hotel-images {
  width: 250px;
  flex-shrink: 0;
}

.hotel-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.no-image {
  width: 100%;
  height: 200px;
  background: #ecf0f1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7f8c8d;
}

.hotel-info {
  flex: 1;
  padding: 1.5rem;
}

.hotel-name {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.25rem;
}

.hotel-location {
  margin: 0 0 1rem 0;
  color: #7f8c8d;
}

.hotel-rating {
  margin-bottom: 1rem;
  color: #f39c12;
  font-weight: 500;
}

.hotel-amenities {
  margin-bottom: 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.amenity-tag {
  background: #3498db;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  font-size: 0.8rem;
}

.amenity-more {
  background: #bdc3c7;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  font-size: 0.8rem;
}

.hotel-description {
  color: #5d6d7e;
  line-height: 1.5;
  margin: 0;
}

.hotel-pricing {
  width: 200px;
  flex-shrink: 0;
  padding: 1.5rem;
  background: #f8f9fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #27ae60;
  margin-bottom: 0.5rem;
}

.available-rooms {
  color: #7f8c8d;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.view-details-btn {
  background: #3498db;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.view-details-btn:hover {
  background: #2980b9;
}
</style>