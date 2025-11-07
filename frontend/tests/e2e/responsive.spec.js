import { test, expect } from '@playwright/test'
import { setViewport, takeScreenshot } from './utils/test-helpers.js'

test.describe('响应式认证页面测试', () => {
  const devices = [
    { name: 'Desktop', width: 1280, height: 720 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Mobile', width: 375, height: 667 }
  ]

  devices.forEach(device => {
    test.describe(`${device.name} - Login Page`, () => {
      test.beforeEach(async ({ page }) => {
        await setViewport(page, device.name.toLowerCase())
        await page.goto('/login')
      })

      test(`should display login page correctly on ${device.name}`, async ({ page }) => {
        // 验证页面标题
        await expect(page.locator('h2')).toContainText('登录')

        // 验证表单元素存在
        await expect(page.locator('input[placeholder="请输入用户名"]')).toBeVisible()
        await expect(page.locator('input[placeholder="请输入密码"]')).toBeVisible()
        await expect(page.locator('button:has-text("登录")')).toBeVisible()

        // 验证注册链接
        await expect(page.locator('text=立即注册')).toBeVisible()

        // 截图
        await takeScreenshot(page, `login-${device.name.toLowerCase()}`)
      })

      test(`should handle form interaction on ${device.name}`, async ({ page }) => {
        // 填写表单
        await page.fill('input[placeholder="请输入用户名"]', 'testuser')
        await page.fill('input[placeholder="请输入密码"]', 'password123')

        // 验证输入成功
        await expect(page.locator('input[placeholder="请输入用户名"]')).toHaveValue('testuser')
        await expect(page.locator('input[placeholder="请输入密码"]')).toHaveValue('password123')

        // 截图：表单填写完成
        await takeScreenshot(page, `login-filled-${device.name.toLowerCase()}`)
      })

      test(`should show validation errors on ${device.name}`, async ({ page }) => {
        // 提交空表单
        await page.click('button:has-text("登录")')

        // 验证错误消息显示
        await expect(page.locator('text=请输入用户名')).toBeVisible()
        await expect(page.locator('text=请输入密码')).toBeVisible()

        // 截图：验证错误
        await takeScreenshot(page, `login-errors-${device.name.toLowerCase()}`)
      })
    })

    test.describe(`${device.name} - Register Page`, () => {
      test.beforeEach(async ({ page }) => {
        await setViewport(page, device.name.toLowerCase())
        await page.goto('/register')
      })

      test(`should display register page correctly on ${device.name}`, async ({ page }) => {
        // 验证页面标题
        await expect(page.locator('h2')).toContainText('注册')

        // 验证所有表单字段存在
        await expect(page.locator('input[placeholder="请输入用户名"]')).toBeVisible()
        await expect(page.locator('input[placeholder="请输入邮箱"]')).toBeVisible()
        await expect(page.locator('input[placeholder="请输入密码"]')).toBeVisible()
        await expect(page.locator('input[placeholder="请确认密码"]')).toBeVisible()

        // 验证登录链接
        await expect(page.locator('text=立即登录')).toBeVisible()

        // 截图
        await takeScreenshot(page, `register-${device.name.toLowerCase()}`)
      })

      test(`should handle long form on ${device.name}`, async ({ page }) => {
        // 填写所有字段
        await page.fill('input[placeholder="请输入用户名"]', 'verylongusername')
        await page.fill('input[placeholder="请输入邮箱"]', 'verylongemail@example.com')
        await page.fill('input[placeholder="请输入密码"]', 'verylongpassword123')
        await page.fill('input[placeholder="请确认密码"]', 'verylongpassword123')

        // 验证所有字段都有值
        const inputs = page.locator('input')
        const count = await inputs.count()
        for (let i = 0; i < count; i++) {
          const input = inputs.nth(i)
          const value = await input.inputValue()
          expect(value).not.toBe('')
        }

        // 截图：长表单
        await takeScreenshot(page, `register-long-${device.name.toLowerCase()}`)
      })
    })

    test.describe(`${device.name} - Profile Page`, () => {
      test.beforeEach(async ({ page }) => {
        await setViewport(page, device.name.toLowerCase())

        // 登录
        await page.goto('/login')
        await page.fill('input[placeholder="请输入用户名"]', 'testuser1')
        await page.fill('input[placeholder="请输入密码"]', 'TestPassword123!')
        await page.click('button:has-text("登录")')
        await page.waitForURL(/\/dashboard/)

        // 跳转到profile页面
        await page.goto('/profile')
      })

      test(`should display profile page correctly on ${device.name}`, async ({ page }) => {
        // 验证页面标题
        await expect(page.locator('h1')).toContainText('个人资料')

        // 验证用户信息区域
        await expect(page.locator('.el-avatar')).toBeVisible()
        await expect(page.locator('text=Profile Information')).toBeVisible()
        await expect(page.locator('text=Change Password')).toBeVisible()

        // 截图
        await takeScreenshot(page, `profile-${device.name.toLowerCase()}`)
      })

      test(`should handle profile forms on ${device.name}`, async ({ page }) => {
        // 测试信息更新表单
        await page.fill('input[placeholder="Enter display name"]', 'Updated Name')

        // 验证输入成功
        await expect(page.locator('input[placeholder="Enter display name"]')).toHaveValue('Updated Name')

        // 截图：profile表单交互
        await takeScreenshot(page, `profile-form-${device.name.toLowerCase()}`)
      })
    })

    test.describe(`${device.name} - Navigation`, () => {
      test(`should handle navigation correctly on ${device.name}`, async ({ page }) => {
        await setViewport(page, device.name.toLowerCase())
        await page.goto('/')

        // 如果移动设备，可能需要点击菜单按钮
        if (device.name === 'Mobile') {
          const menuButton = page.locator('.el-menu--collapse, .mobile-menu-button')
          if (await menuButton.isVisible()) {
            await menuButton.click()
          }
        }

        // 验证导航链接
        await expect(page.locator('text=Dashboard')).toBeVisible()

        // 截图：导航
        await takeScreenshot(page, `navigation-${device.name.toLowerCase()}`)
      })
    })

    test.describe(`${device.name} - Orientation Tests`, () => {
      if (device.name === 'Mobile') {
        test(`should handle mobile landscape orientation`, async ({ page }) => {
          await page.setViewportSize({ width: 667, height: 375 }) // 横屏
          await page.goto('/login')

          // 验证页面在横屏模式下正常显示
          await expect(page.locator('h2')).toContainText('登录')
          await expect(page.locator('input[placeholder="请输入用户名"]')).toBeVisible()

          // 截图：移动端横屏
          await takeScreenshot(page, `login-mobile-landscape`)
        })

        test(`should handle mobile portrait orientation`, async ({ page }) => {
          await page.setViewportSize({ width: 375, height: 667 }) // 竖屏
          await page.goto('/login')

          // 验证页面在竖屏模式下正常显示
          await expect(page.locator('h2')).toContainText('登录')
          await expect(page.locator('input[placeholder="请输入用户名"]')).toBeVisible()

          // 截图：移动端竖屏
          await takeScreenshot(page, `login-mobile-portrait`)
        })
      }
    })
  })

  test.describe('跨设备一致性测试', () => {
    test('should maintain consistent functionality across devices', async ({ page }) => {
      // 测试关键功能在不同设备上的一致性
      const keyFlows = [
        { name: 'Login', url: '/login', selector: 'input[placeholder="请输入用户名"]' },
        { name: 'Register', url: '/register', selector: 'input[placeholder="请输入用户名"]' },
        { name: 'Dashboard', url: '/dashboard', selector: 'text=仪表板' }
      ]

      for (const device of devices) {
        await page.setViewportSize({ width: device.width, height: device.height })

        for (const flow of keyFlows) {
          await page.goto(flow.url)
          await expect(page.locator(flow.selector)).toBeVisible()

          // 截图：跨设备一致性
          await takeScreenshot(page, `${flow.name.toLowerCase()}-${device.name.toLowerCase()}-consistent`)
        }
      }
    })
  })
})