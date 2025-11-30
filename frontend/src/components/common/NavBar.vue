<template>
  <nav class="navbar">
    <div class="nav-brand">
      <h2>Hotel Booking</h2>
    </div>
    <div class="nav-links">
      <template v-if="userRole === 'guest'">
        <router-link to="/">Главная</router-link>
        <router-link to="/search">Поиск отелей</router-link>
        <router-link to="/my-bookings">Мои бронирования</router-link>
      </template>
      
      <template v-else-if="userRole === 'hotel_manager'">
        <router-link to="/manager">Дашборд</router-link>
        <router-link to="/manager/hotels">Мои отели</router-link>
      </template>
      
      <template v-else-if="userLink === 'admin'">
        <router-link to="/admin">Дашборд</router-link>
        <router-link to="/admin/users">Пользователи</router-link>
      </template>
      
      <span class="user-info">
        {{ user?.first_name }} {{ user?.last_name }} ({{ userRole }})
      </span>
      <button @click="logout" class="logout-btn">Выйти</button>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '../../stores/auth'

export default {
  name: 'NavBar',
  setup() {
    const authStore = useAuthStore()
    
    const logout = () => {
      authStore.logout()
    }
    
    return {
      user: authStore.user,
      userRole: authStore.userRole,
      logout
    }
  }
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
}

.nav-brand h2 {
  margin: 0;
  color: #3498db;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-links a:hover {
  background-color: #34495e;
}

.nav-links a.router-link-active {
  background-color: #3498db;
}

.user-info {
  color: #bdc3c7;
  margin-right: 1rem;
}

.logout-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background: #c0392b;
}
</style>