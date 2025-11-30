<template>
  <el-dialog
    v-model="visible"
    title="查看评价"
    width="600px"
    :before-close="handleClose"
  >
    <div v-if="review" class="review-view">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="总体评分">
          <el-rate
            :model-value="review.rating"
            disabled
            show-score
            text-color="#ff9900"
            score-template="{value} 分"
          />
        </el-descriptions-item>

        <el-descriptions-item label="服务态度">
          <el-rate
            :model-value="review.serviceRating"
            disabled
            show-score
            text-color="#ff9900"
            score-template="{value} 分"
          />
        </el-descriptions-item>

        <el-descriptions-item label="专业水平">
          <el-rate
            :model-value="review.professionalRating"
            disabled
            show-score
            text-color="#ff9900"
            score-template="{value} 分"
          />
        </el-descriptions-item>

        <el-descriptions-item label="环境设施">
          <el-rate
            :model-value="review.environmentRating"
            disabled
            show-score
            text-color="#ff9900"
            score-template="{value} 分"
          />
        </el-descriptions-item>

        <el-descriptions-item label="评价内容" v-if="review.content">
          <div class="review-content">{{ review.content }}</div>
        </el-descriptions-item>

        <el-descriptions-item label="评价标签" v-if="tagList && tagList.length > 0">
          <div class="review-tags">
            <el-tag v-for="tag in tagList" :key="tag" size="small" style="margin-right: 8px;">
              {{ tag }}
            </el-tag>
          </div>
        </el-descriptions-item>

        <el-descriptions-item label="是否匿名">
          {{ review.isAnonymous === 1 ? '是' : '否' }}
        </el-descriptions-item>

        <el-descriptions-item label="评价时间" v-if="review.createdAt">
          {{ formatDateTime(review.createdAt) }}
        </el-descriptions-item>

        <el-descriptions-item label="医生回复" v-if="review.doctorReply">
          <div class="doctor-reply">
            <div class="reply-content">{{ review.doctorReply }}</div>
            <div class="reply-time" v-if="review.doctorReplyTime">
              {{ formatDateTime(review.doctorReplyTime) }}
            </div>
          </div>
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <el-empty v-else description="暂无评价信息" />

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { getReviewByAppointmentId } from '@/api/review'
import dayjs from 'dayjs'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  appointmentId: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const review = ref(null)
const tagList = computed(() => {
  if (!review.value || !review.value.tags) {
    return []
  }
  try {
    const parsed = JSON.parse(review.value.tags)
    return Array.isArray(parsed) ? parsed : []
  } catch (error) {
    return []
  }
})

// 监听弹窗打开，加载评价数据
watch(visible, async (val) => {
  if (val && props.appointmentId) {
    await loadReview()
  } else {
    review.value = null
  }
})

const loadReview = async () => {
  if (!props.appointmentId) {
    review.value = null
    return
  }

  try {
    const res = await getReviewByAppointmentId(props.appointmentId)
    if (res.code === 200) {
      review.value = res.data
    } else {
      review.value = null
    }
  } catch (error) {
    console.error('加载评价失败', error)
    review.value = null
  }
}

const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '-'
  return dayjs(dateTimeStr).format('YYYY年MM月DD日 HH:mm:ss')
}

const handleClose = () => {
  visible.value = false
}
</script>

<style scoped lang="scss">
.review-view {
  .review-content {
    white-space: pre-wrap;
    word-break: break-word;
    line-height: 1.6;
    color: #333;
  }

  .review-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .doctor-reply {
    background-color: #f5f7fa;
    padding: 12px;
    border-radius: 4px;
    border-left: 3px solid #409eff;

    .reply-content {
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.6;
      color: #333;
      margin-bottom: 8px;
    }

    .reply-time {
      font-size: 12px;
      color: #909399;
      text-align: right;
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.el-descriptions__label) {
  font-weight: 500;
  width: 120px;
}
</style>
