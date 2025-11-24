const defaultConfig = {
  apiBaseUrl: '/api',
  wsBaseUrl: '/ws',
  requestTimeout: 10000,
  messageDuration: 3000,
  defaultAvatars: {
    patient: 'https://api.dicebear.com/7.x/thumbs/svg?seed=patient',
    doctor: 'https://api.dicebear.com/7.x/thumbs/svg?seed=doctor',
    system: 'https://api.dicebear.com/7.x/shapes/svg?seed=assistant'
  },
  basic: {
    advanceDays: 7,
    cancelHours: 2,
    paymentTimeout: 30
  },
  systemInfo: {
    name: '中医体质辨识系统',
    version: 'v1.0.0',
    maintenanceMode: false
  },
  notification: {
    appointmentReminder: true,
    reminderHours: 2,
    smsEnabled: false,
    emailEnabled: false,
    systemEnabled: true
  },
  security: {
    minPasswordLength: 6,
    loginLockEnabled: false,
    maxLoginAttempts: 5,
    lockDurationMinutes: 15,
    sessionTimeoutMinutes: 120
  },
  email: {
    smtpHost: '',
    smtpPort: 587,
    fromEmail: '',
    sslEnabled: true
  }
}

let appConfig = { ...defaultConfig }
let configLoaded = false
let loadPromise = null

const toBoolean = (value, fallback = false) => {
  if (typeof value === 'boolean') return value
  if (typeof value === 'number') return value !== 0
  if (typeof value === 'string') {
    const normalized = value.trim().toLowerCase()
    if (['true', '1', 'yes', 'on'].includes(normalized)) return true
    if (['false', '0', 'no', 'off'].includes(normalized)) return false
  }
  return fallback
}

const normalizeConfig = (config = {}) => {
  return {
    apiBaseUrl: config.apiBaseUrl || defaultConfig.apiBaseUrl,
    wsBaseUrl: config.wsBaseUrl || defaultConfig.wsBaseUrl,
    requestTimeout: Number.parseInt(config.requestTimeout ?? defaultConfig.requestTimeout, 10),
    messageDuration: Number.parseInt(config.messageDuration ?? defaultConfig.messageDuration, 10),
    defaultAvatars: {
      patient: config.defaultAvatars?.patient || defaultConfig.defaultAvatars.patient,
      doctor: config.defaultAvatars?.doctor || defaultConfig.defaultAvatars.doctor,
      system: config.defaultAvatars?.system || defaultConfig.defaultAvatars.system
    },
    basic: {
      advanceDays: Number.parseInt(config.basic?.advanceDays ?? defaultConfig.basic.advanceDays, 10),
      cancelHours: Number.parseInt(config.basic?.cancelHours ?? defaultConfig.basic.cancelHours, 10),
      paymentTimeout: Number.parseInt(config.basic?.paymentTimeout ?? defaultConfig.basic.paymentTimeout, 10)
    },
    systemInfo: {
      name: config.systemInfo?.name || defaultConfig.systemInfo.name,
      version: config.systemInfo?.version || defaultConfig.systemInfo.version,
      maintenanceMode: toBoolean(config.systemInfo?.maintenanceMode, defaultConfig.systemInfo.maintenanceMode)
    },
    notification: {
      appointmentReminder: toBoolean(config.notification?.appointmentReminder, defaultConfig.notification.appointmentReminder),
      reminderHours: Number.parseInt(config.notification?.reminderHours ?? defaultConfig.notification.reminderHours, 10),
      smsEnabled: toBoolean(config.notification?.smsEnabled, defaultConfig.notification.smsEnabled),
      emailEnabled: toBoolean(config.notification?.emailEnabled, defaultConfig.notification.emailEnabled),
      systemEnabled: toBoolean(config.notification?.systemEnabled, defaultConfig.notification.systemEnabled)
    },
    security: {
      minPasswordLength: Number.parseInt(config.security?.minPasswordLength ?? defaultConfig.security.minPasswordLength, 10),
      loginLockEnabled: toBoolean(config.security?.loginLockEnabled, defaultConfig.security.loginLockEnabled),
      maxLoginAttempts: Number.parseInt(config.security?.maxLoginAttempts ?? defaultConfig.security.maxLoginAttempts, 10),
      lockDurationMinutes: Number.parseInt(config.security?.lockDurationMinutes ?? defaultConfig.security.lockDurationMinutes, 10),
      sessionTimeoutMinutes: Number.parseInt(config.security?.sessionTimeoutMinutes ?? defaultConfig.security.sessionTimeoutMinutes, 10)
    },
    email: {
      smtpHost: config.email?.smtpHost || defaultConfig.email.smtpHost,
      smtpPort: Number.parseInt(config.email?.smtpPort ?? defaultConfig.email.smtpPort, 10),
      fromEmail: config.email?.fromEmail || defaultConfig.email.fromEmail,
      sslEnabled: toBoolean(config.email?.sslEnabled, defaultConfig.email.sslEnabled)
    }
  }
}

const assignAndMarkLoaded = (config) => {
  appConfig = normalizeConfig(config)
  configLoaded = true
  if (typeof window !== 'undefined') {
    window.__APP_CONFIG__ = appConfig
  }
  return appConfig
}

export const loadAppConfig = async () => {
  if (configLoaded && !loadPromise) {
    return appConfig
  }

  if (!loadPromise) {
    // 尝试从 localStorage 获取 token（如果存在）
    let token = null
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        token = window.localStorage.getItem('token')
      }
    } catch (e) {
      // localStorage 访问失败，忽略
    }

    // 构建请求配置
    const fetchOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }

    // 如果存在 token，添加到请求头
    if (token) {
      fetchOptions.headers['Authorization'] = `Bearer ${token}`
    }

    loadPromise = fetch('/api/config', fetchOptions)
      .then(async (response) => {
        if (!response.ok) {
          // 如果是 401 且没有 token，使用默认配置（这是正常的，用户可能未登录）
          if (response.status === 401 && !token) {
            console.log('[runtime-config] 未登录状态，使用默认配置')
            return assignAndMarkLoaded(defaultConfig)
          }
          throw new Error(`获取配置失败，HTTP ${response.status}`)
        }
        const payload = await response.json()
        if (payload?.code === 200 && payload.data) {
          return assignAndMarkLoaded(payload.data)
        }
        // 如果业务状态码不是 200，但也不是认证错误，使用默认配置
        if (payload?.code === 401 && !token) {
          console.log('[runtime-config] 未登录状态，使用默认配置')
          return assignAndMarkLoaded(defaultConfig)
        }
        throw new Error(payload?.message || '配置中心返回异常')
      })
      .catch((error) => {
        console.error('[runtime-config] 无法从后端加载配置，使用默认值', error)
        return assignAndMarkLoaded(defaultConfig)
      })
      .finally(() => {
        loadPromise = null
      })
  }

  return loadPromise
}

export const getAppConfig = () => {
  if (!configLoaded && typeof window !== 'undefined' && window.__APP_CONFIG__) {
    appConfig = normalizeConfig(window.__APP_CONFIG__)
    configLoaded = true
  }
  return appConfig
}

export const refreshAppConfig = async () => {
  // 尝试从 localStorage 获取 token
  let token = null
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      token = window.localStorage.getItem('token')
    }
  } catch (e) {
    // localStorage 访问失败，忽略
  }

  const fetchOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  }

  if (token) {
    fetchOptions.headers['Authorization'] = `Bearer ${token}`
  }

  const payload = await fetch('/api/config', fetchOptions).then(res => res.json()).catch(() => null)
  if (payload?.code === 200 && payload.data) {
    assignAndMarkLoaded(payload.data)
  }
  return appConfig
}

