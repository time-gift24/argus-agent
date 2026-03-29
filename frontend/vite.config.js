import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [
      vue(),
      tailwindcss()
    ],
    resolve: {
      alias: {
        '@': '/src'
      }
    },
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: env.API_TARGET || 'http://localhost:8000',
          changeOrigin: true,
        }
      }
    }
  }
})
