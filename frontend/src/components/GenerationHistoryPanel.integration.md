# 生成历史记录组件集成指南

## 组件说明

`GenerationHistoryPanel.vue` 是一个通用的生成历史记录展示和选择组件，支持图片和视频两种媒体类型。

## 使用方法

### 1. 导入组件

```vue
<script setup>
import GenerationHistoryPanel from '@/components/GenerationHistoryPanel.vue'
import { ref } from 'vue'

const showHistory = ref(false)
</script>
```

### 2. 在模板中使用

```vue
<template>
  <!-- 触发按钮 -->
  <el-button @click="showHistory = true">
    查看历史记录
  </el-button>

  <!-- 历史记录面板 -->
  <GenerationHistoryPanel
    v-model="showHistory"
    resource-type="scene_image"
    :resource-id="sceneId"
    media-type="image"
    @selected="handleHistorySelected"
  />
</template>
```

### 3. 处理选择事件

```vue
<script setup>
const handleHistorySelected = (history) => {
  // 选择历史记录后，组件会自动更新后端资源URL
  // 这里可以刷新当前显示的数据
  console.log('已选择历史记录:', history)
  
  // 例如：重新加载场景数据
  await loadSceneData()
}
</script>
```

## 集成示例

### 示例 1: 场景图历史记录

```vue
<template>
  <div class="scene-image-container">
    <!-- 场景图显示 -->
    <img :src="scene.scene_image_url" alt="场景图" />
    
    <!-- 历史记录按钮 -->
    <el-button 
      type="primary" 
      icon="History"
      @click="showSceneImageHistory = true"
    >
      历史记录
    </el-button>

    <!-- 历史记录面板 -->
    <GenerationHistoryPanel
      v-model="showSceneImageHistory"
      resource-type="scene_image"
      :resource-id="scene.id"
      media-type="image"
      @selected="handleSceneImageSelected"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import GenerationHistoryPanel from '@/components/GenerationHistoryPanel.vue'

const props = defineProps({
  scene: Object
})

const showSceneImageHistory = ref(false)

const handleSceneImageSelected = async (history) => {
  // 刷新场景数据
  emit('refresh')
}
</script>
```

### 示例 2: 关键帧历史记录

```vue
<template>
  <div class="keyframe-container">
    <!-- 关键帧显示 -->
    <img :src="shot.keyframe_url" alt="关键帧" />
    
    <!-- 历史记录按钮 -->
    <el-button 
      size="small"
      @click="showKeyframeHistory = true"
    >
      <el-icon><Clock /></el-icon>
      历史
    </el-button>

    <!-- 历史记录面板 -->
    <GenerationHistoryPanel
      v-model="showKeyframeHistory"
      resource-type="shot_keyframe"
      :resource-id="shot.id"
      media-type="image"
      @selected="handleKeyframeSelected"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import GenerationHistoryPanel from '@/components/GenerationHistoryPanel.vue'

const props = defineProps({
  shot: Object
})

const showKeyframeHistory = ref(false)

const handleKeyframeSelected = async (history) => {
  // 刷新分镜数据
  emit('refresh')
}
</script>
```

### 示例 3: 角色头像历史记录

```vue
<template>
  <div class="character-avatar-container">
    <!-- 头像显示 -->
    <el-avatar :src="character.avatar_url" :size="100" />
    
    <!-- 历史记录按钮 -->
    <el-button 
      type="text"
      @click="showAvatarHistory = true"
    >
      查看历史头像
    </el-button>

    <!-- 历史记录面板 -->
    <GenerationHistoryPanel
      v-model="showAvatarHistory"
      resource-type="character_avatar"
      :resource-id="character.id"
      media-type="image"
      @selected="handleAvatarSelected"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import GenerationHistoryPanel from '@/components/GenerationHistoryPanel.vue'

const props = defineProps({
  character: Object
})

const showAvatarHistory = ref(false)

const handleAvatarSelected = async (history) => {
  // 刷新角色数据
  emit('refresh')
}
</script>
```

### 示例 4: 过渡视频历史记录

```vue
<template>
  <div class="transition-video-container">
    <!-- 视频显示 -->
    <video :src="transition.video_url" controls />
    
    <!-- 历史记录按钮 -->
    <el-button 
      type="primary"
      @click="showVideoHistory = true"
    >
      历史版本
    </el-button>

    <!-- 历史记录面板 -->
    <GenerationHistoryPanel
      v-model="showVideoHistory"
      resource-type="transition_video"
      :resource-id="transition.id"
      media-type="video"
      @selected="handleVideoSelected"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import GenerationHistoryPanel from '@/components/GenerationHistoryPanel.vue'

const props = defineProps({
  transition: Object
})

const showVideoHistory = ref(false)

const handleVideoSelected = async (history) => {
  // 刷新过渡视频数据
  emit('refresh')
}
</script>
```

## Props 说明

| Prop | 类型 | 必填 | 说明 | 可选值 |
|------|------|------|------|--------|
| modelValue | Boolean | 是 | 控制对话框显示/隐藏 | - |
| resourceType | String | 是 | 资源类型 | scene_image, shot_keyframe, character_avatar, transition_video |
| resourceId | String | 是 | 资源ID | - |
| mediaType | String | 是 | 媒体类型 | image, video |

## Events 说明

| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:modelValue | Boolean | 对话框显示状态变化 |
| selected | history: Object | 选择历史记录后触发 |

## 样式定制

组件使用了 scoped 样式，如需定制可以通过以下方式：

```vue
<style>
/* 覆盖历史记录项的样式 */
.history-item {
  /* 自定义样式 */
}
</style>
```

## 注意事项

1. **自动刷新**: 选择历史记录后，后端会自动更新资源的URL字段，前端需要重新加载数据以显示最新内容
2. **URL签名**: 所有URL都已在后端自动签名，有效期24小时
3. **权限控制**: 组件会使用当前用户的认证信息调用API
4. **错误处理**: 组件内置了基本的错误提示，无需额外处理

## API 端点

组件会根据 `resourceType` 自动选择对应的API端点：

- 场景图: `/api/v1/movie/generation-history/scenes/{id}/images`
- 关键帧: `/api/v1/movie/generation-history/shots/{id}/keyframes`
- 角色头像: `/api/v1/movie/generation-history/characters/{id}/avatars`
- 过渡视频: `/api/v1/movie/generation-history/transitions/{id}/videos`

## 完整示例

查看 `frontend/src/views/MovieStudio/` 下的组件以获取完整的集成示例。
