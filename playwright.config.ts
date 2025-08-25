import { defineConfig } from '@playwright/test'

export default defineConfig({
  webServer: {
    command: 'npm --prefix frontend run dev',
    port: 5173,
    reuseExistingServer: true,
  },
  testDir: 'frontend/tests',
})
