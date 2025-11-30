import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/hotel-booking-system',
  build: {
    outDir: 'dist'
  }
})