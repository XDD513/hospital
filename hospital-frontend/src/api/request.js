import axios from 'axios'
import message from '@/plugins/message'
import { useUserStore } from '@/stores/user'
import router from '@/router'
import { retryRequest } from '@/utils/retryRequest'

// 创建axios实例，默认使用本地代理
const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const configureRequestClient = (config) => {
  if (!config) return
  if (config.apiBaseUrl) {
    request.defaults.baseURL = config.apiBaseUrl
  }
  if (config.requestTimeout) {
    const parsed = parseInt(config.requestTimeout, 10)
    if (!Number.isNaN(parsed)) {
      request.defaults.timeout = parsed
    }
  }
}

// 标记是否正在跳转登录页，防止多个请求同时失败时重复跳转和显示消息
let isRedirectingToLogin = false

// 处理token失效的统一方法
const handleTokenExpired = () => {
  // 如果已经在跳转中，直接返回（不显示错误消息，不执行任何操作）
  if (isRedirectingToLogin) {
    return
  }
  
  // 立即设置标记，阻止所有后续的错误消息显示（必须在最前面）
  isRedirectingToLogin = true
  
  // 立即关闭所有现有的消息提示，避免显示多个错误消息
  message.closeAll()
  
  const userStore = useUserStore()
  
  // 清除用户信息和token
  userStore.clearUserInfo()
  
  // 使用nextTick确保在关闭所有消息后再显示新消息
  setTimeout(() => {
    // 显示统一的登录过期提示（只显示一次）
    message.warning('登录已过期，请重新登录')
  }, 100)
  
  // 跳转到登录页
  router.push('/login').finally(() => {
    // 延迟重置标记，允许后续的错误处理
    setTimeout(() => {
      isRedirectingToLogin = false
    }, 1000)
  })
}

// 判断是否为token失效错误（需要跳转登录页的错误）
// 仅针对明确的认证错误：HTTP 401 或业务状态码 401
// HTTP 403 可能是权限不足，不是token失效，所以不在这里处理
const isTokenExpired = (status, code) => {
  // HTTP状态码 401（未授权）或业务状态码 401（token失效/未登录）
  // 注意：HTTP 403 可能是权限不足，不是token失效，所以不跳转登录页
  return status === 401 || code === 401
}

// 请求拦截器
request.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    // 如果存在token，添加到请求头
    if (userStore.token) {
      config.headers['Authorization'] = `Bearer ${userStore.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    // 如果正在跳转登录页，直接返回响应，不处理错误消息
    if (isRedirectingToLogin) {
      return response.data
    }
    
    // 文件下载（如导出Excel）直接返回二进制数据
    if (response.config?.responseType === 'blob') {
      return response.data
    }

    const res = response.data
    
    // 如果返回的状态码不是200，说明接口请求有问题
    if (res.code !== 200) {
      // 判断是否为token失效错误
      if (isTokenExpired(null, res.code)) {
        // token失效，统一处理为跳转登录页，不显示业务错误消息
        handleTokenExpired()
        // 返回reject，但不显示错误消息
        return Promise.reject(new Error('Token expired'))
      } else {
        // 其他业务错误（权限不足、参数错误等），但如果在跳转登录页中，则不显示错误消息
        if (!isRedirectingToLogin) {
          message.error(res.message || '请求失败')
        }
      }
      
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    
    return res
  },
  error => {
    // 如果正在跳转登录页，不处理任何错误消息
    if (isRedirectingToLogin) {
      return Promise.reject(error)
    }
    
    let errorMessage = '网络错误'
    
    if (error.response) {
      const status = error.response.status
      const data = error.response.data
      
      // 判断是否为token失效错误
      if (isTokenExpired(status, data?.code)) {
        // token失效，统一处理为跳转登录页，不显示错误消息
        handleTokenExpired()
        // 直接返回，不继续处理
        return Promise.reject(error)
      } else {
        // 其他HTTP错误（403权限不足、404找不到、500服务器错误等）
        // 再次检查标记，因为handleTokenExpired可能是异步的
        if (!isRedirectingToLogin) {
          switch (status) {
            case 403:
              errorMessage = data?.message || '没有权限访问该资源'
              break
            case 404:
              errorMessage = '请求地址不存在'
              break
            case 500:
              errorMessage = '服务器内部错误'
              break
            default:
              errorMessage = data?.message || '请求失败'
          }
          message.error(errorMessage)
        }
      }
    } else if (error.request) {
      // 请求已发出，但没有收到响应（网络错误）
      // 标记为可重试错误，让重试机制处理
      error._shouldRetry = true
      if (!isRedirectingToLogin) {
        errorMessage = '网络连接失败，请检查网络'
        // 网络错误不立即显示消息，让重试机制处理
      }
    } else {
      // 请求配置出错
      if (!isRedirectingToLogin) {
        errorMessage = '请求配置错误'
        message.error(errorMessage)
      }
    }
    
    return Promise.reject(error)
  }
)

// 保存原始的 request 方法
const originalRequest = request.request.bind(request)

// 重写 request 方法，添加自动重试功能
request.request = function(config) {
  // 如果配置中明确禁用重试，直接使用原始请求
  if (config?.retry === false) {
    return originalRequest(config)
  }
  
  // 默认启用重试（最多3次）
  const maxRetries = config?.maxRetries ?? 3
  const baseDelay = config?.retryDelay ?? 500
  const silentRetry = config?.silentRetry ?? false
  
  return retryRequest(
    () => originalRequest(config),
    {
      maxRetries,
      baseDelay,
      silent: silentRetry,
      shouldRetry: (error) => {
        // 401/403 认证/授权错误不应该重试
        if (error.response) {
          const status = error.response.status
          if (status === 401 || status === 403 || status === 400) {
            return false
          }
          // 5xx 服务器错误应该重试
          if (status >= 500 && status < 600) {
            return true
          }
          // 429 请求过多应该重试
          if (status === 429) {
            return true
          }
        }
        
        // 网络错误（没有响应）应该重试
        if (error.request && !error.response) {
          return true
        }
        
        // 超时错误应该重试
        if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
          return true
        }
        
        // 标记为可重试的错误
        if (error._shouldRetry) {
          return true
        }
        
        return false
      },
      onRetry: (attempt, error, delayMs) => {
        if (!silentRetry && import.meta.env.DEV) {
          console.log(`[请求重试] ${config?.url || config?.method || '请求'} 第 ${attempt} 次重试，延迟 ${delayMs}ms`)
        }
      }
    }
  )
}

export default request


