<template>
  <div class="room-card">
    <div class="room-header">
      <div class="room-info">
        <h4>Номер {{ room.room_number }}</h4>
        <p class="room-type">{{ room.room_type?.name }}</p>
        <div class="room-details">
          <span class="detail">Этаж: {{ room.floor || 'Не указан' }}</span>
          <span class="detail">Вместимость: {{ room.room_type?.capacity }} гостей</span>
          <span class="detail">Цена: {{ formatPrice(room.room_type?.base_price) }} ₽/ночь</span>
        </div>
      </div>
      
      <div class="room-status">
        <span class="status-badge" :class="room.is_available ? 'available' : 'unavailable'">
          {{ room.is_available ? 'Доступен' : 'Не доступен' }}
        </span>
      </div>
    </div>

    <div class="room-amenities" v-if="room.room_type?.amenities && room.room_type.amenities.length > 0">
      <div class="amenities-list">
        <span 
          v-for="amenity in room.room_type.amenities.slice(0, 3)" 
          :key="amenity" 
          class="amenity-tag"
        >
          {{ amenity }}
        </span>
        <span v-if="room.room_type.amenities.length > 3" class="amenity-more">
          +{{ room.room_type.amenities.length - 3 }}
        </span>
      </div>
    </div>

    <div class="room-actions">
      <button 
        @click="toggleRoomAvailability"
        class="action-btn status-btn"
        :class="room.is_available ? 'unavailable' : 'available'"
      >
        {{ room.is_available ? '❌ Сделать недоступным' : '✅ Сделать доступным' }}
      </button>
      <button 
        @click="editRoom"
        class="action-btn edit-btn"
      >
        ✏️ Редактировать
      </button>
    </div>
  </div>
</template>

<script>
import { useManagerStore } from '../../stores/manager'

export default {
  name: 'RoomCard',
  props: {
    room: {
      type: Object,
      required: true
    },
    hotelId: {
      type: String,
      required: true
    }
  },
  emits: ['edit'],
  setup(props, { emit }) {
    const managerStore = useManagerStore()

    const toggleRoomAvailability = async () => {
      try {
        await managerStore.updateRoom(props.room.id, {
          is_available: !props.room.is_available
        })
      } catch (error) {
        console.error('Error updating room availability:', error)
      }
    }

    const editRoom = () => {
      emit('edit', props.room)
    }

    const formatPrice = (price) => {
      return new Intl.NumberFormat('ru-RU').format(price)
    }

    return {
      toggleRoomAvailability,
      editRoom,
      formatPrice
    }
  }
}
</script>

<style scoped>
.room-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 1.25rem;
  border-left: 3px solid #3498db;
  transition: transform 0.2s, box-shadow 0.2s;
}

.room-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.room-info h4 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.room-type {
  margin: 0 0 0.75rem 0;
  color: #3498db;
  font-weight: 500;
  font-size: 0.9rem;
}

.room-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail {
  color: #7f8c8d;
  font-size: 0.85rem;
}

.room-status {
  flex-shrink: 0;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.available {
  background: #d4edda;
  color: #155724;
}

.status-badge.unavailable {
  background: #f8d7da;
  color: #721c24;
}

.room-amenities {
  margin-bottom: 1rem;
}

.amenities-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.amenity-tag {
  background: #ecf0f1;
  color: #2c3e50;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  font-size: 0.75rem;
}

.amenity-more {
  background: #bdc3c7;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  font-size: 0.75rem;
}

.room-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.4rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.status-btn.available {
  background: #27ae60;
  color: white;
}

.status-btn.available:hover {
  background: #219a52;
}

.status-btn.unavailable {
  background: #e74c3c;
  color: white;
}

.status-btn.unavailable:hover {
  background: #c0392b;
}

.edit-btn {
  background: #f39c12;
  color: white;
}

.edit-btn:hover {
  background: #e67e22;
}

@media (max-width: 768px) {
  .room-header {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .room-actions {
    flex-direction: column;
  }
  
  .action-btn {
    text-align: center;
  }
}
</style>