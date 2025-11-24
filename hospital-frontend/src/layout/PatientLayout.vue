<template>
  <div class="layout-container" @touchstart="handleTouchStart" @touchend="handleTouchEnd">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-left">
        <button class="menu-toggle" v-if="isMobile" @click="sidebarDrawerVisible = true">
          <el-icon :size="20">
            <Menu />
          </el-icon>
        </button>
        <el-icon class="logo-icon" :size="32">
          <Van />
        </el-icon>
        <span class="logo-text">{{ patientLogoText }}</span>
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

        <span class="username">{{ userStore.userInfo.realName || userStore.userInfo.username }}</span>
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
                </el-icon> 个人中心
              </el-dropdown-item>
              <el-dropdown-item command="notifications">
                <el-icon>
                  <Bell />
                </el-icon> 消息中心
              </el-dropdown-item>
              <el-dropdown-item command="logout" divided>
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
      <el-aside v-if="!isMobile" width="220px" class="sidebar">
        <PatientSidebarMenu :active-menu="activeMenu" @select="handleMenuSelect" />
      </el-aside>

      <!-- 内容区 -->
      <el-main class="content">
        <router-view />
      </el-main>
    </el-container>

    <!-- 右下角聊天按钮 -->
    <div class="chat-float-button" @click="handleChatButtonClick">
      <el-icon :size="24">
        <Close v-if="chatWidgetVisible" />
        <ChatLineRound v-else />
      </el-icon>
    </div>

    <!-- 聊天窗口组件 -->
    <ChatWidget 
      :visible="chatWidgetVisible" 
      :conversationId="adminConversationId"
      @close="handleChatClose" 
      @send="handleChatSend" 
    />

    <el-drawer
      v-model="sidebarDrawerVisible"
      direction="ltr"
      size="70%"
      append-to-body
      :with-header="false"
      class="sidebar-drawer"
    >
      <div class="drawer-header">
        <span>功能导航</span>
        <el-button circle text @click="sidebarDrawerVisible = false">
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
      <PatientSidebarMenu :active-menu="activeMenu" @select="handleMenuSelect" />
    </el-drawer>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox, ElNotification } from 'element-plus'
import message from '@/plugins/message'
import {
  Van,
  HomeFilled,
  Calendar,
  Plus,
  Tickets,
  User,
  Document,
  Food,
  List,
  Star,
  Pointer,
  Location,
  Connection,
  ChatDotRound,
  ChatLineRound,
  Reading,
  EditPen,
  CollectionTag,
  Notebook,
  DataAnalysis,
  Setting,
  Bell,
  Close,
  Menu
} from '@element-plus/icons-vue'
import { getUserInfo } from '@/api/user'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notification'
import SockJS from 'sockjs-client'
import { Client } from '@stomp/stompjs'
import dayjs from 'dayjs'
import { markNotificationAsRead } from '@/api/notification'
import ChatWidget from '@/components/ChatWidget.vue'
import PatientSidebarMenu from '@/components/patient/PatientSidebarMenu.vue'
import { fetchConversations, createConversation, getOrCreateAdminConversation, markAllConversationsAsRead } from '@/api/dialogue'
import { DEFAULT_AVATAR } from '@/constants/avatar'
import { getAppConfig } from '@/config/runtimeConfig'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const notificationStore = useNotificationStore()
const appConfig = inject('appConfig', getAppConfig())
const systemName = computed(() => appConfig?.systemInfo?.name || '中医体质辨识系统')
const patientLogoText = computed(() => `${systemName.value} - 患者端`)

let stompClient = null

// 当前激活的菜单
const activeMenu = computed(() => route.path)

// 聊天窗口显示状态
const chatWidgetVisible = ref(false)
const isMobile = ref(false)
const sidebarDrawerVisible = ref(false)
const touchStartX = ref(0)
const touchStartY = ref(0)

// 管理员对话ID
const adminConversationId = ref(null)

// 获取或创建管理员对话
const getOrCreateAdminConversationHandler = async () => {
  if (adminConversationId.value) {
    return adminConversationId.value
  }
  
  const currentUserId = userStore.userInfo?.id
  if (!currentUserId) {

    return null
  }
  
  try {
    // 调用后端接口获取或创建管理员对话
    const res = await getOrCreateAdminConversation(currentUserId)
    if (res.code === 200 && res.data) {
      adminConversationId.value = res.data.id
      return adminConversationId.value
    } else {

      return null
    }
  } catch (error) {

    return null
  }
}

// 处理聊天按钮点击
const handleChatButtonClick = async () => {
  if (!chatWidgetVisible.value) {
    // 打开聊天窗口时，尝试获取或创建管理员对话
    await getOrCreateAdminConversationHandler()
  }
  
  chatWidgetVisible.value = !chatWidgetVisible.value
}

// 关闭聊天窗口
const handleChatClose = () => {
  chatWidgetVisible.value = false
}

// 处理发送消息
const handleChatSend = (message) => {
  // 消息发送逻辑由ChatWidget组件处理
}

const unreadNotifications = computed(() => notificationStore.unread || [])
const unreadCount = computed(() => unreadNotifications.value.length)
const hasUnreadNotifications = computed(() => unreadCount.value > 0)
const avatarSrc = computed(() => userStore.userInfo?.avatar || DEFAULT_AVATAR)

// 下拉菜单命令处理
const handleCommand = (command) => {
  if (command === 'profile') {
    router.push('/patient/profile')
  } else if (command === 'notifications') {
    router.push('/patient/notifications')
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
  handleResize()
  window.addEventListener('resize', handleResize)
  await refreshUserInfo()
  await notificationStore.fetchUnread()
  connectNotificationSocket()
})

onUnmounted(() => {
  disconnectNotificationSocket()
  window.removeEventListener('resize', handleResize)
})

const handleResize = () => {
  isMobile.value = window.innerWidth < 992
  if (!isMobile.value) {
    sidebarDrawerVisible.value = false
  }
}

const handleMenuSelect = () => {
  if (isMobile.value) {
    sidebarDrawerVisible.value = false
  }
}

const handleTouchStart = (event) => {
  if (!isMobile.value || event.touches.length !== 1) return
  const touch = event.touches[0]
  touchStartX.value = touch.clientX
  touchStartY.value = touch.clientY
}

const handleTouchEnd = (event) => {
  if (!isMobile.value || event.changedTouches.length !== 1) return
  const touch = event.changedTouches[0]
  const deltaX = touch.clientX - touchStartX.value
  const deltaY = touch.clientY - touchStartY.value
  if (Math.abs(deltaX) < 80 || Math.abs(deltaX) < Math.abs(deltaY)) {
    return
  }
  if (deltaX > 0 && touchStartX.value <= 60) {
    sidebarDrawerVisible.value = true
  } else if (deltaX < 0) {
    sidebarDrawerVisible.value = false
  }
}

watch(
  () => route.path,
  () => {
    if (isMobile.value) {
      sidebarDrawerVisible.value = false
    }
  }
)

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
        role: 'PATIENT'
      }
      if (userStore.userInfo?.id) {
        params.userId = userStore.userInfo.id
      }
      await markAllConversationsAsRead(params)
      // 触发自定义事件，通知对话页面刷新
      window.dispatchEvent(new CustomEvent('conversations-marked-all-read', { 
        detail: { role: 'PATIENT', userId: userStore.userInfo?.id } 
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;

    .menu-toggle {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      border-radius: 8px;
      border: none;
      margin-right: 6px;
      background: rgba(255, 255, 255, 0.2);
      color: #fff;
      cursor: pointer;
    }

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

.main-container {
  flex: 1;
  overflow: hidden;
}

.sidebar {
  background: #fff;
  border-right: 1px solid #e0e0e0;
  overflow-y: auto;

  :deep(.patient-menu) {
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
    background: linear-gradient(90deg, #52c41a 0%, #389e0d 100%);
    color: white !important;

    .el-icon {
      color: white !important;
    }
  }
}

:deep(.el-sub-menu__title:hover) {
  background-color: #f0f9ff !important;
}

:deep(.el-sub-menu.is-active .el-sub-menu__title) {
  color: #52c41a !important;
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

.chat-float-button {
  position: fixed;
  right: 24px;
  bottom: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(82, 196, 26, 0.4);
  transition: all 0.3s ease;
  z-index: 1000;

  &:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(82, 196, 26, 0.5);
  }

  &:active {
    transform: scale(0.95);
  }
}

@media (max-width: 991px) {
  .header {
    padding: 0 12px;
  }

  .header-right {
    gap: 10px;

    .notification-wrapper,
    .username {
      display: none;
    }
  }

  .content {
    padding: 12px;
  }

  .chat-float-button {
    right: 16px;
    bottom: 16px;
    width: 48px;
    height: 48px;
  }
}

.sidebar-drawer {
  :deep(.el-drawer__body) {
    padding: 0;
  }
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  font-weight: 600;
  font-size: 16px;
}
</style>
