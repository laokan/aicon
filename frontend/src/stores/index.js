import { createPinia } from 'pinia'

const pinia = createPinia()

export default pinia

// 导出所有store
export { useAuthStore } from './auth'
export { useProjectStore } from './projects'
export { useGenerationStore } from './generations'
export { useSettingsStore } from './settings'