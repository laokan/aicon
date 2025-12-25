<template>
  <div class="scene-image-panel">
    <div class="panel-header">
      <h3>场景图生成</h3>
      <div class="actions">
        <el-button 
          type="primary"
          :loading="batchGenerating"
          :disabled="!canGenerate || generatingIds.size > 0 || batchGenerating"
          @click="handleBatchGenerateClick"
        >
          批量生成场景图
        </el-button>
      </div>
    </div>

    <div class="scene-list">
      <el-empty v-if="scenes.length === 0" description="暂无场景数据，请先提取场景" />
      
      <div v-else class="scene-grid">
        <div 
          v-for="scene in scenes" 
          :key="scene.id"
          class="scene-card"
        >
          <div class="scene-header">
            <span class="scene-number">场景 {{ scene.order_index }}</span>
            <div class="scene-actions">
              <el-button
                v-if="!scene.scene_image_url"
                type="success"
                size="small"
                :loading="generatingIds.has(scene.id)"
                :disabled="generatingIds.has(scene.id)"
                @click="handleGenerateSceneImage(scene)"
              >
                生成
              </el-button>
              <el-button
                v-else
                type="warning"
                size="small"
                :loading="generatingIds.has(scene.id)"
                :disabled="generatingIds.has(scene.id)"
                @click="handleRegenerateSceneImage(scene)"
              >
                重新生成
              </el-button>
            </div>
          </div>
          
          <div class="scene-description">
            <p>{{ scene.scene }}</p>
          </div>

          <!-- 场景图预览 -->
          <div v-if="scene.scene_image_url" class="scene-image" @click="handlePreviewImage(scene.scene_image_url)">
            <img :src="scene.scene_image_url" alt="场景图" />
            <div class="scene-overlay">
              <el-icon><ZoomIn /></el-icon>
            </div>
          </div>
          <div v-else class="scene-placeholder">
            <el-icon :size="40"><Picture /></el-icon>
            <p>待生成场景图</p>
            <p class="hint">无人物环境图</p>
          </div>

          <!-- 场景中的角色 -->
          <div v-if="scene.characters && scene.characters.length > 0" class="scene-characters">
            <el-tag 
              v-for="char in scene.characters" 
              :key="char"
              size="small"
              type="info"
              effect="plain"
            >
              {{ char }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>

    <!-- 批量生成对话框 -->
    <el-dialog
      v-model="showBatchDialog"
      title="批量生成场景图"
      width="500px"
    >
      <el-form :model="batchFormData" label-width="100px">
        <el-form-item label="API Key">
          <el-select v-model="batchFormData.apiKeyId" placeholder="请选择API Key" style="width: 100%">
            <el-option
              v-for="key in apiKeys"
              :key="key.id"
              :label="`${key.name} (${key.provider})`"
              :value="key.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="模型">
          <el-select 
            v-model="batchFormData.model" 
            placeholder="选择模型" 
            style="width: 100%"
            :loading="loadingBatchModels"
            filterable
            allow-create
            default-first-option
          >
            <el-option
              v-for="model in batchModelOptions"
              :key="model"
              :label="model"
              :value="model"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showBatchDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="handleBatchDialogConfirm" 
          :disabled="!batchFormData.apiKeyId || !batchFormData.model"
        >
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 单个生成对话框 -->
    <el-dialog
      v-model="showSceneImageDialog"
      :title="sceneImageDialogType === 'generate' ? '生成场景图' : '重新生成场景图'"
      width="700px"
    >
      <el-form :model="sceneImageFormData" label-width="100px">
        <el-form-item label="API Key">
          <el-select v-model="sceneImageFormData.apiKeyId" placeholder="请选择API Key" style="width: 100%">
            <el-option
              v-for="key in apiKeys"
              :key="key.id"
              :label="`${key.name} (${key.provider})`"
              :value="key.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="模型">
          <el-select 
            v-model="sceneImageFormData.model" 
            placeholder="选择模型" 
            style="width: 100%"
            :loading="loadingSceneImageModels"
            filterable
            allow-create
            default-first-option
          >
            <el-option
              v-for="model in sceneImageModelOptions"
              :key="model"
              :label="model"
              :value="model"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="生成提示词">
          <el-input
            v-model="sceneImageFormData.prompt"
            type="textarea"
            :rows="12"
            placeholder="场景图提示词（可编辑调整）"
            style="font-family: monospace; font-size: 12px;"
          />
          <div style="margin-top: 8px; color: #909399; font-size: 12px;">
            💡 提示词已使用 Veo 3.1 最佳实践优化（摄影、氛围、风格），您可以根据需要调整。
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSceneImageDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="handleSceneImageDialogConfirm" 
          :disabled="!sceneImageFormData.apiKeyId || !sceneImageFormData.model"
        >
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 图片预览 -->
    <el-image-viewer
      v-if="showImageViewer"
      :url-list="[currentPreviewImage]"
      @close="showImageViewer = false"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Picture, ZoomIn } from '@element-plus/icons-vue'
import api from '@/services/api'

const props = defineProps({
  scenes: {
    type: Array,
    default: () => []
  },
  canGenerate: {
    type: Boolean,
    default: true
  },
  apiKeys: {
    type: Array,
    default: () => []
  },
  generatingIds: {
    type: Set,
    default: () => new Set()
  },
  batchGenerating: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['batch-generate', 'generate-scene-image'])

// 批量生成
const showBatchDialog = ref(false)
const batchFormData = ref({
  apiKeyId: '',
  model: ''
})
const batchModelOptions = ref([])
const loadingBatchModels = ref(false)

// 单个生成
const showSceneImageDialog = ref(false)
const sceneImageDialogType = ref('generate')
const currentScene = ref(null)
const sceneImageFormData = ref({
  apiKeyId: '',
  model: '',
  prompt: ''
})
const sceneImageModelOptions = ref([])
const loadingSceneImageModels = ref(false)

// 图片预览
const showImageViewer = ref(false)
const currentPreviewImage = ref('')

// 监听批量生成API Key变化
watch(() => batchFormData.value.apiKeyId, async (newKeyId) => {
  if (!newKeyId) {
    batchModelOptions.value = []
    batchFormData.value.model = ''
    return
  }
  
  loadingBatchModels.value = true
  try {
    const models = await api.get(`/api-keys/${newKeyId}/models?type=image`)
    batchModelOptions.value = models || []
    if (batchModelOptions.value.length > 0) {
      batchFormData.value.model = batchModelOptions.value[0]
    }
  } catch (error) {
    console.error('获取模型列表失败', error)
    ElMessage.warning('获取模型列表失败')
    batchModelOptions.value = []
    batchFormData.value.model = ''
  } finally {
    loadingBatchModels.value = false
  }
})

// 监听单个生成API Key变化
watch(() => sceneImageFormData.value.apiKeyId, async (newKeyId) => {
  if (!newKeyId) {
    sceneImageModelOptions.value = []
    sceneImageFormData.value.model = ''
    return
  }
  
  loadingSceneImageModels.value = true
  try {
    const models = await api.get(`/api-keys/${newKeyId}/models?type=image`)
    sceneImageModelOptions.value = models || []
    if (sceneImageModelOptions.value.length > 0) {
      sceneImageFormData.value.model = sceneImageModelOptions.value[0]
    }
  } catch (error) {
    console.error('获取模型列表失败', error)
    ElMessage.warning('获取模型列表失败')
    sceneImageModelOptions.value = []
    sceneImageFormData.value.model = ''
  } finally {
    loadingSceneImageModels.value = false
  }
})

// 构建 Veo 3.1 优化的场景图提示词
const buildVeo31ScenePrompt = (sceneDescription) => {
  return `Create a cinematic establishing shot of the following environment.
This is a LIVE-ACTION PHOTOGRAPH for a film production, not CGI or 3D render.

## Scene Description
${sceneDescription}

## Prompt Structure (Apply Veo 3.1 Formula)

### [Cinematography]
Choose appropriate camera work for establishing the environment:
- Camera angle: Wide establishing shot, aerial view, crane shot, sweeping panorama, high angle (show scope), eye-level perspective
- Composition: Rule of thirds, leading lines, depth layers (foreground/midground/background), balanced framing
- Lens: Wide-angle lens for expansive views, deep focus to capture environmental detail

### [Environment Subject]
The location and setting itself is the subject:
- Identify the main environmental elements (landscape, architecture, interior space, natural features)
- Emphasize spatial relationships and scale
- Highlight distinctive characteristics of the location

### [Atmospheric Context]
Define the temporal and weather conditions:
- Time of day: Golden hour (warm sunset/sunrise light), blue hour (twilight), midday sun, overcast day, night
- Weather: Clear skies, scattered clouds, fog/mist, light rain, snow, storm clouds gathering
- Season: Spring bloom, summer lushness, autumn colors, winter bareness (if relevant)

### [Style & Ambiance]
Establish the mood and visual aesthetic:
- Lighting quality: Soft diffused natural light, dramatic shadows and highlights, volumetric light rays through atmosphere, ambient environmental glow, harsh direct sunlight
- Mood: Serene and peaceful, ominous and foreboding, mysterious and enigmatic, vibrant and lively, desolate and abandoned, welcoming and warm
- Aesthetic: Cinematic film photography, photorealistic, rich color palette or muted tones, high dynamic range

## Critical Requirements

**UNINHABITED ENVIRONMENT - No Human Presence:**
- This is a pristine, empty, deserted location
- Vacant space with no people, figures, or human activity
- Unpopulated natural landscape or abandoned built environment
- No human silhouettes, shadows, or reflections
- No crowds, groups, individuals, or any human-like shapes
- The environment exists in complete solitude

**Technical Specifications:**
- Shot on professional cinema camera (ARRI Alexa, RED, Sony Venice)
- Cinematic color grading with film look (not digital/video look)
- High dynamic range with rich environmental detail
- Professional landscape or architectural photography standards
- Natural depth of field characteristic of cinema lenses

**Forbidden Elements:**
- NO 3D rendering artifacts or CGI aesthetics
- NO video game or synthetic imagery look
- NO people, characters, humans, persons, faces, bodies
- NO human-made activity or human presence indicators
- NO mannequins or human-shaped objects

Generate a detailed, cinematic establishing shot that captures the essence and atmosphere of this environment.`
}

const handleBatchGenerateClick = () => {
  batchFormData.value = {
    apiKeyId: props.apiKeys[0]?.id || '',
    model: ''
  }
  showBatchDialog.value = true
}

const handleBatchDialogConfirm = () => {
  if (!batchFormData.value.apiKeyId || !batchFormData.value.model) {
    return
  }
  emit('batch-generate', batchFormData.value.apiKeyId, batchFormData.value.model)
  showBatchDialog.value = false
}

const handleGenerateSceneImage = (scene) => {
  currentScene.value = scene
  sceneImageDialogType.value = 'generate'
  
  sceneImageFormData.value = {
    apiKeyId: props.apiKeys[0]?.id || '',
    model: '',
    prompt: scene.scene_image_prompt || buildVeo31ScenePrompt(scene.scene)
  }
  showSceneImageDialog.value = true
}

const handleRegenerateSceneImage = (scene) => {
  currentScene.value = scene
  sceneImageDialogType.value = 'regenerate'
  
  sceneImageFormData.value = {
    apiKeyId: props.apiKeys[0]?.id || '',
    model: '',
    prompt: scene.scene_image_prompt || buildVeo31ScenePrompt(scene.scene)
  }
  showSceneImageDialog.value = true
}

const handleSceneImageDialogConfirm = () => {
  if (!sceneImageFormData.value.apiKeyId || !sceneImageFormData.value.model || !currentScene.value) {
    return
  }
  emit('generate-scene-image', 
    currentScene.value.id, 
    sceneImageFormData.value.apiKeyId, 
    sceneImageFormData.value.model,
    sceneImageFormData.value.prompt
  )
  showSceneImageDialog.value = false
}

const handlePreviewImage = (url) => {
  currentPreviewImage.value = url
  showImageViewer.value = true
}
</script>

<style scoped>
.scene-image-panel {
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

.scene-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.scene-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s;
  background: white;
}

.scene-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.scene-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  gap: 8px;
}

.scene-number {
  font-weight: 600;
  color: #409eff;
  font-size: 15px;
  flex-shrink: 0;
}

.scene-actions {
  flex-shrink: 0;
}

.scene-description {
  margin-bottom: 12px;
  color: #606266;
  font-size: 13px;
  line-height: 1.6;
}

.scene-description p {
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.scene-image {
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  aspect-ratio: 16/9;
  margin-bottom: 12px;
}

.scene-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s;
}

.scene-image:hover img {
  transform: scale(1.05);
}

.scene-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: white;
  font-size: 32px;
}

.scene-image:hover .scene-overlay {
  opacity: 1;
}

.scene-placeholder {
  aspect-ratio: 16/9;
  background: #f5f7fa;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  margin-bottom: 12px;
}

.scene-placeholder p {
  margin: 8px 0 0 0;
  font-size: 13px;
}

.scene-placeholder .hint {
  font-size: 11px;
  color: #c0c4cc;
  margin-top: 4px;
}

.scene-characters {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
</style>
