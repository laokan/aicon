import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import movieService from '@/services/movie'
import { useTaskPoller } from './useTaskPoller'

/**
 * 分镜工作流管理
 * 遵循架构：使用movieService而非直接调用api
 */
export function useShotWorkflow(script) {
    const extracting = ref(false)
    const generatingKeyframes = ref(false)

    const allShots = computed(() => {
        if (!script.value?.scenes) return []
        return script.value.scenes.flatMap(scene =>
            scene.shots.map(shot => ({ ...shot, scene_id: scene.id }))
        ).sort((a, b) => a.order_index - b.order_index)
    })

    const extractShots = async (scriptId, apiKeyId, model) => {
        extracting.value = true
        try {
            const response = await movieService.extractShots(scriptId, {
                api_key_id: apiKeyId,
                model
            })

            if (response.task_id) {
                ElMessage.success('分镜提取任务已提交')
                const { startPolling } = useTaskPoller()
                startPolling(response.task_id, async (result) => {
                    ElMessage.success(`分镜提取完成: 成功 ${result.success}, 失败 ${result.failed}`)
                    extracting.value = false
                    // Reload script to get shots
                    window.location.reload() // Temporary solution
                }, (error) => {
                    ElMessage.error(`提取失败: ${error.message}`)
                    extracting.value = false
                })
            }
        } catch (error) {
            ElMessage.error('分镜提取失败')
            extracting.value = false
        }
    }

    const generateKeyframes = async (scriptId, apiKeyId, model) => {
        generatingKeyframes.value = true
        try {
            const response = await movieService.generateKeyframes(scriptId, {
                api_key_id: apiKeyId,
                model
            })

            if (response.task_id) {
                ElMessage.success('关键帧生成任务已提交')
                const { startPolling } = useTaskPoller()
                startPolling(response.task_id, async (result) => {
                    if (result.failed > 0) {
                        ElMessage.warning(`关键帧生成部分完成: 成功 ${result.success}, 失败 ${result.failed}`)
                    } else {
                        ElMessage.success(`关键帧生成完成: 共 ${result.success} 个分镜`)
                    }
                    generatingKeyframes.value = false
                    window.location.reload() // Temporary solution
                }, (error) => {
                    ElMessage.error(`生成失败: ${error.message}`)
                    generatingKeyframes.value = false
                })
            }
        } catch (error) {
            ElMessage.error('关键帧生成失败')
            generatingKeyframes.value = false
        }
    }

    return {
        allShots,
        extracting,
        generatingKeyframes,
        extractShots,
        generateKeyframes
    }
}
