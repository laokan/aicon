async function globalTeardown(config) {
  console.log('🧹 Global teardown for E2E tests')

  // 清理测试数据、关闭数据库连接等
  // 这里可以根据需要添加清理逻辑
}

module.exports = globalTeardown