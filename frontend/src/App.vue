<template>
  <div id="app">
    <NavBar v-if="isAuthenticated" />
    <main :class="{ 'with-navbar': isAuthenticated }">
      <router-view />
    </main>
    <Footer v-if="isAuthenticated" />
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'
import NavBar from './components/common/NavBar.vue'
import Footer from './components/common/Footer.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    Footer
  },
  setup() {
    const authStore = useAuthStore()
    
    return {
      isAuthenticated: computed(() => authStore.isAuthenticated)
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
  padding: 20px;
}

main.with-navbar {
  padding-top: 80px;
}
</style>