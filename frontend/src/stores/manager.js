import { defineStore } from 'pinia'
import { ref } from 'vue'
import { managerApi } from '../api/manager'

export const useManagerStore = defineStore('manager', () => {
  const myHotels = ref([])
  const currentHotel = ref(null)
  const hotelBookings = ref([])
  const loading = ref(false)
  const error = ref(null)
  const roomTypes = ref([])
  const currentRoom = ref(null)

  const getMyHotels = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await managerApi.getMyHotels()
      myHotels.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки отелей'
      throw err
    } finally {
      loading.value = false
    }
  }

  const createHotel = async (hotelData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await managerApi.createHotel(hotelData)
      myHotels.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка создания отеля'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateHotel = async (hotelId, hotelData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await managerApi.updateHotel(hotelId, hotelData)
      const index = myHotels.value.findIndex(h => h.id === hotelId)
      if (index !== -1) {
        myHotels.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка обновления отеля'
      throw err
    } finally {
      loading.value = false
    }
  }

  const getHotelBookings = async (hotelId, status = null) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await managerApi.getHotelBookings(hotelId, status)
      hotelBookings.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки бронирований'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateBookingStatus = async (bookingId, statusData) => {
    try {
      const response = await managerApi.updateBookingStatus(bookingId, statusData)
      
      // Обновляем статус в локальном списке
      const bookingIndex = hotelBookings.value.findIndex(b => b.id === bookingId)
      if (bookingIndex !== -1) {
        hotelBookings.value[bookingIndex] = response.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка обновления статуса'
      throw err
    }
  }

  const clearError = () => {
    error.value = null
  }

  const getRoomTypes = async () => {
    try {
      const response = await managerApi.getRoomTypes()
      roomTypes.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки типов номеров'
      throw err
    }
  }

  const createRoomType = async (roomTypeData) => {
    try {
      const response = await managerApi.createRoomType(roomTypeData)
      roomTypes.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка создания типа номера'
      throw err
    }
  }

  const createRoom = async (hotelId, roomData) => {
    try {
      const response = await managerApi.createRoom(hotelId, roomData)
      
      // Обновляем список отелей, чтобы отобразить новый номер
      const hotelIndex = myHotels.value.findIndex(h => h.id === hotelId)
      if (hotelIndex !== -1) {
        if (!myHotels.value[hotelIndex].rooms) {
          myHotels.value[hotelIndex].rooms = []
        }
        myHotels.value[hotelIndex].rooms.push(response.data)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка создания номера'
      throw err
    }
  }

  const updateRoom = async (roomId, roomData) => {
    try {
      const response = await managerApi.updateRoom(roomId, roomData)
      
      // Обновляем номер в списке отелей
      for (const hotel of myHotels.value) {
        if (hotel.rooms) {
          const roomIndex = hotel.rooms.findIndex(r => r.id === roomId)
          if (roomIndex !== -1) {
            hotel.rooms[roomIndex] = response.data
            break
          }
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка обновления номера'
      throw err
    }
  }

  return {
    myHotels,
    currentHotel,
    hotelBookings,
    loading,
    error,
    roomTypes,
    currentRoom,
    getMyHotels,
    createHotel,
    updateHotel,
    getHotelBookings,
    updateBookingStatus,
    createRoom,
    clearError,
    getRoomTypes,
    createRoomType,
    createRoom,
    updateRoom
  }
})