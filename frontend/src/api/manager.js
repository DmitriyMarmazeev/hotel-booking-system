import apiClient from './client'

export const managerApi = {
  // Получить мои отели
  getMyHotels() {
    return apiClient.get('/api/hotels/my/hotels')
  },

  // Создать отель
  createHotel(hotelData) {
    return apiClient.post('/api/hotels/', hotelData)
  },

  // Обновить отель
  updateHotel(hotelId, hotelData) {
    return apiClient.put(`/api/hotels/${hotelId}`, hotelData)
  },

  // Получить бронирования отеля
  getHotelBookings(hotelId, status = null) {
    const params = status ? { status } : {}
    return apiClient.get(`/api/bookings/hotel/${hotelId}/bookings`, { params })
  },

  // Обновить статус бронирования
  updateBookingStatus(bookingId, statusData) {
    return apiClient.put(`/api/bookings/${bookingId}/status`, statusData)
  },

  // Создать номер
  createRoom(hotelId, roomData) {
    return apiClient.post(`/api/hotels/${hotelId}/rooms`, roomData)
  },

  // Обновить номер
  updateRoom(roomId, roomData) {
    return apiClient.put(`/api/hotels/rooms/${roomId}`, roomData)
  },

  // Создать номер
  createRoom(hotelId, roomData) {
    return apiClient.post(`/api/hotels/${hotelId}/rooms`, roomData)
  },

  // Обновить номер
  updateRoom(roomId, roomData) {
    return apiClient.put(`/api/hotels/rooms/${roomId}`, roomData)
  },

  // Получить типы номеров
  getRoomTypes() {
    return apiClient.get('/api/hotels/room-types/')
  },

  // Создать тип номера
  createRoomType(roomTypeData) {
    return apiClient.post('/api/hotels/room-types/', roomTypeData)
  }
}