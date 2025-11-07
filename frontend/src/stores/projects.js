import { defineStore } from 'pinia'
import { ref } from 'vue'
import { get, post, put, del } from '@/services/api'

export const useProjectStore = defineStore('projects', () => {
  const projects = ref([])
  const currentProject = ref(null)
  const loading = ref(false)
  const pagination = ref({
    page: 1,
    limit: 20,
    total: 0,
    totalPages: 0
  })

  // 获取项目列表
  const fetchProjects = async (params = {}) => {
    loading.value = true
    try {
      const response = await get('/projects', { params })
      projects.value = response.items
      pagination.value = response.pagination
      return response
    } finally {
      loading.value = false
    }
  }

  // 获取项目详情
  const fetchProject = async (id) => {
    loading.value = true
    try {
      const project = await get(`/projects/${id}`)
      currentProject.value = project
      return project
    } finally {
      loading.value = false
    }
  }

  // 创建项目
  const createProject = async (projectData) => {
    const project = await post('/projects', projectData)
    projects.value.unshift(project)
    return project
  }

  // 更新项目
  const updateProject = async (id, projectData) => {
    const project = await put(`/projects/${id}`, projectData)
    const index = projects.value.findIndex(p => p.id === id)
    if (index !== -1) {
      projects.value[index] = project
    }
    if (currentProject.value?.id === id) {
      currentProject.value = project
    }
    return project
  }

  // 删除项目
  const deleteProject = async (id) => {
    await del(`/projects/${id}`)
    projects.value = projects.value.filter(p => p.id !== id)
    if (currentProject.value?.id === id) {
      currentProject.value = null
    }
  }

  return {
    projects,
    currentProject,
    loading,
    pagination,
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject
  }
})