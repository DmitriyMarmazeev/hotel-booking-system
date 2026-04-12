import apiClient from './client'

export const hotelsApi = {
  // Поиск отелей
  searchHotels(params) {
    return apiClient.get('/api/hotels/search', { params })
  },

  // Получить детали отеля
  getHotelDetails(hotelId) {
    return apiClient.get(`/api/hotels/${hotelId}`)
  },

  // Получить доступность номеров
  getHotelAvailability(hotelId, params) {
    return apiClient.get(`/api/hotels/availability/${hotelId}`, { params })
  },

  // Популярные направления
  getPopularDestinations(limit = 10) {
    return apiClient.get('/api/hotels/destinations/popular', { 
      params: { limit } 
    })
  },

  // Типы номеров
  getRoomTypes() {
    return apiClient.get('/api/hotels/room-types/')
  }
}