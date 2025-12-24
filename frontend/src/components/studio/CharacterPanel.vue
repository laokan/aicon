<template>
  <div class="character-panel">
    <div class="panel-header">
      <h3>角色管理</h3>
      <div class="actions">
        <el-button 
          type="primary" 
          :loading="extracting"
          :disabled="!canExtract"
          @click="handleExtractClick"
        >
          提取角色
        </el-button>
        <el-button 
          type="success"
          :disabled="characters.length === 0"
          @click="handleBatchGenerateClick"
        >
          批量生成形象
        </el-button>
      </div>
    </div>

    <div class="character-list">
      <el-empty v-if="characters.length === 0" description="暂无角色，请先提取角色" />
      
      <div v-else class="character-grid">
        <div 
          v-for="char in characters" 
          :key="char.id"
          class="character-card"
        >
          <div class="character-avatar">
            <!-- 后端已返回presigned URL，直接使用 -->
            <img v-if="char.avatar_url" :src="char.avatar_url" :alt="char.name" />
            <div v-else class="avatar-placeholder">
              <el-icon :size="40"><User /></el-icon>
            </div>
          </div>
          
          <div class="character-info">
            <h4>{{ char.name }}</h4>
            <p class="role">{{ char.role_description }}</p>
            <p class="traits">{{ char.visual_traits }}</p>
          </div>

          <div class="character-actions">
            <el-button 
              v-if="!char.avatar_url"
              type="primary" 
              size="small"
              :loading="generatingId === char.id"
              @click="handleGenerateClick(char)"
            >
              生成形象
            </el-button>
            <template v-else>
              <el-button 
                type="success" 
                size="small"
                icon="Check"
                disabled
              >
                已生成
              </el-button>
              <el-button 
                type="warning" 
                size="small"
                icon="Refresh"
                :loading="generatingId === char.id"
                @click="handleRegenerateClick(char)"
              >
                重新生成
              </el-button>
            </template>
            <el-button 
              type="danger" 
              size="small"
              icon="Delete"
              @click="$emit('delete-character', char.id)"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- API Key选择对话框 -->
    <el-dialog
      v-model="showDialog"
      :title="dialogTitle"
      width="500px"
    >
      <el-form :model="formData" label-width="100px">
        <el-form-item label="API Key">
          <el-select v-model="formData.apiKeyId" placeholder="请选择API Key" style="width: 100%">
            <el-option
              v-for="key in apiKeys"
              :key="key.id"
              :label="`${key.provider} - ${key.name}`"
              :value="key.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="模型">
          <el-input v-model="formData.model" placeholder="请输入模型名称" />
        </el-form-item>
        <el-form-item v-if="dialogType === 'generate' || dialogType === 'regenerate'" label="提示词">
          <el-input 
            v-model="formData.prompt" 
            type="textarea"
            :rows="3"
            placeholder="可选，留空使用默认提示词"
          />
        </el-form-item>
        <el-form-item v-if="dialogType === 'generate' || dialogType === 'regenerate'" label="风格">
          <el-select v-model="formData.style" placeholder="请选择风格" style="width: 100%">
            <el-option label="电影级" value="cinematic" />
            <el-option label="写实" value="realistic" />
            <el-option label="艺术" value="artistic" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleDialogConfirm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { User } from '@element-plus/icons-vue'

const props = defineProps({
  characters: {
    type: Array,
    default: () => []
  },
  extracting: {
    type: Boolean,
    default: false
  },
  generatingId: {
    type: String,
    default: null
  },
  canExtract: {
    type: Boolean,
    default: true
  },
  apiKeys: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits([
  'extract-characters',
  'generate-avatar',
  'delete-character',
  'batch-generate'
])

const showDialog = ref(false)
const dialogType = ref('extract') // 'extract' | 'generate' | 'regenerate' | 'batch'
const dialogTitle = ref('')
const currentCharacter = ref(null)
const formData = ref({
  apiKeyId: '',
  model: '',
  prompt: '',
  style: 'cinematic'
})

const handleExtractClick = () => {
  dialogType.value = 'extract'
  dialogTitle.value = '提取角色'
  formData.value = {
    apiKeyId: props.apiKeys[0]?.id || '',
    model: 'gemini-2.0-flash-exp',
    prompt: '',
    style: 'cinematic'
  }
  showDialog.value = true
}

const handleGenerateClick = (char) => {
  dialogType.value = 'generate'
  dialogTitle.value = `生成角色形象 - ${char.name}`
  currentCharacter.value = char
  formData.value = {
    apiKeyId: props.apiKeys[0]?.id || '',
    model: 'gemini-2.0-flash-exp',
    prompt: '',
    style: 'cinematic'
  }
  showDialog.value = true
}

const handleRegenerateClick = (char) => {
  dialogType.value = 'regenerate'
  dialogTitle.value = `重新生成角色形象 - ${char.name}`
  currentCharacter.value = char
  formData.value = {
    apiKeyId: props.apiKeys[0]?.id || '',
    model: 'gemini-2.0-flash-exp',
    prompt: '',
    style: 'cinematic'
  }
  showDialog.value = true
}

const handleBatchGenerateClick = () => {
  dialogType.value = 'batch'
  dialogTitle.value = '批量生成角色形象'
  formData.value = {
    apiKeyId: props.apiKeys[0]?.id || '',
    model: 'gemini-2.0-flash-exp',
    prompt: '',
    style: 'cinematic'
  }
  showDialog.value = true
}

const handleDialogConfirm = () => {
  if (!formData.value.apiKeyId || !formData.value.model) {
    return
  }

  if (dialogType.value === 'extract') {
    emit('extract-characters', formData.value.apiKeyId, formData.value.model)
  } else if (dialogType.value === 'generate' || dialogType.value === 'regenerate') {
    emit('generate-avatar', 
      currentCharacter.value.id,
      formData.value.apiKeyId,
      formData.value.model,
      formData.value.prompt,
      formData.value.style
    )
  } else if (dialogType.value === 'batch') {
    emit('batch-generate', formData.value.apiKeyId, formData.value.model)
  }

  showDialog.value = false
}
</script>

<style scoped>
.character-panel {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.panel-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.actions {
  display: flex;
  gap: 10px;
}

.character-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.character-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s;
}

.character-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.character-avatar {
  width: 100%;
  height: 160px;
  border-radius: 8px;
  overflow: hidden;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.character-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  color: #c0c4cc;
}

.character-info h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
}

.character-info .role {
  margin: 0 0 4px 0;
  font-size: 13px;
  color: #606266;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-clamp: 2;
}

.character-info .traits {
  margin: 0;
  font-size: 12px;
  color: #909399;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-clamp: 2;
}

.character-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.character-actions .el-button {
  flex: 1;
  min-width: 80px;
}
</style>
