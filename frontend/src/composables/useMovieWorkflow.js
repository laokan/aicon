import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCharacterWorkflow } from './useCharacterWorkflow'
import { useSceneWorkflow } from './useSceneWorkflow'
import { useShotWorkflow } from './useShotWorkflow'
import { useTransitionWorkflow } from './useTransitionWorkflow'

/**
 * 电影工作流主控制器
 * 遵循架构：不传递api实例，让子workflow自己使用service
 */
export function useMovieWorkflow() {
    const route = useRoute()
    const router = useRouter()

    const selectedChapterId = ref(route.params.chapterId || null)
    const projectId = ref(route.params.projectId || null)
    const currentStep = ref(0)
    const loading = ref(false)

    console.log('useMovieWorkflow init:', {
        chapterId: selectedChapterId.value,
        projectId: projectId.value,
        routeParams: route.params
    })

    // Initialize workflows - 不传递api实例
    const characterWorkflow = useCharacterWorkflow(projectId)
    const sceneWorkflow = useSceneWorkflow()
    const shotWorkflow = useShotWorkflow(sceneWorkflow.script)
    const transitionWorkflow = useTransitionWorkflow()

    // Computed states
    const canExtractScenes = computed(() => {
        return characterWorkflow.characters.value.length > 0
    })

    const canExtractShots = computed(() => {
        return sceneWorkflow.script.value?.scenes?.length > 0
    })

    const canGenerateKeyframes = computed(() => {
        return shotWorkflow.allShots.value.length > 0 &&
            characterWorkflow.characters.value.every(c => c.avatar_url)
    })

    const canCreateTransitions = computed(() => {
        return shotWorkflow.allShots.value.every(s => s.keyframe_url)
    })

    const canGenerateTransitionVideos = computed(() => {
        return transitionWorkflow.transitions.value.length > 0
    })

    // Auto-determine current step based on data
    const determineCurrentStep = () => {
        if (!sceneWorkflow.script.value) {
            currentStep.value = 0 // Characters
        } else if (!sceneWorkflow.script.value.scenes?.length) {
            currentStep.value = 1 // Scenes
        } else if (!shotWorkflow.allShots.value.length) {
            currentStep.value = 2 // Shots
        } else if (!shotWorkflow.allShots.value.every(s => s.keyframe_url)) {
            currentStep.value = 3 // Keyframes
        } else if (!transitionWorkflow.transitions.value.length) {
            currentStep.value = 4 // Transitions
        } else {
            currentStep.value = 5 // Final
        }
    }

    // Load initial data
    const loadData = async () => {
        if (!selectedChapterId.value || !projectId.value) {
            console.warn('Cannot load data: missing chapterId or projectId')
            return
        }

        loading.value = true
        try {
            // Load characters
            await characterWorkflow.loadCharacters()

            // Try to load script if it exists
            try {
                await sceneWorkflow.loadScript(selectedChapterId.value)
                if (sceneWorkflow.script.value) {
                    await transitionWorkflow.loadTransitions(sceneWorkflow.script.value.id)
                }
            } catch (error) {
                console.log('No script found for this chapter yet')
            }

            determineCurrentStep()
        } catch (error) {
            console.error('Failed to load data:', error)
        } finally {
            loading.value = false
        }
    }

    const goBack = () => {
        if (projectId.value) {
            router.push({ name: 'ProjectDetail', params: { projectId: projectId.value } })
        } else {
            router.push('/projects')
        }
    }

    // Watch for chapter changes
    watch(selectedChapterId, (newId) => {
        if (newId) {
            loadData()
        }
    })

    // Watch for route changes
    watch(() => route.params, (newParams) => {
        console.log('Route params changed:', newParams)
        if (newParams.projectId) {
            projectId.value = newParams.projectId
        }
        if (newParams.chapterId) {
            selectedChapterId.value = newParams.chapterId
        }
    }, { deep: true })

    onMounted(() => {
        if (selectedChapterId.value && projectId.value) {
            loadData()
        }
    })

    return {
        // State
        selectedChapterId,
        projectId,
        currentStep,
        loading,

        // Workflows
        characterWorkflow,
        sceneWorkflow,
        shotWorkflow,
        transitionWorkflow,

        // Computed
        canExtractScenes,
        canExtractShots,
        canGenerateKeyframes,
        canCreateTransitions,
        canGenerateTransitionVideos,

        // Methods
        loadData,
        goBack
    }
}
