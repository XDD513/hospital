<template>
  <div class="my-appointments-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <h2>我的预约</h2>
          <div class="header-actions">
            <el-button type="success" plain :loading="exportLoading" @click="handleExportAppointments">
              <el-icon>
                <Download />
              </el-icon>
              导出预约
            </el-button>
            <el-button type="primary" @click="router.push('/patient/appointment')">
              <el-icon>
                <Plus />
              </el-icon>
              新建预约
            </el-button>
          </div>
        </div>
      </template>

      <!-- 状态筛选 -->
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="全部" name="all" />
        <el-tab-pane label="待就诊" name="CONFIRMED" />
        <el-tab-pane label="就诊中" name="IN_PROGRESS" />
        <el-tab-pane label="已完成" name="COMPLETED" />
        <el-tab-pane label="已取消" name="CANCELLED" />
      </el-tabs>

      <!-- 预约列表 -->
      <div v-loading="loading">
        <el-timeline v-if="appointments.length > 0">
          <el-timeline-item v-for="item in appointments" :key="item.id" :timestamp="item.appointmentDate"
            placement="top">
            <el-card class="appointment-card">
              <div class="appointment-content">
                <div class="appointment-info">
                  <div class="info-row">
                    <h3>{{ item.deptName }} - {{ item.doctorName }}</h3>
                    <el-tag :type="getStatusType(item.status)">
                      {{ getStatusText(item.status) }}
                    </el-tag>
                  </div>

                  <div class="info-details">
                    <div class="detail-item">
                      <el-icon>
                        <Calendar />
                      </el-icon>
                      <span>{{ formatDate(item.appointmentDate) }}</span>
                    </div>
                    <div class="detail-item">
                      <el-icon>
                        <Clock />
                      </el-icon>
                      <span>{{ formatTimeSlot(item.timeSlot) }}</span>
                    </div>
                    <div class="detail-item">
                      <el-icon>
                        <Location />
                      </el-icon>
                      <span>门诊{{ item.queueNumber }}号</span>
                    </div>
                    <div class="detail-item">
                      <el-icon>
                        <Money />
                      </el-icon>
                      <span>挂号费：¥{{ item.consultationFee }}</span>
                    </div>
                  </div>

                  <div v-if="item.doctorTitle" class="doctor-info">
                    <strong>医生职称：</strong>{{ item.doctorTitle }}
                  </div>
                </div>

                <div class="appointment-actions">
                  <!-- 取消预约按钮：在CONFIRMED和IN_PROGRESS状态显示 -->
                  <el-button 
                    v-if="item.status === 'CONFIRMED' || item.status === 'IN_PROGRESS'" 
                    type="danger" 
                    size="small" 
                    plain
                    @click="cancelAppointmentHandler(item)">
                    <el-icon>
                      <Close />
                    </el-icon>
                    取消预约
                  </el-button>
                  <!-- 就诊中状态：根据是否已有测试记录显示不同按钮 -->
                  <el-button v-if="item.status === 'IN_PROGRESS' && !item.hasTest" type="success" size="small"
                    @click="goToConstitutionTest(item)">
                    <el-icon>
                      <Document />
                    </el-icon>
                    进行体质测试
                  </el-button>
                  <el-button v-if="item.status === 'IN_PROGRESS' && item.hasTest" type="info" size="small" plain
                    @click="viewTestResult(item)">
                    <el-icon>
                      <Document />
                    </el-icon>
                    查看测试结果
                  </el-button>
                  <el-button v-if="item.status === 'COMPLETED' && !item.hasReview" type="primary" size="small" plain
                    @click="reviewDoctor(item)">
                    评价医生
                  </el-button>
                  <template v-if="item.status === 'COMPLETED' && item.hasReview">
                    <el-tag type="primary" size="small" style="margin-right: 8px;">
                      已评价
                    </el-tag>
                    <el-button type="info" size="small" plain
                      @click="viewReview(item)">
                      <el-icon>
                        <Document />
                      </el-icon>
                      查看评价
                    </el-button>
                  </template>
                  <el-button size="small" @click="viewDetail(item)">
                    查看详情
                  </el-button>
                </div>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>

        <el-empty v-else description="暂无预约记录" />
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination v-model:current-page="queryParams.page" v-model:page-size="queryParams.pageSize" :total="total"
          layout="total, prev, pager, next" @current-change="loadAppointments" />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailVisible" title="预约详情" width="600px">
      <el-descriptions :column="1" border v-if="selectedAppointment">
        <el-descriptions-item label="预约ID">
          {{ selectedAppointment.id }}
        </el-descriptions-item>
        <el-descriptions-item label="科室">
          {{ selectedAppointment.deptName }}
        </el-descriptions-item>
        <el-descriptions-item label="医生">
          {{ selectedAppointment.doctorName }}<span v-if="selectedAppointment.doctorTitle"> ({{
            selectedAppointment.doctorTitle }})</span>
        </el-descriptions-item>
        <el-descriptions-item label="就诊日期">
          {{ formatDate(selectedAppointment.appointmentDate) }}
        </el-descriptions-item>
        <el-descriptions-item label="就诊时段">
          {{ formatTimeSlot(selectedAppointment.timeSlot) }}
        </el-descriptions-item>
        <el-descriptions-item label="排队号">
          {{ selectedAppointment.queueNumber }}号
        </el-descriptions-item>
        <el-descriptions-item label="挂号费">
          ¥{{ selectedAppointment.consultationFee }}
        </el-descriptions-item>
        <el-descriptions-item label="预约状态">
          <el-tag :type="getStatusType(selectedAppointment.status)">
            {{ getStatusText(selectedAppointment.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="患者姓名">
          {{ selectedAppointment.patientName }}
        </el-descriptions-item>
        <el-descriptions-item label="患者手机">
          {{ selectedAppointment.patientPhone }}
        </el-descriptions-item>
        <el-descriptions-item label="完成时间">
          {{ formatDateTime(selectedAppointment.updateTime) }}
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 评价弹窗 -->
    <ReviewDialog
      v-model="reviewDialogVisible"
      :appointment="selectedAppointmentForReview"
      @success="handleReviewSuccess"
    />

    <!-- 查看评价弹窗 -->
    <ReviewViewDialog
      v-model="reviewViewDialogVisible"
      :appointment-id="selectedAppointmentForViewReview?.id"
    />
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { Close, Document, Calendar, Clock, Location, Money, Plus, Download } from '@element-plus/icons-vue'
import { getPatientAppointments, cancelAppointment, exportPatientAppointments } from '@/api/appointment'
import { checkTestByAppointment } from '@/api/constitution'
import { getReviewByAppointmentId } from '@/api/review'
import ReviewDialog from '@/components/patient/ReviewDialog.vue'
import ReviewViewDialog from '@/components/patient/ReviewViewDialog.vue'
import dayjs from 'dayjs'

const router = useRouter()

// 状态
const activeTab = ref('all')
const loading = ref(false)
const detailVisible = ref(false)
const reviewDialogVisible = ref(false)
const reviewViewDialogVisible = ref(false)
const exportLoading = ref(false)

// 数据
const appointments = ref([])
const selectedAppointment = ref(null)
const selectedAppointmentForReview = ref(null)
const selectedAppointmentForViewReview = ref(null)
const total = ref(0)

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10,
  status: ''
})

// 加载预约列表
const loadAppointments = async () => {
  loading.value = true
  try {
    const res = await getPatientAppointments()

    let filteredData = res.data || []

    // 按状态筛选
    if (queryParams.status) {
      filteredData = filteredData.filter(a => a.status === queryParams.status)
    }

    // 检查"就诊中"状态的预约是否已有测试记录
    // 检查"已完成"状态的预约是否已有评价
    for (const appointment of filteredData) {
      if (appointment.status === 'IN_PROGRESS') {
        try {
          const testRes = await checkTestByAppointment(appointment.id)
          appointment.hasTest = testRes.code === 200 && testRes.data === true
        } catch (error) {
          appointment.hasTest = false
        }
      } else {
        appointment.hasTest = false
      }
      
      // 检查是否已有评价
      if (appointment.status === 'COMPLETED') {
        try {
          const reviewRes = await getReviewByAppointmentId(appointment.id)
          // 判断是否有评价：code为200且data存在且有id字段
          if (reviewRes && reviewRes.code === 200 && reviewRes.data) {
            // 检查data是否有id字段（有id说明是有效的评价对象）
            appointment.hasReview = reviewRes.data.id !== null && reviewRes.data.id !== undefined
          } else {
            appointment.hasReview = false
          }
        } catch (error) {
          console.error('检查评价失败:', error)
          appointment.hasReview = false
        }
      } else {
        appointment.hasReview = false
      }
    }

    appointments.value = filteredData
    total.value = filteredData.length

  } catch (error) {

    message.error('加载预约列表失败')
  } finally {
    loading.value = false
  }
}

// Tab切换
const handleTabChange = (tabName) => {
  queryParams.status = tabName === 'all' ? '' : tabName
  queryParams.page = 1
  loadAppointments()
}

// 查看详情
const viewDetail = (appointment) => {
  selectedAppointment.value = appointment
  detailVisible.value = true
}

// 导出预约记录
const handleExportAppointments = async () => {
  if (!appointments.value || appointments.value.length === 0) {
    message.warning('暂无可导出的预约记录')
    return
  }

  try {
    exportLoading.value = true
    const params = {}
    if (queryParams.status) {
      params.status = queryParams.status
    }

    const res = await exportPatientAppointments(params)
    if (!(res instanceof Blob) || res.size === 0) {
      message.error('导出失败，文件为空')
      return
    }

    const blob = new Blob([res], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `预约记录_${dayjs().format('YYYYMMDD_HHmm')}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    message.success('导出成功')
  } catch (error) {
    console.error('导出预约记录失败', error)
    message.error(error?.message || '导出失败，请稍后重试')
  } finally {
    exportLoading.value = false
  }
}

// 取消预约
const cancelAppointmentHandler = (appointment) => {
  ElMessageBox.confirm(
    '确定要取消这个预约吗？取消后将无法恢复。',
    '取消预约',
    {
      confirmButtonText: '确定取消',
      cancelButtonText: '我再想想',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    }
  ).then(async () => {
    try {
      loading.value = true
      const res = await cancelAppointment(appointment.id)
      
      if (res.code === 200) {
        message.success('预约已取消')
        // 重新加载预约列表
        await loadAppointments()
      } else {
        message.error(res.message || '取消失败')
      }
    } catch (error) {

      message.error(error.response?.data?.message || '取消失败，请稍后重试')
    } finally {
      loading.value = false
    }
  }).catch(() => {
    // 用户取消操作，不做任何处理
  })
}

// 评价医生
const reviewDoctor = (appointment) => {
  selectedAppointmentForReview.value = appointment
  reviewDialogVisible.value = true
}

// 查看评价
const viewReview = (appointment) => {
  selectedAppointmentForViewReview.value = appointment
  reviewViewDialogVisible.value = true
}

// 评价成功回调
const handleReviewSuccess = () => {
  // 重新加载预约列表
  loadAppointments()
}

// 进行体质测试
const goToConstitutionTest = (appointment) => {
  // 跳转到体质测试页面，并传递预约ID
  router.push({
    path: '/patient/constitution/test',
    query: { appointmentId: appointment.id }
  })
}

// 查看测试结果
const viewTestResult = (appointment) => {
  // 跳转到测试历史页面
  router.push({
    path: '/patient/constitution/history'
  })
}

// 格式化日期
const formatDate = (dateStr) => {
  return dayjs(dateStr).format('YYYY年MM月DD日')
}

// 格式化时段
const formatTimeSlot = (slot) => {
  const slotMap = {
    'MORNING': '上午 08:00-12:00',
    'AFTERNOON': '下午 14:00-17:00',
    'EVENING': '晚间 18:00-21:00'
  }
  return slotMap[slot] || ''
}

// 获取状态类型
const getStatusType = (status) => {
  const typeMap = {
    'CONFIRMED': 'warning',
    'IN_PROGRESS': 'primary',
    'COMPLETED': 'success',
    'CANCELLED': 'info',
    'NO_SHOW': 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = {
    'CONFIRMED': '待就诊',
    'IN_PROGRESS': '就诊中',
    'COMPLETED': '已完成',
    'CANCELLED': '已取消',
    'NO_SHOW': '爽约'
  }
  return textMap[status] || '未知'
}

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '-'
  return dayjs(dateTimeStr).format('YYYY年MM月DD日 HH:mm:ss')
}

onMounted(() => {
  loadAppointments()
})
</script>

<style scoped lang="scss">
.my-appointments-container {
  max-width: 1200px;
  margin: 0 auto;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
      font-size: 20px;
    }

    .header-actions {
      display: flex;
      gap: 10px;
    }
  }

  .appointment-card {
    .appointment-content {
      .appointment-info {
        .info-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 15px;

          h3 {
            margin: 0;
            font-size: 18px;
            color: #333;
          }
        }

        .info-details {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 12px;
          margin-bottom: 15px;

          .detail-item {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #666;
            font-size: 14px;

            .el-icon {
              color: #909399;
            }
          }
        }

        .doctor-info {
          margin-top: 10px;
          padding-top: 10px;
          border-top: 1px dashed #e0e0e0;
          color: #666;
          font-size: 14px;

          strong {
            color: #333;
          }
        }
      }

      .appointment-actions {
        display: flex;
        gap: 10px;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid #f0f0f0;
      }
    }
  }

  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
}
</style>
