<template>
  <el-dialog
    v-model="visible"
    title="评价医生"
    width="600px"
    :before-close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
    >
      <el-form-item label="总体评分" prop="rating" required>
        <el-rate
          v-model="form.rating"
          :max="5"
          show-score
          text-color="#ff9900"
          score-template="{value} 分"
        />
      </el-form-item>

      <el-form-item label="服务态度" prop="serviceRating" required>
        <el-rate
          v-model="form.serviceRating"
          :max="5"
          show-score
          text-color="#ff9900"
          score-template="{value} 分"
        />
      </el-form-item>

      <el-form-item label="专业水平" prop="professionalRating" required>
        <el-rate
          v-model="form.professionalRating"
          :max="5"
          show-score
          text-color="#ff9900"
          score-template="{value} 分"
        />
      </el-form-item>

      <el-form-item label="环境设施" prop="environmentRating" required>
        <el-rate
          v-model="form.environmentRating"
          :max="5"
          show-score
          text-color="#ff9900"
          score-template="{value} 分"
        />
      </el-form-item>

      <el-form-item label="评价内容" prop="content">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="4"
          placeholder="请输入您的评价内容（选填）"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="评价标签">
        <el-checkbox-group v-model="form.tags">
          <el-checkbox label="医术精湛">医术精湛</el-checkbox>
          <el-checkbox label="态度友好">态度友好</el-checkbox>
          <el-checkbox label="耐心细致">耐心细致</el-checkbox>
          <el-checkbox label="诊断准确">诊断准确</el-checkbox>
          <el-checkbox label="环境舒适">环境舒适</el-checkbox>
          <el-checkbox label="等待时间短">等待时间短</el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <el-form-item>
        <el-checkbox v-model="form.isAnonymous">
          匿名评价
        </el-checkbox>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          提交评价
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, computed, watch } from 'vue'

import { createReview } from '@/api/review'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  appointment: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const formRef = ref(null)
const submitting = ref(false)

const form = reactive({
  rating: null,
  serviceRating: null,
  professionalRating: null,
  environmentRating: null,
  content: '',
  tags: [],
  isAnonymous: false
})

const rules = {
  rating: [
    { required: true, message: '请选择总体评分', trigger: 'change' }
  ],
  serviceRating: [
    { required: true, message: '请选择服务态度评分', trigger: 'change' }
  ],
  professionalRating: [
    { required: true, message: '请选择专业水平评分', trigger: 'change' }
  ],
  environmentRating: [
    { required: true, message: '请选择环境设施评分', trigger: 'change' }
  ]
}

// 监听弹窗打开，重置表单
watch(visible, (val) => {
  if (val) {
    resetForm()
  }
})

const resetForm = () => {
  Object.assign(form, {
    rating: null,
    serviceRating: null,
    professionalRating: null,
    environmentRating: null,
    content: '',
    tags: [],
    isAnonymous: false
  })
  formRef.value?.clearValidate()
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    
    submitting.value = true

    const reviewData = {
      appointmentId: props.appointment.id,
      consultationRecordId: props.appointment.consultationRecordId || null,
      patientId: props.appointment.patientId,
      doctorId: props.appointment.doctorId,
      categoryId: props.appointment.categoryId,
      rating: form.rating,
      serviceRating: form.serviceRating,
      professionalRating: form.professionalRating,
      environmentRating: form.environmentRating,
      content: form.content || null,
      tags: form.tags.length > 0 ? JSON.stringify(form.tags) : null,
      images: null,
      isAnonymous: form.isAnonymous ? 1 : 0
    }

    const res = await createReview(reviewData)

    if (res.code === 200) {
      message.success('评价提交成功，感谢您的反馈！')
      emit('success')
      visible.value = false
    } else {
      message.error(res.message || '提交评价失败')
    }
  } catch (error) {
    if (error !== false) {

      message.error('提交评价失败')
    }
  } finally {
    submitting.value = false
  }
}

const handleClose = () => {
  visible.value = false
}
</script>

<style scoped lang="scss">
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-checkbox-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

:deep(.el-checkbox) {
  margin-right: 0;
}
</style>

