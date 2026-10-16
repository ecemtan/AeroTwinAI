import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  // During development the browser talks to Vite (port 5173), which forwards
  // API calls to FastAPI. Override the target with VITE_API_PROXY_TARGET.
  const apiTarget = env.VITE_API_PROXY_TARGET || 'http://127.0.0.1:8000'

  return {
    plugins: [react()],
    server: {
      port: 5173,
      strictPort: true,
      proxy: {
        '/api': apiTarget,
        '/health': apiTarget,
      },
    },
  }
})
