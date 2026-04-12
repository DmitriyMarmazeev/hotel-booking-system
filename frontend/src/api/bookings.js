import apiClient from './client'

export const bookingsApi = {
  // Создать бронирование
  createBooking(bookingData) {
    return apiClient.post('/api/bookings/', bookingData)
  },

  // Мои бронирования
  getMyBookings() {
    return apiClient.get('/api/bookings/my-bookings')
  },

  // Получить бронирование по ID
  getBooking(bookingId) {
    return apiClient.get(`/api/bookings/${bookingId}`)
  },

  // Отменить бронирование
  cancelBooking(bookingId) {
    return apiClient.put(`/api/bookings/${bookingId}/cancel`)
  },

  // Проверить доступность номера
  checkAvailability(params) {
    return apiClient.get('/api/bookings/availability/check', { params })
  }
}