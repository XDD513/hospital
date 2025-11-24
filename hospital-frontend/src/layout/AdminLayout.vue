<template>
  <div class="layout-container">
    <!-- 顶部导航栏 -->
    <el-header class="header admin-header">
      <div class="header-left">
        <el-icon class="logo-icon" :size="32">
          <Setting />
        </el-icon>
        <span class="logo-text">{{ adminLogoText }}</span>
      </div>
      <div class="header-right">
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

        <span class="username">管理员：{{ userStore.userInfo.realName || userStore.userInfo.username }}</span>
        <el-dropdown class="avatar-dropdown" trigger="click" @command="handleCommand">
          <el-avatar class="avatar-trigger" :size="40" :src="avatarSrc">
            <el-icon>
              <User />
            </el-icon>
          </el-avatar>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">
                <el-icon>
                  <User />
                </el-icon> 个人信息
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
    </el-header>

    <!-- 主体内容 -->
    <el-container class="main-container">
      <!-- 侧边栏 -->
      <el-aside width="220px" class="sidebar">
        <el-menu :default-active="activeMenu" router class="menu">
          <el-menu-item index="/admin/dashboard">
            <el-icon>
              <DataAnalysis />
            </el-icon>
            <span>系统概览</span>
          </el-menu-item>
          <el-menu-item index="/admin/departments">
            <el-icon>
              <OfficeBuilding />
            </el-icon>
            <span>中医分类管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/doctors">
            <el-icon>
              <User />
            </el-icon>
            <span>中医师管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/users">
            <el-icon>
              <UserFilled />
            </el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/schedules">
            <el-icon>
              <Calendar />
            </el-icon>
            <span>排班管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/appointments">
            <el-icon>
              <Document />
            </el-icon>
            <span>预约管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/settings">
            <el-icon>
              <Tools />
            </el-icon>
            <span>系统设置</span>
          </el-menu-item>
          <el-menu-item index="/admin/settings/test">
            <el-icon>
              <TrendCharts />
            </el-icon>
            <span>设置生效检测</span>
          </el-menu-item>
          <el-menu-item index="/admin/statistics">
            <el-icon>
              <TrendCharts />
            </el-icon>
            <span>数据统计</span>
          </el-menu-item>
          <el-menu-item index="/admin/logs">
            <el-icon>
              <Tickets />
            </el-icon>
            <span>操作日志</span>
          </el-menu-item>
          <el-menu-item index="/admin/dialogue">
            <el-icon>
              <ChatLineRound />
            </el-icon>
            <span>智能对话</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 内容区 -->
      <el-main class="content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, onUnmounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox, ElNotification } from 'element-plus'
import message from '@/plugins/message'
import { Bell, User, SwitchButton, Setting, DataAnalysis, OfficeBuilding, Calendar, Document, Tools, TrendCharts, Tickets, ChatLineRound } from '@element-plus/icons-vue'
import { getUserInfo } from '@/api/user'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notification'
import SockJS from 'sockjs-client'
import { Client } from '@stomp/stompjs'
import dayjs from 'dayjs'
import { markNotificationAsRead } from '@/api/notification'
import { markAllConversationsAsRead } from '@/api/dialogue'
import { DEFAULT_AVATAR } from '@/constants/avatar'
import { getAppConfig } from '@/config/runtimeConfig'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const notificationStore = useNotificationStore()
const appConfig = inject('appConfig', getAppConfig())
const systemName = computed(() => appConfig?.systemInfo?.name || '中医体质辨识系统')
const adminLogoText = computed(() => `${systemName.value} - 管理后台`)

let stompClient = null

const activeMenu = computed(() => route.path)

const unreadNotifications = computed(() => notificationStore.unread || [])
const unreadCount = computed(() => unreadNotifications.value.length)
const hasUnreadNotifications = computed(() => unreadCount.value > 0)
const avatarSrc = computed(() => userStore.userInfo?.avatar || DEFAULT_AVATAR)

const handleCommand = (command) => {
  if (command === 'profile') {
    router.push('/admin/profile')
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

      }
    })
  }

  stompClient.onStompError = (frame) => {

  }

  stompClient.onWebSocketError = (event) => {

  }

  stompClient.activate()
}

const disconnectNotificationSocket = () => {
  if (stompClient) {
    try {
      stompClient.deactivate()
    } catch (error) {

    }
    stompClient = null
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
        role: 'ADMIN'
      }
      if (userStore.userInfo?.id) {
        params.userId = userStore.userInfo.id
      }
      await markAllConversationsAsRead(params)
      // 触发自定义事件，通知对话页面刷新
      window.dispatchEvent(new CustomEvent('conversations-marked-all-read', { 
        detail: { role: 'ADMIN', userId: userStore.userInfo?.id } 
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
</script>

<style scoped lang="scss">
.layout-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.admin-header {
  background: linear-gradient(135deg, #e6a23c 0%, #f56c6c 100%) !important;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;

    .logo-icon {
      font-size: 32px;
    }

    .logo-text {
      font-size: 20px;
      font-weight: bold;
    }
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 18px;

    .notification-wrapper {
      position: relative;
      display: flex;
      align-items: center;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.18);
      transition: all 0.3s ease;

      &.has-unread {
        background: rgba(255, 255, 255, 0.28);
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.4);

        .notification-trigger {
          color: #fff5f0;
        }

        .el-badge__content.is-fixed {
          background-color: #ff4d4f;
        }
      }

      .notification-trigger {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border: none;
        background: transparent;
        color: #f0f5ff;
        cursor: pointer;
        font-size: 14px;
      }

      .notification-text {
        white-space: nowrap;
      }
    }

    .username {
      font-size: 14px;
    }

    .avatar-dropdown {
      :deep(.avatar-trigger) {
        cursor: pointer;
        border: 2px solid transparent;
        transition: all 0.3s;
        background: rgba(255, 255, 255, 0.08);

        &:hover {
          border-color: rgba(255, 255, 255, 0.85);
          background: rgba(255, 255, 255, 0.2);
          box-shadow: 0 0 12px rgba(255, 255, 255, 0.35);
        }
      }
    }
  }
}

.notification-popover {
  padding: 12px 0 0 !important;
}

.notification-header {
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

.notification-list {
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

.notification-empty {
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

.main-container {
  flex: 1;
  overflow: hidden;
}

.sidebar {
  background: #fff;
  border-right: 1px solid #e0e0e0;
  overflow-y: auto;

  .menu {
    border-right: none;
  }
}

.content {
  background: #f5f5f5;
  overflow-y: auto;
  padding: 20px;
}

:deep(.el-menu-item) {
  &.is-active {
    background: linear-gradient(90deg, #e6a23c 0%, #f56c6c 100%);
    color: white !important;

    .el-icon {
      color: white !important;
    }
  }
}
</style>
