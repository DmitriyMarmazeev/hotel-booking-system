<template>
  <div class="search-widget">
    <form @submit.prevent="handleSubmit" class="search-form">
      <div class="form-row">
        <div class="form-group">
          <label>Город</label>
          <input 
            v-model="form.city"
            type="text" 
            placeholder="Введите город"
          >
        </div>
        
        <div class="form-group">
          <label>Страна</label>
          <input 
            v-model="form.country"
            type="text" 
            placeholder="Введите страну"
          >
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label>Заезд</label>
          <input 
            v-model="form.check_in"
            type="date" 
            :min="today"
          >
        </div>
        
        <div class="form-group">
          <label>Выезд</label>
          <input 
            v-model="form.check_out"
            type="date" 
            :min="minCheckoutDate"
          >
        </div>
        
        <div class="form-group">
          <label>Гости</label>
          <input 
            v-model="form.guests"
            type="number" 
            min="1"
            placeholder="Количество"
          >
        </div>
      </div>
      
      <button type="submit" class="search-btn">
        🔍 Найти отели
      </button>
    </form>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'HotelSearchWidget',
  emits: ['search'],
  setup(props, { emit }) {
    const form = ref({
      city: '',
      country: '',
      check_in: '',
      check_out: '',
      guests: 1
    })

    const today = computed(() => {
      return new Date().toISOString().split('T')[0]
    })

    const minCheckoutDate = computed(() => {
      return form.value.check_in || today.value
    })

    const handleSubmit = () => {
      // Очищаем пустые поля
      const searchParams = Object.fromEntries(
        Object.entries(form.value).filter(([_, value]) => value !== '')
      )
      emit('search', searchParams)
    }

    return {
      form,
      today,
      minCheckoutDate,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.search-widget {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
}

.search-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 5px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  align-self: center;
}

.search-btn:hover {
  background: #c0392b;
}
</style>