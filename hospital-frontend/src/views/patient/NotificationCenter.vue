<template>
  <div class="notification-center">
    <div class="page-header">
      <h2>消息中心</h2>
      <div class="header-actions">
        <el-button 
          type="primary" 
          :disabled="selectedNotifications.length === 0"
          @click="handleBatchRead"
        >
          批量标记已读 ({{ selectedNotifications.length }})
        </el-button>
      </div>
    </div>

    <!-- 消息分类标签 -->
    <div class="filter-tabs">
      <div class="primary-categories">
        <el-radio-group
          v-model="activePrimaryCategory"
          @change="handlePrimaryChange"
          size="default"
        >
          <el-radio-button
            v-for="category in notificationCategoryTree"
            :key="category.id"
            :label="category.id"
          >
            {{ category.label }}
          </el-radio-button>
        </el-radio-group>
      </div>

      <transition name="fade">
        <div
          v-if="secondaryCategories.length"
          class="sub-category secondary"
        >
          <el-radio-group
            v-model="activeSecondaryCategory"
            @change="handleSecondaryCategoryChange"
            size="small"
            class="sub-radio-group"
          >
            <el-radio-button
              v-for="child in secondaryCategories"
              :key="child.id"
              :label="child.id"
            >
              {{ child.label }}
            </el-radio-button>
          </el-radio-group>
        </div>
      </transition>

      <transition name="fade">
        <div
          v-if="tertiaryCategories.length"
          class="sub-category tertiary"
        >
          <el-radio-group
            v-model="activeTertiaryCategory"
            @change="handleTertiaryCategoryChange"
            size="small"
            class="sub-radio-group"
          >
            <el-radio-button
              v-for="child in tertiaryCategories"
              :key="child.id"
              :label="child.id"
            >
              {{ child.label }}
            </el-radio-button>
          </el-radio-group>
        </div>
      </transition>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <el-radio-group v-model="readStatusFilter" @change="handleFilterChange" size="default">
        <el-radio-button :label="null">全部</el-radio-button>
        <el-radio-button :label="0">未读</el-radio-button>
        <el-radio-button :label="1">已读</el-radio-button>
      </el-radio-group>
      <div class="unread-count">
        <el-tag type="danger" v-if="unreadCount > 0">
          未读消息: {{ unreadCount }}
        </el-tag>
      </div>
    </div>

    <!-- 消息列表 -->
    <el-card
      class="notification-list-card"
      v-loading="loading"
      element-loading-text="加载中..."
      element-loading-background="rgba(255, 255, 255, 0.8)"
    >
      <div v-if="notificationList.length > 0">
        <el-checkbox 
          v-model="selectAll" 
          @change="handleSelectAll"
          style="margin-bottom: 15px;"
        >
          全选
        </el-checkbox>
        
        <div class="notification-list">
          <div
            v-for="notification in notificationList"
            :key="notification.id"
            :class="['notification-item', { 'unread': notification.readStatus === 0 }]"
            @click="handleNotificationClick(notification)"
          >
            <el-checkbox
              :model-value="selectedNotifications.includes(notification.id)"
              @change="(val) => handleSelectChange(notification.id, val)"
              @click.stop
              style="margin-right: 10px;"
            />
            <div class="notification-content">
              <div class="notification-header">
                <el-tag :type="getTypeTagType(notification.type)" size="small">
                  {{ getTypeName(notification.type) }}
                </el-tag>
                <span class="notification-title">{{ notification.title }}</span>
                <span class="notification-time">{{ formatTime(notification.createdAt) }}</span>
              </div>
              <div class="notification-body">
                <p>{{ notification.content }}</p>
              </div>
            </div>
            <div class="notification-status">
              <el-badge :value="notification.readStatus === 0 ? '未读' : ''" :hidden="notification.readStatus === 1">
                <el-icon v-if="notification.readStatus === 0" :size="20" style="color: #409eff;">
                  <Message />
                </el-icon>
              </el-badge>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>

      <el-empty v-else-if="!loading" description="暂无消息" />
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, onMounted, computed, reactive } from 'vue'
import { Message } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import { getNotifications, markNotificationAsRead, markAllNotificationsAsRead } from '@/api/notification'

// 数据
const loading = ref(false)
const notificationList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const activeType = ref('')
const readStatusFilter = ref(null)
const selectedNotifications = ref([])
const selectAll = ref(false)
const unreadCount = ref(0)

const notificationCategoryTree = [
  { id: 'ALL', label: '全部', value: '' },
  {
    id: 'COMMUNICATION',
    label: '沟通联络',
    children: [
      { id: 'COMMUNICATION_CONVERSATION', label: '对话消息', value: 'CONVERSATION_MESSAGE' },
      { id: 'COMMUNICATION_DOCTOR_REPLY', label: '医生回复', value: 'DOCTOR_REPLY' }
    ]
  },
  {
    id: 'APPOINTMENT',
    label: '预约与就诊',
    children: [
      {
        id: 'APPOINTMENT_FLOW',
        label: '预约流程',
        children: [
          { id: 'APPOINTMENT_CREATED', label: '预约创建', value: 'APPOINTMENT_CREATED' },
          { id: 'APPOINTMENT_CONFIRMED', label: '预约确认', value: 'APPOINTMENT_CONFIRMED' },
          { id: 'APPOINTMENT_CANCELLED', label: '预约取消', value: 'APPOINTMENT_CANCELLED' },
          { id: 'APPOINTMENT_COMPLETED', label: '预约完成', value: 'APPOINTMENT_COMPLETED' }
        ]
      },
      {
        id: 'APPOINTMENT_REMINDER',
        label: '提醒事项',
        children: [
          { id: 'CONSULTATION_REMINDER', label: '就诊提醒', value: 'CONSULTATION_REMINDER' }
        ]
      }
    ]
  },
  {
    id: 'HEALTH_MONITORING',
    label: '健康监测',
    children: [
      {
        id: 'CONSTITUTION_TEST',
        label: '体质测试',
        children: [
          { id: 'CONSTITUTION_TEST_REMINDER', label: '测试提醒', value: 'CONSTITUTION_TEST_REMINDER' },
          { id: 'CONSTITUTION_TEST_COMPLETED', label: '测试完成', value: 'CONSTITUTION_TEST_COMPLETED' }
        ]
      }
    ]
  },
  {
    id: 'FEEDBACK',
    label: '评价反馈',
    children: [
      { id: 'REVIEW', label: '就医反馈', value: 'REVIEW' }
    ]
  },
  { id: 'SYSTEM', label: '系统通知', value: 'SYSTEM' }
]

const activePrimaryCategory = ref(notificationCategoryTree[0].id)
const activeSecondaryCategory = ref(null)
const activeTertiaryCategory = ref(null)
const categorySelections = reactive({
  secondary: {},
  tertiary: {}
})

const secondaryCategories = computed(() => {
  const primary = notificationCategoryTree.find(item => item.id === activePrimaryCategory.value)
  return primary?.children || []
})

const tertiaryCategories = computed(() => {
  const secondary = secondaryCategories.value.find(item => item.id === activeSecondaryCategory.value)
  return secondary?.children || []
})

const handlePrimaryChange = () => handlePrimaryCategoryChange(true)

// 加载消息列表
const loadNotifications = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value
    }
    
    if (activeType.value) {
      params.type = activeType.value
    }
    
    if (readStatusFilter.value !== null) {
      params.readStatus = readStatusFilter.value
    }
    
    const res = await getNotifications(params)
    if (res.code === 200) {
      notificationList.value = res.data?.records || []
      total.value = Number(res.data?.total) || 0
      
      // 统计未读数
      if (activeType.value === '' && readStatusFilter.value === null) {
        countUnread()
      }
    }
  } catch (error) {
    console.error('加载消息列表失败', error)
    message.error('加载消息列表失败')
  } finally {
    loading.value = false
  }
}

// 统计未读数
const countUnread = async () => {
  try {
    const res = await getNotifications({ page: 1, pageSize: 1, readStatus: 0 })
    if (res.code === 200) {
      unreadCount.value = Number(res.data?.total) || 0
    }
  } catch (error) {
    console.error('统计未读数失败', error)
  }
}

// 处理类型变化
const handleTypeChange = () => {
  currentPage.value = 1
  selectedNotifications.value = []
  selectAll.value = false
  loadNotifications()
}

const applyTypeFromNode = (node) => {
  if (!node) return
  const nextType = node.value ?? ''
  if (nextType === activeType.value) {
    return
  }
  activeType.value = nextType
  handleTypeChange()
}

const handlePrimaryCategoryChange = (restore = false) => {
  const primaryNode = notificationCategoryTree.find(item => item.id === activePrimaryCategory.value)
  if (!primaryNode) return

  if (primaryNode.children?.length) {
    const savedSecondary = restore
      ? categorySelections.secondary[primaryNode.id]
      : null
    activeSecondaryCategory.value = savedSecondary || primaryNode.children[0].id
    handleSecondaryCategoryChange(true)
    return
  }

  activeSecondaryCategory.value = null
  activeTertiaryCategory.value = null
  applyTypeFromNode(primaryNode)
}

const handleSecondaryCategoryChange = (restore = false) => {
  const secondaryNode = secondaryCategories.value.find(item => item.id === activeSecondaryCategory.value)
  if (!secondaryNode) return
  categorySelections.secondary[activePrimaryCategory.value] = secondaryNode.id

  if (secondaryNode.children?.length) {
    const savedTertiary = restore
      ? categorySelections.tertiary[secondaryNode.id]
      : null
    activeTertiaryCategory.value = savedTertiary || secondaryNode.children[0].id
    handleTertiaryCategoryChange(true)
    return
  }

  activeTertiaryCategory.value = null
  applyTypeFromNode(secondaryNode)
}

const handleTertiaryCategoryChange = (restore = false) => {
  const tertiaryNode = tertiaryCategories.value.find(item => item.id === activeTertiaryCategory.value)
  if (!tertiaryNode) return
  categorySelections.tertiary[activeSecondaryCategory.value] = tertiaryNode.id
  applyTypeFromNode(tertiaryNode)
}

// 处理筛选变化
const handleFilterChange = () => {
  currentPage.value = 1
  selectedNotifications.value = []
  selectAll.value = false
  loadNotifications()
}

// 处理消息点击
const handleNotificationClick = async (notification) => {
  if (notification.readStatus === 0) {
    try {
      await markNotificationAsRead(notification.id)
      notification.readStatus = 1
      notification.readAt = new Date()
      unreadCount.value = Math.max(0, unreadCount.value - 1)
      message.success('已标记为已读')
    } catch (error) {
      console.error('标记已读失败', error)
      message.error('标记已读失败')
    }
  }
}

// 处理选择变化
const handleSelectChange = (id, checked) => {
  if (checked) {
    if (!selectedNotifications.value.includes(id)) {
      selectedNotifications.value.push(id)
    }
  } else {
    const index = selectedNotifications.value.indexOf(id)
    if (index > -1) {
      selectedNotifications.value.splice(index, 1)
    }
  }
  updateSelectAll()
}

// 处理全选
const handleSelectAll = (checked) => {
  if (checked) {
    selectedNotifications.value = notificationList.value.map(n => n.id)
  } else {
    selectedNotifications.value = []
  }
}

// 更新全选状态
const updateSelectAll = () => {
  selectAll.value = notificationList.value.length > 0 && 
    selectedNotifications.value.length === notificationList.value.length
}

// 批量标记已读
const handleBatchRead = async () => {
  if (selectedNotifications.value.length === 0) {
    message.warning('请选择要标记的消息')
    return
  }
  
  try {
    await markAllNotificationsAsRead(selectedNotifications.value)
    message.success('批量标记已读成功')
    
    // 更新列表中的状态
    notificationList.value.forEach(notification => {
      if (selectedNotifications.value.includes(notification.id)) {
        notification.readStatus = 1
        notification.readAt = new Date()
      }
    })
    
    // 更新未读数
    unreadCount.value = Math.max(0, unreadCount.value - selectedNotifications.value.length)
    
    selectedNotifications.value = []
    selectAll.value = false
  } catch (error) {
    console.error('批量标记已读失败', error)
    message.error('批量标记已读失败')
  }
}

// 获取类型名称
const getTypeName = (type) => {
  const typeMap = {
    SYSTEM: '系统通知',
    CONVERSATION_MESSAGE: '对话消息',
    DOCTOR_REPLY: '医生回复',
    APPOINTMENT_CREATED: '预约创建',
    APPOINTMENT_CONFIRMED: '预约确认',
    APPOINTMENT_CANCELLED: '预约取消',
    APPOINTMENT_COMPLETED: '预约完成',
    CONSULTATION_REMINDER: '就诊提醒',
    CONSTITUTION_TEST_REMINDER: '体质测试提醒',
    CONSTITUTION_TEST_COMPLETED: '体质测试完成',
    REVIEW: '评价反馈'
  }
  return typeMap[type] || type || '未知类型'
}

// 获取类型标签颜色
const getTypeTagType = (type) => {
  const typeMap = {
    SYSTEM: 'info',
    CONVERSATION_MESSAGE: 'primary',
    DOCTOR_REPLY: 'success',
    APPOINTMENT_CREATED: 'warning',
    APPOINTMENT_CONFIRMED: 'success',
    APPOINTMENT_CANCELLED: 'danger',
    APPOINTMENT_COMPLETED: 'success',
    CONSULTATION_REMINDER: 'warning',
    CONSTITUTION_TEST_REMINDER: 'info',
    CONSTITUTION_TEST_COMPLETED: 'info',
    REVIEW: 'success'
  }
  return typeMap[type] || 'info'
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const now = dayjs()
  const timeObj = dayjs(time)
  const diff = now.diff(timeObj, 'day')
  
  if (diff === 0) {
    return timeObj.format('HH:mm')
  } else if (diff === 1) {
    return '昨天 ' + timeObj.format('HH:mm')
  } else if (diff < 7) {
    return timeObj.format('MM-DD HH:mm')
  } else {
    return timeObj.format('YYYY-MM-DD HH:mm')
  }
}

// 分页变化
const handlePageChange = (page) => {
  currentPage.value = page
  loadNotifications()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  loadNotifications()
}

// 页面加载
onMounted(() => {
  loadNotifications()
  countUnread()
})
</script>

<style scoped>
.notification-center {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.filter-tabs {
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.primary-categories {
  margin-bottom: 10px;
}

.sub-category {
  padding: 6px 0;
}

.sub-radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.sub-category + .sub-category {
  border-top: 1px dashed #e4e7ed;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.notification-list-card {
  min-height: 400px;
}

.loading-container {
  padding: 40px;
}

.notification-list {
  margin-top: 10px;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  margin-bottom: 10px;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.notification-item:hover {
  background: #f5f7fa;
  border-color: #409eff;
}

.notification-item.unread {
  background: #ecf5ff;
  border-color: #b3d8ff;
}

.notification-content {
  flex: 1;
  margin-left: 10px;
}

.notification-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.notification-title {
  flex: 1;
  font-weight: 500;
  color: #303133;
}

.notification-time {
  font-size: 12px;
  color: #909399;
}

.notification-body {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}

.notification-status {
  margin-left: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>

