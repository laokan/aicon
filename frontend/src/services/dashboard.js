/**
 * 仪表盘数据服务
 * 提供仪表盘所需的统计数据和概览信息
 */

import { get } from './api'

export const dashboardService = {
  /**
   * 获取仪表盘统计数据
   * @returns {Promise<Object>} 统计数据
   */
  async getStatistics() {
    return await get('/dashboard/statistics')
  },

  /**
   * 获取最近的项目列表
   * @param {number} limit - 返回数量限制，默认5
   * @returns {Promise<Object>} 最近项目列表
   */
  async getRecentProjects(limit = 5) {
    return await get('/dashboard/recent-projects', {
      params: { limit }
    })
  },

  /**
   * 获取最近的活动记录
   * @param {number} limit - 返回数量限制，默认10
   * @returns {Promise<Object>} 最近活动列表
   */
  async getRecentActivities(limit = 10) {
    return await get('/dashboard/recent-activities', {
      params: { limit }
    })
  },

  /**
   * 获取任务队列状态
   * @returns {Promise<Object>} 任务队列状态
   */
  async getTaskQueue() {
    return await get('/dashboard/task-queue')
  }
}

export default dashboardService
