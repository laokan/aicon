<template>
  <div class="page">
    <div class="page-header">
      <div class="flex-between items-center">
        <div>
          <h1 class="page-title">仪表板</h1>
          <p class="page-description">欢迎回来！这是您的内容创作概览</p>
        </div>
        <div class="user-welcome">
          <el-avatar :size="48" :src="authStore.user?.avatar_url">
            <el-icon><User /></el-icon>
          </el-avatar>
          <div class="ml-3">
            <p class="font-semibold text-primary">
              {{ authStore.user?.display_name || authStore.user?.username }}
            </p>
            <p class="text-sm text-secondary">
              准备开始创作精彩内容
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- 统计卡片 -->
      <el-row :gutter="24" class="mb-8">
        <el-col :xs="24" :sm="12" :md="6">
          <div class="stat-card hover-lift modern-gradient-1" style="animation: slide-up 0.6s ease-out 0.1s both">
            <div class="stat-card-icon">
              <el-icon size="24"><Folder /></el-icon>
            </div>
            <div class="stat-card-content">
              <h3 class="stat-number">0</h3>
              <p class="stat-label">项目</p>
              <div class="stat-trend">
                <el-icon><TrendCharts /></el-icon>
                <span class="ml-1 text-sm">开始创作</span>
              </div>
            </div>
          </div>
        </el-col>

        <el-col :xs="24" :sm="12" :md="6">
          <div class="stat-card hover-lift modern-gradient-2" style="animation: slide-up 0.6s ease-out 0.2s both">
            <div class="stat-card-icon">
              <el-icon size="24"><VideoPlay /></el-icon>
            </div>
            <div class="stat-card-content">
              <h3 class="stat-number">0</h3>
              <p class="stat-label">任务</p>
              <div class="stat-trend">
                <el-icon><Timer /></el-icon>
                <span class="ml-1 text-sm">暂无活动任务</span>
              </div>
            </div>
          </div>
        </el-col>

        <el-col :xs="24" :sm="12" :md="6">
          <div class="stat-card hover-lift modern-gradient-3" style="animation: slide-up 0.6s ease-out 0.3s both">
            <div class="stat-card-icon">
              <el-icon size="24"><Promotion /></el-icon>
            </div>
            <div class="stat-card-content">
              <h3 class="stat-number">0</h3>
              <p class="stat-label">视频</p>
              <div class="stat-trend">
                <el-icon><Share /></el-icon>
                <span class="ml-1 text-sm">准备发布</span>
              </div>
            </div>
          </div>
        </el-col>

        <el-col :xs="24" :sm="12" :md="6">
          <div class="stat-card hover-lift modern-gradient-4" style="animation: slide-up 0.6s ease-out 0.4s both">
            <div class="stat-card-icon">
              <el-icon size="24"><Money /></el-icon>
            </div>
            <div class="stat-card-content">
              <h3 class="stat-number">¥0</h3>
              <p class="stat-label">总成本</p>
              <div class="stat-trend">
                <el-icon><TrendCharts /></el-icon>
                <span class="ml-1 text-sm">暂无支出</span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>

      <!-- 快速操作区域 -->
      <el-row :gutter="24" class="mb-8">
        <el-col :span="24">
          <div class="card hover-lift" style="animation: slide-up 0.6s ease-out 0.5s both">
            <div class="card-header">
              <h3>快速开始</h3>
              <p class="text-sm text-secondary">开始您的内容创作之旅</p>
            </div>
            <div class="card-body">
              <div class="quick-actions">
                <div class="action-item" @click="$router.push('/projects')">
                  <div class="action-icon" style="background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));">
                    <el-icon size="20"><Folder /></el-icon>
                  </div>
                  <div class="action-content">
                    <h4>项目管理</h4>
                    <p class="text-sm text-secondary">创建和管理您的内容项目</p>
                  </div>
                  <el-icon class="action-arrow"><ArrowRight /></el-icon>
                </div>

                <div class="action-item" @click="$router.push('/generation')">
                  <div class="action-icon" style="background: linear-gradient(135deg, var(--success-color), var(--success-dark));">
                    <el-icon size="20"><VideoPlay /></el-icon>
                  </div>
                  <div class="action-content">
                    <h4>视频生成</h4>
                    <p class="text-sm text-secondary">将文本转换为引人入胜的视频</p>
                  </div>
                  <el-icon class="action-arrow"><ArrowRight /></el-icon>
                </div>

                <div class="action-item" @click="$router.push('/publish')">
                  <div class="action-icon" style="background: linear-gradient(135deg, var(--warning-color), var(--warning-dark));">
                    <el-icon size="20"><Promotion /></el-icon>
                  </div>
                  <div class="action-content">
                    <h4>内容分发</h4>
                    <p class="text-sm text-secondary">在各平台分享您的内容</p>
                  </div>
                  <el-icon class="action-arrow"><ArrowRight /></el-icon>
                </div>

                <div class="action-item" @click="$router.push('/settings')">
                  <div class="action-icon" style="background: linear-gradient(135deg, var(--info-color), var(--info-dark));">
                    <el-icon size="20"><Setting /></el-icon>
                  </div>
                  <div class="action-content">
                    <h4>设置</h4>
                    <p class="text-sm text-secondary">配置AI服务和偏好设置</p>
                  </div>
                  <el-icon class="action-arrow"><ArrowRight /></el-icon>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>

      <!-- 最近活动 -->
      <el-row :gutter="24">
        <el-col :span="24">
          <div class="card" style="animation: slide-up 0.6s ease-out 0.6s both">
            <div class="card-header">
              <h3>最近活动</h3>
              <p class="text-sm text-secondary">您最新的内容创作活动</p>
            </div>
            <div class="card-body">
              <div class="empty-state">
                <div class="empty-icon">
                  <el-icon size="48"><Document /></el-icon>
                </div>
                <h4>暂无活动</h4>
                <p class="text-secondary">开始创作内容以查看您的活动记录</p>
                <el-button type="primary" @click="$router.push('/projects')" class="mt-4">
                  创建您的第一个项目
                </el-button>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import {
  User,
  Folder,
  VideoPlay,
  Promotion,
  Money,
  TrendCharts,
  Timer,
  Share,
  Setting,
  Document,
  ArrowRight
} from '@element-plus/icons-vue'

const authStore = useAuthStore()
</script>

<style scoped>
.dashboard-content {
  padding: var(--space-xl);
}

/* 统计卡片样式 */
.stat-card {
  background: var(--bg-primary);
  border-radius: var(--radius-2xl);
  padding: var(--space-2xl);
  box-shadow: var(--shadow-base);
  border: 1px solid var(--border-primary);
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-card::before {
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

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl), var(--shadow-colored);
  border-color: var(--primary-lighter);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-card-icon {
  width: 60px;
  height: 60px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

/* 现代渐变类 */
.modern-gradient-1 .stat-card-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.modern-gradient-2 .stat-card-icon {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.modern-gradient-3 .stat-card-icon {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.modern-gradient-4 .stat-card-icon {
  background: linear-gradient(135deg, #fa709a, #fee140);
}

.stat-card-icon::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
  animation: float-icon 3s ease-in-out infinite;
}

@keyframes float-icon {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-3px) rotate(180deg); }
}

.stat-card-content {
  flex: 1;
  margin-left: var(--space-xl);
}

.stat-number {
  font-size: var(--text-3xl);
  font-weight: 800;
  margin: 0 0 var(--space-xs) 0;
  color: var(--text-primary);
  line-height: 1;
}

.stat-label {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 var(--space-sm) 0;
}

.stat-trend {
  display: flex;
  align-items: center;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
}

/* 快速操作区域 */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-lg);
}

.action-item {
  display: flex;
  align-items: center;
  padding: var(--space-xl);
  background: var(--bg-secondary);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-primary);
  cursor: pointer;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.action-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent,
    rgba(255,255,255,0.1),
    transparent
  );
  transition: left var(--transition-slow);
}

.action-item:hover::before {
  left: 100%;
}

.action-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  background: var(--bg-primary);
  border-color: var(--primary-lighter);
}

.action-icon {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: var(--space-lg);
  position: relative;
  z-index: 1;
}

.action-content {
  flex: 1;
  position: relative;
  z-index: 1;
}

.action-content h4 {
  margin: 0 0 var(--space-xs) 0;
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--text-primary);
}

.action-content p {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.action-arrow {
  color: var(--text-tertiary);
  transition: all var(--transition-base);
  position: relative;
  z-index: 1;
}

.action-item:hover .action-arrow {
  color: var(--primary-color);
  transform: translateX(4px);
}

/* 空状态样式 */
.empty-state {
  text-align: center;
  padding: var(--space-4xl) var(--space-2xl);
  color: var(--text-secondary);
}

.empty-icon {
  margin-bottom: var(--space-2xl);
  color: var(--text-tertiary);
  opacity: 0.6;
}

.empty-state h4 {
  margin: 0 0 var(--space-md) 0;
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--text-primary);
}

.empty-state p {
  margin: 0 0 var(--space-xl) 0;
  font-size: var(--text-base);
}

.empty-state .el-button {
  padding: var(--space-md) var(--space-2xl);
  font-weight: 600;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.empty-state .el-button::before {
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

.empty-state .el-button:hover::before {
  left: 100%;
}

/* 用户欢迎区域 */
.user-welcome {
  display: flex;
  align-items: center;
}

.user-welcome .el-avatar {
  box-shadow: var(--shadow-lg);
  border: 3px solid var(--bg-primary);
  position: relative;
}

.user-welcome .el-avatar::before {
  content: '';
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
  border-radius: var(--radius-full);
  z-index: -1;
  opacity: 0.8;
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
  .dashboard-content {
    padding: var(--space-lg);
  }

  .stat-card {
    height: auto;
    min-height: 120px;
    flex-direction: column;
    text-align: center;
    padding: var(--space-xl);
  }

  .stat-card-icon {
    margin-bottom: var(--space-lg);
    margin-left: 0;
  }

  .stat-card-content {
    margin-left: 0;
    text-align: center;
  }

  .quick-actions {
    grid-template-columns: 1fr;
    gap: var(--space-md);
  }

  .action-item {
    padding: var(--space-lg);
  }

  .action-icon {
    width: 40px;
    height: 40px;
    margin-right: var(--space-md);
  }

  .user-welcome {
    flex-direction: column;
    text-align: center;
    margin-top: var(--space-lg);
  }

  .user-welcome .ml-3 {
    margin-left: 0 !important;
    margin-top: var(--space-md);
  }
}

@media (max-width: 480px) {
  .dashboard-content {
    padding: var(--space-md);
  }

  .stat-card {
    padding: var(--space-lg);
    min-height: 100px;
  }

  .stat-card-icon {
    width: 50px;
    height: 50px;
  }

  .stat-number {
    font-size: var(--text-2xl);
  }

  .action-item {
    padding: var(--space-md);
  }

  .empty-state {
    padding: var(--space-2xl) var(--space-lg);
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .stat-card,
  .action-item {
    background: var(--bg-dark);
    border-color: var(--gray-700);
  }

  .action-item:hover {
    background: var(--gray-800);
  }
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .stat-card,
  .action-item {
    border-width: 2px;
  }

  .stat-card:hover,
  .action-item:hover {
    border-width: 3px;
  }
}

/* 现代化渐变背景 */
.modern-gradient-1 {
  position: relative;
}

.modern-gradient-1::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
    rgba(102, 126, 234, 0.05) 0%,
    rgba(118, 75, 162, 0.05) 100%);
  border-radius: var(--radius-2xl);
  opacity: 0;
  transition: opacity var(--transition-base);
  z-index: 0;
}

.modern-gradient-1:hover::after {
  opacity: 1;
}

.modern-gradient-2::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
    rgba(240, 147, 251, 0.05) 0%,
    rgba(245, 87, 108, 0.05) 100%);
  border-radius: var(--radius-2xl);
  opacity: 0;
  transition: opacity var(--transition-base);
  z-index: 0;
}

.modern-gradient-2:hover::after {
  opacity: 1;
}

.modern-gradient-3::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
    rgba(79, 172, 254, 0.05) 0%,
    rgba(0, 242, 254, 0.05) 100%);
  border-radius: var(--radius-2xl);
  opacity: 0;
  transition: opacity var(--transition-base);
  z-index: 0;
}

.modern-gradient-3:hover::after {
  opacity: 1;
}

.modern-gradient-4::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
    rgba(250, 112, 154, 0.05) 0%,
    rgba(254, 225, 64, 0.05) 100%);
  border-radius: var(--radius-2xl);
  opacity: 0;
  transition: opacity var(--transition-base);
  z-index: 0;
}

.modern-gradient-4:hover::after {
  opacity: 1;
}

/* 脉冲动画 */
.stat-card:hover .stat-card-icon {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: var(--shadow-md);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
  }
}

/* 数字跳动动画 */
.stat-card:hover .stat-number {
  animation: bounce 1s ease-in-out;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-5px);
  }
  60% {
    transform: translateY(-3px);
  }
}

/* 磁性边框效果 */
.stat-card {
  position: relative;
  z-index: 1;
}

.stat-card::before {
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
  border-radius: var(--radius-2xl);
  z-index: -1;
  opacity: 0;
  transition: opacity var(--transition-base);
  animation: border-rotate 3s linear infinite;
}

@keyframes border-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.stat-card:hover::before {
  opacity: 1;
}

/* 3D变换效果 */
.stat-card {
  transform-style: preserve-3d;
  transition: transform var(--transition-base);
}

.stat-card:hover {
  transform: translateY(-8px) rotateX(5deg);
}

/* 浮动粒子效果 */
.stat-card::after {
  content: '';
  position: absolute;
  top: 10%;
  left: 10%;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  animation: float-particle 3s ease-in-out infinite;
  opacity: 0;
  transition: opacity var(--transition-base);
}

.stat-card:hover::after {
  opacity: 1;
}

@keyframes float-particle {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.8;
  }
  33% {
    transform: translate(30px, -30px) scale(0.5);
    opacity: 0.4;
  }
  66% {
    transform: translate(-20px, 20px) scale(1.5);
    opacity: 0.6;
  }
}

/* 响应式增强 */
@media (max-width: 768px) {
  .stat-card:hover {
    transform: translateY(-4px);
  }

  .stat-card:hover .stat-card-icon {
    animation: none;
  }

  .stat-card:hover .stat-number {
    animation: none;
  }
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