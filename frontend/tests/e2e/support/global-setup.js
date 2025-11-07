const { chromium } = require('@playwright/test')

async function globalSetup(config) {
  console.log('🚀 Starting global setup for E2E tests')

  // 设置测试用户数据
  const testUsers = [
    {
      username: 'testuser1',
      email: 'test1@example.com',
      password: 'TestPassword123!',
      displayName: 'Test User 1'
    },
    {
      username: 'testuser2',
      email: 'test2@example.com',
      password: 'TestPassword123!',
      displayName: 'Test User 2'
    }
  ]

  process.env.TEST_USERS = JSON.stringify(testUsers)

  console.log('✅ Global setup completed')
}

async function globalTeardown(config) {
  console.log('🧹 Cleaning up global test setup')

  // 清理测试数据
  delete process.env.TEST_USERS

  console.log('✅ Global teardown completed')
}

module.exports = { globalSetup, globalTeardown }