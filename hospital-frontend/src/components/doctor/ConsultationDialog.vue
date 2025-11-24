<template>
  <el-dialog
    v-model="visible"
    title="接诊记录"
    width="900px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
      <!-- 患者信息 -->
      <el-card class="patient-info-card" shadow="never">
        <template #header>
          <span>患者信息</span>
        </template>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="info-item">
              <span class="label">姓名：</span>
              <span class="value">{{ patientInfo.patientName }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <span class="label">性别：</span>
              <span class="value">{{ patientInfo.gender === 1 ? '男' : '女' }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <span class="label">年龄：</span>
              <span class="value">{{ patientInfo.age || '-' }}岁</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <span class="label">手机号：</span>
              <span class="value">{{ patientInfo.phone }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <span class="label">预约时段：</span>
              <span class="value">{{ formatTimeSlot(patientInfo.timeSlot) }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <span class="label">排队号：</span>
              <span class="value">{{ patientInfo.queueNumber }}</span>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 接诊信息 -->
      <el-divider content-position="left">接诊信息</el-divider>

      <el-form-item label="主诉" prop="chiefComplaint">
        <el-input
          v-model="form.chiefComplaint"
          type="textarea"
          :rows="3"
          placeholder="请输入患者主诉"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="现病史" prop="presentIllness">
        <el-input
          v-model="form.presentIllness"
          type="textarea"
          :rows="3"
          placeholder="请输入现病史"
          maxlength="1000"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="既往史">
        <el-input
          v-model="form.pastHistory"
          type="textarea"
          :rows="2"
          placeholder="请输入既往史"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="体格检查">
        <el-input
          v-model="form.physicalExamination"
          type="textarea"
          :rows="2"
          placeholder="请输入体格检查结果"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="辅助检查">
        <el-input
          v-model="form.auxiliaryExamination"
          type="textarea"
          :rows="2"
          placeholder="请输入辅助检查结果"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="诊断" prop="diagnosis">
        <el-input
          v-model="form.diagnosis"
          type="textarea"
          :rows="2"
          placeholder="请输入诊断结果"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="治疗方案" prop="treatmentPlan">
        <el-input
          v-model="form.treatmentPlan"
          type="textarea"
          :rows="3"
          placeholder="请输入治疗方案"
          maxlength="1000"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="处方">
        <el-input
          v-model="form.prescription"
          type="textarea"
          :rows="4"
          placeholder="请输入处方内容（药品名称、用量、用法等）"
          maxlength="2000"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="随访建议">
        <el-input
          v-model="form.followUpAdvice"
          type="textarea"
          :rows="2"
          placeholder="请输入随访建议"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="诊疗费">
        <el-input-number
          v-model="form.consultationFee"
          :min="0"
          :max="9999"
          :precision="2"
          :step="10"
          placeholder="请输入诊疗费"
        />
        <span style="margin-left: 10px; color: #999;">元</span>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" plain @click="handleSaveDraft" :loading="saving">
          <el-icon><Document /></el-icon>
          保存草稿
        </el-button>
        <el-button type="success" @click="handleComplete" :loading="saving">
          <el-icon><CircleCheck /></el-icon>
          完成接诊
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, computed, watch } from 'vue'

import { Document, CircleCheck } from '@element-plus/icons-vue'
import { completeConsultation, createConsultationRecord, updateConsultationRecord } from '@/api/consultation'
import dayjs from 'dayjs'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  patientInfo: {
    type: Object,
    default: () => ({})
  },
  doctorId: {
    type: [String, Number],
    required: false,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const formRef = ref(null)
const saving = ref(false)
const startTime = ref(null)

// 表单数据
const form = reactive({
  chiefComplaint: '',
  presentIllness: '',
  pastHistory: '',
  physicalExamination: '',
  auxiliaryExamination: '',
  diagnosis: '',
  treatmentPlan: '',
  prescription: '',
  followUpAdvice: '',
  consultationFee: 0,
  recordId: null // 用于保存草稿后的记录ID
})

// 表单验证规则
const rules = {
  chiefComplaint: [
    { required: true, message: '请输入患者主诉', trigger: 'blur' }
  ],
  diagnosis: [
    { required: true, message: '请输入诊断结果', trigger: 'blur' }
  ],
  treatmentPlan: [
    { required: true, message: '请输入治疗方案', trigger: 'blur' }
  ]
}

// 监听弹窗打开，记录开始时间
watch(visible, (val) => {
  if (val) {
    startTime.value = dayjs()
    resetForm()
  }
})

// 格式化时段
const formatTimeSlot = (slot) => {
  const slotMap = {
    'MORNING': '上午',
    'AFTERNOON': '下午',
    'EVENING': '晚间'
  }
  return slotMap[slot] || slot
}

// 计算接诊时长（分钟）
const calculateDuration = () => {
  if (!startTime.value) return 0
  return dayjs().diff(startTime.value, 'minute')
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    chiefComplaint: '',
    presentIllness: '',
    pastHistory: '',
    physicalExamination: '',
    auxiliaryExamination: '',
    diagnosis: '',
    treatmentPlan: '',
    prescription: '',
    followUpAdvice: '',
    consultationFee: props.patientInfo.consultationFee || 0,
    recordId: null
  })
  formRef.value?.clearValidate()
}

// 保存草稿
const handleSaveDraft = async () => {
  try {
    saving.value = true
    
    // 验证 doctorId
    if (!props.doctorId) {
      message.error('医生ID不能为空')
      return
    }
    
    const payload = {
      appointmentId: props.patientInfo.appointmentId,
      patientId: props.patientInfo.patientId,
      doctorId: props.doctorId,
      categoryId: props.patientInfo.categoryId,
      consultationDate: dayjs().format('YYYY-MM-DD'),
      consultationTime: dayjs().format('HH:mm:ss'),
      chiefComplaint: form.chiefComplaint,
      presentIllness: form.presentIllness,
      pastHistory: form.pastHistory,
      physicalExamination: form.physicalExamination,
      auxiliaryExamination: form.auxiliaryExamination,
      diagnosis: form.diagnosis,
      treatmentPlan: form.treatmentPlan,
      prescription: form.prescription,
      followUpAdvice: form.followUpAdvice,
      consultationFee: form.consultationFee,
      durationMinutes: calculateDuration(),
      status: 'IN_PROGRESS'
    }

    let res
    if (form.recordId) {
      // 更新草稿
      payload.id = form.recordId
      res = await updateConsultationRecord(payload)
    } else {
      // 创建草稿
      res = await createConsultationRecord(payload)
      if (res.code === 200 && res.data) {
        form.recordId = res.data
      }
    }

    if (res.code === 200) {
      message.success('草稿保存成功')
    } else {
      message.error(res.message || '保存草稿失败')
    }
  } catch (error) {

    message.error('保存草稿失败')
  } finally {
    saving.value = false
  }
}

// 完成接诊
const handleComplete = async () => {
  try {
    await formRef.value.validate()
    
    saving.value = true
    
    const payload = {
      chiefComplaint: form.chiefComplaint,
      presentIllness: form.presentIllness,
      pastHistory: form.pastHistory,
      physicalExamination: form.physicalExamination,
      auxiliaryExamination: form.auxiliaryExamination,
      diagnosis: form.diagnosis,
      treatmentPlan: form.treatmentPlan,
      prescription: form.prescription,
      followUpAdvice: form.followUpAdvice,
      consultationFee: form.consultationFee,
      durationMinutes: calculateDuration()
    }

    const res = await completeConsultation(props.patientInfo.appointmentId, payload)
    
    if (res.code === 200) {
      message.success('接诊完成')
      emit('success')
      visible.value = false
    } else {
      message.error(res.message || '完成接诊失败')
    }
  } catch (error) {
    if (error !== false) { // 不是表单验证错误

      message.error('完成接诊失败')
    }
  } finally {
    saving.value = false
  }
}

// 关闭弹窗
const handleClose = () => {
  visible.value = false
}
</script>

<style scoped lang="scss">
.patient-info-card {
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-textarea__inner) {
  font-family: inherit;
}
</style>

