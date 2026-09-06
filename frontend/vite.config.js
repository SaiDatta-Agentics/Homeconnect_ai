import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy: {
    '/auth': 'http://127.0.0.1:8000', '/chat': 'http://127.0.0.1:8000', '/visits': 'http://127.0.0.1:8000',
    '/enquiries': 'http://127.0.0.1:8000', '/properties': 'http://127.0.0.1:8000',
    '/notifications': 'http://127.0.0.1:8000', '/activity': 'http://127.0.0.1:8000', '/health': 'http://127.0.0.1:8000',
  }}
})
