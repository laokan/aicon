<template>
  <div class="settings-page">
    <div class="settings-header">
      <h1>系统设置</h1>
      <p>管理您的账户和应用程序设置</p>
    </div>

    <div class="settings-content">
      <el-row :gutter="24">
        <el-col :span="8">
          <div class="settings-menu">
            <el-menu
              :default-active="activeTab"
              mode="vertical"
              @select="handleMenuSelect"
              class="settings-nav"
            >
              <el-menu-item index="profile">
                <el-icon><User /></el-icon>
                <span>个人资料</span>
              </el-menu-item>
              <el-menu-item index="account">
                <el-icon><Lock /></el-icon>
                <span>账户安全</span>
              </el-menu-item>
              <el-menu-item index="preferences">
                <el-icon><Setting /></el-icon>
                <span>偏好设置</span>
              </el-menu-item>
            </el-menu>
          </div>
        </el-col>

        <el-col :span="16">
          <div class="settings-panel">
            <div v-show="activeTab === 'profile'" class="setting-section">
              <h2>个人资料</h2>
              <p>更新您的个人信息</p>
              <el-form :model="userForm" label-width="100px">
                <el-form-item label="显示名称">
                  <el-input v-model="userForm.display_name" placeholder="请输入显示名称" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="saveProfile">保存更改</el-button>
                </el-form-item>
              </el-form>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { User, Lock, Setting } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const activeTab = ref('profile')

const userForm = reactive({
  display_name: authStore.user?.display_name || ''
})

const handleMenuSelect = (index) => {
  activeTab.value = index
}

const saveProfile = () => {
  ElMessage.success('个人资料保存成功')
}
</script>

<style scoped>
.settings-page {
  padding: var(--space-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.settings-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.settings-header h1 {
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 var(--space-sm) 0;
}

.settings-content {
  background: var(--bg-secondary);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-primary);
  overflow: hidden;
}

.settings-panel {
  padding: var(--space-xl);
}
</style>
