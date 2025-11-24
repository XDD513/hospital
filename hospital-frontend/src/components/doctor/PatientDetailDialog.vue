<template>
  <el-dialog v-model="visible" title="患者详情" width="1200px" :close-on-click-modal="false">
    <div v-loading="loading" class="patient-detail">
      <!-- 患者基本信息（简化显示） -->
      <el-card class="info-card summary-card" shadow="never">
        <el-row :gutter="20">
          <el-col :span="4">
            <div class="info-item">
              <span class="label">姓名：</span>
              <span class="value">{{ patientInfo.realName || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="info-item">
              <span class="label">性别：</span>
              <span class="value">{{ patientInfo.gender === 1 ? '男' : patientInfo.gender === 2 ? '女' : '-' }}</span>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="info-item">
              <span class="label">年龄：</span>
              <span class="value">{{ calculateAge(patientInfo.birthDate) }}岁</span>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="info-item">
              <span class="label">手机号：</span>
              <span class="value">{{ patientInfo.phone || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="info-item">
              <span class="label">就诊次数：</span>
              <span class="value highlight">{{ consultationHistory.length }} 次</span>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="info-item">
              <span class="label">最近就诊：</span>
              <span class="value">{{ getLastVisitDate() }}</span>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 就诊记录列表（主要内容） -->
      <el-card class="info-card records-card" shadow="never">
        <template #header>
          <div class="card-header-content">
            <span>
              <el-icon><Document /></el-icon>
              就诊记录
            </span>
            <el-tag type="primary">共 {{ consultationHistory.length }} 条</el-tag>
          </div>
        </template>
        <div v-if="consultationHistory.length > 0">
          <el-table :data="consultationHistory" stripe style="width: 100%">
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="consultationDate" label="就诊日期" width="120" align="center">
              <template #default="{ row }">
                {{ row.consultationDate }}
              </template>
            </el-table-column>
            <el-table-column prop="consultationTime" label="就诊时间" width="100" align="center">
              <template #default="{ row }">
                {{ formatConsultationTime(row) }}
              </template>
            </el-table-column>
            <el-table-column prop="diagnosis" label="诊断" min-width="150" show-overflow-tooltip>
              <template #default="{ row }">
                <span class="diagnosis-text">{{ row.diagnosis || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="chiefComplaint" label="主诉" min-width="200" show-overflow-tooltip>
              <template #default="{ row }">
                {{ row.chiefComplaint || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="treatmentPlan" label="治疗方案" min-width="200" show-overflow-tooltip>
              <template #default="{ row }">
                {{ row.treatmentPlan || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="consultationFee" label="诊疗费" width="100" align="center">
              <template #default="{ row }">
                <span class="fee-text">¥{{ row.consultationFee || 0 }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right" align="center">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="viewRecordDetail(row.id)">
                  <el-icon><View /></el-icon>
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else class="empty-state">
          <el-empty description="暂无就诊记录" :image-size="100" />
        </div>
      </el-card>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="visible = false">关闭</el-button>
      </div>
    </template>

    <!-- 接诊记录详情弹窗 -->
    <RecordDetailDialog v-model="recordDetailVisible" :record-id="selectedRecordId" />
  </el-dialog>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, computed, watch } from 'vue'

import { Document, View } from '@element-plus/icons-vue'
import { getPatientById } from '@/api/patient'
import { getConsultationRecords } from '@/api/consultation'
import RecordDetailDialog from './RecordDetailDialog.vue'
import dayjs from 'dayjs'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  patientId: {
    type: [String, Number],
    default: null
  },
  appointmentId: {
    type: [String, Number],
    default: null
  },
  doctorId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const loading = ref(false)
const patientInfo = ref({})
const consultationHistory = ref([])
const recordDetailVisible = ref(false)
const selectedRecordId = ref(null)

// 监听弹窗打开，加载数据
watch(visible, (newVisible, oldVisible) => {
  // 只在从关闭变为打开时加载数据
  if (newVisible && !oldVisible) {
    if (props.patientId) {
      loadPatientDetail()
    } else {
      message.warning('患者ID缺失，无法加载详情')
    }
  } else if (!newVisible && oldVisible) {
    // 弹窗关闭时清空数据
    patientInfo.value = {}
    consultationHistory.value = []
  }
})

// 同时监听patientId变化（当弹窗已打开但patientId变化时）
watch(() => props.patientId, (newPatientId, oldPatientId) => {
  if (visible.value && newPatientId && newPatientId !== oldPatientId) {
    loadPatientDetail()
  }
})

// 加载患者详情
const loadPatientDetail = async () => {
  if (!props.patientId) {
    return
  }
  
  if (!props.doctorId) {
    return
  }
  
  loading.value = true
  try {
    await Promise.all([
      loadPatientInfo(),
      loadConsultationHistory()
    ])
  } catch (error) {
    message.error('加载患者详情失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 加载患者基本信息
const loadPatientInfo = async () => {
  try {
    if (!props.patientId) {
      patientInfo.value = {}
      return
    }
    
    const res = await getPatientById(props.patientId)
    
    if (res.code === 200) {
      patientInfo.value = res.data || {}
    } else {
      message.warning(res.message || '加载患者信息失败')
      patientInfo.value = {}
    }
  } catch (error) {
    message.error('加载患者信息失败，请稍后重试')
    patientInfo.value = {}
  }
}

// 加载接诊历史
const loadConsultationHistory = async () => {
  try {
    if (!props.patientId) {
      consultationHistory.value = []
      return
    }
    
    if (!props.doctorId) {
      consultationHistory.value = []
      return
    }

    const res = await getConsultationRecords(props.doctorId, {
      patientId: props.patientId,
      page: 1,
      pageSize: 100
    })
    
    if (res.code === 200) {
      // IPage对象可能直接是data，或者data.records
      let records = []
      if (Array.isArray(res.data)) {
        records = res.data
      } else if (res.data?.records && Array.isArray(res.data.records)) {
        records = res.data.records
      } else if (res.data?.list && Array.isArray(res.data.list)) {
        records = res.data.list
      }
      
      // 按日期和时间倒序排列，最新的在前面
      consultationHistory.value = records.sort((a, b) => {
        const dateA = dayjs(a.consultationDate + ' ' + (a.consultationTime || ''))
        const dateB = dayjs(b.consultationDate + ' ' + (b.consultationTime || ''))
        return dateB - dateA
      })
    } else {
      message.warning(res.message || '加载就诊记录失败')
      consultationHistory.value = []
    }
  } catch (error) {
    message.error('加载就诊记录失败，请稍后重试')
    consultationHistory.value = []
  }
}

// 获取最近就诊日期
const getLastVisitDate = () => {
  if (consultationHistory.value.length === 0) {
    return '-'
  }
  // 按日期排序，获取最新的
  const sorted = [...consultationHistory.value].sort((a, b) => {
    const dateA = dayjs(a.consultationDate + ' ' + a.consultationTime)
    const dateB = dayjs(b.consultationDate + ' ' + b.consultationTime)
    return dateB - dateA
  })
  return sorted[0].consultationDate || '-'
}

// 计算年龄
const calculateAge = (birthDate) => {
  if (!birthDate) return '-'
  return dayjs().diff(dayjs(birthDate), 'year')
}

// 格式化就诊时间
const formatConsultationTime = (row) => {
  // 优先使用consultationTime，如果没有则从consultationDateTime中提取
  if (row.consultationTime) {
    // 如果是LocalTime格式（HH:mm:ss），只显示时分
    const timeStr = String(row.consultationTime)
    return timeStr.substring(0, 5) // 取前5个字符（HH:mm）
  } else if (row.consultationDateTime) {
    // 从日期时间字符串中提取时间部分
    const dateTimeStr = String(row.consultationDateTime)
    const parts = dateTimeStr.split(' ')
    if (parts.length > 1) {
      return parts[1].substring(0, 5) // 提取时间部分并只显示时分
    }
  }
  return '-'
}

// 查看接诊记录详情
const viewRecordDetail = (recordId) => {
  selectedRecordId.value = recordId
  recordDetailVisible.value = true
}
</script>

<style scoped lang="scss">
.patient-detail {
  .summary-card {
    margin-bottom: 20px;
    background: linear-gradient(135deg, #f6ffed 0%, #d9f7be 100%);
    border: 1px solid #b7eb8f;

    :deep(.el-card__body) {
      padding: 16px 20px;
    }
  }

  .records-card {
    :deep(.el-card__header) {
      background: linear-gradient(90deg, #e6f7ff 0%, #bae7ff 100%);
      color: #1890ff;
      font-weight: bold;
      padding: 16px 20px;

      .card-header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;

        span {
          display: flex;
          align-items: center;
          gap: 8px;
        }
      }
    }
  }

  .info-item {
    margin-bottom: 0;

    .label {
      color: #666;
      font-size: 14px;
      margin-right: 8px;
    }

    .value {
      color: #333;
      font-size: 14px;
      font-weight: 500;

      &.highlight {
        color: #1890ff;
        font-weight: bold;
        font-size: 15px;
      }
    }
  }

  .diagnosis-text {
    color: #52c41a;
    font-weight: 500;
  }

  .fee-text {
    color: #f5222d;
    font-weight: bold;
  }

  .empty-state {
    padding: 40px;
    text-align: center;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
