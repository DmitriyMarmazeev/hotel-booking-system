<template>
  <div class="hotel-rooms">
    <div class="page-header">
      <div class="header-content">
        <h1>Номера отеля</h1>
        <div class="header-actions">
          <button @click="showRoomForm = true" class="create-btn">
            ➕ Добавить номер
          </button>
          <button @click="showRoomTypeForm = true" class="create-type-btn">
            🏷️ Создать тип номера
          </button>
          <router-link :to="`/manager/hotels`" class="back-link">
            ← Назад к отелям
          </router-link>
        </div>
      </div>
      <p v-if="hotel">{{ hotel.name }}, {{ hotel.city }}</p>
    </div>

    <div v-if="loading" class="loading-state">
      <LoadingSpinner message="Загружаем номера..." />
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-message">
        {{ error }}
      </div>
    </div>

    <div v-else class="rooms-content">
      <!-- Статистика -->
      <div class="rooms-stats">
        <div class="stat">
          <span class="stat-number">{{ totalRooms }}</span>
          <span class="stat-label">всего номеров</span>
        </div>
        <div class="stat">
          <span class="stat-number">{{ availableRooms }}</span>
          <span class="stat-label">доступно</span>
        </div>
        <div class="stat">
          <span class="stat-number">{{ roomTypesCount }}</span>
          <span class="stat-label">типов номеров</span>
        </div>
      </div>

      <!-- Список номеров -->
      <div v-if="rooms.length === 0" class="no-rooms">
        <div class="empty-state">
          <div class="empty-icon">🛏️</div>
          <h3>Номера не добавлены</h3>
          <p>Добавьте номера чтобы принимать бронирования</p>
          <button @click="showRoomForm = true" class="create-link">
            Добавить первый номер
          </button>
        </div>
      </div>

      <div v-else class="rooms-grid">
        <RoomCard 
          v-for="room in rooms" 
          :key="room.id" 
          :room="room"
          :hotel-id="hotelId"
          @edit="editRoom"
        />
      </div>
    </div>

    <!-- Модальное окно создания/редактирования номера -->
    <RoomFormModal 
      v-if="showRoomForm"
      :hotel-id="hotelId"
      :room="editingRoom"
      :room-types="roomTypes"
      @save="handleRoomSave"
      @close="closeRoomForm"
    />

    <!-- Модальное окно создания типа номера -->
    <RoomTypeFormModal 
      v-if="showRoomTypeForm"
      @save="handleRoomTypeSave"
      @close="showRoomTypeForm = false"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useManagerStore } from '../../stores/manager'
import RoomCard from '../../components/manager/RoomCard.vue'
import RoomFormModal from '../../components/manager/RoomFormModal.vue'
import RoomTypeFormModal from '../../components/manager/RoomTypeFormModal.vue'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'HotelRooms',
  components: {
    RoomCard,
    RoomFormModal,
    RoomTypeFormModal,
    LoadingSpinner
  },
  setup() {
    const route = useRoute()
    const managerStore = useManagerStore()
    
    const hotelId = route.params.id
    const loading = ref(false)
    const error = ref('')
    const showRoomForm = ref(false)
    const showRoomTypeForm = ref(false)
    const editingRoom = ref(null)

    const hotel = computed(() => 
      managerStore.myHotels.find(h => h.id === hotelId) || {}
    )
    
    const rooms = computed(() => hotel.value.rooms || [])
    const roomTypes = computed(() => managerStore.roomTypes)

    const totalRooms = computed(() => rooms.value.length)
    const availableRooms = computed(() => 
      rooms.value.filter(room => room.is_available).length
    )
    const roomTypesCount = computed(() => roomTypes.value.length)

    const loadData = async () => {
      loading.value = true
      error.value = ''
      
      try {
        await managerStore.getMyHotels()
        await managerStore.getRoomTypes()
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка загрузки данных'
      } finally {
        loading.value = false
      }
    }

    const editRoom = (room) => {
      editingRoom.value = room
      showRoomForm.value = true
    }

    const handleRoomSave = async () => {
      await loadData() // Перезагружаем данные после сохранения
      closeRoomForm()
    }

    const handleRoomTypeSave = async () => {
      await managerStore.getRoomTypes() // Обновляем список типов номеров
      showRoomTypeForm.value = false
    }

    const closeRoomForm = () => {
      showRoomForm.value = false
      editingRoom.value = null
    }

    onMounted(() => {
      loadData()
    })

    return {
      hotelId,
      hotel,
      rooms,
      roomTypes,
      loading,
      error,
      showRoomForm,
      showRoomTypeForm,
      editingRoom,
      totalRooms,
      availableRooms,
      roomTypesCount,
      editRoom,
      handleRoomSave,
      handleRoomTypeSave,
      closeRoomForm
    }
  }
}
</script>

<style scoped>
.hotel-rooms {
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

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.create-btn {
  background: linear-gradient(135deg, #27ae60 0%, #219a52 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.create-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(39, 174, 96, 0.3);
}

.create-type-btn {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.create-type-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
}

.back-link {
  color: #7f8c8d;
  text-decoration: none;
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  border: 1px solid #bdc3c7;
  border-radius: 6px;
  transition: all 0.3s;
}

.back-link:hover {
  background: #f8f9fa;
  text-decoration: none;
}

.page-header p {
  color: #7f8c8d;
  margin: 0;
  font-size: 1.1rem;
}

.rooms-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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

.rooms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.loading-state, .error-state, .no-rooms {
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
  max-width: 400px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin-bottom: 1rem;
}

.empty-state p {
  margin-bottom: 2rem;
  line-height: 1.5;
}

.create-link {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
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
  
  .header-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .create-btn, .create-type-btn, .back-link {
    text-align: center;
  }
  
  .rooms-grid {
    grid-template-columns: 1fr;
  }
  
  .rooms-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>