<template>
  <el-dialog
    v-model="visible"
    title="接诊记录详情"
    width="900px"
    :close-on-click-modal="false"
  >
    <div v-loading="loading" class="record-detail">
      <!-- 患者信息 -->
      <el-card class="info-card" shadow="never">
        <template #header>
          <span>患者信息</span>
        </template>
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="info-item">
              <span class="label">姓名：</span>
              <span class="value">{{ record.patientName }}</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="info-item">
              <span class="label">接诊日期：</span>
              <span class="value">{{ record.consultationDate }}</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="info-item">
              <span class="label">接诊时间：</span>
              <span class="value">{{ record.consultationTime }}</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="info-item">
              <span class="label">接诊时长：</span>
              <span class="value">{{ record.durationMinutes || 0 }}分钟</span>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 接诊信息 -->
      <el-card class="info-card" shadow="never">
        <template #header>
          <span>接诊信息</span>
        </template>

        <div class="detail-section">
          <div class="section-title">主诉</div>
          <div class="section-content">{{ record.chiefComplaint || '-' }}</div>
        </div>

        <div class="detail-section">
          <div class="section-title">现病史</div>
          <div class="section-content">{{ record.presentIllness || '-' }}</div>
        </div>

        <div class="detail-section">
          <div class="section-title">既往史</div>
          <div class="section-content">{{ record.pastHistory || '-' }}</div>
        </div>

        <div class="detail-section">
          <div class="section-title">体格检查</div>
          <div class="section-content">{{ record.physicalExamination || '-' }}</div>
        </div>

        <div class="detail-section">
          <div class="section-title">辅助检查</div>
          <div class="section-content">{{ record.auxiliaryExamination || '-' }}</div>
        </div>

        <div class="detail-section">
          <div class="section-title">诊断</div>
          <div class="section-content highlight">{{ record.diagnosis || '-' }}</div>
        </div>

        <div class="detail-section">
          <div class="section-title">治疗方案</div>
          <div class="section-content">{{ record.treatmentPlan || '-' }}</div>
        </div>

        <div class="detail-section">
          <div class="section-title">处方</div>
          <div class="section-content prescription">
            <pre>{{ record.prescription || '-' }}</pre>
          </div>
        </div>

        <div class="detail-section">
          <div class="section-title">随访建议</div>
          <div class="section-content">{{ record.followUpAdvice || '-' }}</div>
        </div>

        <div class="detail-section">
          <div class="section-title">诊疗费</div>
          <div class="section-content fee">¥{{ record.consultationFee || 0 }}</div>
        </div>
      </el-card>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="visible = false">关闭</el-button>
        <el-button type="primary" @click="handlePrint">
          <el-icon><Printer /></el-icon>
          打印记录
        </el-button>
        <el-button type="success" @click="handlePrintPrescription">
          <el-icon><Document /></el-icon>
          打印处方
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, computed, watch } from 'vue'

import { Printer, Document } from '@element-plus/icons-vue'
import { getConsultationRecordById } from '@/api/consultation'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  recordId: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const loading = ref(false)
const record = ref({})

// 监听弹窗打开，加载数据
watch(visible, (val) => {
  if (val && props.recordId) {
    loadRecordDetail()
  }
})

// 加载接诊记录详情
const loadRecordDetail = async () => {
  loading.value = true
  try {
    const res = await getConsultationRecordById(props.recordId)
    if (res.code === 200) {
      record.value = res.data || {}
    } else {
      message.error(res.message || '加载接诊记录失败')
    }
  } catch (error) {

    message.error('加载接诊记录失败')
  } finally {
    loading.value = false
  }
}

// 打印接诊记录
const handlePrint = () => {
  const printContent = `
    <html>
      <head>
        <title>接诊记录</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; }
          h1 { text-align: center; color: #333; }
          .section { margin-bottom: 15px; }
          .label { font-weight: bold; color: #666; }
          .value { color: #333; }
          .divider { border-top: 1px solid #ddd; margin: 20px 0; }
        </style>
      </head>
      <body>
        <h1>接诊记录</h1>
        <div class="section">
          <span class="label">患者姓名：</span>
          <span class="value">${record.value.patientName}</span>
        </div>
        <div class="section">
          <span class="label">接诊日期：</span>
          <span class="value">${record.value.consultationDate} ${record.value.consultationTime}</span>
        </div>
        <div class="divider"></div>
        <div class="section">
          <div class="label">主诉：</div>
          <div class="value">${record.value.chiefComplaint || '-'}</div>
        </div>
        <div class="section">
          <div class="label">现病史：</div>
          <div class="value">${record.value.presentIllness || '-'}</div>
        </div>
        <div class="section">
          <div class="label">既往史：</div>
          <div class="value">${record.value.pastHistory || '-'}</div>
        </div>
        <div class="section">
          <div class="label">体格检查：</div>
          <div class="value">${record.value.physicalExamination || '-'}</div>
        </div>
        <div class="section">
          <div class="label">辅助检查：</div>
          <div class="value">${record.value.auxiliaryExamination || '-'}</div>
        </div>
        <div class="section">
          <div class="label">诊断：</div>
          <div class="value">${record.value.diagnosis || '-'}</div>
        </div>
        <div class="section">
          <div class="label">治疗方案：</div>
          <div class="value">${record.value.treatmentPlan || '-'}</div>
        </div>
        <div class="section">
          <div class="label">处方：</div>
          <pre class="value">${record.value.prescription || '-'}</pre>
        </div>
        <div class="section">
          <div class="label">随访建议：</div>
          <div class="value">${record.value.followUpAdvice || '-'}</div>
        </div>
        <div class="divider"></div>
        <div class="section">
          <span class="label">诊疗费：</span>
          <span class="value">¥${record.value.consultationFee || 0}</span>
        </div>
        <div class="section">
          <span class="label">医生签名：</span>
          <span class="value">${record.value.doctorName}</span>
        </div>
      </body>
    </html>
  `
  
  const printWindow = window.open('', '_blank')
  printWindow.document.write(printContent)
  printWindow.document.close()
  printWindow.print()
}

// 打印处方
const handlePrintPrescription = () => {
  if (!record.value.prescription) {
    message.warning('暂无处方信息')
    return
  }

  const printContent = `
    <html>
      <head>
        <title>处方</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; }
          h1 { text-align: center; color: #333; }
          .header { margin-bottom: 20px; }
          .prescription { white-space: pre-wrap; font-size: 14px; line-height: 1.8; }
          .footer { margin-top: 40px; text-align: right; }
        </style>
      </head>
      <body>
        <h1>处方</h1>
        <div class="header">
          <div>患者姓名：${record.value.patientName}</div>
          <div>日期：${record.value.consultationDate}</div>
        </div>
        <div class="prescription">${record.value.prescription}</div>
        <div class="footer">
          <div>医生签名：${record.value.doctorName}</div>
        </div>
      </body>
    </html>
  `
  
  const printWindow = window.open('', '_blank')
  printWindow.document.write(printContent)
  printWindow.document.close()
  printWindow.print()
}
</script>

<style scoped lang="scss">
.record-detail {
  .info-card {
    margin-bottom: 20px;

    :deep(.el-card__header) {
      background: linear-gradient(90deg, #f6ffed 0%, #d9f7be 100%);
      color: #52c41a;
      font-weight: bold;
    }
  }

  .info-item {
    margin-bottom: 10px;

    .label {
      color: #666;
      font-size: 14px;
    }

    .value {
      color: #333;
      font-size: 14px;
      font-weight: 500;
    }
  }

  .detail-section {
    margin-bottom: 20px;

    .section-title {
      font-weight: bold;
      color: #52c41a;
      margin-bottom: 8px;
      font-size: 15px;
    }

    .section-content {
      color: #333;
      line-height: 1.6;
      padding: 10px;
      background: #f9f9f9;
      border-radius: 4px;

      &.highlight {
        background: #fff7e6;
        border-left: 3px solid #faad14;
        font-weight: 500;
      }

      &.prescription {
        background: #f0f9ff;
        border-left: 3px solid #1890ff;

        pre {
          margin: 0;
          font-family: inherit;
          white-space: pre-wrap;
          word-wrap: break-word;
        }
      }

      &.fee {
        font-size: 18px;
        font-weight: bold;
        color: #f5222d;
      }
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>

