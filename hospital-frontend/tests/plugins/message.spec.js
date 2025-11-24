import { describe, it, expect, vi, beforeEach } from 'vitest'
import message from '@/plugins/message'
import { ElMessage } from 'element-plus'

const mocks = vi.hoisted(() => {
  const createHandler = () => ({ close: vi.fn() })
  const createMethod = () => vi.fn(() => createHandler())
  return { createMethod }
})

vi.mock('@/config/runtimeConfig', () => ({
  getAppConfig: () => ({
    messageDuration: 3200
  })
}))

vi.mock('element-plus', () => {
  const base = mocks.createMethod()
  base.success = mocks.createMethod()
  base.warning = mocks.createMethod()
  base.info = mocks.createMethod()
  base.error = mocks.createMethod()
  base.close = vi.fn()
  base.closeAll = vi.fn()
  return { ElMessage: base }
})

describe('message plugin', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('deduplicates identical success messages', () => {
    const firstHandler = message.success('操作成功')
    message.success('操作成功')

    expect(firstHandler.close).toHaveBeenCalledTimes(1)
    expect(ElMessage.success).toHaveBeenCalledTimes(2)
  })

  it('extends duration for error type messages', () => {
    message.error({ message: '失败', duration: 1000 })

    const lastCallArgs = ElMessage.error.mock.calls.at(-1)[0]
    expect(lastCallArgs.duration).toBeGreaterThanOrEqual(5000)
    expect(lastCallArgs.showClose).toBe(true)
  })

  it('provides loading helper with zero duration', () => {
    message.loading()

    expect(ElMessage).toHaveBeenCalledTimes(1)
    const payload = ElMessage.mock.calls[0][0]
    expect(payload.duration).toBe(0)
    expect(payload.message).toBe('加载中...')
    expect(payload.type).toBe('info')
  })
})


