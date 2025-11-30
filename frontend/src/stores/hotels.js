import { defineStore } from 'pinia'
import { ref } from 'vue'
import { hotelsApi } from '../api/hotels'

export const useHotelsStore = defineStore('hotels', () => {
  const hotels = ref([])
  const currentHotel = ref(null)
  const availability = ref(null)
  const popularDestinations = ref([])
  const roomTypes = ref([])
  const loading = ref(false)
  const error = ref(null)

  const searchHotels = async (searchParams) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await hotelsApi.searchHotels(searchParams)
      hotels.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка поиска отелей'
      throw err
    } finally {
      loading.value = false
    }
  }

  const getHotelDetails = async (hotelId) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await hotelsApi.getHotelDetails(hotelId)
      currentHotel.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки отеля'
      throw err
    } finally {
      loading.value = false
    }
  }

  const getHotelAvailability = async (hotelId, params) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await hotelsApi.getHotelAvailability(hotelId, params)
      availability.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка проверки доступности'
      throw err
    } finally {
      loading.value = false
    }
  }

  const getPopularDestinations = async (limit = 10) => {
    try {
      const response = await hotelsApi.getPopularDestinations(limit)
      popularDestinations.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки направлений'
      throw err
    }
  }

  const getRoomTypes = async () => {
    try {
      const response = await hotelsApi.getRoomTypes()
      roomTypes.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки типов номеров'
      throw err
    }
  }

  const clearHotels = () => {
    hotels.value = []
  }

  const clearCurrentHotel = () => {
    currentHotel.value = null
    availability.value = null
  }

  return {
    hotels,
    currentHotel,
    availability,
    popularDestinations,
    roomTypes,
    loading,
    error,
    searchHotels,
    getHotelDetails,
    getHotelAvailability,
    getPopularDestinations,
    getRoomTypes,
    clearHotels,
    clearCurrentHotel
  }
})