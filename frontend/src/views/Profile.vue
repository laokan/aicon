<template>
  <div class="page">
    <div class="page-header">
      <div class="flex-between items-center">
        <div>
          <h1 class="page-title">个人资料</h1>
          <p class="page-description">管理您的账户设置和偏好</p>
        </div>
        <div class="profile-summary">
          <div class="flex items-center">
            <el-avatar :size="48" :src="authStore.user?.avatar_url" class="profile-avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <div class="ml-3">
              <p class="font-semibold text-primary">
                {{ authStore.user?.display_name || authStore.user?.username }}
              </p>
              <p class="text-sm text-secondary">
                {{ authStore.user?.email }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="profile-content">
      <el-row :gutter="24">
        <!-- 用户信息卡片 -->
        <el-col :xs="24" :lg="8">
          <div class="profile-card hover-lift" style="animation: slide-up 0.6s ease-out 0.1s both">
            <div class="profile-header">
              <div class="profile-avatar-container">
                <el-avatar :size="100" :src="authStore.user?.avatar_url">
                  <el-icon size="50"><User /></el-icon>
                </el-avatar>
                <div class="avatar-badge">
                  <el-tag :type="authStore.user?.is_verified ? 'success' : 'warning'" size="small">
                    <el-icon class="mr-1">
                      <Check v-if="authStore.user?.is_verified" />
                      <Warning v-else />
                    </el-icon>
                    {{ authStore.user?.is_verified ? 'Verified' : 'Unverified' }}
                  </el-tag>
                </div>
              </div>
              <div class="profile-info">
                <h3 class="profile-name">{{ authStore.user?.display_name || authStore.user?.username }}</h3>
                <p class="profile-email">{{ authStore.user?.email }}</p>
                <div class="profile-meta">
                  <div class="meta-item">
                    <el-icon><Calendar /></el-icon>
                    <span>Joined {{ formatDate(authStore.user?.created_at) }}</span>
                  </div>
                  <div class="meta-item">
                    <el-icon><Clock /></el-icon>
                    <span>{{ authStore.user?.timezone || 'Asia/Shanghai' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-col>

        <!-- 设置表单 -->
        <el-col :xs="24" :lg="16">
          <div class="settings-section">
            <!-- 个人信息设置 -->
            <div class="card hover-lift" style="animation: slide-up 0.6s ease-out 0.2s both">
              <div class="card-header">
                <div class="flex items-center">
                  <div class="card-icon" style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));">
                    <el-icon size="20"><User /></el-icon>
                  </div>
                  <div class="ml-3">
                    <h3>个人信息</h3>
                    <p class="text-sm text-secondary">更新您的个人信息</p>
                  </div>
                </div>
              </div>
              <div class="card-body">
                <el-form
                  ref="profileFormRef"
                  :model="profileForm"
                  :rules="profileRules"
                  label-position="top"
                  @submit.prevent="updateProfile"
                >
                  <el-row :gutter="16">
                    <el-col :span="12">
                      <el-form-item label="用户名" prop="username">
                        <el-input v-model="profileForm.username" disabled>
                          <template #prefix>
                            <el-icon><User /></el-icon>
                          </template>
                        </el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="邮箱" prop="email">
                        <el-input v-model="profileForm.email" disabled>
                          <template #prefix>
                            <el-icon><Message /></el-icon>
                          </template>
                        </el-input>
                      </el-form-item>
                    </el-col>
                  </el-row>

                  <el-form-item label="显示名称" prop="display_name">
                    <el-input v-model="profileForm.display_name" placeholder="请输入显示名称">
                      <template #prefix>
                        <el-icon><User /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="头像链接" prop="avatar_url">
                    <el-input v-model="profileForm.avatar_url" placeholder="请输入头像URL">
                      <template #prefix>
                        <el-icon><Picture /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-row :gutter="16">
                    <el-col :span="12">
                      <el-form-item label="时区" prop="timezone">
                        <el-select v-model="profileForm.timezone" style="width: 100%" placeholder="选择时区">
                          <el-option label="亚洲/上海" value="Asia/Shanghai" />
                          <el-option label="UTC" value="UTC" />
                          <el-option label="美国/纽约" value="America/New_York" />
                          <el-option label="欧洲/伦敦" value="Europe/London" />
                          <el-option label="亚洲/东京" value="Asia/Tokyo" />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="语言" prop="language">
                        <el-select v-model="profileForm.language" style="width: 100%" placeholder="选择语言">
                          <el-option label="中文" value="zh-CN" />
                          <el-option label="English" value="en-US" />
                          <el-option label="日本語" value="ja-JP" />
                        </el-select>
                      </el-form-item>
                    </el-col>
                  </el-row>

                  <el-form-item>
                    <el-button
                      type="primary"
                      size="large"
                      :loading="loading"
                      @click="updateProfile"
                      class="modern-button"
                    >
                      <el-icon class="mr-2"><Check /></el-icon>
                      Update Profile
                    </el-button>
                  </el-form-item>
                </el-form>
              </div>
            </div>

            <!-- 密码修改 -->
            <div class="card hover-lift" style="animation: slide-up 0.6s ease-out 0.3s both">
              <div class="card-header">
                <div class="flex items-center">
                  <div class="card-icon" style="background: linear-gradient(135deg, var(--warning-color), var(--warning-dark));">
                    <el-icon size="20"><Lock /></el-icon>
                  </div>
                  <div class="ml-3">
                    <h3>修改密码</h3>
                    <p class="text-sm text-secondary">更新您的账户密码</p>
                  </div>
                </div>
              </div>
              <div class="card-body">
                <el-form
                  ref="passwordFormRef"
                  :model="passwordForm"
                  :rules="passwordRules"
                  label-position="top"
                  @submit.prevent="changePassword"
                >
                  <el-form-item label="当前密码" prop="current_password">
                    <el-input
                      v-model="passwordForm.current_password"
                      type="password"
                      placeholder="请输入当前密码"
                      show-password
                    >
                      <template #prefix>
                        <el-icon><Lock /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="新密码" prop="new_password">
                    <el-input
                      v-model="passwordForm.new_password"
                      type="password"
                      placeholder="请输入新密码"
                      show-password
                    >
                      <template #prefix>
                        <el-icon><Key /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="确认新密码" prop="confirm_password">
                    <el-input
                      v-model="passwordForm.confirm_password"
                      type="password"
                      placeholder="请确认新密码"
                      show-password
                    >
                      <template #prefix>
                        <el-icon><Key /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item>
                    <el-button
                      type="warning"
                      size="large"
                      :loading="loading"
                      @click="changePassword"
                      class="modern-button"
                    >
                      <el-icon class="mr-2"><Lock /></el-icon>
                      Change Password
                    </el-button>
                  </el-form-item>
                </el-form>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  User,
  Check,
  Warning,
  Calendar,
  Clock,
  Message,
  Picture,
  Lock,
  Key
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const loading = ref(false)

const profileFormRef = ref()
const passwordFormRef = ref()

const profileForm = reactive({
  username: '',
  email: '',
  display_name: '',
  avatar_url: '',
  timezone: 'Asia/Shanghai',
  language: 'zh-CN'
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const profileRules = {
  display_name: [
    { max: 100, message: 'Display name cannot exceed 100 characters', trigger: 'blur' }
  ],
  avatar_url: [
    { max: 500, message: 'Avatar URL cannot exceed 500 characters', trigger: 'blur' }
  ]
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('Please confirm new password'))
  } else if (value !== passwordForm.new_password) {
    callback(new Error('Passwords do not match'))
  } else {
    callback()
  }
}

const passwordRules = {
  current_password: [
    { required: true, message: 'Please enter current password', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: 'Please enter new password', trigger: 'blur' },
    { min: 8, max: 128, message: 'Password must be 8-128 characters', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const formatDate = (dateString) => {
  if (!dateString) return 'Recently'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long'
  })
}

const initializeForm = () => {
  if (authStore.user) {
    profileForm.username = authStore.user.username || ''
    profileForm.email = authStore.user.email || ''
    profileForm.display_name = authStore.user.display_name || ''
    profileForm.avatar_url = authStore.user.avatar_url || ''
    profileForm.timezone = authStore.user.timezone || 'Asia/Shanghai'
    profileForm.language = authStore.user.language || 'zh-CN'
  }
}

const updateProfile = async () => {
  if (!profileFormRef.value) return

  try {
    await profileFormRef.value.validate()
    loading.value = true

    await authStore.updateProfile(profileForm)
    ElMessage.success('Profile updated successfully')
  } catch (error) {
    console.error('Profile update failed:', error)
  } finally {
    loading.value = false
  }
}

const changePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
    loading.value = true

    await authStore.changePassword({
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password
    })

    ElMessage.success('Password changed successfully')

    // Clear password form
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
    passwordFormRef.value.resetFields()
  } catch (error) {
    console.error('Password change failed:', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await authStore.getCurrentUser()
  initializeForm()
})
</script>

<style scoped>
.profile-content {
  padding: var(--space-xl);
}

/* 用户信息卡片 */
.profile-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-2xl);
  padding: var(--space-2xl);
  box-shadow: var(--shadow-base);
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
  height: fit-content;
}

.profile-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent,
    rgba(255,255,255,0.1),
    transparent
  );
  opacity: 0;
  transition: opacity var(--transition-base);
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl), var(--shadow-colored);
  border-color: var(--primary-lighter);
}

.profile-card:hover::before {
  opacity: 1;
}

.profile-header {
  text-align: center;
}

.profile-avatar-container {
  position: relative;
  display: inline-block;
  margin-bottom: var(--space-xl);
}

.profile-avatar-container .el-avatar {
  border: 4px solid var(--bg-primary);
  box-shadow: var(--shadow-lg);
  position: relative;
}

.profile-avatar-container .el-avatar::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
  border-radius: var(--radius-full);
  z-index: -1;
  opacity: 0.8;
}

.avatar-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  transform: translate(20%, 20%);
}

.profile-info {
  text-align: center;
}

.profile-name {
  font-size: var(--text-xl);
  font-weight: 700;
  margin: 0 0 var(--space-sm) 0;
  color: var(--text-primary);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.profile-email {
  font-size: var(--text-base);
  color: var(--text-secondary);
  margin: 0 0 var(--space-lg) 0;
}

.profile-meta {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.meta-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  font-size: var(--text-sm);
  color: var(--text-tertiary);
}

.meta-item .el-icon {
  color: var(--primary-color);
}

/* 设置区域 */
.settings-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.card-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: var(--shadow-md);
}

/* 现代化按钮 */
.modern-button {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  border: none;
  border-radius: var(--radius-lg);
  font-weight: 600;
  padding: var(--space-md) var(--space-xl);
  transition: all var(--transition-base);
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.modern-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent,
    rgba(255,255,255,0.2),
    transparent
  );
  transition: left var(--transition-base);
}

.modern-button:hover::before {
  left: 100%;
}

.modern-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), var(--shadow-colored);
}

/* 表单样式 */
:deep(.el-form-item__label) {
  font-weight: 600;
  color: var(--text-primary);
}

:deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  border: 2px solid var(--border-primary);
  background: var(--bg-primary);
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

:deep(.el-input__wrapper:hover) {
  border-color: var(--primary-lighter);
  box-shadow: var(--shadow-md);
}

:deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

:deep(.el-select .el-input .el-input__wrapper) {
  cursor: pointer;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  border: none;
  border-radius: var(--radius-lg);
  font-weight: 600;
  box-shadow: var(--shadow-md);
}

:deep(.el-button--warning) {
  background: linear-gradient(135deg, var(--warning-color), var(--warning-dark));
  border: none;
  border-radius: var(--radius-lg);
  font-weight: 600;
  box-shadow: var(--shadow-md);
}

/* 页面头部用户摘要 */
.profile-summary {
  background: var(--bg-secondary);
  padding: var(--space-lg) var(--space-xl);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-primary);
}

.profile-avatar {
  box-shadow: var(--shadow-md);
  border: 2px solid var(--bg-primary);
}

/* 动画 */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-content {
    padding: var(--space-lg);
  }

  .profile-card {
    padding: var(--space-xl);
    margin-bottom: var(--space-lg);
  }

  .profile-avatar-container {
    margin-bottom: var(--space-lg);
  }

  .profile-meta {
    gap: var(--space-xs);
  }

  .meta-item {
    font-size: var(--text-xs);
  }

  .settings-section {
    gap: var(--space-lg);
  }

  .card {
    margin-bottom: var(--space-lg);
  }

  .profile-summary {
    padding: var(--space-md);
    margin-top: var(--space-lg);
  }

  .profile-summary .flex {
    flex-direction: column;
    text-align: center;
  }

  .profile-summary .ml-3 {
    margin-left: 0 !important;
    margin-top: var(--space-sm);
  }
}

@media (max-width: 480px) {
  .profile-content {
    padding: var(--space-md);
  }

  .profile-card {
    padding: var(--space-lg);
  }

  .profile-name {
    font-size: var(--text-lg);
  }

  .profile-email {
    font-size: var(--text-sm);
  }

  .card-icon {
    width: 36px;
    height: 36px;
  }

  .card-icon .el-icon {
    font-size: 16px;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .profile-card,
  .profile-summary {
    background: var(--bg-dark);
    border-color: var(--gray-700);
  }

  .profile-card:hover {
    background: var(--gray-800);
  }
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .profile-card,
  .profile-summary {
    border-width: 2px;
  }

  .profile-card:hover {
    border-width: 3px;
  }
}

/* 现代化交互动效 */
.profile-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 0.1) 0%,
    rgba(139, 92, 246, 0.1) 100%);
  border-radius: var(--radius-2xl);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.profile-card:hover::before {
  opacity: 1;
}

.profile-card:hover {
  transform: translateY(-8px);
  box-shadow:
    var(--shadow-xl),
    var(--shadow-colored),
    0 20px 40px rgba(99, 102, 241, 0.1);
}

/* 头像动画 */
.profile-avatar-container:hover .profile-avatar {
  animation: avatar-pulse 2s ease-in-out infinite;
}

@keyframes avatar-pulse {
  0%, 100% {
    transform: scale(1);
    border-color: var(--primary-color);
  }
  50% {
    transform: scale(1.05);
    border-color: var(--secondary-color);
  }
}

/* 卡片磁吸效果 */
.card {
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg,
    var(--primary-color),
    var(--secondary-color),
    var(--success-color),
    var(--warning-color));
  border-radius: var(--radius-xl);
  z-index: -1;
  opacity: 0;
  transition: opacity var(--transition-base);
  animation: border-flow 3s linear infinite;
}

@keyframes border-flow {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.card:hover::before {
  opacity: 1;
}

/* 表单输入现代化 */
:deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  border: 2px solid var(--border-primary);
  background: var(--bg-primary);
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}

:deep(.el-input__wrapper::before) {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent,
    rgba(99, 102, 241, 0.1),
    transparent
  );
  transition: left var(--transition-base);
}

:deep(.el-input__wrapper:hover::before) {
  left: 100%;
}

:deep(.el-input__wrapper:hover) {
  border-color: var(--primary-lighter);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

:deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow:
    0 0 0 4px rgba(99, 102, 241, 0.1),
    var(--shadow-lg);
  transform: translateY(-2px);
}

/* 按钮现代化 */
.modern-button {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  border: none;
  border-radius: var(--radius-lg);
  font-weight: 600;
  padding: var(--space-md) var(--space-xl);
  transition: all var(--transition-base);
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.modern-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent,
    rgba(255,255,255,0.2),
    transparent
  );
  transition: left var(--transition-base);
}

.modern-button:hover::before {
  left: 100%;
}

.modern-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), 0 10px 25px rgba(99, 102, 241, 0.3);
}

.modern-button:active {
  transform: translateY(0);
}

/* 选择框现代化 */
:deep(.el-select .el-input .el-input__wrapper) {
  cursor: pointer;
}

:deep(.el-select .el-input .el-input__wrapper:hover) {
  border-color: var(--primary-lighter);
}

:deep(.el-select-dropdown) {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border-primary);
}

:deep(.el-select-dropdown__item) {
  transition: all var(--transition-base);
}

:deep(.el-select-dropdown__item:hover) {
  background: var(--primary-color);
  color: white;
  transform: translateX(4px);
}

/* 悬浮效果 */
.hover-lift {
  transition: all var(--transition-base);
  position: relative;
}

.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.hover-lift:hover::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.05) 100%);
  border-radius: inherit;
  pointer-events: none;
}

/* 数据展示动画 */
.profile-name {
  animation: slide-in-left 0.6s ease-out;
}

.profile-email {
  animation: slide-in-left 0.6s ease-out 0.1s both;
}

@keyframes slide-in-left {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 成功状态动画 */
:deep(.el-form-item.is-success .el-input__wrapper) {
  animation: success-glow 1s ease-out;
}

@keyframes success-glow {
  0% {
    box-shadow: var(--shadow-sm);
  }
  50% {
    box-shadow: 0 0 15px rgba(103, 194, 58, 0.5);
  }
  100% {
    box-shadow: var(--shadow-sm);
  }
}

/* 加载状态 */
:deep(.el-button.is-loading) {
  pointer-events: none;
}

:deep(.el-loading-spinner) {
  margin-right: var(--space-sm);
}

/* 减少动画偏好支持 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>