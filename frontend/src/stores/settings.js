import { defineStore } from 'pinia'
import { ref } from 'vue'
import { get, post, put, del } from '@/services/api'

export const useSettingsStore = defineStore('settings', () => {
  const apiConfigs = ref([])
  const usageStats = ref(null)
  const loading = ref(false)

  // 获取API配置列表
  const fetchApiConfigs = async () => {
    loading.value = true
    try {
      const configs = await get('/api-configs')
      apiConfigs.value = configs
      return configs
    } finally {
      loading.value = false
    }
  }

  // 创建API配置
  const createApiConfig = async (configData) => {
    const config = await post('/api-configs', configData)
    apiConfigs.value.unshift(config)
    return config
  }

  // 更新API配置
  const updateApiConfig = async (id, configData) => {
    const config = await put(`/api-configs/${id}`, configData)
    const index = apiConfigs.value.findIndex(c => c.id === id)
    if (index !== -1) {
      apiConfigs.value[index] = config
    }
    return config
  }

  // 删除API配置
  const deleteApiConfig = async (id) => {
    await del(`/api-configs/${id}`)
    apiConfigs.value = apiConfigs.value.filter(c => c.id !== id)
  }

  // 验证API配置
  const validateApiConfig = async (id) => {
    const result = await post(`/api-configs/${id}/validate`)
    return result
  }

  // 获取用量统计
  const fetchUsageStats = async () => {
    const stats = await get('/api-configs/usage-stats')
    usageStats.value = stats
    return stats
  }

  return {
    apiConfigs,
    usageStats,
    loading,
    fetchApiConfigs,
    createApiConfig,
    updateApiConfig,
    deleteApiConfig,
    validateApiConfig,
    fetchUsageStats
  }
})