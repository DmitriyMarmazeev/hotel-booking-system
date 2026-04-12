import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Auth views
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'

// Guest views
import GuestDashboard from '../views/guest/Dashboard.vue'
import HotelSearch from '../views/guest/HotelSearch.vue'
import HotelDetails from '../views/guest/HotelDetails.vue'
import MyBookings from '../views/guest/MyBookings.vue'
import CreateBooking from '../views/guest/CreateBooking.vue'
import BookingDetails from '../views/guest/BookingDetails.vue'

// Manager views
import ManagerDashboard from '../views/manager/Dashboard.vue'
import MyHotels from '../views/manager/MyHotels.vue'
import HotelForm from '../views/manager/HotelForm.vue'
import HotelBookings from '../views/manager/HotelBookings.vue'
import HotelRooms from '../views/manager/HotelRooms.vue'

// Admin views
import AdminDashboard from '../views/admin/Dashboard.vue'
import UserManagement from '../views/admin/UserManagement.vue'

const routes = [
  // Auth routes
  { path: '/login', component: Login, meta: { requiresGuest: true } },
  { path: '/register', component: Register, meta: { requiresGuest: true } },
  
  // Guest routes
  { path: '/', component: GuestDashboard, meta: { requiresAuth: true, role: 'guest' } },
  { path: '/search', component: HotelSearch, meta: { requiresAuth: true, role: 'guest' } },
  { path: '/hotel/:id', component: HotelDetails, meta: { requiresAuth: true, role: 'guest' } },
  { path: '/my-bookings', component: MyBookings, meta: { requiresAuth: true, role: 'guest' } },
  { path: '/booking/create/:roomId', component: CreateBooking, meta: { requiresAuth: true, role: 'guest' } },
  { path: '/booking/:id', component: BookingDetails, meta: { requiresAuth: true, role: 'guest' } },
  
  // Manager routes
  { path: '/manager', component: ManagerDashboard, meta: { requiresAuth: true, role: 'hotel_manager' } },
  { path: '/manager/hotels', component: MyHotels, meta: { requiresAuth: true, role: 'hotel_manager' } },
  { path: '/manager/hotels/new', component: HotelForm, meta: { requiresAuth: true, role: 'hotel_manager' } },
  { path: '/manager/hotels/:id/edit', component: HotelForm, meta: { requiresAuth: true, role: 'hotel_manager' } },
  { path: '/manager/hotels/:id/bookings', component: HotelBookings, meta: { requiresAuth: true, role: 'hotel_manager' } },
  { path: '/manager/hotels/:id/rooms', component: HotelRooms, meta: { requiresAuth: true, role: 'hotel_manager' } },
  
  // Admin routes
  { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/users', component: UserManagement, meta: { requiresAuth: true, role: 'admin' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    // Редирект в зависимости от роли
    const role = authStore.userRole
    if (role === 'admin') next('/admin')
    else if (role === 'hotel_manager') next('/manager')
    else next('/')
  } else if (to.meta.requiresAuth && to.meta.role && authStore.userRole !== to.meta.role) {
    // Если у пользователя нет прав для этого маршрута
    next('/')
  } else {
    next()
  }
})

export default router