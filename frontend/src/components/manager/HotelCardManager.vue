<template>
  <div class="hotel-card-manager">
    <div class="hotel-header">
      <div class="hotel-info">
        <h3>{{ hotel.name }}</h3>
        <p class="hotel-location">📍 {{ hotel.city }}, {{ hotel.country }}</p>
        <div class="hotel-status">
          <span class="status-badge" :class="hotel.is_active ? 'active' : 'inactive'">
            {{ hotel.is_active ? 'Активен' : 'Неактивен' }}
          </span>
          <span class="star-rating" v-if="hotel.star_rating">
            ⭐ {{ hotel.star_rating }}
          </span>
        </div>
      </div>
      
      <div class="hotel-stats">
        <div class="stat">
          <span class="stat-number">{{ hotel.rooms?.length || 0 }}</span>
          <span class="stat-label">номеров</span>
        </div>
      </div>
    </div>

    <div class="hotel-actions">
      <router-link 
        :to="`/manager/hotels/${hotel.id}/bookings`" 
        class="action-btn bookings-btn"
      >
        📋 Бронирования
      </router-link>
      <router-link 
        :to="`/manager/hotels/${hotel.id}/edit`" 
        class="action-btn edit-btn"
      >
        ✏️ Редактировать
      </router-link>
      <router-link 
        :to="`/manager/hotels/${hotel.id}/rooms`" 
        class="action-btn rooms-btn"
      >
        🛏️ Номера
      </router-link>
      <button 
        @click="toggleHotelStatus"
        class="action-btn status-btn"
        :class="hotel.is_active ? 'deactivate' : 'activate'"
      >
        {{ hotel.is_active ? '⏸️ Деактивировать' : '▶️ Активировать' }}
      </button>
    </div>

    <div class="hotel-description" v-if="hotel.description">
      <p>{{ hotel.description }}</p>
    </div>

    <div class="hotel-amenities" v-if="hotel.amenities && hotel.amenities.length > 0">
      <div class="amenities-list">
        <span 
          v-for="amenity in hotel.amenities.slice(0, 4)" 
          :key="amenity" 
          class="amenity-tag"
        >
          {{ amenity }}
        </span>
        <span v-if="hotel.amenities.length > 4" class="amenity-more">
          +{{ hotel.amenities.length - 4 }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { useManagerStore } from '../../stores/manager'

export default {
  name: 'HotelCardManager',
  props: {
    hotel: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const managerStore = useManagerStore()

    const toggleHotelStatus = async () => {
      try {
        await managerStore.updateHotel(props.hotel.id, {
          is_active: !props.hotel.is_active
        })
      } catch (error) {
        console.error('Error updating hotel status:', error)
      }
    }

    return {
      toggleHotelStatus
    }
  }
}
</script>

<style scoped>
.hotel-card-manager {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border-left: 4px solid #3498db;
  transition: transform 0.2s, box-shadow 0.2s;
}

.hotel-card-manager:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.hotel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.hotel-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.25rem;
}

.hotel-location {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
}

.hotel-status {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background: #f8d7da;
  color: #721c24;
}

.star-rating {
  background: #fff3cd;
  color: #856404;
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  font-size: 0.8rem;
}

.hotel-stats {
  display: flex;
  gap: 1rem;
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
}

.hotel-actions {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.bookings-btn {
  background: #3498db;
  color: white;
}

.bookings-btn:hover {
  background: #2980b9;
}

.edit-btn {
  background: #f39c12;
  color: white;
}

.edit-btn:hover {
  background: #e67e22;
}

.status-btn.activate {
  background: #27ae60;
  color: white;
}

.status-btn.activate:hover {
  background: #219a52;
}

.status-btn.deactivate {
  background: #e74c3c;
  color: white;
}

.status-btn.deactivate:hover {
  background: #c0392b;
}

.hotel-description {
  margin-bottom: 1rem;
  color: #5d6d7e;
  line-height: 1.5;
}

.amenities-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.amenity-tag {
  background: #ecf0f1;
  color: #2c3e50;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.amenity-more {
  background: #bdc3c7;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.rooms-btn {
  background: #9b59b6;
  color: white;
}

.rooms-btn:hover {
  background: #8e44ad;
}

@media (max-width: 768px) {
  .hotel-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .hotel-actions {
    flex-direction: column;
  }
  
  .action-btn {
    text-align: center;
  }
}
</style>