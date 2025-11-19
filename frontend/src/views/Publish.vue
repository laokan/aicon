<template>
  <div class="publish-page">
    <!-- 页面头部信息 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon class="title-icon"><Promotion /></el-icon>
        内容分发
      </h1>
      <p class="page-description">将您的内容一键发布到多个平台</p>
    </div>

    <!-- 主要内容区 -->
    <div class="publish-content">
      <div class="publish-steps">
        <el-steps :active="currentStep" finish-status="success" align-center>
          <el-step title="选择内容" description="选择要发布的项目内容"></el-step>
          <el-step title="配置平台" description="选择发布平台和配置"></el-step>
          <el-step title="预览发布" description="预览并确认发布内容"></el-step>
          <el-step title="发布完成" description="内容已成功发布"></el-step>
        </el-steps>
      </div>

      <div class="publish-form">
        <!-- 步骤1: 选择内容 -->
        <div v-if="currentStep === 0" class="step-content">
          <div class="step-header">
            <h3>选择要发布的内容</h3>
            <p>请从您的项目中选择一个进行发布</p>
          </div>

          <div class="content-selection">
            <el-empty description="暂无可发布的内容">
              <el-button type="primary" @click="$router.push('/projects')">
                前往项目管理
              </el-button>
            </el-empty>
          </div>
        </div>

        <!-- 步骤2: 配置平台 -->
        <div v-if="currentStep === 1" class="step-content">
          <div class="step-header">
            <h3>配置发布平台</h3>
            <p>选择您要发布的平台并设置相关参数</p>
          </div>

          <div class="platform-config">
            <el-empty description="发布平台功能开发中">
              <el-icon size="64"><Platform /></el-icon>
            </el-empty>
          </div>
        </div>

        <!-- 步骤3: 预览发布 -->
        <div v-if="currentStep === 2" class="step-content">
          <div class="step-header">
            <h3>预览发布内容</h3>
            <p>确认内容无误后进行发布</p>
          </div>

          <div class="content-preview">
            <el-empty description="预览功能开发中">
              <el-icon size="64"><View /></el-icon>
            </el-empty>
          </div>
        </div>

        <!-- 步骤4: 发布完成 -->
        <div v-if="currentStep === 3" class="step-content">
          <div class="step-header">
            <h3>发布成功！</h3>
            <p>您的内容已成功发布到选定平台</p>
          </div>

          <div class="publish-success">
            <el-result
              icon="success"
              title="发布成功"
              sub-title="您的内容已成功发布"
            >
              <template #extra>
                <el-button type="primary" @click="resetPublish">继续发布</el-button>
                <el-button @click="$router.push('/projects')">返回项目</el-button>
              </template>
            </el-result>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="step-actions">
        <el-button
          v-if="currentStep > 0"
          @click="prevStep"
          :disabled="currentStep === 0"
        >
          上一步
        </el-button>
        <el-button
          v-if="currentStep < 3"
          type="primary"
          @click="nextStep"
          :disabled="!canProceed"
        >
          下一步
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Promotion, Platform, View } from '@element-plus/icons-vue'

const currentStep = ref(0)

// 是否可以进入下一步
const canProceed = computed(() => {
  // 这里可以根据实际业务逻辑判断
  return true
})

// 下一步
const nextStep = () => {
  if (currentStep.value < 3) {
    currentStep.value++
  }
}

// 上一步
const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 重置发布流程
const resetPublish = () => {
  currentStep.value = 0
}
</script>

<style scoped>
.publish-page {
  display: flex;
  flex-direction: column;
  gap: 40px;
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
}

.publish-content {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  padding: 40px;
  box-shadow: var(--shadow-sm);
  min-height: 600px;
  display: flex;
  flex-direction: column;
}

.publish-steps {
  margin-bottom: 60px;
  padding: 0 40px;
}

:deep(.el-step__title) {
  font-size: 14px;
  font-weight: 600;
  margin-top: 8px;
}

:deep(.el-step__description) {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.publish-form {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.step-content {
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.step-header {
  text-align: center;
  margin-bottom: 40px;
}

.step-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.step-header p {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0;
}

.content-selection,
.platform-config,
.content-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px dashed var(--border-primary);
  margin-bottom: 40px;
  transition: all 0.3s ease;
}

.content-selection:hover,
.platform-config:hover,
.content-preview:hover {
  border-color: var(--primary-color);
  background: var(--bg-primary);
}

.step-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: auto;
  padding-top: 20px;
}

.step-actions .el-button {
  min-width: 120px;
  height: 40px;
  font-weight: 500;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .publish-content {
    padding: 20px;
  }

  .publish-steps {
    padding: 0;
    margin-bottom: 40px;
  }

  :deep(.el-step__title) {
    font-size: 12px;
  }

  .step-header h3 {
    font-size: 20px;
  }
}
</style>