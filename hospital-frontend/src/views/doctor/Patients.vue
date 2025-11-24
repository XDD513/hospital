<template>
  <div class="patients-container">
    <div class="doctor-card">
      <div class="card-header">
        <h3>
          <el-icon>
            <User />
          </el-icon>
          患者管理
        </h3>
      </div>

      <div class="card-body">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="今日患者" name="today">
            <el-table :data="todayPageData" v-loading="loading">
              <el-table-column prop="queueNumber" label="序号" width="80" />
              <el-table-column prop="patientName" label="患者姓名" width="120" />
              <el-table-column prop="gender" label="性别" width="70" />
              <el-table-column prop="age" label="年龄" width="70" />
              <el-table-column prop="phone" label="联系电话" width="130" />
              <el-table-column prop="appointmentTime" label="预约时间" width="120" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" fixed="right" width="250">
                <template #default="{ row }">
                  <el-button v-if="['PENDING', 'CONFIRMED'].includes(row.status)" type="primary" size="small"
                    @click="startConsultation(row)">
                    <el-icon>
                      <Checked />
                    </el-icon>
                    开始接诊
                  </el-button>
                  <el-button v-if="row.status === 'IN_PROGRESS'" type="success" size="small"
                    @click="completeConsultation(row)">
                    <el-icon>
                      <CircleCheckFilled />
                    </el-icon>
                    完成接诊
                  </el-button>
                  <el-button size="small" type="info" @click="viewPatientDetail(row)">
                    <el-icon>
                      <View />
                    </el-icon>
                    详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination" v-if="todayTotal > 0">
              <el-pagination v-model:current-page="todayQuery.page" v-model:page-size="todayQuery.pageSize"
                :total="todayTotal" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" />
            </div>
          </el-tab-pane>

          <el-tab-pane label="历史患者" name="history">
            <el-input v-model="searchText" placeholder="搜索患者姓名或电话" style="width: 300px; margin-bottom: 20px"
              clearable />
            <el-table :data="historyPageData">
              <el-table-column prop="patientName" label="患者姓名" />
              <el-table-column prop="lastVisitDate" label="最近就诊" width="150" />
              <el-table-column prop="visitCount" label="就诊次数" width="100" />
              <el-table-column label="操作" width="120">
                <template #default="{ row }">
                  <el-button size="small" type="info" @click="viewPatientDetail(row)">
                    <el-icon>
                      <View />
                    </el-icon>
                    详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination" v-if="historyTotal > 0">
              <el-pagination v-model:current-page="historyQuery.page" v-model:page-size="historyQuery.pageSize"
                :total="historyTotal" :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper" />
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>

    <!-- 接诊弹窗 -->
    <ConsultationDialog v-model="consultationDialogVisible" :patient-info="selectedPatient"
      :doctor-id="doctorStore.getDoctorId()" @success="handleConsultationSuccess" />

    <!-- 患者详情弹窗 -->
    <PatientDetailDialog v-model="patientDetailVisible" :patient-id="selectedPatientId"
      :appointment-id="selectedAppointmentId" :doctor-id="doctorStore.getDoctorId()" />
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, watch, onMounted, reactive, computed, nextTick } from 'vue'

import { User, Checked, View, CircleCheckFilled } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useDoctorStore } from '@/stores/doctor'
import { getTodayPatients, getHistoryPatients } from '@/api/patient'
import { startConsultation as startConsultationApi } from '@/api/consultation'
import ConsultationDialog from '@/components/doctor/ConsultationDialog.vue'
import PatientDetailDialog from '@/components/doctor/PatientDetailDialog.vue'

const userStore = useUserStore()
const doctorStore = useDoctorStore()

const activeTab = ref('today')
const loading = ref(false)
const searchText = ref('')

// 弹窗状态
const consultationDialogVisible = ref(false)
const patientDetailVisible = ref(false)
const selectedPatient = ref({})
const selectedPatientId = ref(null)
const selectedAppointmentId = ref(null)

// 今日患者
const todayPatients = ref([])
// 历史患者
const historyPatients = ref([])

// 分页参数与总数
const todayQuery = reactive({ page: 1, pageSize: 10 })
const historyQuery = reactive({ page: 1, pageSize: 10 })
const todayTotal = ref(0)
const historyTotal = ref(0)

// 前端分页数据切片
const todayPageData = computed(() => {
  const start = (todayQuery.page - 1) * todayQuery.pageSize
  return todayPatients.value.slice(start, start + todayQuery.pageSize)
})
const historyPageData = computed(() => {
  const start = (historyQuery.page - 1) * historyQuery.pageSize
  return historyPatients.value.slice(start, start + historyQuery.pageSize)
})

// 加载今日患者
const loadTodayPatients = async () => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) return

  loading.value = true
  try {
    const res = await getTodayPatients(doctorId)
    if (res.code === 200) {
      todayPatients.value = res.data || []
      todayTotal.value = todayPatients.value.length
      todayQuery.page = 1
    }
  } catch (error) {

  } finally {
    loading.value = false
  }
}

// 加载历史患者
const loadHistoryPatients = async () => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) return

  loading.value = true
  try {
    const res = await getHistoryPatients(doctorId, { searchText: searchText.value })
    if (res.code === 200) {
      const list = res.data?.records || res.data || []
      // 前端搜索过滤（若后端未分页返回）
      const keyword = String(searchText.value || '').trim()
      historyPatients.value = keyword
        ? list.filter(item =>
          item.patientName?.includes(keyword) ||
          item.phone?.includes(keyword)
        )
        : list
      historyTotal.value = historyPatients.value.length
      historyQuery.page = 1
    }
  } catch (error) {

  } finally {
    loading.value = false
  }
}

// 监听Tab切换
watch(activeTab, (newTab) => {
  if (newTab === 'today') {
    loadTodayPatients()
  } else if (newTab === 'history') {
    loadHistoryPatients()
  }
})

// 监听搜索文本变化，重载历史数据并重置页码
watch(searchText, () => {
  historyQuery.page = 1
  if (activeTab.value === 'history') {
    loadHistoryPatients()
  }
})

// 获取状态类型
const getStatusType = (status) => {
  const map = {
    PENDING: 'warning',
    CONFIRMED: 'warning',
    IN_PROGRESS: 'success',
    COMPLETED: 'success'
  }
  return map[status] || 'info'
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

// 完成接诊
const completeConsultation = (patient) => {
  selectedPatient.value = {
    ...patient,
    appointmentId: patient.appointmentId,
    patientId: patient.patientId,
    patientName: patient.patientName,
    gender: patient.gender,
    age: patient.age,
    phone: patient.phone,
    timeSlot: patient.timeSlot,
    queueNumber: patient.queueNumber,
    categoryId: patient.categoryId || patient.deptId,
    consultationFee: patient.consultationFee || doctorStore.doctorInfo?.consultationFee || 0
  }
  consultationDialogVisible.value = true
}

// 接诊成功回调
const handleConsultationSuccess = () => {
  // 刷新数据
  doctorStore.fetchTodayStats()
  loadTodayPatients()
}

// 查看患者详情
const viewPatientDetail = (patient) => {

  // 先设置patientId，确保在弹窗打开前已设置
  const patientId = patient.patientId || patient.id || null
  const appointmentId = patient.appointmentId || null

  if (!patientId) {

    message.warning('无法获取患者ID，请重试')
    return
  }
  
  // 先设置ID，再打开弹窗，确保watch能获取到正确的patientId
  selectedPatientId.value = patientId
  selectedAppointmentId.value = appointmentId

  // 使用nextTick确保patientId已更新后再打开弹窗
  nextTick(() => {
    patientDetailVisible.value = true

  })
}

// 初始化
onMounted(async () => {
  await doctorStore.fetchDoctorInfo()
  loadTodayPatients()
})
</script>

<style scoped lang="scss">
.patients-container {
  max-width: 1400px;
  margin: 0 auto;

  h2 {
    margin: 0;
    font-size: 20px;
  }

  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 16px;
  }
}
</style>
