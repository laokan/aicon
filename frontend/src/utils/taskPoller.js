import api from '@/services/api'

/**
 * 轮询Celery任务状态
 * @param {string} taskId - 任务ID
 * @param {number} maxAttempts - 最大尝试次数
 * @param {number} interval - 轮询间隔（毫秒）
 * @returns {Promise} 任务结果
 */
export async function pollTaskStatus(taskId, maxAttempts = 60, interval = 1000) {
    for (let i = 0; i < maxAttempts; i++) {
        await new Promise(resolve => setTimeout(resolve, interval))

        try {
            // 正确的任务状态API路径
            const response = await api.get(`/tasks/${taskId}`)
            const status = response.status

            if (status === 'SUCCESS') {
                return response.result
            } else if (status === 'FAILURE') {
                throw new Error(response.result?.message || response.result?.error || '任务执行失败')
            } else if (status === 'PENDING' || status === 'PROGRESS' || status === 'STARTED') {
                // 继续轮询
                continue
            } else {
                console.warn(`未知的任务状态: ${status}`)
                continue
            }
        } catch (error) {
            // 如果是任务失败的错误，直接抛出
            if (error.message && error.message.includes('任务')) {
                throw error
            }
            console.error('查询任务状态失败:', error)
            // 最后一次尝试时抛出错误
            if (i === maxAttempts - 1) {
                throw new Error('无法查询任务状态: ' + error.message)
            }
            // 否则继续轮询
            continue
        }
    }

    throw new Error(`任务超时: 已尝试 ${maxAttempts} 次，每次间隔 ${interval}ms`)
}

/**
 * 带进度回调的任务轮询
 * @param {string} taskId - 任务ID
 * @param {Function} onProgress - 进度回调函数
 * @param {number} maxAttempts - 最大尝试次数
 * @param {number} interval - 轮询间隔（毫秒）
 * @returns {Promise} 任务结果
 */
export async function pollTaskStatusWithProgress(taskId, onProgress, maxAttempts = 60, interval = 1000) {
    for (let i = 0; i < maxAttempts; i++) {
        await new Promise(resolve => setTimeout(resolve, interval))

        try {
            const response = await api.get(`/tasks/${taskId}`)
            const status = response.status

            // 调用进度回调
            if (onProgress && typeof onProgress === 'function') {
                onProgress({
                    status,
                    result: response.result,
                    attempt: i + 1,
                    maxAttempts
                })
            }

            if (status === 'SUCCESS') {
                return response.result
            } else if (status === 'FAILURE') {
                throw new Error(response.result?.message || response.result?.error || '任务执行失败')
            } else if (status === 'PENDING' || status === 'PROGRESS' || status === 'STARTED') {
                continue
            } else {
                console.warn(`未知的任务状态: ${status}`)
                continue
            }
        } catch (error) {
            if (error.message && error.message.includes('任务')) {
                throw error
            }
            console.error('查询任务状态失败:', error)
            if (i === maxAttempts - 1) {
                throw new Error('无法查询任务状态: ' + error.message)
            }
            continue
        }
    }

    throw new Error(`任务超时: 已尝试 ${maxAttempts} 次，每次间隔 ${interval}ms`)
}
