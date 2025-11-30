<template>
  <header class="doctor-header">
    <div class="header-left">
      <el-icon 
        class="menu-toggle" 
        :size="24"
        @click="toggleSidebar"
      >
        <Menu />
      </el-icon>
      
      <nav class="breadcrumbs">
        <span 
          v-for="(item, index) in breadcrumbs" 
          :key="index"
          class="breadcrumb-item"
          :class="{ active: index === breadcrumbs.length - 1 }"
        >
          {{ item }}
          <span v-if="index < breadcrumbs.length - 1" class="separator">/</span>
        </span>
      </nav>
    </div>

    <div class="header-right">
      <!-- 消息提醒 -->
      <div class="notification-wrapper" :class="{ 'has-unread': hasUnreadNotifications }">
        <el-popover
          placement="bottom-end"
          trigger="hover"
          width="320"
          transition="el-zoom-in-top"
          popper-class="notification-popover"
        >
          <template #reference>
            <el-badge
              :value="unreadCount"
              :hidden="unreadCount === 0"
              :max="99"
              class="notification-badge"
            >
              <button class="notification-trigger" type="button">
                <el-icon :size="18">
                  <Bell />
                </el-icon>
                <span class="notification-text">消息提醒</span>
              </button>
            </el-badge>
          </template>

          <template v-if="unreadNotifications.length">
            <div class="notification-header">
              <span>未读消息（{{ unreadCount }}）</span>
              <el-button link size="small" @click="markAllNotificationsRead">全部标记已读</el-button>
            </div>
            <el-scrollbar max-height="260">
              <ul class="notification-list">
                <li v-for="item in unreadNotifications" :key="item.id" class="notification-item">
                  <div class="notification-title">{{ item.title || '系统通知' }}</div>
                  <div class="notification-content">{{ item.content }}</div>
                  <div class="notification-footer">
                    <span class="notification-time">{{ formatDateTime(item.createdAt) }}</span>
                    <el-button link type="primary" size="small" @click="markNotificationRead(item.id)">标记已读</el-button>
                  </div>
                </li>
              </ul>
            </el-scrollbar>
          </template>
          <template v-else>
            <div class="notification-empty">
              <el-icon :size="24">
                <Bell />
              </el-icon>
              <p>暂无未读消息</p>
            </div>
          </template>
        </el-popover>
      </div>

      <!-- 中医师名称 -->
      <span class="username">中医师：{{ userStore.userInfo.realName || userStore.userInfo.username }}</span>

      <!-- 用户头像下拉菜单 -->
      <el-dropdown class="avatar-dropdown" trigger="click" @command="handleCommand">
        <el-avatar class="avatar-trigger" :size="40" :src="avatarSrc">
          <el-icon>
            <User />
          </el-icon>
        </el-avatar>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="settings">
              <el-icon>
                <Setting />
              </el-icon> 个人设置
            </el-dropdown-item>
            <el-dropdown-item command="logout">
              <el-icon>
                <SwitchButton />
              </el-icon> 退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup>
import { computed, onMounted, onUnmounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElNotification } from 'element-plus'
import message from '@/plugins/message'
import { Menu, User, Bell, SwitchButton, Setting } from '@element-plus/icons-vue'
import { DEFAULT_AVATAR } from '@/constants/avatar'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notification'
import { getUserInfo } from '@/api/user'
import { markNotificationAsRead } from '@/api/notification'
import { markAllConversationsAsRead } from '@/api/dialogue'
import SockJS from 'sockjs-client'
import { Client } from '@stomp/stompjs'
import dayjs from 'dayjs'
import { getAppConfig } from '@/config/runtimeConfig'

const props = defineProps({
  breadcrumbs: {
    type: Array,
    default: () => []
  },
  sidebarOpen: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['toggle-sidebar'])

const router = useRouter()
const userStore = useUserStore()
const notificationStore = useNotificationStore()
const appConfig = inject('appConfig', getAppConfig())

let stompClient = null

const avatarSrc = computed(() => userStore.userInfo?.avatar || DEFAULT_AVATAR)
const unreadNotifications = computed(() => notificationStore.unread || [])
const unreadCount = computed(() => unreadNotifications.value.length)
const hasUnreadNotifications = computed(() => unreadCount.value > 0)

const toggleSidebar = () => {
  emit('toggle-sidebar')
}

const handleCommand = (command) => {
  if (command === 'settings') {
    router.push('/doctor/settings')
  } else if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      await userStore.logout()
      disconnectNotificationSocket()
      notificationStore.clear()
      message.success('已退出登录')
      router.push('/login')
    }).catch(() => { })
  }
}

const refreshUserInfo = async () => {
  try {
    const res = await getUserInfo()
    if (res.code === 200 && res.data) {
      userStore.setUserInfo(res.data)
    }
  } catch (error) {
    // 静默失败
  }
}

const connectNotificationSocket = () => {
  const token = userStore.token
  if (!token) return
  if (stompClient?.connected) {
    return
  }

  stompClient = new Client({
    webSocketFactory: () => new SockJS(`/ws?token=${encodeURIComponent(token)}`),
    reconnectDelay: 5000,
    heartbeatIncoming: 10000,
    heartbeatOutgoing: 10000
  })

  stompClient.onConnect = () => {
    stompClient.subscribe('/user/queue/notifications', (message) => {
      if (!message.body) return
      try {
        const payload = JSON.parse(message.body)
        notificationStore.addNotification(payload)
        ElNotification({
          title: payload.title || '新提醒',
          message: payload.content,
          type: 'info',
          duration: 5000
        })
      } catch (error) {
        // 静默失败
      }
    })
  }

  stompClient.onStompError = (frame) => {
    // 静默失败
  }

  stompClient.onWebSocketError = (event) => {
    // 静默失败
  }

  stompClient.activate()
}

const disconnectNotificationSocket = () => {
  if (stompClient) {
    try {
      stompClient.deactivate()
    } catch (error) {
      // 静默失败
    }
    stompClient = null
  }
}

const formatDateTime = (value) => {
  if (!value) return ''
  return dayjs(value).format('YYYY-MM-DD HH:mm')
}

const markNotificationRead = async (notificationId) => {
  try {
    const res = await markNotificationAsRead(notificationId)
    if (res.code === 200) {
      notificationStore.removeNotification(notificationId)
    }
  } catch (error) {
    message.error('标记通知失败')
  }
}

const markAllNotificationsRead = async () => {
  if (!unreadNotifications.value.length) return
  try {
    // 标记所有通知为已读
    await Promise.all(unreadNotifications.value.map(item => markNotificationAsRead(item.id)))
    notificationStore.clear()
    
    // 同时标记所有对话为已读
    try {
      const params = {
        role: 'DOCTOR'
      }
      if (userStore.userInfo?.id) {
        params.userId = userStore.userInfo.id
      }
      await markAllConversationsAsRead(params)
      // 触发自定义事件，通知对话页面刷新
      window.dispatchEvent(new CustomEvent('conversations-marked-all-read', { 
        detail: { role: 'DOCTOR', userId: userStore.userInfo?.id } 
      }))
    } catch (conversationError) {
      // 对话标记失败不影响通知标记，只记录错误
      console.warn('标记所有对话为已读失败:', conversationError)
    }
    
    message.success('已全部标记为已读')
  } catch (error) {
    message.error('全部标记已读失败')
  }
}

onMounted(async () => {
  await refreshUserInfo()
  await notificationStore.fetchUnread()
  connectNotificationSocket()
})

onUnmounted(() => {
  disconnectNotificationSocket()
})
</script>

<style scoped lang="scss">
.doctor-header {
  height: 50px;
  background: #009688;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;

  .header-left {
    display: flex;
    align-items: center;
    gap: 16px;

    .menu-toggle {
      cursor: pointer;
      padding: 4px;
      border-radius: 4px;
      transition: all 0.2s;

      &:hover {
        background: rgba(255, 255, 255, 0.1);
      }
    }

    .breadcrumbs {
      display: flex;
      align-items: center;
      font-size: 14px;

      .breadcrumb-item {
        opacity: 0.8;

        &.active {
          opacity: 1;
          font-weight: 500;
        }

        .separator {
          margin: 0 8px;
          opacity: 0.6;
        }
      }
    }
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 18px;
    font-size: 14px;

    .notification-wrapper {
      position: relative;
      display: flex;
      align-items: center;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.1);
      transition: all 0.2s;

      &.has-unread {
        background: rgba(255, 255, 255, 0.15);
      }

      .notification-trigger {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border: none;
        background: transparent;
        color: white;
        cursor: pointer;
        font-size: 14px;
      }

      .notification-text {
        white-space: nowrap;
      }
    }

    .username {
      font-size: 14px;
      white-space: nowrap;
    }

    .avatar-dropdown {
      :deep(.avatar-trigger) {
        cursor: pointer;
        border: 2px solid rgba(255, 255, 255, 0.3);
        transition: all 0.2s;
        background: rgba(255, 255, 255, 0.1);

        &:hover {
          border-color: rgba(255, 255, 255, 0.5);
          background: rgba(255, 255, 255, 0.15);
        }
      }
    }
  }
}

:deep(.notification-popover) {
  padding: 12px 0 0 !important;
}

:deep(.notification-header) {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px 8px;
  font-size: 14px;
  font-weight: 500;
  color: #1f2933;

  .el-button {
    padding: 0 4px;
  }
}

:deep(.notification-list) {
  list-style: none;
  margin: 0;
  padding: 0 16px 12px;

  .notification-item {
    padding: 10px 0;
    border-bottom: 1px dashed #e9e9e9;

    &:last-child {
      border-bottom: none;
    }

    .notification-title {
      font-size: 14px;
      font-weight: 600;
      color: #1f2933;
      margin-bottom: 4px;
    }

    .notification-content {
      font-size: 13px;
      color: #4a5568;
      line-height: 1.5;
      margin-bottom: 6px;
    }

    .notification-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: #94a3b8;
    }
  }
}

:deep(.notification-empty) {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 20px 0 24px;
  color: #94a3b8;

  p {
    margin: 0;
    font-size: 13px;
  }
}
</style>

