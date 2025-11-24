<template>
  <div class="doctor-dashboard">
    <!-- 欢迎横幅 -->
    <div class="doctor-card welcome-card">
      <div class="card-body">
        <div class="welcome-content">
          <div class="welcome-text">
            <h1>{{ greeting }}，{{ doctorStore.doctorInfo?.doctorName || userStore.userInfo.realName }}医生！</h1>
            <p>今天是 {{ currentDate }}，祝您工作顺利</p>
          </div>
          <el-icon :size="100" color="#52c41a">
            <Van />
          </el-icon>
        </div>
      </div>
    </div>

    <!-- 今日数据统计 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <div class="doctor-stat-card blue">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Calendar />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ doctorStore.todayStats.appointments }}</div>
              <div class="stat-label">今日预约</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="doctor-stat-card green">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <CircleCheckFilled />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ doctorStore.todayStats.completed }}</div>
              <div class="stat-label">已接诊</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="doctor-stat-card orange">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Clock />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ doctorStore.todayStats.pending }}</div>
              <div class="stat-label">待接诊</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="doctor-stat-card red">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <TrendCharts />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ doctorStore.todayStats.total }}</div>
              <div class="stat-label">累计接诊</div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 今日排班 -->
    <div class="doctor-card">
      <div class="card-header">
        <h3>
          <el-icon>
            <Calendar />
          </el-icon>
          今日排班
        </h3>
        <div class="header-actions">
          <el-button type="primary" @click="router.push('/doctor/schedule')">
            <el-icon>
              <Setting />
            </el-icon>
            管理排班
          </el-button>
        </div>
      </div>
      <div class="card-body">
        <div class="doctor-table">
          <el-table :data="todaySchedule" stripe v-loading="loading">
            <el-table-column prop="timeSlot" label="时段" width="120">
              <template #default="{ row }">
                <el-tag :type="getTimeSlotType(row.timeSlot)" size="large">{{ row.timeSlot }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="totalQuota" label="总号源" width="100">
              <template #default="{ row }">
                <span style="font-weight: bold">{{ row.totalQuota }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="bookedQuota" label="已预约" width="100">
              <template #default="{ row }">
                <span style="color: #409eff; font-weight: bold">{{ row.bookedQuota }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="remainingQuota" label="剩余号源" width="100">
              <template #default="{ row }">
                <span :style="{ color: row.remainingQuota > 0 ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
                  {{ row.remainingQuota }}
                </span>
              </template>
            </el-table-column>
            <el-table-column label="使用率" width="250">
              <template #default="{ row }">
                <el-progress :percentage="((row.bookedQuota / row.totalQuota) * 100).toFixed(0) * 1"
                  :color="getProgressColor(row.bookedQuota, row.totalQuota)" :stroke-width="20">
                  <span style="font-size: 14px; font-weight: bold">
                    {{ ((row.bookedQuota / row.totalQuota) * 100).toFixed(0) }}%
                  </span>
                </el-progress>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="row.status === '可预约' ? 'success' : 'info'" size="large">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
          <div v-if="todaySchedule.length === 0" class="doctor-empty">
            <div class="empty-icon">
              <el-icon>
                <Calendar />
              </el-icon>
            </div>
            <div class="empty-text">今日暂无排班</div>
            <el-button type="primary" @click="router.push('/doctor/schedule')">
              去添加排班
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 评价统计 -->
    <div class="doctor-card">
      <div class="card-header">
        <h3>
          <el-icon>
            <StarFilled />
          </el-icon>
          患者评价统计
        </h3>
        <div class="header-actions">
          <el-button type="primary" @click="router.push('/doctor/reviews')">
            查看全部评价
          </el-button>
        </div>
      </div>
      <div class="card-body">
        <el-row :gutter="20">
          <el-col :xs="24" :md="8">
            <div class="review-summary">
              <div class="avg-rating">
                <div class="rating-number">{{ reviewStats.avgRating || '0.0' }}</div>
                <el-rate v-model="reviewStats.avgRating" disabled show-score text-color="#ff9900" />
              </div>
              <div class="review-stats-grid">
                <div class="stat-item">
                  <div class="stat-label">总评价数</div>
                  <div class="stat-value">{{ reviewStats.totalReviews || 0 }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">本月评价</div>
                  <div class="stat-value">{{ reviewStats.monthlyReviews || 0 }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">好评率</div>
                  <div class="stat-value">{{ reviewStats.goodRate || '0' }}%</div>
                </div>
              </div>
            </div>
          </el-col>
          <el-col :xs="24" :md="16">
            <div ref="reviewChartRef" style="width: 100%; height: 300px;"></div>
          </el-col>
        </el-row>
      </div>
    </div>

    <el-row :gutter="20">
      <!-- 待接诊患者 -->
      <el-col :xs="24" :lg="12">
        <div class="doctor-card patient-card">
          <div class="card-header">
            <h3>
              <el-icon>
                <Bell />
              </el-icon>
              待接诊患者
              <el-badge :value="pendingPatients.length" type="warning" style="margin-left: 8px" />
            </h3>
            <div class="header-actions">
              <el-button type="primary" @click="router.push('/doctor/patients')">
                查看全部
              </el-button>
            </div>
          </div>
          <div class="card-body">
            <div class="patient-list">
              <div v-for="patient in pendingPatients" :key="patient.queueNumber" class="patient-item pending">
                <div class="patient-header">
                  <div class="queue-badge">
                    <span class="queue-number">{{ patient.queueNumber }}</span>
                    <span class="queue-label">号</span>
                  </div>
                  <div class="patient-info">
                    <h4>{{ patient.patientName }}</h4>
                    <p>
                      <el-icon>
                        <User />
                      </el-icon> {{ patient.gender }} | {{ patient.age }}岁 |
                      <el-icon>
                        <Phone />
                      </el-icon> {{ patient.phone }}
                    </p>
                    <p>
                      <el-icon>
                        <Clock />
                      </el-icon> {{ patient.timeSlot }} {{ patient.appointmentTime }}
                    </p>
                  </div>
                  <div class="patient-action">
                    <el-button type="success" @click="startConsultation(patient)">
                      <el-icon>
                        <Checked />
                      </el-icon>
                      开始接诊
                    </el-button>
                  </div>
                </div>
              </div>
              <div v-if="pendingPatients.length === 0" class="doctor-empty">
                <div class="empty-icon">
                  <el-icon>
                    <User />
                  </el-icon>
                </div>
                <div class="empty-text">暂无待接诊患者</div>
              </div>
            </div>
          </div>
        </div>
      </el-col>

      <!-- 今日已接诊 -->
      <el-col :xs="24" :lg="12">
        <div class="doctor-card patient-card">
          <div class="card-header">
            <h3>
              <el-icon>
                <CircleCheckFilled />
              </el-icon>
              今日已接诊
              <el-badge :value="completedPatients.length" type="success" style="margin-left: 8px" />
            </h3>
            <div class="header-actions">
              <el-button type="primary" @click="router.push('/doctor/records')">
                接诊记录
              </el-button>
            </div>
          </div>
          <div class="card-body">
            <div class="patient-list">
              <div v-for="patient in completedPatients" :key="patient.queueNumber" class="patient-item completed">
                <div class="patient-header">
                  <div class="queue-badge completed-badge">
                    <span class="queue-number">{{ patient.queueNumber }}</span>
                    <span class="queue-label">号</span>
                  </div>
                  <div class="patient-info">
                    <h4>{{ patient.patientName }}</h4>
                    <p>
                      <el-icon>
                        <Clock />
                      </el-icon> 接诊时间：{{ patient.consultationTime }}
                    </p>
                    <p class="diagnosis-text">
                      <el-icon>
                        <Document />
                      </el-icon> {{ patient.diagnosis }}
                    </p>
                  </div>
                  <div class="patient-action">
                    <el-button size="small" @click="viewRecord(patient)">
                      查看详情
                    </el-button>
                  </div>
                </div>
              </div>
              <div v-if="completedPatients.length === 0" class="doctor-empty">
                <div class="empty-icon">
                  <el-icon>
                    <Document />
                  </el-icon>
                </div>
                <div class="empty-text">今日暂无接诊记录</div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 接诊弹窗 -->
    <ConsultationDialog 
      v-if="doctorStore.getDoctorId()" 
      v-model="consultationDialogVisible" 
      :patient-info="selectedPatient"
      :doctor-id="doctorStore.getDoctorId()" 
      @success="handleConsultationSuccess" 
    />
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useDoctorStore } from '@/stores/doctor'
import { useNotificationStore } from '@/stores/notification'
import { ElMessageBox } from 'element-plus'
import {
  Van,
  Calendar,
  CircleCheckFilled,
  Clock,
  TrendCharts,
  User,
  Phone,
  Checked,
  Document,
  Bell,
  Setting,
  StarFilled
} from '@element-plus/icons-vue'
import { getDoctorScheduleByDate } from '@/api/schedule'
import { getTodayPendingPatients, getTodayCompletedPatients } from '@/api/patient'
import { createConsultationRecord, startConsultation as startConsultationApi } from '@/api/consultation'
import { getDoctorReviewStats } from '@/api/statistics'
import ConsultationDialog from '@/components/doctor/ConsultationDialog.vue'
import * as echarts from 'echarts'
import dayjs from 'dayjs'

const router = useRouter()
const userStore = useUserStore()
const doctorStore = useDoctorStore()
const notificationStore = useNotificationStore()

// 接诊弹窗
const consultationDialogVisible = ref(false)
const selectedPatient = ref({})

// ECharts实例引用
const reviewChartRef = ref(null)
let reviewChartInstance = null

// 通知计数，用于检测新通知
const lastNotificationCount = ref(0)

// 当前日期和问候语
const currentDate = computed(() => {
  const weekDays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  const dayOfWeek = dayjs().day()
  return dayjs().format('YYYY年MM月DD日') + ' ' + weekDays[dayOfWeek]
})

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return '早上好'
  if (hour < 18) return '下午好'
  return '晚上好'
})


// 加载状态
const loading = ref(false)

// 今日排班
const todaySchedule = ref([])

// 待接诊患者
const pendingPatients = ref([])

// 已接诊患者
const completedPatients = ref([])

// 评价统计
const reviewStats = ref({
  avgRating: 0,
  totalReviews: 0,
  monthlyReviews: 0,
  goodRate: 0
})

// 加载今日排班
const loadTodaySchedule = async () => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) {

    return
  }

  try {
    loading.value = true
    const today = dayjs().format('YYYY-MM-DD')
    const res = await getDoctorScheduleByDate(doctorId, today)
    if (res.code === 200) {
      todaySchedule.value = res.data || []
    }
  } catch (error) {

    message.error('加载今日排班失败')
  } finally {
    loading.value = false
  }
}

// 加载待接诊患者
const loadPendingPatients = async () => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) return

  try {
    const res = await getTodayPendingPatients(doctorId + '')
    if (res.code === 200) {
      pendingPatients.value = res.data || []
    }
  } catch (error) {

    message.error('加载待接诊患者失败')
  }
}

// 加载已接诊患者
const loadCompletedPatients = async () => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) return

  try {
    const res = await getTodayCompletedPatients(doctorId + '')
    if (res.code === 200) {
      completedPatients.value = res.data || []
    }
  } catch (error) {

    message.error('加载已接诊患者失败')
  }
}

// 获取时段类型
const getTimeSlotType = (slot) => {
  const typeMap = {
    '上午': 'success',
    '下午': 'warning',
    '晚间': 'danger'
  }
  return typeMap[slot] || 'info' // 默认返回 'info' 而不是空字符串
}

// 获取进度条颜色
const getProgressColor = (booked, total) => {
  const rate = booked / total
  if (rate < 0.5) return '#67c23a'
  if (rate < 0.8) return '#e6a23c'
  return '#f56c6c'
}

// 开始接诊
const startConsultation = async (patient) => {
  try {
    // 调用后端API开始接诊
    const res = await startConsultationApi(patient.appointmentId)

    if (res.code === 200) {
      message.success('开始接诊成功，已提醒患者进行体质测试')
      // 刷新数据
      handleConsultationSuccess()
    } else {
      message.error(res.message || '开始接诊失败')
    }
  } catch (error) {

    message.error('开始接诊失败')
  }
}

// 接诊成功回调
const handleConsultationSuccess = () => {
  // 刷新数据
  doctorStore.fetchTodayStats()
  loadPendingPatients()
  loadCompletedPatients()
}

// 查看接诊记录
const viewRecord = (record) => {
  message.info(`查看接诊记录：${record.patientName}`)
  router.push('/doctor/records')
}

// 加载评价统计
const loadReviewStats = async () => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) return

  try {
    const res = await getDoctorReviewStats(doctorId)
    if (res.code === 200) {
      reviewStats.value = res.data || {
        avgRating: 0,
        totalReviews: 0,
        monthlyReviews: 0,
        goodRate: 0
      }
      // 加载完数据后初始化图表
      await nextTick()
      initReviewChart()
    }
  } catch (error) {

  }
}

// 初始化评价图表
const initReviewChart = () => {
  if (!reviewChartRef.value) return

  reviewChartInstance = echarts.init(reviewChartRef.value)

  // 模拟评分分布数据（实际应该从后端获取）
  const ratingDistribution = [
    { rating: '5星', count: Math.floor((reviewStats.value.totalReviews || 0) * 0.6) },
    { rating: '4星', count: Math.floor((reviewStats.value.totalReviews || 0) * 0.25) },
    { rating: '3星', count: Math.floor((reviewStats.value.totalReviews || 0) * 0.1) },
    { rating: '2星', count: Math.floor((reviewStats.value.totalReviews || 0) * 0.03) },
    { rating: '1星', count: Math.floor((reviewStats.value.totalReviews || 0) * 0.02) }
  ]

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ratingDistribution.map(item => item.rating),
      axisLabel: {
        color: '#666'
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#666'
      }
    },
    series: [
      {
        name: '评价数量',
        type: 'bar',
        data: ratingDistribution.map(item => item.count),
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: '#52c41a' },
              { offset: 1, color: '#73d13d' }
            ]
          },
          borderRadius: [8, 8, 0, 0]
        },
        barWidth: '50%'
      }
    ]
  }

  reviewChartInstance.setOption(option)

  // 响应式调整
  window.addEventListener('resize', () => {
    reviewChartInstance?.resize()
  })
}

// 监听通知变化，当收到预约相关通知时自动刷新数据
watch(() => notificationStore.unread, (newNotifications, oldNotifications) => {
  // 检查是否有新通知（通知数量增加）
  if (newNotifications && newNotifications.length > lastNotificationCount.value) {
    const latestNotification = newNotifications[0] // 最新的通知在数组第一个位置
    const appointmentRelatedTypes = ['APPOINTMENT_CREATED', 'APPOINTMENT_CANCELLED', 'CONSTITUTION_TEST_COMPLETED']
    
    // 如果是预约相关通知，刷新待接诊患者列表和统计数据
    if (latestNotification && latestNotification.type && appointmentRelatedTypes.includes(latestNotification.type)) {

      // 刷新待接诊患者列表
      loadPendingPatients()
      // 刷新统计数据
      doctorStore.fetchTodayStats()
      
      // 如果是取消预约，也需要刷新已接诊列表（可能从待接诊移除了）
      if (latestNotification.type === 'APPOINTMENT_CANCELLED') {
        loadCompletedPatients()
      }
    }
    // 更新通知计数
    lastNotificationCount.value = newNotifications.length
  } else if (newNotifications) {
    // 通知数量减少（标记已读），更新计数
    lastNotificationCount.value = newNotifications.length
  }
}, { deep: true, immediate: true })

onMounted(async () => {
  // 先加载医生信息
  await doctorStore.fetchDoctorInfo()
  // 加载今日统计
  await doctorStore.fetchTodayStats()
  // 加载其他数据
  loadTodaySchedule()
  loadPendingPatients()
  loadCompletedPatients()
  loadReviewStats()
  // 初始化通知计数
  lastNotificationCount.value = notificationStore.unread?.length || 0
})
</script>

<style scoped lang="scss">
.doctor-dashboard {
  max-width: 1400px;
  margin: 0 auto;

  .welcome-card {
    margin-bottom: 20px;

    .welcome-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px;
      background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
      border-radius: 12px;
      color: white;

      .welcome-text {
        h1 {
          margin: 0 0 10px 0;
          font-size: 28px;
          font-weight: 600;
        }

        p {
          margin: 0;
          font-size: 16px;
          opacity: 0.9;
        }
      }
    }
  }

  .stats-row {
    margin-bottom: 20px;

    .stat-card {
      margin-bottom: 20px;
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        transform: translateY(-5px);
      }

      &.blue :deep(.el-icon) {
        color: #409eff;
      }

      &.green :deep(.el-icon) {
        color: #67c23a;
      }

      &.orange :deep(.el-icon) {
        color: #e6a23c;
      }

      &.red :deep(.el-icon) {
        color: #f56c6c;
      }
    }
  }

  h3 {
    margin: 0;
    font-size: 16px;
    color: #333;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  // 评价统计样式
  .review-summary {
    padding: 20px;
    text-align: center;

    .avg-rating {
      margin-bottom: 30px;

      .rating-number {
        font-size: 48px;
        font-weight: bold;
        color: #52c41a;
        margin-bottom: 10px;
      }
    }

    .review-stats-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 15px;

      .stat-item {
        padding: 15px;
        background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
        border-radius: 8px;

        .stat-label {
          font-size: 14px;
          color: #666;
          margin-bottom: 8px;
        }

        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: #52c41a;
        }
      }
    }
  }

  .patient-card {
    min-height: 500px;
  }

  .patient-list {
    max-height: 450px;
    overflow-y: auto;
  }

  .patient-item {
    padding: 20px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    margin-bottom: 15px;
    transition: all 0.3s;

    &:hover {
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    }

    &.pending {
      border-left: 4px solid #e6a23c;
      background: #fef9f0;
    }

    &.completed {
      border-left: 4px solid #67c23a;
      background: #f0f9ff;
    }

    .patient-header {
      display: flex;
      gap: 20px;
      align-items: center;

      .queue-badge {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #e6a23c 0%, #f56c6c 100%);
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        flex-shrink: 0;

        &.completed-badge {
          background: linear-gradient(135deg, #67c23a 0%, #409eff 100%);
        }

        .queue-number {
          font-size: 24px;
          font-weight: bold;
          line-height: 1;
        }

        .queue-label {
          font-size: 12px;
        }
      }

      .patient-info {
        flex: 1;

        h4 {
          margin: 0 0 8px 0;
          font-size: 18px;
          color: #333;
        }

        p {
          margin: 5px 0;
          color: #666;
          font-size: 14px;
          display: flex;
          align-items: center;
          gap: 5px;

          .el-icon {
            color: #909399;
          }
        }

        .diagnosis-text {
          color: #409eff;
          font-weight: 500;
        }
      }

      .patient-action {
        flex-shrink: 0;
      }
    }
  }
}
</style>
