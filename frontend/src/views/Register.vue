<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-header">
        <h1>AICG 平台</h1>
        <p>AI内容分发平台</p>
      </div>

      <el-card class="register-card">
        <template #header>
          <h2>注册</h2>
        </template>

        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
            />
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              type="email"
              placeholder="请输入邮箱"
              size="large"
              :prefix-icon="Message"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请确认密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="authStore.loading"
              @click="handleRegister"
              style="width: 100%"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>

        <div class="register-footer">
          <p>已有账户？ <router-link to="/login">立即登录</router-link></p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const registerFormRef = ref()

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('Please confirm password'))
  } else if (value !== registerForm.password) {
    callback(new Error('Passwords do not match'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: 'Please enter username', trigger: 'blur' },
    { min: 3, max: 50, message: 'Username must be 3-50 characters', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Please enter email', trigger: 'blur' },
    { type: 'email', message: 'Please enter valid email', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' },
    { min: 8, max: 128, message: 'Password must be 8-128 characters', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    await registerFormRef.value.validate()

    await authStore.register({
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password
    })

    ElMessage.success('Registration successful! Please login.')

    // Redirect to login page
    router.push({ name: 'Login' })

  } catch (error) {
    // Error is handled by the auth store
    console.error('Registration failed:', error)
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg,
    #667eea 0%,
    #764ba2 50%,
    #6366f1 100%
  );
  padding: var(--space-lg);
  position: relative;
  overflow: hidden;
}

.register-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(139, 92, 246, 0.2) 0%, transparent 50%);
  animation: float-bg 20s ease-in-out infinite;
}

@keyframes float-bg {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  33% { transform: translateY(-20px) rotate(120deg); }
  66% { transform: translateY(-10px) rotate(240deg); }
}

.register-container {
  width: 100%;
  max-width: 440px;
  position: relative;
  z-index: 1;
}

.register-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
  color: white;
  animation: slide-down 0.8s ease-out;
}

@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-header h1 {
  font-size: var(--text-4xl);
  font-weight: 800;
  margin: 0 0 var(--space-sm) 0;
  letter-spacing: -0.02em;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-header p {
  font-size: var(--text-lg);
  margin: 0;
  opacity: 0.95;
  font-weight: 500;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.register-card {
  border-radius: var(--radius-2xl);
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: scale-up 0.6s ease-out 0.2s both;
  overflow: hidden;
}

@keyframes scale-up {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.register-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg,
    transparent,
    rgba(99, 102, 241, 0.8),
    transparent
  );
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  50%, 100% { left: 100%; }
}

.register-card :deep(.el-card__header) {
  text-align: center;
  padding: var(--space-2xl) var(--space-xl) var(--space-lg);
  background: transparent;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
}

.register-card :deep(.el-card__header) h2 {
  margin: 0;
  font-weight: 700;
  font-size: var(--text-2xl);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-card :deep(.el-card__body) {
  padding: var(--space-xl) var(--space-2xl);
}

/* 现代化输入框 */
.register-card :deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  border: 2px solid var(--border-primary);
  background: var(--bg-primary);
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.register-card :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-lighter);
  box-shadow: var(--shadow-md);
}

.register-card :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.register-card :deep(.el-input__inner) {
  font-size: var(--text-base);
  padding: var(--space-md) var(--space-lg);
}

.register-card :deep(.el-input__prefix-inner) {
  color: var(--text-tertiary);
}

/* 现代化按钮 */
.register-card :deep(.el-button--primary) {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  border: none;
  border-radius: var(--radius-lg);
  font-weight: 600;
  font-size: var(--text-base);
  padding: var(--space-md) var(--space-xl);
  transition: all var(--transition-base);
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.register-card :deep(.el-button--primary)::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent,
    rgba(255,255,255,0.3),
    transparent
  );
  transition: left var(--transition-base);
}

.register-card :deep(.el-button--primary:hover)::before {
  left: 100%;
}

.register-card :deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), 0 10px 25px rgba(99, 102, 241, 0.3);
}

.register-card :deep(.el-button--primary:active) {
  transform: translateY(0);
}

.register-footer {
  text-align: center;
  margin-top: var(--space-lg);
  padding-top: var(--space-lg);
  border-top: 1px solid rgba(99, 102, 241, 0.1);
  animation: fade-in 0.8s ease-out 0.4s both;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-footer p {
  margin: 0;
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.register-footer a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  transition: all var(--transition-base);
  position: relative;
}

.register-footer a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--primary-color);
  transition: width var(--transition-base);
}

.register-footer a:hover {
  color: var(--primary-hover);
}

.register-footer a:hover::after {
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .register-page {
    padding: var(--space-md);
  }

  .register-container {
    max-width: 100%;
  }

  .register-header h1 {
    font-size: var(--text-3xl);
  }

  .register-header p {
    font-size: var(--text-base);
  }

  .register-card :deep(.el-card__body) {
    padding: var(--space-lg);
  }

  .register-card :deep(.el-button--primary) {
    width: 100%;
  }
}

/* 加载状态 */
.register-card :deep(.el-button.is-loading) {
  pointer-events: none;
}

.register-card :deep(.el-loading-spinner) {
  margin-right: var(--space-sm);
}

/* 错误状态动画 */
.register-card :deep(.el-form-item.is-error .el-input__wrapper) {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
</style>