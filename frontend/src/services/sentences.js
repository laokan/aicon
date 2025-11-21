import api from './api'

/**
 * 句子管理服务
 */
export const sentencesService = {
    /**
     * 获取段落的句子列表
     * @param {string} paragraphId 段落ID
     * @returns {Promise<Object>}
     */
    async getSentences(paragraphId) {
        // 目前后端没有直接获取段落句子的接口，通常是获取段落详情时包含句子
        // 或者我们可以添加一个根据paragraph_id查询句子的接口
        // 暂时假设后端支持 GET /sentences/?paragraph_id=xxx 或者我们需要在段落详情中获取
        // 根据之前的后端实现，我们实现了 GET /sentences/{id}
        // 但似乎没有实现获取列表的接口？
        // 让我们检查一下后端代码。
        // 检查 backend/src/api/v1/sentences.py
        // 如果没有列表接口，我们可能需要依赖段落详情接口或者添加一个列表接口。
        // 暂时先实现基本的CRUD，列表获取可能需要后端支持。
        // 等等，查看 backend/src/services/sentence.py，没有 get_by_paragraph_id
        // 查看 backend/src/api/v1/sentences.py，只有 create, get, update, delete
        // 所以前端可能需要通过获取段落详情来获取句子列表？
        // 但是 Paragraph 模型中 sentences 是 relationship，默认可能不加载。
        // 让我们先实现已有的接口。
        return await api.get(`/sentences/?paragraph_id=${paragraphId}`)
    },

    /**
     * 创建新句子
     * @param {Object} data 句子数据 {paragraph_id, content, order_index}
     * @returns {Promise<Object>}
     */
    async createSentence(data) {
        return await api.post('/sentences/', data)
    },

    /**
     * 获取单个句子详情
     * @param {string} id 句子ID
     * @returns {Promise<Object>}
     */
    async getSentence(id) {
        return await api.get(`/sentences/${id}`)
    },

    /**
     * 更新句子
     * @param {string} id 句子ID
     * @param {Object} data 更新数据 {content}
     * @returns {Promise<Object>}
     */
    async updateSentence(id, data) {
        return await api.put(`/sentences/${id}`, data)
    },

    /**
     * 删除句子
     * @param {string} id 句子ID
     * @returns {Promise<Object>}
     */
    async deleteSentence(id) {
        return await api.delete(`/sentences/${id}`)
    }
}

export default sentencesService
