import { ElMessage } from 'element-plus'
import { markRaw } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import { getAppConfig } from '@/config/runtimeConfig'

const resolveDefaultDuration = () => {
  const duration = getAppConfig()?.messageDuration
  if (!duration) return 3000
  const parsed = parseInt(duration, 10)
  return Number.isNaN(parsed) ? 3000 : parsed
}

const buildDefaultOptions = () => ({
  duration: resolveDefaultDuration(),
  offset: 24,
  showClose: false,
  grouping: true
})

const normalizeOptions = (options) => {
  if (typeof options === 'string') {
    return { message: options }
  }
  return options || {}
}

const messagePool = new Map()

const enhanceByType = (type, options) => {
  if (type === 'error' || type === 'warning') {
    return {
      showClose: true,
      duration: Math.max(options.duration || 0, 5000)
    }
  }
  if (type === 'success') {
    return {
      duration: options.duration || 2500
    }
  }
  return {}
}

const createMessage = (method, type = 'default') => (options) => {
  const normalized = {
    ...buildDefaultOptions(),
    ...normalizeOptions(options)
  }

  const dedupeKey =
    normalized.dedupe !== false
      ? normalized.key || `${type}-${normalized.message}`
      : null

  if (dedupeKey && messagePool.has(dedupeKey)) {
    const existing = messagePool.get(dedupeKey)
    existing.close?.()
    messagePool.delete(dedupeKey)
  }

  const merged = {
    ...normalized,
    ...enhanceByType(type, normalized)
  }

  const handler = method({
    ...merged,
    onClose: () => {
      if (dedupeKey) {
        messagePool.delete(dedupeKey)
      }
      merged.onClose?.()
    }
  })

  if (dedupeKey) {
    messagePool.set(dedupeKey, handler)
  }

  return handler
}

const message = createMessage(ElMessage)

;['success', 'warning', 'info', 'error'].forEach((type) => {
  message[type] = createMessage(ElMessage[type], type)
})

message.close = ElMessage.close
message.closeAll = ElMessage.closeAll

message.loading = (options = {}) => {
  const normalized = normalizeOptions(options)
  return ElMessage({
    ...buildDefaultOptions(),
    ...normalized,
    icon: normalized.icon || markRaw(Loading),
    duration: normalized.duration ?? 0,
    showClose: true,
    type: 'info',
    message: normalized.message || '加载中...'
  })
}

export default message

