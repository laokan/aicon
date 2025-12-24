import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import movieService from '@/services/movie'
import { useTaskPoller } from './useTaskPoller'

/**
 * 场景工作流管理
 * 遵循架构：使用movieService而非直接调用api
 */
export function useSceneWorkflow() {
    const script = ref(null)
    const extracting = ref(false)

    const loadScript = async (chapterId) => {
        if (!chapterId) return
        try {
            const response = await movieService.getScript(chapterId)
            // response已经是data
            script.value = response
        } catch (error) {
            console.error('Failed to load script:', error)
            script.value = null
        }
    }

    const extractScenes = async (chapterId, apiKeyId, model) => {
        extracting.value = true
        try {
            const response = await movieService.extractScenes(chapterId, {
                api_key_id: apiKeyId,
                model
            })

            if (response.task_id) {
                ElMessage.success('场景提取任务已提交')
                const { startPolling } = useTaskPoller()
                startPolling(response.task_id, async () => {
                    ElMessage.success('场景提取完成')
                    await loadScript(chapterId)
                    extracting.value = false
                }, (error) => {
                    ElMessage.error(`提取失败: ${error.message}`)
                    extracting.value = false
                })
            }
        } catch (error) {
            ElMessage.error('场景提取失败')
            extracting.value = false
        }
    }

    return {
        script,
        extracting,
        loadScript,
        extractScenes
    }
}
