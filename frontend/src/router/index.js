import { createRouter, createWebHistory } from 'vue-router'
import { setupAuthGuard } from '@/router/guards'

// 布局组件
const MainLayout = () => import('@/components/layout/MainLayout.vue')

// 页面组件
const Login = () => import('@/views/Login.vue')
const Register = () => import('@/views/Register.vue')
const Dashboard = () => import('@/views/Dashboard.vue')
const Projects = () => import('@/views/Projects.vue')
const ContentStudio = () => import('@/views/studio/ContentStudio.vue')
const DirectorEngine = () => import('@/views/studio/DirectorEngine.vue')
const GenerationSettings = () => import('@/views/GenerationSettings.vue')
const Publish = () => import('@/views/Publish.vue')
const APIKeys = () => import('@/views/APIKeys.vue')
const Settings = () => import('@/views/Settings.vue')

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'DashboardPage',
        component: Dashboard
      }
    ]
  },
  {
    path: '/projects',
    name: 'Projects',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'ProjectsPage',
        component: Projects
      }
    ]
  },
  {
    path: '/content-studio/:projectId/:chapterId?',
    name: 'ContentStudio',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'ContentStudioPage',
        component: ContentStudio
      }
    ]
  },
  {
    path: '/director-engine/:projectId/:chapterId',
    name: 'DirectorEngine',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'DirectorEnginePage',
        component: DirectorEngine
      }
    ]
  },
  {
    path: '/generation',
    name: 'Generation',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'GenerationPage',
        component: () => import('@/views/VideoTasks.vue')
      }
    ]
  },
  {
    path: '/generation/settings',
    name: 'GenerationSettings',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'GenerationSettingsPage',
        component: GenerationSettings
      }
    ]
  },
  {
    path: '/publish',
    name: 'Publish',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'PublishPage',
        component: Publish
      }
    ]
  },
  {
    path: '/api-keys',
    name: 'APIKeys',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'APIKeysPage',
        component: APIKeys
      }
    ]
  },
  {
    path: '/bgm-management',
    name: 'BGMManagement',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'BGMManagementPage',
        component: () => import('@/views/BGMManagement.vue')
      }
    ]
  },
  {
    path: '/settings',
    name: 'Settings',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'SettingsPage',
        component: Settings
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 设置路由守卫
setupAuthGuard(router)

export default router