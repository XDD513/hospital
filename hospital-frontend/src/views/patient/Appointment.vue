<template>
  <div class="appointment-container">
    <el-card shadow="never">
      <template #header>
        <h2>预约挂号</h2>
      </template>

      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step title="选择分类" />
        <el-step title="选择科室" />
        <el-step title="选择医生" />
        <el-step title="选择时间" />
        <el-step title="确认预约" />
      </el-steps>

      <div class="step-content">
        <!-- 步骤1: 选择分类 -->
        <div v-show="currentStep === 0" class="step-panel">
          <h3>请选择科室分类</h3>
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="cat in categories" :key="cat.id">
              <div class="select-card" :class="{ active: selectedCategory?.id === cat.id }"
                @click="selectCategory(cat)">
                <el-icon :size="40">
                  <Folder />
                </el-icon>
                <h4>{{ cat.categoryName }}</h4>
                <p>{{ cat.description }}</p>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 步骤2: 选择科室 -->
        <div v-show="currentStep === 1" class="step-panel">
          <h3>请选择科室</h3>
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="dept in departments" :key="dept.id">
              <div class="select-card" :class="{ active: selectedDept?.id === dept.id }"
                @click="selectDepartment(dept)">
                <el-icon :size="40" :color="dept.color">
                  <OfficeBuilding />
                </el-icon>
                <h4>{{ dept.deptName }}</h4>
                <p>{{ dept.description }}</p>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 步骤3: 选择医生 -->
        <div v-show="currentStep === 2" class="step-panel">
          <h3>请选择医生</h3>
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" v-for="doctor in doctors" :key="doctor.id">
              <div class="doctor-select-card" :class="{ active: selectedDoctor?.id === doctor.id }"
                @click="selectDoctor(doctor)">
                <div class="doctor-header">
                  <el-avatar :size="60">
                    <el-icon>
                      <User />
                    </el-icon>
                  </el-avatar>
                  <div class="doctor-basic">
                    <h4>{{ doctor.doctorName }}</h4>
                    <el-tag type="warning" size="small">{{ doctor.title }}</el-tag>
                  </div>
                </div>
                <div class="doctor-info">
                  <p><strong>擅长：</strong>{{ doctor.specialty }}</p>
                  <p class="fee">挂号费：¥{{ doctor.consultationFee }}</p>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 步骤4: 选择时间 -->
        <div v-show="currentStep === 3" class="step-panel">
          <h3>请选择就诊时间</h3>

          <div class="date-selector">
            <h4>选择日期</h4>
            <el-radio-group v-model="selectedDate" class="date-group" @change="onDateChange">
              <el-radio-button v-for="date in availableDates" :key="date.value" :label="date.value">
                <div class="date-item">
                  <div class="date-day">{{ date.day }}</div>
                  <div class="date-label">{{ date.label }}</div>
                </div>
              </el-radio-button>
            </el-radio-group>
          </div>

          <div class="time-selector" v-if="selectedDate">
            <h4>选择时段</h4>
            <div v-loading="loadingSchedules">
              <el-radio-group v-model="selectedScheduleId" class="time-group">
                <el-radio-button v-for="schedule in availableSchedules" :key="schedule.id" :label="schedule.id"
                  :disabled="schedule.remainingQuota === 0">
                  <div class="time-item">
                    <el-icon v-if="schedule.timeSlot === 'MORNING'">
                      <Sunrise />
                    </el-icon>
                    <el-icon v-else-if="schedule.timeSlot === 'AFTERNOON'">
                      <Sunny />
                    </el-icon>
                    <el-icon v-else>
                      <Moon />
                    </el-icon>
                    <span>{{ formatTimeSlotName(schedule.timeSlot) }}</span>
                    <small>{{ formatTimeSlotTime(schedule.timeSlot) }}</small>
                    <el-tag :type="schedule.remainingQuota > 0 ? 'success' : 'danger'" size="small"
                      style="margin-left: 10px">
                      {{ schedule.remainingQuota > 0 ? `剩余${schedule.remainingQuota}号` : '已满' }}
                    </el-tag>
                  </div>
                </el-radio-button>
              </el-radio-group>

              <el-empty v-if="!loadingSchedules && availableSchedules.length === 0" description="该日期暂无排班"
                :image-size="100" />
            </div>
          </div>
        </div>

        <!-- 步骤5: 确认预约 -->
        <div v-show="currentStep === 4" class="step-panel">
          <h3>确认预约信息</h3>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="分类">
              {{ selectedCategory?.categoryName }}
            </el-descriptions-item>
            <el-descriptions-item label="科室">
              {{ selectedDept?.deptName }}
            </el-descriptions-item>
            <el-descriptions-item label="医生">
              {{ selectedDoctor?.doctorName }} ({{ selectedDoctor?.title }})
            </el-descriptions-item>
            <el-descriptions-item label="就诊日期">
              {{ formatDate(selectedDate) }}
            </el-descriptions-item>
            <el-descriptions-item label="就诊时段">
              {{ selectedSchedule ? formatTimeSlotName(selectedSchedule.timeSlot) + ' ' +
                formatTimeSlotTime(selectedSchedule.timeSlot) : '' }}
            </el-descriptions-item>
            <el-descriptions-item label="剩余号源">
              <el-tag type="success">{{ selectedSchedule?.remainingQuota }}号</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="挂号费">
              <span class="fee-text">¥{{ selectedDoctor?.consultationFee }}</span>
            </el-descriptions-item>
          </el-descriptions>

          <el-alert title="温馨提示" type="info" :closable="false" style="margin-top: 20px">
            <p>1. 请在就诊日期前一天取消预约，否则将收取挂号费</p>
            <p>2. 请提前30分钟到达医院取号</p>
            <p>3. 请携带身份证和就诊卡</p>
          </el-alert>
        </div>
      </div>

      <div class="step-actions">
        <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
        <el-button v-if="currentStep < 4" type="primary" @click="nextStep" :disabled="!canNext">
          下一步
        </el-button>
        <el-button v-if="currentStep === 4" type="success" @click="confirmAppointment" :loading="submitting">
          确认预约并支付
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { getEnabledDepartmentListByCategory, getEnabledDepartmentCategoryList } from '@/api/department'
import { getDoctorListByDept } from '@/api/doctor'
import { getDoctorScheduleByDate } from '@/api/schedule'
import { createAppointment } from '@/api/appointment'
import dayjs from 'dayjs'

const router = useRouter()

// 当前步骤
const currentStep = ref(0)
const submitting = ref(false)
const loadingSchedules = ref(false)

// 选中的数据
const selectedCategory = ref(null)
const selectedDept = ref(null)
const selectedDoctor = ref(null)
const selectedDate = ref('')
const selectedScheduleId = ref(null)

// 数据列表
const categories = ref([])
const departments = ref([])
const doctors = ref([])
const availableSchedules = ref([])

// 可选日期（未来7天）
const availableDates = computed(() => {
  const dates = []
  const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  for (let i = 0; i < 7; i++) {
    const date = dayjs().add(i, 'day')
    const dayOfWeek = date.day()
    dates.push({
      value: date.format('YYYY-MM-DD'),
      day: date.format('MM-DD'),
      label: i === 0 ? '今天' : i === 1 ? '明天' : weekDays[dayOfWeek]
    })
  }
  return dates
})

// 选中的排班
const selectedSchedule = computed(() => {
  return availableSchedules.value.find(s => s.id === selectedScheduleId.value)
})

// 是否可以进入下一步
const canNext = computed(() => {
  if (currentStep.value === 0) return selectedCategory.value !== null
  if (currentStep.value === 1) return selectedDept.value !== null
  if (currentStep.value === 2) return selectedDoctor.value !== null
  if (currentStep.value === 3) return selectedDate.value && selectedScheduleId.value
  return false
})

// 颜色列表
const colors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c']

// 选择分类
const selectCategory = async (cat) => {
  selectedCategory.value = cat
  selectedDept.value = null
  selectedDoctor.value = null

  await loadDepartmentsByCategory(cat.id)
}

// 选择科室
const selectDepartment = (dept) => {
  selectedDept.value = dept
  selectedDoctor.value = null

  // 加载该科室的医生
  loadDoctors(dept.id)
}

// 选择医生
const selectDoctor = (doctor) => {
  selectedDoctor.value = doctor
}

// 日期变化
const onDateChange = async (date) => {
  selectedScheduleId.value = null
  availableSchedules.value = []

  if (date && selectedDoctor.value) {
    await loadSchedules(selectedDoctor.value.id, date)
  }
}

// 加载排班信息
const loadSchedules = async (doctorId, date) => {
  loadingSchedules.value = true
  try {
    const res = await getDoctorScheduleByDate(doctorId, date)
    if (res.code === 200) {
      // 只显示有剩余号源的排班
      availableSchedules.value = (res.data || []).filter(s => s.status === 'AVAILABLE')
    }
  } catch (error) {

    message.error('加载排班信息失败')
  } finally {
    loadingSchedules.value = false
  }
}

// 上一步
const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 下一步
const nextStep = () => {
  if (canNext.value && currentStep.value < 4) {
    currentStep.value++

    // 进入步骤4时，如果已选择日期，加载排班
    if (currentStep.value === 3 && selectedDate.value && selectedDoctor.value) {
      loadSchedules(selectedDoctor.value.id, selectedDate.value)
    }
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  return dayjs(dateStr).format('YYYY年MM月DD日')
}

// 格式化时段名称
const formatTimeSlotName = (slot) => {
  const slotMap = {
    'MORNING': '上午',
    'AFTERNOON': '下午',
    'EVENING': '晚间'
  }
  return slotMap[slot] || ''
}

// 格式化时段时间
const formatTimeSlotTime = (slot) => {
  const slotMap = {
    'MORNING': '(08:00-12:00)',
    'AFTERNOON': '(14:00-17:00)',
    'EVENING': '(18:00-21:00)'
  }
  return slotMap[slot] || ''
}

// 确认预约
const confirmAppointment = async () => {
  if (!selectedSchedule.value) {
    message.warning('请选择就诊时段')
    return
  }

  ElMessageBox.confirm(
    `确认预约${selectedDoctor.value.doctorName}医生？需支付挂号费¥${selectedDoctor.value.consultationFee}`,
    '确认预约',
    {
      confirmButtonText: '确认并支付',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    submitting.value = true

    try {
      const appointmentData = {
        doctorId: selectedDoctor.value.id,
        deptId: selectedDept.value.id,
        scheduleId: selectedScheduleId.value,
        appointmentDate: selectedDate.value,
        timeSlot: selectedSchedule.value.timeSlot,
        consultationFee: selectedDoctor.value.consultationFee
      }

      const res = await createAppointment(appointmentData)

      if (res.code === 200) {
        message.success('预约成功！')

        // 跳转到我的预约页面
        setTimeout(() => {
          router.push('/patient/my-appointments')
        }, 1500)
      } else {
        message.error(res.message || '预约失败')
      }

    } catch (error) {

      message.error(error.response?.data?.message || '预约失败，请重试')
    } finally {
      submitting.value = false
    }
  }).catch(() => { })
}

// 加载分类列表
const loadCategories = async () => {
  try {
    const res = await getEnabledDepartmentCategoryList()
    categories.value = res.data || []
  } catch (error) {

  }
}

// 按分类加载科室列表
const loadDepartmentsByCategory = async (categoryId) => {
  try {
    const res = await getEnabledDepartmentListByCategory(categoryId)
    departments.value = (res.data || []).map((dept, index) => ({
      ...dept,
      color: colors[index % colors.length]
    }))
  } catch (error) {

  }
}

// 加载医生列表
const loadDoctors = async (deptId) => {
  try {
    const res = await getDoctorListByDept(deptId)
    doctors.value = res.data || []
  } catch (error) {

  }
}

// 初始化
onMounted(() => {
  loadCategories()
})
</script>

<style scoped lang="scss">
.appointment-container {
  max-width: 1200px;
  margin: 0 auto;

  h2 {
    margin: 0;
    font-size: 20px;
  }

  h3 {
    margin: 0 0 20px 0;
    font-size: 18px;
    color: #333;
  }

  h4 {
    margin: 10px 0;
    font-size: 16px;
    color: #333;
  }

  .step-content {
    margin: 40px 0;
    min-height: 400px;
  }

  .step-panel {
    animation: fadeIn 0.3s;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .select-card {
    padding: 30px 20px;
    text-align: center;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
    margin-bottom: 20px;

    &:hover {
      border-color: #409eff;
      box-shadow: 0 2px 12px rgba(64, 158, 255, 0.2);
    }

    &.active {
      border-color: #409eff;
      background: #ecf5ff;
    }

    h4 {
      margin: 15px 0 10px;
    }

    p {
      margin: 0;
      color: #666;
      font-size: 13px;
    }
  }

  .doctor-select-card {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s;
    margin-bottom: 20px;

    &:hover {
      border-color: #67c23a;
      box-shadow: 0 2px 12px rgba(103, 194, 58, 0.2);
    }

    &.active {
      border-color: #67c23a;
      background: #f0f9ff;
    }

    .doctor-header {
      display: flex;
      gap: 15px;
      align-items: center;
      margin-bottom: 15px;

      .doctor-basic {
        flex: 1;

        h4 {
          margin: 0 0 8px 0;
        }
      }
    }

    .doctor-info {
      p {
        margin: 8px 0;
        font-size: 13px;
        color: #666;
      }

      .fee {
        color: #f56c6c;
        font-weight: bold;
        font-size: 16px;
      }
    }
  }

  .date-selector,
  .time-selector {
    margin-bottom: 30px;
  }

  .date-group,
  .time-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .date-item {
    text-align: center;
    padding: 5px;

    .date-day {
      font-size: 16px;
      font-weight: bold;
      color: #333;
    }

    .date-label {
      font-size: 12px;
      color: #666;
      margin-top: 4px;
    }
  }

  // 选中日期按钮的样式优化
  :deep(.el-radio-button__inner) {
    padding: 12px 20px;
    border-color: #dcdfe6;
  }

  :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
    background-color: #409eff;
    border-color: #409eff;
    box-shadow: -1px 0 0 0 #409eff;

    .date-item {
      .date-day {
        color: #fff !important;
      }

      .date-label {
        color: rgba(255, 255, 255, 0.85) !important;
      }
    }
  }

  :deep(.el-radio-button:first-child .el-radio-button__inner) {
    border-left: 1px solid #dcdfe6;
  }

  .time-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    padding: 10px;

    .el-icon {
      font-size: 24px;
      color: #666;
    }

    span {
      font-size: 14px;
      font-weight: bold;
      color: #333;
    }

    small {
      font-size: 12px;
      color: #999;
    }
  }

  // 选中时段按钮的样式优化
  :deep(.time-group .el-radio-button__original-radio:checked + .el-radio-button__inner) {
    .time-item {
      .el-icon {
        color: #fff !important;
      }

      span {
        color: #fff !important;
      }

      small {
        color: rgba(255, 255, 255, 0.85) !important;
      }
    }
  }

  .fee-text {
    font-size: 20px;
    color: #f56c6c;
    font-weight: bold;
  }

  .step-actions {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #e0e0e0;
  }
}

:deep(.el-alert p) {
  margin: 5px 0;
  font-size: 13px;
}
</style>
