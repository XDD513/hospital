<template>
  <div class="schedule-container">
    <!-- 排班统计 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="8">
        <div class="doctor-stat-card blue">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Calendar />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ scheduleStats.monthlyDays }}</div>
              <div class="stat-label">本月排班天数</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="8">
        <div class="doctor-stat-card green">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Tickets />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ scheduleStats.totalQuota }}</div>
              <div class="stat-label">本月总号源</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="8">
        <div class="doctor-stat-card orange">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <User />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ scheduleStats.bookedQuota }}</div>
              <div class="stat-label">已预约号源</div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <!-- 左侧：日历视图 -->
      <el-col :xs="24" :lg="14">
        <div class="doctor-card">
          <div class="card-header">
            <h3>
              <el-icon>
                <Calendar />
              </el-icon>
              排班日历
            </h3>
            <div class="header-actions">
              <!-- 月份切换 -->
              <div class="month-switcher">
                <el-button size="small" @click="prevMonth">
                  <el-icon>
                    <ArrowLeft />
                  </el-icon>
                  上月
                </el-button>
                <el-date-picker v-model="currentMonth" type="month" placeholder="选择月份" format="YYYY年MM月"
                  value-format="YYYY-MM" @change="onMonthChange" style="width: 150px; margin: 0 10px" />
                <el-button size="small" @click="nextMonth">
                  下月
                  <el-icon>
                    <ArrowRight />
                  </el-icon>
                </el-button>
                <el-button size="small" type="success" @click="goToToday" style="margin-left: 10px">
                  <el-icon>
                    <Calendar />
                  </el-icon>
                  回到今天
                </el-button>
              </div>
              <el-button type="primary" @click="showAddDialog">
                <el-icon>
                  <Plus />
                </el-icon>
                添加排班
              </el-button>
            </div>
          </div>

          <div class="card-body">
            <!-- 自定义日历表格 -->
            <div class="custom-calendar">
              <!-- 星期标题 -->
              <div class="calendar-header">
                <div class="week-day">日</div>
                <div class="week-day">一</div>
                <div class="week-day">二</div>
                <div class="week-day">三</div>
                <div class="week-day">四</div>
                <div class="week-day">五</div>
                <div class="week-day">六</div>
              </div>

              <!-- 日期格子 -->
              <div class="calendar-body">
                <div v-for="day in calendarDays" :key="day.date || Math.random()" class="calendar-cell" :class="{
                  'is-today': day.isToday,
                  'has-schedule': hasSchedule(day.date),
                  'is-selected': isSelectedDate(day.date),
                  'is-past': day.isPast,
                  'is-empty': day.isEmpty
                }" @click="selectDate(day.date)">
                  <div class="calendar-day">
                    <p class="day-number">{{ day.day }}</p>
                    <div v-if="hasSchedule(day.date)" class="schedule-badges">
                      <el-badge v-for="slot in getDateSchedules(day.date)" :key="slot.timeSlot"
                        :value="slot.remainingQuota" :type="slot.remainingQuota > 0 ? 'success' : 'danger'"
                        class="schedule-badge">
                        <el-tag size="small" :type="getTimeSlotTagType(slot.timeSlot)">
                          {{ formatTimeSlot(slot.timeSlot) }}
                        </el-tag>
                      </el-badge>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-col>

      <!-- 右侧：选中日期的排班详情 -->
      <el-col :xs="24" :lg="10">
        <div class="doctor-card detail-card">
          <div class="card-header">
            <h3>
              <el-icon>
                <Document />
              </el-icon>
              {{ formatSelectedDate(clickedDate) }} 排班详情
            </h3>
            <div class="header-actions">
              <el-button type="primary" @click="quickAddSchedule" v-if="clickedDate">
                <el-icon>
                  <Plus />
                </el-icon>
                添加
              </el-button>
            </div>
          </div>

          <div class="card-body">
            <div v-if="clickedDate">
              <!-- 该日期的排班列表 -->
              <div v-if="selectedDateSchedules.length > 0">
                <div v-for="schedule in selectedDateSchedules" :key="schedule.id" class="schedule-detail-item">
                  <div class="schedule-header">
                    <el-tag :type="getTimeSlotTagType(schedule.timeSlot)" size="large">
                      {{ formatTimeSlot(schedule.timeSlot) }}
                    </el-tag>
                    <el-tag :type="schedule.status === '可预约' ? 'success' : 'info'">
                      {{ schedule.status }}
                    </el-tag>
                  </div>

                  <div class="schedule-info">
                    <div class="info-row">
                      <span class="label">总号源：</span>
                      <span class="value">{{ schedule.totalQuota }} 个</span>
                    </div>
                    <div class="info-row">
                      <span class="label">已预约：</span>
                      <span class="value booked">{{ schedule.bookedQuota || schedule.totalQuota -
                        schedule.remainingQuota }} 个</span>
                    </div>
                    <div class="info-row">
                      <span class="label">剩余：</span>
                      <span class="value remaining">{{ schedule.remainingQuota }} 个</span>
                    </div>

                    <el-progress :percentage="getUsagePercentage(schedule)" :color="getProgressColor(schedule)"
                      :stroke-width="15" style="margin-top: 10px" />
                  </div>

                  <div class="schedule-actions">
                    <el-button size="small" @click="editSchedule(schedule)">
                      <el-icon>
                        <Edit />
                      </el-icon>
                      编辑
                    </el-button>
                    <el-button size="small" type="danger" @click="cancelSchedule(schedule)">
                      <el-icon>
                        <Delete />
                      </el-icon>
                      取消排班
                    </el-button>
                  </div>
                </div>
              </div>

              <!-- 该日期无排班 -->
              <div v-else class="doctor-empty">
                <div class="empty-icon">
                  <el-icon>
                    <Calendar />
                  </el-icon>
                </div>
                <div class="empty-text">该日期暂无排班</div>
                <el-button type="primary" @click="quickAddSchedule">
                  <el-icon>
                    <Plus />
                  </el-icon>
                  添加排班
                </el-button>
              </div>
            </div>

            <!-- 未选择日期 -->
            <div v-else class="doctor-empty">
              <div class="empty-icon">
                <el-icon>
                  <Calendar />
                </el-icon>
              </div>
              <div class="empty-text">请点击日历选择日期查看排班详情</div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 添加排班弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="日期" prop="date">
          <el-date-picker v-model="form.date" type="date" placeholder="选择日期" style="width: 100%"
            :disabled-date="disabledDate" @change="handleFieldBlur('date')" />
        </el-form-item>
        <el-form-item label="时段" prop="timeSlot">
          <el-select v-model="form.timeSlot" placeholder="请选择" style="width: 100%" @change="handleFieldBlur('timeSlot')">
            <el-option label="上午 (08:00-12:00)" value="MORNING" />
            <el-option label="下午 (14:00-17:00)" value="AFTERNOON" />
            <el-option label="晚间 (18:00-21:00)" value="EVENING" />
          </el-select>
        </el-form-item>
        <el-form-item label="号源数量" prop="totalQuota">
          <el-input-number v-model="form.totalQuota" :min="1" :max="50" style="width: 100%" @blur="handleFieldBlur('totalQuota')" />
          <span style="margin-left: 10px; color: #909399">建议：10-30个</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveSchedule" :loading="saving">
          {{ saving ? '保存中...' : '保存' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  ArrowRight,
  Plus,
  Edit,
  Delete,
  Calendar,
  Document,
  Tickets,
  User
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useDoctorStore } from '@/stores/doctor'
import { getDoctorScheduleByMonth, createSchedule, updateSchedule, deleteSchedule } from '@/api/schedule'
import dayjs from 'dayjs'
import { useFormValidation } from '@/composables/useFormValidation'

const userStore = useUserStore()
const doctorStore = useDoctorStore()

const currentMonth = ref(dayjs().format('YYYY-MM'))  // 当前显示的月份
const clickedDate = ref(dayjs().format('YYYY-MM-DD'))  // 初始选中今天
const dialogVisible = ref(false)
const dialogTitle = ref('添加排班')
const saving = ref(false)
const formRef = ref(null)

// 创建字段失焦处理函数
const { handleFieldBlur } = useFormValidation(formRef)

// 排班统计
const scheduleStats = reactive({
  monthlyDays: 0,
  totalQuota: 0,
  bookedQuota: 0
})

// 排班表单
const form = reactive({
  date: '',
  timeSlot: '',
  totalQuota: 10
})

// 表单验证规则
const formRules = {
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  timeSlot: [{ required: true, message: '请选择时段', trigger: 'change' }],
  totalQuota: [{ required: true, message: '请输入号源数量', trigger: 'blur' }]
}

// 排班列表
const schedules = ref([])

// 加载排班数据
const loadSchedules = async (month) => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) {

    return
  }

  try {
    const res = await getDoctorScheduleByMonth(doctorId, month)
    if (res.code === 200) {
      // 转换后端数据格式为前端需要的格式
      schedules.value = (res.data || []).map(schedule => ({
        id: schedule.id,
        date: schedule.scheduleDate,
        timeSlot: schedule.timeSlot,
        totalQuota: schedule.totalQuota,
        bookedQuota: schedule.bookedQuota,
        remainingQuota: schedule.remainingQuota,
        status: schedule.status === 'AVAILABLE' ? '可预约' : schedule.status === 'FULL' ? '已满' : '停诊'
      }))

      // 计算统计数据
      calculateStats()
    }
  } catch (error) {

  }
}

// 计算统计数据
const calculateStats = () => {
  // 获取本月所有排班的日期（去重）
  const uniqueDates = new Set(schedules.value.map(s => s.date))
  scheduleStats.monthlyDays = uniqueDates.size

  // 计算总号源和已预约号源
  scheduleStats.totalQuota = schedules.value.reduce((sum, s) => sum + s.totalQuota, 0)
  scheduleStats.bookedQuota = schedules.value.reduce((sum, s) => sum + s.bookedQuota, 0)
}

// 生成日历天数（只显示当月1号到最后一天）
const calendarDays = computed(() => {
  const year = parseInt(currentMonth.value.split('-')[0])
  const month = parseInt(currentMonth.value.split('-')[1])

  // 当月第一天
  const firstDay = dayjs(`${year}-${month}-01`)
  // 当月最后一天
  const lastDay = firstDay.endOf('month')
  // 当月天数
  const daysInMonth = lastDay.date()
  // 第一天是星期几（0-6，0是周日）
  const firstDayOfWeek = firstDay.day()

  const days = []

  // 填充第一周之前的空白
  for (let i = 0; i < firstDayOfWeek; i++) {
    days.push({ date: null, day: '', isEmpty: true })
  }

  // 填充当月所有日期
  for (let i = 1; i <= daysInMonth; i++) {
    const date = dayjs(`${year}-${month}-${i}`).format('YYYY-MM-DD')
    const isToday = date === dayjs().format('YYYY-MM-DD')
    const isPast = dayjs(date).isBefore(dayjs(), 'day')

    days.push({
      date: date,
      day: i,
      isToday: isToday,
      isPast: isPast,
      isEmpty: false
    })
  }

  return days
})

// 上一月
const prevMonth = () => {
  const newMonth = dayjs(currentMonth.value).subtract(1, 'month').format('YYYY-MM')
  currentMonth.value = newMonth
}

// 下一月
const nextMonth = () => {
  const newMonth = dayjs(currentMonth.value).add(1, 'month').format('YYYY-MM')
  currentMonth.value = newMonth
}

// 监听月份变化，清空选中的日期
watch(currentMonth, () => {
  // 切换月份时清空选中状态，让用户手动选择
  clickedDate.value = null
})

// 月份变化处理
const onMonthChange = (value) => {
  // 日期选择器已经更新了currentMonth，watch会自动触发
}

// 检查某天是否有排班
const hasSchedule = (day) => {
  return schedules.value.some(s => s.date === day)
}

// 获取某天的所有排班
const getDateSchedules = (day) => {
  return schedules.value.filter(s => s.date === day)
}

// 选中日期的排班
const selectedDateSchedules = computed(() => {
  if (!clickedDate.value) return []
  return schedules.value.filter(s => s.date === clickedDate.value)
})

// 选择日期
const selectDate = (day) => {
  if (!day) return  // 空白格子不处理

  // 直接选中日期（包括过去的日期也可以查看）
  clickedDate.value = day
}

// 判断是否为选中日期
const isSelectedDate = (day) => {
  if (!day || !clickedDate.value) return false
  return clickedDate.value === day
}

// 格式化选中日期
const formatSelectedDate = (date) => {
  if (!date) return ''
  const weekDays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  const dayOfWeek = dayjs(date).day()
  return dayjs(date).format('YYYY年MM月DD日') + ' ' + weekDays[dayOfWeek]
}

// 格式化时段
const formatTimeSlot = (slot) => {
  const slotMap = {
    'MORNING': '上午',
    'AFTERNOON': '下午',
    'EVENING': '晚间'
  }
  return slotMap[slot] || slot
}

// 获取时段标签类型
const getTimeSlotTagType = (slot) => {
  const typeMap = {
    'MORNING': 'success',
    'AFTERNOON': 'warning',
    'EVENING': 'danger'
  }
  return typeMap[slot] || ''
}

// 回到今天
const goToToday = () => {
  const today = dayjs().format('YYYY-MM-DD')
  const todayMonth = dayjs().format('YYYY-MM')

  // 如果当前月份不是今天所在月份，切换到今天所在月份
  if (currentMonth.value !== todayMonth) {
    currentMonth.value = todayMonth
    loadSchedules(todayMonth)
  }

  // 选中今天
  clickedDate.value = today
}

// 获取状态类型
const getStatusType = (status) => {
  return status === '可预约' ? 'success' : 'info'
}

// 获取使用率百分比
const getUsagePercentage = (schedule) => {
  const booked = schedule.bookedQuota || (schedule.totalQuota - schedule.remainingQuota)
  return ((booked / schedule.totalQuota) * 100).toFixed(0) * 1
}

// 获取进度条颜色
const getProgressColor = (schedule) => {
  const percentage = getUsagePercentage(schedule)
  if (percentage < 50) return '#67c23a'
  if (percentage < 80) return '#e6a23c'
  return '#f56c6c'
}

// 禁用过去的日期
const disabledDate = (time) => {
  return time.getTime() < Date.now() - 24 * 60 * 60 * 1000
}

// 显示添加弹窗
const showAddDialog = () => {
  dialogTitle.value = '添加排班'
  Object.assign(form, {
    date: clickedDate.value || '',
    timeSlot: '',
    totalQuota: 10
  })
  dialogVisible.value = true
}

// 快速添加排班（为选中日期）
const quickAddSchedule = () => {
  dialogTitle.value = `添加排班 - ${formatSelectedDate(clickedDate.value)}`
  Object.assign(form, {
    date: clickedDate.value,
    timeSlot: '',
    totalQuota: 10
  })
  dialogVisible.value = true
}

// 编辑排班
const editSchedule = (schedule) => {
  dialogTitle.value = '编辑排班'
  Object.assign(form, {
    id: schedule.id,
    date: schedule.date,
    timeSlot: schedule.timeSlot,
    totalQuota: schedule.totalQuota
  })
  dialogVisible.value = true
}

// 取消排班
const cancelSchedule = (schedule) => {
  ElMessageBox.confirm(
    `确定要取消 ${formatSelectedDate(schedule.date)} ${formatTimeSlot(schedule.timeSlot)} 的排班吗？`,
    '取消排班',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteSchedule(schedule.id)
      message.success('取消排班成功')

      // 重新加载排班
      await loadSchedules(currentMonth.value)
    } catch (error) {

      message.error('取消失败')
    }
  }).catch(() => { })
}

// 保存排班
const saveSchedule = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    saving.value = true

    const doctorId = doctorStore.getDoctorId()
    if (!doctorId) {
      message.error('医生ID未获取到')
      saving.value = false
      return
    }

    try {
      const scheduleData = {
        doctorId: doctorId,
        scheduleDate: dayjs(form.date).format('YYYY-MM-DD'),
        timeSlot: form.timeSlot,
        totalQuota: form.totalQuota,
        remainingQuota: form.totalQuota,
        status: 'AVAILABLE'
      }

      if (form.id) {
        // 更新
        scheduleData.id = form.id
        await updateSchedule(scheduleData)
      } else {
        // 新增
        await createSchedule(scheduleData)
      }

      message.success('排班保存成功')
      dialogVisible.value = false

      // 重新加载当前月份的排班
      await loadSchedules(currentMonth.value)

      // 刷新选中日期的排班
      if (form.date) {
        clickedDate.value = dayjs(form.date).format('YYYY-MM-DD')
      }
    } catch (error) {

      message.error('保存失败')
    } finally {
      saving.value = false
    }
  })
}

// 初始化时加载医生信息和排班
onMounted(async () => {
  await doctorStore.fetchDoctorInfo()
  loadSchedules(currentMonth.value)
})

// 监听月份变化
watch(currentMonth, (newMonth) => {
  loadSchedules(newMonth)
})
</script>

<style scoped lang="scss">
.schedule-container {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;

    h2,
    h3 {
      margin: 0;
      font-size: 20px;
    }

    h3 {
      font-size: 16px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 15px;

      .month-switcher {
        display: flex;
        align-items: center;
      }
    }
  }

  // 自定义日历样式
  .custom-calendar {
    .calendar-header {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      background: linear-gradient(135deg, #67c23a 0%, #409eff 100%);
      color: white;
      border-radius: 8px 8px 0 0;
      overflow: hidden;

      .week-day {
        padding: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 14px;
      }
    }

    .calendar-body {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 1px;
      background: #e0e0e0;
      border: 1px solid #e0e0e0;
      border-radius: 0 0 8px 8px;
      overflow: hidden;

      .calendar-cell {
        background: white;
        min-height: 100px;
        position: relative;
        transition: all 0.2s;

        // 空白格子
        &.is-empty {
          background: #f5f5f5;
          cursor: default;

          &:hover {
            background: #f5f5f5;
            box-shadow: none;
          }
        }

        // 今天
        &.is-today:not(.is-empty) {
          background: #fff7e6;

          .day-number {
            background: linear-gradient(135deg, #e6a23c 0%, #f56c6c 100%);
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
          }
        }

        // 过去的日期（也可以点击查看）
        &.is-past:not(.is-empty) {
          background: #fafafa;

          .calendar-day {
            opacity: 0.7;
          }
        }

        // 所有非空日期都可以点击
        &:not(.is-empty) {
          cursor: pointer;

          &:hover:not(.is-selected) {
            background: #f0f9ff;
            box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
            transform: translateY(-2px);
          }

          &:active {
            transform: scale(0.98);
          }
        }
      }
    }
  }

  .calendar-cell.has-schedule {
    background: #f0f9ff !important;
  }

  .calendar-cell.is-selected {
    background: linear-gradient(135deg, #e6f7ff 0%, #bae7ff 100%) !important;
    border: 3px solid #409eff !important;
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4) !important;
    position: relative;
    z-index: 10;

    &::before {
      content: '✓';
      position: absolute;
      top: 5px;
      right: 5px;
      width: 20px;
      height: 20px;
      background: #409eff;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: bold;
    }
  }

  .calendar-day {
    min-height: 95px;
    padding: 8px;
    transition: all 0.3s;

    .day-number {
      font-size: 16px;
      font-weight: bold;
      margin: 0 0 8px 0;
      color: #333;
      text-align: left;
    }

    .schedule-badges {
      display: flex;
      flex-direction: column;
      gap: 4px;
      align-items: center;

      .schedule-badge {
        margin: 0;
      }
    }
  }

  .detail-card {
    position: sticky;
    top: 20px;
  }

  .no-selected,
  .no-schedule {
    padding: 40px 20px;
    text-align: center;
  }

  .schedule-detail-item {
    padding: 20px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    margin-bottom: 15px;
    transition: all 0.3s;

    &:hover {
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
      border-color: #409eff;
    }

    .schedule-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
    }

    .schedule-info {
      margin-bottom: 15px;

      .info-row {
        display: flex;
        justify-content: space-between;
        margin: 8px 0;
        font-size: 14px;

        .label {
          color: #606266;
        }

        .value {
          font-weight: bold;

          &.booked {
            color: #409eff;
          }

          &.remaining {
            color: #67c23a;
          }
        }
      }
    }

    .schedule-actions {
      display: flex;
      gap: 10px;
      justify-content: flex-end;
    }
  }
}
</style>
