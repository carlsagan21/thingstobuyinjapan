import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/thingstobuyinjapan/',
  build: {
    rollupOptions: {
      input: {
        main: './index.html',
        ko: './ko/index.html',
        ja: './ja/index.html',
      },
    },
  },
})
