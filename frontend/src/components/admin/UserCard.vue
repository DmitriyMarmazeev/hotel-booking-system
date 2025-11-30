<template>
  <div class="user-card">
    <div class="user-main">
      <div class="user-info">
        <div class="user-avatar">
          {{ getUserInitials(user) }}
        </div>
        <div class="user-details">
          <h4>{{ user.first_name }} {{ user.last_name }}</h4>
          <p class="user-email">{{ user.email }}</p>
          <p class="user-phone" v-if="user.phone">📞 {{ user.phone }}</p>
          <div class="user-meta">
            <span class="registration-date">
              Зарегистрирован: {{ formatDate(user.created_at) }}
            </span>
            <span class="user-status" :class="user.is_active ? 'active' : 'inactive'">
              {{ user.is_active ? 'Активен' : 'Неактивен' }}
            </span>
          </div>
        </div>
      </div>

      <div class="user-role">
        <select 
          v-model="selectedRole" 
          @change="updateUserRole"
          class="role-select"
          :disabled="updatingRole"
        >
          <option value="guest">Гость</option>
          <option value="hotel_manager">Менеджер отеля</option>
          <option value="admin">Администратор</option>
        </select>
        <span class="role-badge" :class="`role-${user.role}`">
          {{ getRoleText(user.role) }}
        </span>
      </div>
    </div>

    <div class="user-actions">
      <button 
        @click="toggleUserStatus"
        class="action-btn status-btn"
        :class="user.is_active ? 'deactivate' : 'activate'"
        :disabled="updatingStatus"
      >
        {{ user.is_active ? '❌ Деактивировать' : '✅ Активировать' }}
      </button>
      <button 
        @click="deleteUser"
        class="action-btn delete-btn"
        :disabled="deleting"
      >
        🗑️ Удалить
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useAdminStore } from '../../stores/admin'

export default {
  name: 'UserCard',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const adminStore = useAdminStore()
    
    const selectedRole = ref(props.user.role)
    const updatingRole = ref(false)
    const updatingStatus = ref(false)
    const deleting = ref(false)

    const getUserInitials = (user) => {
      return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase()
    }

    const getRoleText = (role) => {
      const roleMap = {
        'guest': 'Гость',
        'hotel_manager': 'Менеджер',
        'admin': 'Админ'
      }
      return roleMap[role] || role
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU')
    }

    const updateUserRole = async () => {
      if (selectedRole.value === props.user.role) return
      
      updatingRole.value = true
      try {
        await adminStore.updateUserRole(props.user.id, selectedRole.value)
      } catch (error) {
        console.error('Error updating user role:', error)
        selectedRole.value = props.user.role // Возвращаем предыдущее значение при ошибке
      } finally {
        updatingRole.value = false
      }
    }

    const toggleUserStatus = async () => {
      updatingStatus.value = true
      try {
        // Здесь должен быть вызов API для изменения статуса пользователя
        // Пока просто имитируем изменение
        console.log('Toggle user status:', props.user.id)
      } catch (error) {
        console.error('Error updating user status:', error)
      } finally {
        updatingStatus.value = false
      }
    }

    const deleteUser = async () => {
      if (!confirm(`Вы уверены, что хотите удалить пользователя ${props.user.first_name} ${props.user.last_name}?`)) {
        return
      }

      deleting.value = true
      try {
        await adminStore.deleteUser(props.user.id)
      } catch (error) {
        console.error('Error deleting user:', error)
      } finally {
        deleting.value = false
      }
    }

    return {
      selectedRole,
      updatingRole,
      updatingStatus,
      deleting,
      getUserInitials,
      getRoleText,
      formatDate,
      updateUserRole,
      toggleUserStatus,
      deleteUser
    }
  }
}
</script>

<style scoped>
.user-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 1.5rem;
  margin-bottom: 1rem;
  border-left: 4px solid #3498db;
  transition: transform 0.2s, box-shadow 0.2s;
}

.user-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.user-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.user-info {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.user-details h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.user-email {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.user-phone {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.user-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.registration-date {
  color: #95a5a6;
  font-size: 0.8rem;
}

.user-status {
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 500;
  align-self: flex-start;
}

.user-status.active {
  background: #d4edda;
  color: #155724;
}

.user-status.inactive {
  background: #f8d7da;
  color: #721c24;
}

.user-role {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  min-width: 150px;
}

.role-select {
  padding: 0.4rem 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 0.8rem;
  background: white;
}

.role-select:disabled {
  background: #ecf0f1;
  cursor: not-allowed;
}

.role-badge {
  padding: 0.3rem 0.75rem;
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 500;
}

.role-badge.role-guest {
  background: #e8f4fd;
  color: #2980b9;
}

.role-badge.role-hotel_manager {
  background: #fff3cd;
  color: #856404;
}

.role-badge.role-admin {
  background: #d4edda;
  color: #155724;
}

.user-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.5rem 1rem;
  border-radius: 5px;
  font-size: 0.8rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.status-btn.activate {
  background: #27ae60;
  color: white;
}

.status-btn.activate:hover:not(:disabled) {
  background: #219a52;
}

.status-btn.deactivate {
  background: #e74c3c;
  color: white;
}

.status-btn.deactivate:hover:not(:disabled) {
  background: #c0392b;
}

.delete-btn {
  background: #95a5a6;
  color: white;
}

.delete-btn:hover:not(:disabled) {
  background: #7f8c8d;
}

@media (max-width: 768px) {
  .user-main {
    flex-direction: column;
    align-items: stretch;
  }
  
  .user-role {
    align-items: stretch;
    flex-direction: row;
    justify-content: space-between;
  }
  
  .user-actions {
    flex-direction: column;
  }
  
  .action-btn {
    text-align: center;
  }
}
</style>