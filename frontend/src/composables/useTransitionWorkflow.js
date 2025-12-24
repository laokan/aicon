import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import movieService from '@/services/movie'
import { useTaskPoller } from './useTaskPoller'

/**
 * 过渡视频工作流管理
 * 遵循架构：使用movieService而非直接调用api
 */
export function useTransitionWorkflow() {
    const transitions = ref([])
    const creating = ref(false)
    const generating = ref(false)

    const loadTransitions = async (scriptId) => {
        if (!scriptId) return
        try {
            const response = await movieService.getTransitions(scriptId)
            transitions.value = response.transitions || []
        } catch (error) {
            console.error('Failed to load transitions:', error)
            transitions.value = []
        }
    }

    const createTransitions = async (scriptId, apiKeyId, model) => {
        creating.value = true
        try {
            const response = await movieService.createTransitions(scriptId, {
                api_key_id: apiKeyId,
                model
            })

            if (response.task_id) {
                ElMessage.success('过渡创建任务已提交')
                const { startPolling } = useTaskPoller()
                startPolling(response.task_id, async (result) => {
                    ElMessage.success(`过渡创建完成: ${result.success} 个过渡`)
                    await loadTransitions(scriptId)
                    creating.value = false
                }, (error) => {
                    ElMessage.error(`创建失败: ${error.message}`)
                    creating.value = false
                })
            }
        } catch (error) {
            ElMessage.error('过渡创建失败')
            creating.value = false
        }
    }

    const generateTransitionVideos = async (scriptId, apiKeyId, videoModel) => {
        generating.value = true
        try {
            const response = await movieService.generateTransitionVideos(scriptId, {
                api_key_id: apiKeyId,
                video_model: videoModel
            })

            if (response.task_id) {
                ElMessage.success('过渡视频生成任务已提交')
                const { startPolling } = useTaskPoller()
                startPolling(response.task_id, async (result) => {
                    ElMessage.success(`视频生成完成: 成功 ${result.success}, 失败 ${result.failed}`)
                    await loadTransitions(scriptId)
                    generating.value = false
                }, (error) => {
                    ElMessage.error(`生成失败: ${error.message}`)
                    generating.value = false
                })
            }
        } catch (error) {
            ElMessage.error('视频生成失败')
            generating.value = false
        }
    }

    return {
        transitions,
        creating,
        generating,
        loadTransitions,
        createTransitions,
        generateTransitionVideos
    }
}
