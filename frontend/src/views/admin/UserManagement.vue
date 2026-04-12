<template>
  <div class="user-management">
    <div class="page-header">
      <h1>Управление пользователями</h1>
      <p>Управление всеми пользователями системы и их ролями</p>
    </div>

    <!-- Статистика пользователей -->
    <div class="users-stats">
      <div class="stat">
        <span class="stat-number">{{ totalUsers }}</span>
        <span class="stat-label">Всего пользователей</span>
      </div>
      <div class="stat">
        <span class="stat-number">{{ guestsCount }}</span>
        <span class="stat-label">Гостей</span>
      </div>
      <div class="stat">
        <span class="stat-number">{{ managersCount }}</span>
        <span class="stat-label">Менеджеров</span>
      </div>
      <div class="stat">
        <span class="stat-number">{{ adminsCount }}</span>
        <span class="stat-label">Администраторов</span>
      </div>
    </div>

    <!-- Фильтры и поиск -->
    <div class="users-filters">
      <div class="search-box">
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Поиск по имени, email..."
          class="search-input"
        >
        <span class="search-icon">🔍</span>
      </div>
      
      <select v-model="roleFilter" class="filter-select">
        <option value="">Все роли</option>
        <option value="guest">Гости</option>
        <option value="hotel_manager">Менеджеры</option>
        <option value="admin">Администраторы</option>
      </select>

      <select v-model="statusFilter" class="filter-select">
        <option value="">Все статусы</option>
        <option value="active">Активные</option>
        <option value="inactive">Неактивные</option>
      </select>
    </div>

    <div v-if="loading" class="loading-state">
      <LoadingSpinner message="Загружаем пользователей..." />
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-message">
        {{ error }}
      </div>
      <button @click="loadUsers" class="retry-btn">Попробовать снова</button>
    </div>

    <div v-else-if="filteredUsers.length === 0" class="no-users">
      <div class="empty-state">
        <div class="empty-icon">👥</div>
        <h3>Пользователи не найдены</h3>
        <p>Попробуйте изменить параметры поиска</p>
      </div>
    </div>

    <div v-else class="users-list">
      <UserCard 
        v-for="user in filteredUsers" 
        :key="user.id" 
        :user="user" 
      />
    </div>

    <!-- Пагинация -->
    <div class="pagination" v-if="filteredUsers.length > 0">
      <button 
        @click="prevPage" 
        :disabled="currentPage === 1"
        class="pagination-btn"
      >
        ← Назад
      </button>
      <span class="page-info">
        Страница {{ currentPage }}
      </span>
      <button 
        @click="nextPage" 
        :disabled="filteredUsers.length < pageSize"
        class="pagination-btn"
      >
        Вперед →
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import UserCard from '../../components/admin/UserCard.vue'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

export default {
  name: 'UserManagement',
  components: {
    UserCard,
    LoadingSpinner
  },
  setup() {
    const adminStore = useAdminStore()
    const loading = ref(false)
    const searchQuery = ref('')
    const roleFilter = ref('')
    const statusFilter = ref('')
    const currentPage = ref(1)
    const pageSize = 20

    const users = computed(() => adminStore.users)
    const error = computed(() => adminStore.error)

    const filteredUsers = computed(() => {
      let filtered = users.value

      // Фильтр по поисковому запросу
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(user => 
          user.first_name.toLowerCase().includes(query) ||
          user.last_name.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query) ||
          (user.phone && user.phone.includes(query))
        )
      }

      // Фильтр по роли
      if (roleFilter.value) {
        filtered = filtered.filter(user => user.role === roleFilter.value)
      }

      // Фильтр по статусу
      if (statusFilter.value) {
        filtered = filtered.filter(user => 
          statusFilter.value === 'active' ? user.is_active : !user.is_active
        )
      }

      // Пагинация
      const startIndex = (currentPage.value - 1) * pageSize
      return filtered.slice(startIndex, startIndex + pageSize)
    })

    const totalUsers = computed(() => users.value.length)
    const guestsCount = computed(() => users.value.filter(u => u.role === 'guest').length)
    const managersCount = computed(() => users.value.filter(u => u.role === 'hotel_manager').length)
    const adminsCount = computed(() => users.value.filter(u => u.role === 'admin').length)

    const loadUsers = async () => {
      loading.value = true
      try {
        await adminStore.getUsers()
      } catch (err) {
        console.error('Error loading users:', err)
      } finally {
        loading.value = false
      }
    }

    const nextPage = () => {
      currentPage.value++
    }

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
      }
    }

    // Сбрасываем пагинацию при изменении фильтров
    const resetPagination = () => {
      currentPage.value = 1
    }

    onMounted(() => {
      loadUsers()
    })

    return {
      users: filteredUsers,
      loading,
      error,
      searchQuery,
      roleFilter,
      statusFilter,
      currentPage,
      pageSize,
      totalUsers,
      guestsCount,
      managersCount,
      adminsCount,
      loadUsers,
      nextPage,
      prevPage,
      resetPagination
    }
  }
}
</script>

<style scoped>
.user-management {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.users-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
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

.users-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 250px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
  background: #f8f9fa;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
  background: white;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #7f8c8d;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  font-size: 1rem;
  background: white;
  min-width: 150px;
}

.filter-select:focus {
  outline: none;
  border-color: #3498db;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.loading-state, .error-state, .no-users {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  text-align: center;
}

.error-message {
  background: #e74c3c;
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  max-width: 500px;
}

.retry-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.retry-btn:hover {
  background: #2980b9;
}

.empty-state {
  max-width: 400px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.empty-state p {
  color: #7f8c8d;
  line-height: 1.5;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

.pagination-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  background: #2980b9;
}

.pagination-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.page-info {
  color: #7f8c8d;
  font-weight: 500;
}

@media (max-width: 768px) {
  .users-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .users-filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    min-width: auto;
  }
  
  .filter-select {
    min-width: auto;
  }
}
</style>