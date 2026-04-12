import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  // Загружаем env переменные based on mode
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [vue()],
    server: {
      host: '0.0.0.0',
      port: 5173
    },
    // Конфигурация для продакшена
    build: {
      outDir: 'dist',
      sourcemap: false,
      chunkSizeWarningLimit: 1600
    },
    // Определяем глобальные переменные
    define: {
      __APP_ENV__: JSON.stringify(env.APP_ENV),
    }
  }
})