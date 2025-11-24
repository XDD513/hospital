<template>
  <div class="dialogue-shell">
    <aside class="panel">
      <div class="panel-header">
        <div>
          <h2>{{ activeRole === 'PATIENT' ? '医生列表' : activeRole === 'ADMIN' ? '用户列表' : '患者列表' }}</h2>
        </div>
        <div class="panel-actions">
          <el-button text size="small" @click="historyVisible = true">
            历史记录
          </el-button>
          <el-button
            text
            size="small"
            @click="activeRole === 'PATIENT' ? loadDoctors() : activeRole === 'ADMIN' ? loadUsers() : loadConversations()"
            :loading="activeRole === 'PATIENT' ? loadingDoctors : activeRole === 'ADMIN' ? loadingUsers : loadingConversations"
          >
            刷新
          </el-button>
        </div>
      </div>

      <div
        class="side-list"
        :class="{ 'only-list': activeRole !== 'PATIENT' }"
        v-loading="activeRole === 'PATIENT' ? loadingDoctors : activeRole === 'ADMIN' ? loadingUsers : loadingConversations"
      >
        <!-- 患者端：显示医生列表 -->
        <template v-if="activeRole === 'PATIENT'">
          <template v-if="doctorList.length">
            <article
              v-for="doctor in doctorList"
              :key="doctor.id"
              :class="['person-item', { active: currentConversation?.doctorId === doctor.id }]"
              @click="handleDoctorSelect(doctor)"
            >
              <img
                class="avatar sm"
                :src="getContactAvatar(doctor, 'DOCTOR')"
                :alt="doctor.doctorName"
                @error="handleAvatarError($event, 'DOCTOR')"
              />
              <div class="info">
                <div class="info-header">
                  <strong>{{ doctor.doctorName || '未命名医生' }}</strong>
                  <el-badge
                    v-if="getDoctorUnreadCount(doctor.id) > 0"
                    :value="getDoctorUnreadCount(doctor.id)"
                    :max="99"
                    class="unread-badge"
                  />
                </div>
                <small>{{ doctor.specialty || '擅长体质：' + (doctor.goodAtConstitution || '暂无') }}</small>
                <small>从业{{ doctor.yearsOfExperience || 0 }}年 · 评分 {{ doctor.rating || '5.0' }}</small>
                <small class="contact-meta">
                  {{ getDoctorLastMessage(doctor.id) || '暂无最近沟通' }}
                </small>
                <small>
                  {{ getDoctorUpdatedAt(doctor.id) ? formatTime(getDoctorUpdatedAt(doctor.id)) : '' }}
                </small>
              </div>
            </article>
          </template>
          <el-empty v-else description="暂无医生可选" />
        </template>

        <!-- 医生端和管理员端：显示患者/用户列表 -->
        <template v-else>
          <template v-if="patientList.length">
            <article
              v-for="patient in patientList"
              :key="patient.id"
              :class="['person-item', { active: currentConversation?.patientId === patient.id }]"
              @click="handlePatientSelect(patient)"
            >
              <img
                class="avatar sm"
                :src="getContactAvatar(patient, patient.roleType === 2 ? 'DOCTOR' : 'PATIENT')"
                :alt="patient.name"
                @error="handleAvatarError($event, patient.roleType === 2 ? 'DOCTOR' : 'PATIENT')"
              />
              <div class="info">
                <div class="info-header">
                  <strong>{{ patient.name }}</strong>
                  <el-badge
                    v-if="patient.unreadCount > 0"
                    :value="patient.unreadCount"
                    :max="99"
                    class="unread-badge"
                  />
                </div>
                <small>{{ patient.lastMessage || '暂无最近沟通' }}</small>
                <small>{{ patient.updatedAt ? formatTime(patient.updatedAt) : '' }}</small>
              </div>
            </article>
          </template>
          <el-empty v-else :description="activeRole === 'ADMIN' ? '暂无用户' : '暂无患者会话'" />
        </template>
      </div>
    </aside>

    <section class="chat-view">
      <header class="chat-meta">
        <div>
          <strong>{{ currentConversation?.title || '智能康复助手' }}</strong>
          <span>{{ currentConversation?.summary || '请选择左侧会话开始交流' }}</span>
        </div>
        <span>{{ formatTime(currentConversation?.updatedAt) }}</span>
      </header>

      <div class="message-board" ref="messageBoardRef">
        <template v-if="!currentConversation">
          <div class="empty-state">
            <div class="empty-icon">
              <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="120" height="120">
                <path d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z" fill="#cbd5e1"/>
                <path d="M464 336a48 48 0 1 0 96 0 48 48 0 1 0-96 0zm272 112c0 4.4-3.6 8-8 8H544v275c0 4.4-3.6 8-8 8h-48c-4.4 0-8-3.6-8-8V456H360c-4.4 0-8-3.6-8-8v-48c0-4.4 3.6-8 8-8h112V240c0-4.4 3.6-8 8-8h48c4.4 0 8 3.6 8 8v112h184c4.4 0 8 3.6 8 8v48z" fill="#94a3b8"/>
              </svg>
            </div>
            <h3 class="empty-title">欢迎使用智能对话</h3>
            <p class="empty-description">
              {{ activeRole === 'PATIENT' 
                ? '请从左侧选择一位医生开始对话，或查看历史记录' 
                : activeRole === 'ADMIN' 
                ? '请从左侧选择一位用户查看对话记录' 
                : '请从左侧选择一位患者查看对话记录' }}
            </p>
            <div class="empty-actions">
              <el-button type="primary" @click="historyVisible = true">
                <el-icon><Clock /></el-icon>
                查看历史记录
              </el-button>
              <el-button 
                v-if="activeRole === 'PATIENT'" 
                @click="loadDoctors(); showDoctorListDialog = true"
              >
                <el-icon><User /></el-icon>
                选择医生
              </el-button>
            </div>
            <div class="empty-features">
              <div class="feature-item">
                <el-icon><ChatDotRound /></el-icon>
                <span>实时消息推送</span>
              </div>
              <div class="feature-item">
                <el-icon><Document /></el-icon>
                <span>历史记录保存</span>
              </div>
              <div class="feature-item">
                <el-icon><Bell /></el-icon>
                <span>消息通知提醒</span>
              </div>
            </div>
          </div>
        </template>
        <template v-else-if="loadingMessages">
          <!-- 加载状态：有会话但消息正在加载 -->
          <template v-if="messages.length > 0 && messages[0]?.conversationId === currentConversation?.id">
            <!-- 如果消息属于当前会话，显示消息列表 -->
            <div
              v-for="msg in messages"
              :key="msg.id"
              :class="['message-row', isOwnMessage(msg) ? 'self' : 'other']"
            >
              <img
                class="avatar"
                :src="msg.senderAvatar || roleFallbackAvatar(msg.senderRole)"
                :alt="msg.senderName"
                @error="handleAvatarError($event, msg.senderRole)"
              />
              <div class="message-content">
                <div class="message-meta">
                  <span class="nickname">{{ msg.senderName || roleLabel(msg.senderRole) }}</span>
                  <span class="timestamp">{{ formatTime(msg.sentAt) }}</span>
                </div>
                <div class="message" :class="isOwnMessage(msg) ? 'self' : 'other'">
                  {{ msg.content }}
                </div>
              </div>
            </div>
            <!-- 在消息列表底部显示加载提示 -->
            <div class="loading-messages-inline">
              <el-icon class="loading-icon"><Loading /></el-icon>
              <span>正在加载新消息...</span>
            </div>
          </template>
          <template v-else>
            <!-- 如果没有消息或消息不属于当前会话，显示加载状态 -->
            <div class="loading-messages">
              <el-icon class="loading-icon"><Loading /></el-icon>
              <span>正在加载消息...</span>
            </div>
          </template>
        </template>
        <template v-else-if="messages.length">
          <div
            v-for="msg in messages"
            :key="msg.id"
            :class="['message-row', isOwnMessage(msg) ? 'self' : 'other']"
          >
            <img
              class="avatar"
              :src="msg.senderAvatar || roleFallbackAvatar(msg.senderRole)"
              :alt="msg.senderName"
              @error="handleAvatarError($event, msg.senderRole)"
            />
            <div class="message-content">
              <div class="message-meta">
                <span class="nickname">{{ msg.senderName || roleLabel(msg.senderRole) }}</span>
                <span class="timestamp">{{ formatTime(msg.sentAt) }}</span>
              </div>
              <div class="message" :class="isOwnMessage(msg) ? 'self' : 'other'">
                {{ msg.content }}
              </div>
            </div>
          </div>
        </template>
        <el-empty v-else description="暂无消息，发送一条试试吧" />
      </div>

      <div class="composer">
        <div class="identity">
          当前身份：<span>{{ speakerLabel }}</span>
        </div>
        <el-input
          v-model="messageInput"
          type="textarea"
          :autosize="{ minRows: 3, maxRows: 5 }"
          placeholder="请输入消息内容..."
          @keydown.enter.exact.prevent="handleSend"
        />
        <el-button
          type="primary"
          :disabled="!currentConversation"
          :loading="sending"
          @click="handleSend"
        >
          发送
        </el-button>
      </div>
    </section>
  </div>

  <!-- 历史记录抽屉 -->
  <el-drawer
    v-model="historyVisible"
    title="历史会话"
    size="360px"
    :append-to-body="true"
  >
    <div class="drawer-content" v-loading="loadingConversations">
      <template v-if="conversations.length">
        <article
          v-for="item in conversations"
          :key="item.id"
          class="history-item"
        >
          <div class="history-item-content" @click="handleHistorySelect(item)">
            <div class="history-head">
              <div class="history-title-wrapper">
                <strong>{{ item.title }}</strong>
                <el-badge
                  v-if="getHistoryUnreadCount(item) > 0"
                  :value="getHistoryUnreadCount(item)"
                  :max="99"
                  class="history-unread-badge"
                />
              </div>
              <span>{{ formatTime(item.updatedAt || item.lastMessageTime) }}</span>
            </div>
            <p>{{ item.summary || item.lastMessagePreview || '暂无描述' }}</p>
          </div>
          <el-button
            text
            type="danger"
            size="small"
            @click.stop="handleDeleteConversation(item)"
            :loading="deletingConversationId === item.id"
          >
            删除
          </el-button>
        </article>
      </template>
      <el-empty v-else description="暂无历史记录" />
    </div>
    <template #footer>
      <div style="display: flex; justify-content: space-between; width: 100%;">
        <el-button
          type="danger"
          text
          @click="handleDeleteAllConversations"
          :disabled="conversations.length === 0"
          :loading="deletingAll"
        >
          清空所有
        </el-button>
        <el-button text @click="historyVisible = false">关闭</el-button>
      </div>
    </template>
  </el-drawer>

  <!-- 患者端：选择医生对话框 -->
  <el-dialog
    v-if="activeRole === 'PATIENT'"
    v-model="showDoctorListDialog"
    title="选择医生"
    width="500px"
  >
    <div v-loading="loadingDoctors">
      <template v-if="doctorList.length">
        <article
          v-for="doctor in doctorList"
          :key="doctor.id"
          class="doctor-select-item"
          @click="handleDoctorSelect(doctor)"
        >
          <img
            class="avatar sm"
            :src="getContactAvatar(doctor, 'DOCTOR')"
            :alt="doctor.doctorName"
            @error="handleAvatarError($event, 'DOCTOR')"
          />
          <div class="info">
            <div class="info-header">
              <strong>{{ doctor.doctorName || '未命名医生' }}</strong>
            </div>
            <small>{{ doctor.specialty || '擅长体质：' + (doctor.goodAtConstitution || '暂无') }}</small>
            <small>从业{{ doctor.yearsOfExperience || 0 }}年 · 评分 {{ doctor.rating || '5.0' }}</small>
          </div>
        </article>
      </template>
      <el-empty v-else description="暂无医生可选" />
    </div>
    <template #footer>
      <el-button @click="showDoctorListDialog = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import message from '@/plugins/message'
import { computed, nextTick, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import dayjs from 'dayjs'
import { ElMessageBox } from 'element-plus'
import { ChatDotRound, Document, Bell, Clock, User, Loading } from '@element-plus/icons-vue'
import SockJS from 'sockjs-client'
import { Client } from '@stomp/stompjs'
import { fetchConversations, createConversation, deleteConversation, deleteAllConversations, fetchMessages, sendMessage, markConversationAsRead } from '@/api/dialogue'
import { useUserStore } from '@/stores/user'
import { useDoctorStore } from '@/stores/doctor'
import { getEnabledDoctorList } from '@/api/doctor'
import { getUserList } from '@/api/system'
import { generatePresignedUrl } from '@/api/oss'
import { getAvatarConfig } from '@/config/constants'

const userStore = useUserStore()
const doctorStore = useDoctorStore()

const doctorList = ref([])
const conversations = ref([])
const allUsers = ref([])
const messages = ref([])
const currentConversation = ref(null)
const loadingConversations = ref(false)
const loadingDoctors = ref(false)
const loadingUsers = ref(false)
const loadingMessages = ref(false)
const sending = ref(false)
const messageInput = ref('')
const messageBoardRef = ref(null)
const historyVisible = ref(false)
const showDoctorListDialog = ref(false)
const stompClient = ref(null)
const conversationSubscription = ref(null)
const isSocketConnected = ref(false)
const deletingConversationId = ref(null)
const deletingAll = ref(false)

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const messagePagination = reactive({
  page: 1,
  pageSize: 100,
  total: 0
})

const roleType = computed(() => userStore.userInfo?.roleType || 1)
const activeRole = computed(() => {
  if (roleType.value === 3) return 'ADMIN'
  if (roleType.value === 2) return 'DOCTOR'
  return 'PATIENT'
})
const speakerLabel = computed(() => {
  if (activeRole.value === 'ADMIN') return '管理员'
  if (activeRole.value === 'DOCTOR') return '医生'
  return '患者'
})
const participantId = computed(() => {
  if (activeRole.value === 'DOCTOR') {
    return doctorStore.doctorInfo?.id || null
  }
  if (activeRole.value === 'ADMIN') {
    return userStore.userInfo?.id || null
  }
  return userStore.userInfo?.id || null
})
const currentUserId = computed(() => userStore.userInfo?.id || null)

const isSameId = (a, b) => {
  if (a === undefined || a === null || b === undefined || b === null) {
    return false
  }
  return String(a) === String(b)
}

const resolveUnreadCountForRole = (conversation, roleOverride) => {
  if (!conversation) return 0
  const normalizedRole = (roleOverride || activeRole.value || '').toUpperCase()
  const userId = currentUserId.value

  if (userId) {
    if (conversation.participant1UserId && isSameId(conversation.participant1UserId, userId)) {
      return conversation.unreadForParticipant1 ?? conversation.unreadForPatient ?? 0
    }
    if (conversation.participant2UserId && isSameId(conversation.participant2UserId, userId)) {
      return conversation.unreadForParticipant2 ?? conversation.unreadForDoctor ?? 0
    }
  }

  if (normalizedRole === 'PATIENT') {
    return conversation.unreadForPatient || 0
  }
  if (normalizedRole === 'DOCTOR' || normalizedRole === 'ADMIN') {
    return conversation.unreadForDoctor || 0
  }
  return 0
}

const patientList = computed(() => {
  if (activeRole.value === 'PATIENT') {
    return []
  }
  
  // 管理员端：直接显示所有用户（已过滤掉管理员）
  if (activeRole.value === 'ADMIN') {
    return allUsers.value.map(user => {
      // 尝试从会话中找到该用户的会话信息
      const userConversation = conversations.value.find(c => {
        if (c.conversationType === 'ADMIN_USER') {
          return (c.participant1UserId && String(c.participant1UserId) === String(user.id)) ||
                 (c.participant2UserId && String(c.participant2UserId) === String(user.id))
        }
        return String(c.patientId) === String(user.id)
      })
      
      // 确定用户角色类型，用于获取正确的默认头像
      const userRole = user.roleType === 2 ? 'DOCTOR' : 'PATIENT'
      const normalizedRole = userRole === 'DOCTOR' ? 'DOCTOR' : 'PATIENT'
      const userAvatar = (user.avatar && user.avatar.trim() !== '') ? user.avatar : null
      const finalAvatar = userAvatar || roleFallbackAvatar(normalizedRole)
      
      return {
        id: user.id,
        name: user.realName || user.username || '用户',
        avatar: finalAvatar,
        userAvatar: finalAvatar,
        roleType: user.roleType,
        lastMessage: userConversation?.lastMessagePreview || '暂无最近沟通',
        updatedAt: userConversation?.updatedAt || userConversation?.lastMessageTime || null,
        unreadCount: userConversation ? resolveUnreadCountForRole(userConversation, 'ADMIN') : 0,
        conversationId: userConversation?.id || null
      }
    })
  }
  
  // 医生端：从会话中提取患者列表
  const uniqueMap = new Map()
  conversations.value.forEach((item) => {
    if (!item?.patientId || item.conversationType === 'ADMIN_USER') {
      return
    }
    // 过滤掉被当前用户删除的会话
    if (activeRole.value === 'DOCTOR' && (item.deletedByDoctor === 1 || item.deletedByDoctor === true)) {
      return
    }
    const unread = resolveUnreadCountForRole(item, activeRole.value)
    const updatedAt = item.updatedAt || item.lastMessageTime || null
    if (!uniqueMap.has(item.patientId)) {
      uniqueMap.set(item.patientId, {
        id: item.patientId,
        name: item.patientNickname || '患者',
        avatar: item.patientAvatar,
        patientAvatar: item.patientAvatar, // 同时设置 patientAvatar 以便 getContactAvatar 能获取到
        roleType: 1, // 患者角色类型
        lastMessage: item.lastMessagePreview,
        updatedAt,
        unreadCount: unread,
        conversationId: item.id
      })
    } else {
      const existed = uniqueMap.get(item.patientId)
      existed.unreadCount = (existed.unreadCount || 0) + unread
      if (!existed.updatedAt || (updatedAt && dayjs(updatedAt).isAfter(existed.updatedAt))) {
        existed.updatedAt = updatedAt
        existed.lastMessage = item.lastMessagePreview
        existed.conversationId = item.id
        // 如果当前会话有头像且已存在的没有头像，则更新头像
        if (item.patientAvatar && !existed.avatar) {
          existed.avatar = item.patientAvatar
          existed.patientAvatar = item.patientAvatar
        }
      }
    }
  })
  return Array.from(uniqueMap.values()).sort((a, b) => {
    const timeA = a.updatedAt ? dayjs(a.updatedAt).valueOf() : 0
    const timeB = b.updatedAt ? dayjs(b.updatedAt).valueOf() : 0
    return timeB - timeA
  })
})

const doctorConversationMeta = computed(() => {
  if (activeRole.value !== 'PATIENT') {
    return {}
  }
  return conversations.value.reduce((acc, conversation) => {
    if (!conversation?.doctorId || conversation.conversationType === 'ADMIN_USER') {
      return acc
    }
    // 过滤掉被患者删除的会话
    if (conversation.deletedByPatient === 1 || conversation.deletedByPatient === true) {
      return acc
    }
    const key = String(conversation.doctorId)
    const unread = resolveUnreadCountForRole(conversation, 'PATIENT')
    const updatedAt = conversation.updatedAt || conversation.lastMessageTime || null
    if (!acc[key]) {
      acc[key] = {
        id: conversation.id,
        unread,
        lastMessage: conversation.lastMessagePreview,
        updatedAt
      }
    } else {
      acc[key].unread = (acc[key].unread || 0) + unread
      if (!acc[key].updatedAt || (updatedAt && dayjs(updatedAt).isAfter(acc[key].updatedAt))) {
        acc[key].updatedAt = updatedAt
        acc[key].lastMessage = conversation.lastMessagePreview
        acc[key].id = conversation.id
      }
    }
    return acc
  }, {})
})

const getDoctorUnreadCount = (doctorId) => {
  if (!doctorId) return 0
  const meta = doctorConversationMeta.value[String(doctorId)]
  return meta?.unread || 0
}

const getDoctorLastMessage = (doctorId) => {
  if (!doctorId) return ''
  const meta = doctorConversationMeta.value[String(doctorId)]
  return meta?.lastMessage || ''
}

const getDoctorUpdatedAt = (doctorId) => {
  if (!doctorId) return null
  const meta = doctorConversationMeta.value[String(doctorId)]
  return meta?.updatedAt || null
}

const formatTime = (value) => {
  if (!value) return '--:--'
  return dayjs(value).format('MM-DD HH:mm')
}

const roleLabel = (role) => {
  const normalized = role?.toUpperCase()
  if (normalized === 'DOCTOR') return '医生'
  if (normalized === 'PATIENT') return '患者'
  if (normalized === 'ADMIN') return '管理员'
  return '系统'
}

const roleFallbackAvatar = (role) => {
  const normalized = role?.toUpperCase() || 'SYSTEM'
  const roleFallbacks = getAvatarConfig()
  return roleFallbacks[normalized] || roleFallbacks.SYSTEM
}

const handleAvatarError = (event, role) => {
  if (!event?.target) return
  const fallback = roleFallbackAvatar(role)
  if (event.target.src !== fallback) {
    event.target.src = fallback
  }
}

const getContactAvatar = (target, role) => {
  if (!target) {
    return roleFallbackAvatar(role)
  }
  // 检查头像URL，确保不是空字符串或null
  const avatar = target.avatar || target.userAvatar || target.patientAvatar || target.doctorAvatar
  if (avatar && avatar.trim() !== '') {
    return avatar
  }
  return roleFallbackAvatar(role)
}

const findConversationById = (conversationId) => {
  if (!conversationId) return null
  return conversations.value.find(item => isSameId(item.id, conversationId))
}

const extractAvatarFromConversation = (conversation, role) => {
  if (!conversation || !role) return null
  const normalized = role.toUpperCase()
  const candidateFields = []

  if (conversation.participant1Role && conversation.participant1Role.toUpperCase() === normalized) {
    candidateFields.push('participant1Avatar')
  }
  if (conversation.participant2Role && conversation.participant2Role.toUpperCase() === normalized) {
    candidateFields.push('participant2Avatar')
  }

  if (normalized === 'DOCTOR') {
    candidateFields.push('doctorAvatar')
  } else if (normalized === 'PATIENT') {
    candidateFields.push('patientAvatar')
  }

  candidateFields.push('lastSenderAvatar')
  candidateFields.push('participant1Avatar', 'participant2Avatar')

  for (const field of candidateFields) {
    const value = conversation[field]
    if (value) return value
  }
  return null
}

const resolveAvatarFromContext = (role, senderId, conversationId) => {
  if (!role) return null
  const normalizedRole = role.toUpperCase()

  const conversation = findConversationById(conversationId) ||
    (senderId ? conversations.value.find(item => {
      if (normalizedRole === 'DOCTOR') {
        return (item.doctorId && isSameId(item.doctorId, senderId))
      }
      if (normalizedRole === 'PATIENT') {
        return (item.patientId && isSameId(item.patientId, senderId)) ||
          (item.participant1UserId && isSameId(item.participant1UserId, senderId)) ||
          (item.participant2UserId && isSameId(item.participant2UserId, senderId))
      }
      return false
    }) : null)

  const conversationAvatar = extractAvatarFromConversation(conversation, normalizedRole)
  if (conversationAvatar) {
    return conversationAvatar
  }

  if (normalizedRole === 'DOCTOR') {
    if (senderId && doctorStore.doctorInfo?.id && isSameId(doctorStore.doctorInfo.id, senderId)) {
      return doctorStore.doctorInfo?.avatar || userStore.userInfo?.avatar || null
    }
    const doctor = doctorList.value.find(doc => isSameId(doc.id, senderId))
    if (doctor) {
      return doctor.avatar || doctor.userAvatar || doctor.doctorAvatar || null
    }
  } else if (normalizedRole === 'PATIENT') {
    if (senderId && userStore.userInfo?.id && isSameId(userStore.userInfo.id, senderId)) {
      return userStore.userInfo?.avatar || null
    }

    const patient = patientList.value.find(item => isSameId(item.id, senderId))
    if (patient) {
      return patient.avatar || patient.patientAvatar || patient.userAvatar || null
    }

    const adminUser = allUsers.value.find(item => isSameId(item.id, senderId))
    if (adminUser) {
      return adminUser.avatar || null
    }
  } else if (normalizedRole === 'ADMIN') {
    if (senderId && userStore.userInfo?.id && isSameId(userStore.userInfo.id, senderId)) {
      return userStore.userInfo?.avatar || null
    }
    const adminUser = allUsers.value.find(item => isSameId(item.id, senderId))
    if (adminUser) {
      return adminUser.avatar || null
    }
  }

  return null
}

const resolveSenderAvatar = (source) => {
  if (!source) return roleFallbackAvatar()
  const normalizedRole = source.senderRole?.toUpperCase()
  if (source.senderAvatar) {
    return source.senderAvatar
  }
  const contextualAvatar = resolveAvatarFromContext(normalizedRole, source.senderId, source.conversationId)
  if (contextualAvatar) {
    return contextualAvatar
  }
  return roleFallbackAvatar(normalizedRole)
}

const normalizeMessageAvatar = (message, conversationId) => {
  if (!message) return message
  const avatar = message.senderAvatar ||
    resolveAvatarFromContext(message.senderRole?.toUpperCase(), message.senderId, conversationId || message.conversationId)
  return {
    ...message,
    senderAvatar: avatar || roleFallbackAvatar(message.senderRole)
  }
}

const scrollMessagesToBottom = () => {
  nextTick(() => {
    const board = messageBoardRef.value
    if (board) {
      board.scrollTop = board.scrollHeight
    }
  })
}

const markingConversationIds = new Set()

const clearUnreadLocally = (conversationId) => {
  if (!conversationId) return
  const index = conversations.value.findIndex(item => item.id === conversationId)
  if (index === -1) return
  const target = { ...conversations.value[index] }
  const normalizedRole = activeRole.value
  const userId = currentUserId.value

  if (userId) {
    if (target.participant1UserId && isSameId(target.participant1UserId, userId)) {
      target.unreadForParticipant1 = 0
    }
    if (target.participant2UserId && isSameId(target.participant2UserId, userId)) {
      target.unreadForParticipant2 = 0
    }
  }

  if (normalizedRole === 'PATIENT') {
    target.unreadForPatient = 0
    if (target.participant1Role && target.participant1Role.toUpperCase() === 'PATIENT') {
      target.unreadForParticipant1 = 0
    }
  } else {
    target.unreadForDoctor = 0
    if (target.participant1Role && target.participant1Role.toUpperCase() === normalizedRole) {
      target.unreadForParticipant1 = 0
    }
    if (target.participant2Role && target.participant2Role.toUpperCase() === normalizedRole) {
      target.unreadForParticipant2 = 0
    }
  }

  const next = [...conversations.value]
  next.splice(index, 1, target)
  conversations.value = next
  if (currentConversation.value?.id === target.id) {
    currentConversation.value = target
  }
}

const markConversationAsReadRequest = async (conversation) => {
  if (!conversation?.id) return
  if (resolveUnreadCountForRole(conversation, activeRole.value) <= 0) return
  if (markingConversationIds.has(conversation.id)) return

  clearUnreadLocally(conversation.id)

  const params = {
    role: activeRole.value
  }
  if (currentUserId.value) {
    params.userId = currentUserId.value
  }

  markingConversationIds.add(conversation.id)
  try {
    await markConversationAsRead(conversation.id, params)
    // 标记已读成功后，重新加载会话列表以同步最新的未读数
    // 使用静默加载，不显示loading，避免影响用户体验
    await loadConversations(false, true)
  } catch (error) {
    // 如果后端标记失败，恢复本地未读数
    // 重新加载会话列表以获取正确的未读数
    await loadConversations(false, true)
  } finally {
    markingConversationIds.delete(conversation.id)
  }
}

const getHistoryUnreadCount = (conversation) => {
  return resolveUnreadCountForRole(conversation, activeRole.value)
}

const totalUnreadCount = computed(() => {
  return conversations.value.reduce((sum, c) => sum + resolveUnreadCountForRole(c, activeRole.value), 0)
})

const updatePageTitle = () => {
  const baseTitle = '智能对话'
  if (totalUnreadCount.value > 0) {
    document.title = `(${totalUnreadCount.value}) ${baseTitle}`
  } else {
    document.title = baseTitle
  }
}

const isOwnMessage = (msg) => {
  return msg?.senderRole?.toUpperCase() === activeRole.value
}

const loadConversations = async (showLoading = true, skipAutoSelect = false) => {
  if (activeRole.value === 'DOCTOR' && !doctorStore.doctorInfo) {
    await doctorStore.fetchDoctorInfo()
  }
  
  if (!participantId.value) {
    if (showLoading) {
      message.warning('当前账号尚未获取到身份信息，暂无法加载会话')
    }
    return
  }

  if (showLoading) {
    loadingConversations.value = true
  }
  try {
    const params = {
      page: pagination.page,
      pageSize: pagination.pageSize
    }
    if (userStore.userInfo?.id) {
      params.userId = userStore.userInfo.id
    } else {
      if (activeRole.value === 'DOCTOR') {
        params.doctorId = participantId.value
      } else if (activeRole.value === 'ADMIN') {
        params.doctorId = participantId.value
      } else {
        params.patientId = participantId.value
      }
    }
    const res = await fetchConversations(params)
    const records = res.data?.records || []
    
    let filteredRecords = records
    
    // 根据角色过滤会话：患者端和医生端不显示 ADMIN_USER 类型（与管理员的会话），管理员端显示所有
    // 同时过滤掉被当前用户单方面删除的会话
    if (activeRole.value === 'PATIENT') {
      // 患者端：只显示与医生的普通会话，不显示与管理员的会话（ADMIN_USER 类型）
      filteredRecords = records.filter(c => {
        // 过滤掉 ADMIN_USER 类型的会话
        if (c.conversationType === 'ADMIN_USER') {
          return false
        }
        // 过滤掉被患者删除的会话（单方向删除）
        if (c.deletedByPatient === 1 || c.deletedByPatient === true) {
          return false
        }
        // 普通会话：显示所有有 patientId 的会话
        return c.patientId != null
      })
    } else if (activeRole.value === 'DOCTOR') {
      // 医生端：只显示与患者的普通会话，不显示与管理员的会话（ADMIN_USER 类型）
      filteredRecords = records.filter(c => {
        // 过滤掉 ADMIN_USER 类型的会话
        if (c.conversationType === 'ADMIN_USER') {
          return false
        }
        // 过滤掉被医生删除的会话（单方向删除）
        if (c.deletedByDoctor === 1 || c.deletedByDoctor === true) {
          return false
        }
        // 普通会话：显示所有有 doctorId 和 patientId 的会话
        return c.doctorId != null && c.patientId != null
      })
    } else if (activeRole.value === 'ADMIN') {
      // 管理员端：显示所有会话，但过滤掉被管理员删除的会话
      filteredRecords = records.filter(c => {
        // 对于 ADMIN_USER 类型，检查 participant 删除标记
        if (c.conversationType === 'ADMIN_USER') {
          const userId = currentUserId.value
          if (c.participant1UserId && isSameId(c.participant1UserId, userId)) {
            if (c.deletedByParticipant1 === 1 || c.deletedByParticipant1 === true) {
              return false
            }
          }
          if (c.participant2UserId && isSameId(c.participant2UserId, userId)) {
            if (c.deletedByParticipant2 === 1 || c.deletedByParticipant2 === true) {
              return false
            }
          }
        }
        return true
      })
    }
    
    conversations.value = filteredRecords.sort((a, b) => {
      const timeA = (a.updatedAt || a.lastMessageTime) ? dayjs(a.updatedAt || a.lastMessageTime).valueOf() : 0
      const timeB = (b.updatedAt || b.lastMessageTime) ? dayjs(b.updatedAt || b.lastMessageTime).valueOf() : 0
      return timeB - timeA
    })
    pagination.total = filteredRecords.length

    if (conversations.value.length === 0) {
      if (!skipAutoSelect) {
        currentConversation.value = null
        messages.value = []
      }
      updatePageTitle()
      return
    }

    // 如果 skipAutoSelect 为 true（例如打开历史记录抽屉时），只更新列表，不自动选择会话
    if (skipAutoSelect) {
      // 仅更新当前会话的数据（如果存在）
      if (currentConversation.value?.id) {
        const latest = conversations.value.find((c) => c.id === currentConversation.value.id)
        if (latest) {
          currentConversation.value = { ...latest }
        }
      }
      updatePageTitle()
      return
    }

    // 如果当前没有选中会话，默认选中第一个
    if (!currentConversation.value || !currentConversation.value.id) {
      if (conversations.value.length > 0) {
        await handleSelectConversation(conversations.value[0])
      }
    } else {
      // 更新当前会话数据
      const savedConversationId = currentConversation.value.id
      const latest = conversations.value.find((c) => c.id === savedConversationId)
      if (latest) {
        currentConversation.value = { ...latest }
        markConversationAsReadRequest(latest)
        if (messages.value.length === 0) {
          await loadMessages(latest.id, false)
        }
      } else {
        // 如果当前会话不在列表中，尝试通过其他方式查找
        const savedDoctorId = currentConversation.value.doctorId
        const savedPatientId = currentConversation.value.patientId
        let matched = null
        
        if (activeRole.value === 'PATIENT' && savedDoctorId) {
          matched = conversations.value.find(c => isSameId(c.doctorId, savedDoctorId))
        } else if ((activeRole.value === 'DOCTOR' || activeRole.value === 'ADMIN') && savedPatientId) {
          matched = conversations.value.find(c => isSameId(c.patientId, savedPatientId))
        }
        
        if (matched) {
          await handleSelectConversation(matched)
        } else if (conversations.value.length > 0) {
          await handleSelectConversation(conversations.value[0])
        } else {
          currentConversation.value = null
          messages.value = []
        }
      }
    }
    updatePageTitle()
  } catch (error) {
    if (showLoading) {
      message.error('加载会话失败')
    }
  } finally {
    if (showLoading) {
      loadingConversations.value = false
    }
  }
}

const loadDoctors = async () => {
  if (activeRole.value !== 'PATIENT') return
  loadingDoctors.value = true
  try {
    const res = await getEnabledDoctorList()
    doctorList.value = res.data || []
  } catch (error) {
    message.error('加载医生列表失败')
  } finally {
    loadingDoctors.value = false
  }
}

// 加载所有用户（管理员端）
const loadUsers = async () => {
  if (activeRole.value !== 'ADMIN') return
  loadingUsers.value = true
  try {
    const res = await getUserList({
      page: 1,
      pageSize: 1000 // 获取所有用户
    })
    if (res.code === 200) {
      // 过滤掉管理员角色（roleType === 3）的用户
      const currentUserId = userStore.userInfo?.id
      let filteredUsers = (res.data?.records || []).filter(user => {
        // 排除管理员角色
        if (user.roleType === 3) {
          return false
        }
        // 排除当前登录的管理员自己
        if (currentUserId && String(user.id) === String(currentUserId)) {
          return false
        }
        return true
      })
      
      // 为每个用户的头像生成签名URL（如果是OSS URL且未签名）
      const usersWithSignedAvatars = await Promise.all(
        filteredUsers.map(async (user) => {
          if (user.avatar && user.avatar.includes('oss-cn-')) {
            // 检查是否已经包含签名参数
            const hasSignature = user.avatar.includes('Signature=') || user.avatar.includes('OSSAccessKeyId=')
            if (!hasSignature) {
              try {
                const signedRes = await generatePresignedUrl(user.avatar, 60)
                if (signedRes.code === 200 && signedRes.data) {
                  user.avatar = signedRes.data
                }
              } catch (error) {
                // 如果生成签名URL失败，使用原始URL
                console.warn('生成头像签名URL失败:', error)
              }
            }
          }
          return user
        })
      )
      
      allUsers.value = usersWithSignedAvatars
      // 同时加载会话，以便显示最后消息和未读数
      await loadConversations(false, true)
    }
  } catch (error) {
    message.error('加载用户列表失败')
  } finally {
    loadingUsers.value = false
  }
}

const loadMessages = async (conversationId, showLoading = true) => {
  if (!conversationId) return
  if (showLoading) {
    loadingMessages.value = true
  }
  try {
    const res = await fetchMessages(conversationId, {
      page: messagePagination.page,
      pageSize: messagePagination.pageSize
    })
    const records = res.data?.records || []
    messages.value = records.map(item => normalizeMessageAvatar(item, conversationId))
    messagePagination.total = res.data?.total || 0
    scrollMessagesToBottom()
  } catch (error) {
    if (showLoading) {
      message.error('加载消息失败')
    }
  } finally {
    if (showLoading) {
      loadingMessages.value = false
    }
  }
}

const handleSelectConversation = async (conversation) => {
  if (!conversation?.id) {
    console.warn('handleSelectConversation: 会话数据无效', conversation)
    return
  }
  // 关键修复：立即切换到新会话，避免显示空状态页面
  currentConversation.value = { ...conversation }
  loadingMessages.value = true
  
  // 如果旧消息属于不同的会话，清空它们
  const isSwitchingConversation = messages.value.length > 0 && 
    messages.value[0]?.conversationId !== conversation.id
  
  if (isSwitchingConversation) {
    messages.value = []
  }
  
  // 等待响应式更新完成
  await nextTick()
  
  // 加载新会话的消息
  try {
    const res = await fetchMessages(conversation.id, {
      page: messagePagination.page,
      pageSize: messagePagination.pageSize
    })
    messages.value = res.data?.records || []
    messagePagination.total = res.data?.total || 0
    scrollMessagesToBottom()
  } catch (error) {
    message.error('加载消息失败')
  } finally {
    loadingMessages.value = false
  }
  
  markConversationAsReadRequest(conversation)
  historyVisible.value = false
}

const handleHistorySelect = (conversation) => {
  return handleSelectConversation(conversation)
}

const handleDoctorSelect = async (doctor) => {
  if (activeRole.value !== 'PATIENT') return
  if (!participantId.value) {
    message.warning('请先登录或刷新页面后重试')
    return
  }
  
  if (conversations.value.length === 0) {
    await loadConversations(false)
  }
  
  // 查找已存在的会话（包括被删除的会话，需要从后端重新加载所有会话）
  // 先尝试从当前列表中查找
  const existingConversation = conversations.value.find(item => isSameId(item.doctorId, doctor.id))
  if (existingConversation) {
    // 如果会话存在且未被删除，直接使用
    await handleSelectConversation(existingConversation)
    showDoctorListDialog.value = false
    return
  }
  
  // 如果当前列表中没有，可能是被删除了，需要检查后端是否还有未删除的会话
  // 这里不检查已删除的会话，直接创建新会话
  
  try {
    const payload = {
      patientId: participantId.value,
      doctorId: doctor.id,
      title: `${doctor.doctorName || '医生'} · 对话`,
      summary: doctor.specialty || doctor.summary || '智能康复沟通会话'
    }
    const res = await createConversation(payload)
    if (res.data && res.data.id) {
      const newConversationId = res.data.id
      showDoctorListDialog.value = false
      historyVisible.value = false
      
      await loadConversations(false)
      
      const createdConversation = conversations.value.find(c => 
        isSameId(c.id, newConversationId) || 
        (isSameId(c.doctorId, doctor.id) && conversations.value.indexOf(c) === 0)
      )
      
      if (createdConversation) {
        await handleSelectConversation(createdConversation)
      } else {
        currentConversation.value = { ...res.data }
        await loadMessages(res.data.id)
      }
      
      message.success('对话已创建')
    } else {
      message.error('创建会话失败：未返回会话数据')
    }
  } catch (error) {
    console.error('发起对话失败', error)
    message.error(error?.message || '发起对话失败')
  }
}

const handlePatientSelect = async (patient) => {
  if (activeRole.value !== 'DOCTOR' && activeRole.value !== 'ADMIN') return
  
  // 查找已存在的会话
  let target = conversations.value.find((item) => {
    if (activeRole.value === 'ADMIN') {
      // 管理员端：查找 ADMIN_USER 类型的会话
      if (item.conversationType === 'ADMIN_USER') {
        return (item.participant1UserId && String(item.participant1UserId) === String(patient.id)) ||
               (item.participant2UserId && String(item.participant2UserId) === String(patient.id))
      }
      // 也检查普通会话
      return String(item.patientId) === String(patient.id)
    } else {
      // 医生端：查找普通会话
      return String(item.patientId) === String(patient.id)
    }
  })
  
  if (target) {
    return handleSelectConversation(target)
  } else {
    // 管理员端：如果没有会话，创建新会话
    if (activeRole.value === 'ADMIN') {
      try {
        const newConversation = await createConversation({
          patientId: patient.id,
          conversationType: 'ADMIN_USER',
          title: `${patient.name} x 管理员`,
          summary: '与管理员对话'
        })
        await loadConversations(false, true)
        const updatedConversation = conversations.value.find(c => c.id === newConversation.data?.id)
        if (updatedConversation) {
          await handleSelectConversation(updatedConversation)
        }
      } catch (error) {
        message.error('创建会话失败')
      }
    } else {
      message.warning('暂无与该患者的对话')
    }
  }
}

const handleDeleteConversation = async (conversation) => {
  if (!conversation?.id) return
  try {
    await ElMessageBox.confirm(
      `确认删除「${conversation.title}」？删除后您将无法看到此会话，但对方仍可查看。`,
      '删除会话',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    deletingConversationId.value = conversation.id
    const deleteRole = conversation.conversationType === 'ADMIN_USER' && activeRole.value === 'ADMIN' 
                      ? 'DOCTOR'
                      : activeRole.value
    await deleteConversation(conversation.id, deleteRole)
    message.success('会话已删除')
    
    // 如果当前选中的会话被删除，清空当前会话和消息
    if (currentConversation.value?.id === conversation.id) {
      currentConversation.value = null
      messages.value = []
    }
    
    // 重新加载会话列表（会自动过滤掉被删除的会话）
    // 如果历史记录抽屉是打开的，使用 skipAutoSelect=true 避免自动选择会话
    await loadConversations(true, historyVisible.value)
  } catch (error) {
    if (error !== 'cancel') {
      message.error(error?.message || '删除会话失败')
    }
  } finally {
    deletingConversationId.value = null
  }
}

const handleDeleteAllConversations = async () => {
  if (!participantId.value) {
    message.warning('请先完成登录信息加载')
    return
  }
  
  if (conversations.value.length === 0) {
    message.warning('没有可删除的会话')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确认清空所有历史对话？删除后您将无法看到这些会话，但对方仍可查看。`,
      '清空历史对话',
      {
        confirmButtonText: '清空',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    deletingAll.value = true
    const deleteRole = activeRole.value === 'ADMIN' ? 'DOCTOR' : activeRole.value
    await deleteAllConversations(participantId.value, deleteRole)
    message.success('已清空所有历史对话')
    
    currentConversation.value = null
    messages.value = []
    conversations.value = []
    historyVisible.value = false
  } catch (error) {
    if (error !== 'cancel') {
      message.error(error?.message || '清空历史对话失败')
    }
  } finally {
    deletingAll.value = false
  }
}

const handleSend = async () => {
  if (!currentConversation.value) {
    message.warning('请先选择一个会话')
    return
  }
  if (!currentConversation.value.id) {
    message.error('当前会话无效，请重新选择')
    return
  }
  if (!messageInput.value || !messageInput.value.trim()) {
    return
  }

  if (activeRole.value === 'DOCTOR' && !doctorStore.doctorInfo) {
    await doctorStore.fetchDoctorInfo()
  }

  sending.value = true
  try {
    let senderId
    const isAdminConversation = currentConversation.value?.conversationType === 'ADMIN_USER'
    
    if (isAdminConversation) {
      senderId = userStore.userInfo?.id
    } else if (activeRole.value === 'DOCTOR') {
      senderId = participantId.value
      if (!senderId) {
        message.warning('医生信息未加载，无法发送消息')
        return
      }
    } else {
      senderId = userStore.userInfo?.id
    }
    
    // 确定发送者头像
    let senderAvatar
    if (activeRole.value === 'DOCTOR') {
      // 医生：优先使用医生头像，其次用户头像，最后使用默认头像
      senderAvatar = doctorStore.doctorInfo?.avatar || 
                     userStore.userInfo?.avatar || 
                     roleFallbackAvatar(activeRole.value)
    } else {
      // 患者和管理员：使用用户头像或默认头像
      senderAvatar = userStore.userInfo?.avatar || roleFallbackAvatar(activeRole.value)
    }
    
    const payload = {
      senderRole: activeRole.value,
      senderId: senderId,
      senderName: activeRole.value === 'DOCTOR'
        ? doctorStore.doctorInfo?.doctorName || userStore.userInfo?.realName || '医生'
        : activeRole.value === 'ADMIN'
        ? userStore.userInfo?.realName || userStore.userInfo?.username || '管理员'
        : userStore.userInfo?.realName || userStore.userInfo?.username || '患者',
      senderAvatar: senderAvatar,
      content: messageInput.value.trim(),
      contentType: 'TEXT'
    }
    const res = await sendMessage(currentConversation.value.id, payload)
    messageInput.value = ''
    
    if (res.code === 200 && res.data) {
      const exists = messages.value.some(msg => msg.id === res.data.id)
      if (!exists) {
        messages.value.push({
          id: res.data.id,
          conversationId: res.data.conversationId,
          senderId: res.data.senderId,
          senderRole: res.data.senderRole,
          senderName: res.data.senderName || payload.senderName,
          // 如果后端返回的头像为空，使用发送时设置的头像
          senderAvatar: res.data.senderAvatar || payload.senderAvatar,
          content: res.data.content,
          contentType: res.data.contentType,
          sentAt: res.data.sentAt,
          timestamp: res.data.sentAt
        })
      }
    }
    
    scrollMessagesToBottom()
  } catch (error) {
    message.error(error?.message || '发送消息失败')
  } finally {
    sending.value = false
  }
}

const handleSocketMessage = (frame) => {
  if (!frame?.body) {
    return
  }
  try {
    const event = JSON.parse(frame.body)
    if (!event?.conversationId) {
      return
    }
    applyIncomingEvent(event)
  } catch (error) {
    // 静默失败
  }
}

const applyIncomingEvent = async (event) => {
  if (activeRole.value === 'DOCTOR' && !doctorStore.doctorInfo) {
    await doctorStore.fetchDoctorInfo()
  }

  const resolvedAvatar = resolveSenderAvatar(event)
  event.senderAvatar = resolvedAvatar
  
  const incomingMessage = {
    id: event.messageId,
    conversationId: event.conversationId,
    senderId: event.senderId,
    senderRole: event.senderRole,
    senderName: event.senderName,
    senderAvatar: resolvedAvatar,
    content: event.content,
    contentType: event.contentType,
    sentAt: event.sentAt,
    timestamp: event.sentAt
  }

  const isOwnMessage = (() => {
    const senderRoleUpper = event.senderRole?.toUpperCase()
    if (senderRoleUpper && senderRoleUpper !== activeRole.value) {
      return false
    }
    
    const isAdminConversation = event.conversationType === 'ADMIN_USER' || 
                                (currentConversation.value?.conversationType === 'ADMIN_USER')
    
    if (event.senderId != null) {
      if (activeRole.value === 'DOCTOR') {
        if (isAdminConversation) {
          return String(event.senderId) === String(userStore.userInfo?.id)
        } else {
          if (participantId.value == null) {
            return false
          }
          return String(event.senderId) === String(participantId.value)
        }
      } else {
        return String(event.senderId) === String(userStore.userInfo?.id)
      }
    }
    
    if (activeRole.value === 'DOCTOR') {
      return false
    }
    return senderRoleUpper === activeRole.value
  })()

  const isCurrentConversation = currentConversation.value?.id === event.conversationId
  const shouldShowNotification = !isOwnMessage && (!isCurrentConversation || !document.hasFocus())
  
  if (shouldShowNotification) {
    showBrowserNotification(event)
  }

  if (isCurrentConversation) {
    const exists = messages.value.some(msg => msg.id === incomingMessage.id)
    if (!exists) {
      messages.value = [...messages.value, incomingMessage]
      scrollMessagesToBottom()
    }
  }

  // 保存当前会话信息
  const currentConversationId = currentConversation.value?.id
  const savedCurrentConversation = currentConversation.value ? { ...currentConversation.value } : null
  const savedMessages = [...messages.value]
  
  // 刷新会话列表
  await loadConversations(false)
  
  // 确保当前会话仍然被选中
  if (currentConversationId && savedCurrentConversation) {
    const preservedConversation = conversations.value.find(c => c.id === currentConversationId)
    if (preservedConversation) {
      currentConversation.value = { ...preservedConversation }
      const messagesBelongToCurrentConversation = messages.value.length > 0 && 
        messages.value.every(msg => msg.conversationId === currentConversationId)
      
      if (!messagesBelongToCurrentConversation) {
        await loadMessages(preservedConversation.id, false)
      } else {
        if (messages.value.length === 0 && savedMessages.length > 0) {
          messages.value = savedMessages
        }
      }
    } else {
      let matched = null
      if (activeRole.value === 'PATIENT' && savedCurrentConversation.doctorId) {
        matched = conversations.value.find(c => isSameId(c.doctorId, savedCurrentConversation.doctorId))
      } else if ((activeRole.value === 'DOCTOR' || activeRole.value === 'ADMIN') && savedCurrentConversation.patientId) {
        matched = conversations.value.find(c => isSameId(c.patientId, savedCurrentConversation.patientId))
      }
      
      if (matched) {
        currentConversation.value = { ...matched }
        const messagesBelongToMatchedConversation = messages.value.length > 0 && 
          messages.value.every(msg => msg.conversationId === matched.id)
        
        if (!messagesBelongToMatchedConversation) {
          await loadMessages(matched.id, false)
        }
      } else {
        if (savedCurrentConversation.id) {
          currentConversation.value = savedCurrentConversation
          if (messages.value.length === 0 && savedMessages.length > 0) {
            messages.value = savedMessages
          }
        } else if (conversations.value.length > 0) {
          await handleSelectConversation(conversations.value[0])
        } else {
          currentConversation.value = null
          messages.value = []
        }
      }
    }
  }
  
  updatePageTitle()

  if (isCurrentConversation && !isOwnMessage) {
    markConversationAsReadRequest(currentConversation.value)
  }
}

const showBrowserNotification = (event) => {
  if (!('Notification' in window)) {
    return
  }

  if (Notification.permission === 'default') {
    Notification.requestPermission().then(permission => {
      if (permission === 'granted') {
        createNotification(event)
      }
    })
  } else if (Notification.permission === 'granted') {
    createNotification(event)
  }
}

const createNotification = (event) => {
  const title = `${event.senderName || '新消息'}`
  const options = {
    body: event.content || event.lastMessagePreview || '您有一条新消息',
    icon: event.senderAvatar || roleFallbackAvatar(event.senderRole),
    badge: '/favicon.ico',
    tag: `conversation-${event.conversationId}`,
    requireInteraction: false
  }

  const notification = new Notification(title, options)
  
  notification.onclick = () => {
    window.focus()
    const conversation = conversations.value.find(c => c.id === event.conversationId)
    if (conversation) {
      handleSelectConversation(conversation)
    }
    notification.close()
  }

  setTimeout(() => {
    notification.close()
  }, 5000)
}

const connectConversationSocket = () => {
  if (!userStore.token || stompClient.value?.connected) {
    return
  }

  const client = new Client({
    webSocketFactory: () => new SockJS(`/ws?token=${encodeURIComponent(userStore.token)}`),
    reconnectDelay: 5000,
    heartbeatIncoming: 10000,
    heartbeatOutgoing: 10000
  })

  client.onConnect = () => {
    isSocketConnected.value = true
    conversationSubscription.value = client.subscribe('/user/queue/conversations', handleSocketMessage)
  }

  client.onDisconnect = () => {
    isSocketConnected.value = false
    conversationSubscription.value = null
  }

  client.onStompError = (frame) => {
    // 静默失败
  }

  client.onWebSocketError = (event) => {
    // 静默失败
  }

  client.activate()
  stompClient.value = client
}

const disconnectConversationSocket = () => {
  try {
    conversationSubscription.value?.unsubscribe()
  } catch (error) {
    // 静默失败
  }
  conversationSubscription.value = null

  if (stompClient.value) {
    try {
      stompClient.value.deactivate()
    } catch (error) {
      // 静默失败
    }
    stompClient.value = null
  }

  isSocketConnected.value = false
}

// 监听标记所有对话为已读的事件
const handleConversationsMarkedAllRead = async (event) => {
  const { role, userId } = event.detail || {}
  // 检查是否是当前用户的角色
  if (role && role.toUpperCase() === activeRole.value) {
    // 如果是当前用户，刷新对话列表
    await loadConversations(false, true)
  }
}

onMounted(async () => {
  if (activeRole.value === 'DOCTOR' && !doctorStore.doctorInfo) {
    await doctorStore.fetchDoctorInfo()
  }
  
  if (activeRole.value === 'ADMIN') {
    // 管理员端：加载所有用户
    await loadUsers()
  } else {
    // 其他角色：加载会话
    await Promise.all([
      loadConversations(),
      activeRole.value === 'PATIENT' ? loadDoctors() : Promise.resolve()
    ])
  }
  
  if (conversations.value.length > 0 && !currentConversation.value) {
    const sortedConversations = [...conversations.value].sort((a, b) => {
      const timeA = (a.updatedAt || a.lastMessageTime) ? dayjs(a.updatedAt || a.lastMessageTime).valueOf() : 0
      const timeB = (b.updatedAt || b.lastMessageTime) ? dayjs(b.updatedAt || b.lastMessageTime).valueOf() : 0
      return timeB - timeA
    })
    await handleSelectConversation(sortedConversations[0])
  }
  connectConversationSocket()
  updatePageTitle()
  
  // 监听标记所有对话为已读的事件
  window.addEventListener('conversations-marked-all-read', handleConversationsMarkedAllRead)
})

watch(messages, () => {
  scrollMessagesToBottom()
})

watch(historyVisible, (visible) => {
  if (visible) {
    // 打开历史记录抽屉时，只刷新列表，不自动选择会话
    loadConversations(true, true)
  }
})

watch(totalUnreadCount, () => {
  updatePageTitle()
})

onUnmounted(() => {
  disconnectConversationSocket()
  // 移除事件监听
  window.removeEventListener('conversations-marked-all-read', handleConversationsMarkedAllRead)
})
</script>

<style scoped>
:root {
  color-scheme: light dark;
}

.dialogue-shell {
  width: 100%;
  min-height: calc(100vh - 120px);
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #e0edff, #fdf2f8);
  border-radius: 28px;
  box-shadow: 0 25px 70px rgba(15, 23, 42, 0.12);
}

.panel {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.panel-header h2 {
  margin: 0;
}

.panel-header p {
  margin: 4px 0 0;
  color: #6b7280;
  font-size: 13px;
}

.panel-actions {
  display: flex;
  gap: 6px;
}

.side-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 4px;
}

.person-item {
  display: flex;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 18px;
  background: rgba(148, 163, 184, 0.09);
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 14px;
  border: 1px solid transparent;
}

.person-item.active,
.person-item:hover {
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  transform: translateY(-1px);
}

.person-item .info {
  flex: 1;
  min-width: 0;
}

.person-item .info-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.person-item .info strong {
  font-size: 16px;
  flex: 1;
  min-width: 0;
}

.person-item .info .unread-badge {
  flex-shrink: 0;
}

.person-item .info small {
  display: block;
  color: #6b7280;
  margin-top: 4px;
}

.chat-view {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 32px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chat-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.chat-meta strong {
  display: block;
  font-size: 20px;
}

.chat-meta span {
  color: #6b7280;
  font-size: 14px;
}

.message-board {
  flex: 1;
  background: #f8fafc;
  border-radius: 24px;
  padding: 24px;
  overflow-y: auto;
}

.message-row {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.message-row.self {
  flex-direction: row-reverse;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  object-fit: cover;
}

.avatar.sm {
  width: 44px;
  height: 44px;
  border-radius: 14px;
}

.message-content {
  max-width: 70%;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.message-row.self .message-content {
  align-items: flex-end;
  text-align: right;
}

.message-meta {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.nickname {
  font-weight: 600;
}

.timestamp {
  color: #94a3b8;
}

.message {
  padding: 14px 18px;
  border-radius: 18px;
  line-height: 1.6;
  max-width: 100%;
  word-break: break-word;
}

.message.other {
  background: #ffffff;
  border: 1px solid rgba(15, 23, 42, 0.08);
  color: #0f172a;
  border-bottom-left-radius: 4px;
}

.message.self {
  background: #0ea5e9;
  color: #f8fafc;
  border-bottom-right-radius: 4px;
}

.composer {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.identity {
  font-size: 14px;
  color: #475569;
}

.identity span {
  font-weight: 600;
  margin-left: 6px;
}

.drawer-content {
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px;
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.3);
  margin-bottom: 16px;
  transition: all 0.2s ease;
}

.history-item:hover {
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
}

.history-item-content {
  flex: 1;
  cursor: pointer;
  min-width: 0;
}

.history-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #94a3b8;
  margin-bottom: 8px;
}

.history-title-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.history-head strong {
  color: #0f172a;
  font-size: 15px;
}

.history-unread-badge {
  flex-shrink: 0;
}

.history-item p {
  margin: 0;
  color: #475569;
  line-height: 1.5;
}

.doctor-select-item {
  display: flex;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 18px;
  background: rgba(148, 163, 184, 0.09);
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 12px;
  border: 1px solid transparent;
}

.doctor-select-item:hover {
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  transform: translateY(-1px);
}

.doctor-select-item .info {
  flex: 1;
  min-width: 0;
}

.doctor-select-item .info-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.doctor-select-item .info strong {
  font-size: 16px;
  flex: 1;
  min-width: 0;
}

.doctor-select-item .info small {
  display: block;
  color: #6b7280;
  margin-top: 4px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 60px 40px;
  text-align: center;
}

.empty-icon {
  margin-bottom: 24px;
  opacity: 0.6;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.empty-title {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 12px;
}

.empty-description {
  font-size: 15px;
  color: #64748b;
  margin: 0 0 32px;
  max-width: 400px;
  line-height: 1.6;
}

.empty-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 40px;
  flex-wrap: wrap;
  justify-content: center;
}

.empty-features {
  display: flex;
  gap: 32px;
  margin-top: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 14px;
}

.feature-item .el-icon {
  font-size: 18px;
  color: #3b82f6;
}

.loading-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 16px;
  color: #64748b;
}

.loading-messages-inline {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  color: #64748b;
  font-size: 14px;
}

.loading-icon {
  font-size: 32px;
  color: #3b82f6;
  animation: rotate 1s linear infinite;
}

.loading-messages-inline .loading-icon {
  font-size: 16px;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1100px) {
  .dialogue-shell {
    grid-template-columns: 1fr;
  }

  .message-content {
    max-width: 85%;
  }
  
  .empty-features {
    flex-direction: column;
    gap: 16px;
  }
}
</style>