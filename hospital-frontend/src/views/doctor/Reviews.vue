<template>
  <div class="reviews-container">
    <!-- 评价统计 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <div class="doctor-stat-card red">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Star />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ reviewStats.avgRating.toFixed(1) }}</div>
              <div class="stat-label">平均评分</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="doctor-stat-card blue">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <ChatDotRound />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ reviewStats.totalReviews }}</div>
              <div class="stat-label">总评价数</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="doctor-stat-card green">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Calendar />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ reviewStats.monthlyReviews }}</div>
              <div class="stat-label">本月评价</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="doctor-stat-card orange">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <TrendCharts />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ reviewStats.goodRate }}%</div>
              <div class="stat-label">好评率</div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 评价列表 -->
    <div class="doctor-card">
      <div class="card-header">
        <h3>
          <el-icon>
            <ChatDotRound />
          </el-icon>
          患者评价
        </h3>
        <div class="header-actions">
          <el-select v-model="filterRating" placeholder="筛选评分" clearable style="width: 150px" @change="handleRatingFilterChange">
            <el-option label="5星好评" :value="5" />
            <el-option label="4星" :value="4" />
            <el-option label="3星" :value="3" />
            <el-option label="2星" :value="2" />
            <el-option label="1星" :value="1" />
          </el-select>
        </div>
      </div>

      <div class="card-body">
        <!-- 评价列表 -->
        <div v-loading="loading">
          <div v-for="review in reviews" :key="review.id" class="review-item">
            <div class="review-header">
              <div class="patient-info">
                <el-avatar :size="50" :src="review.patientAvatar">
                  <el-icon>
                    <User />
                  </el-icon>
                </el-avatar>
                <div class="info">
                  <h4>{{ review.patientName }}</h4>
                  <p>{{ review.appointmentDate }} {{ review.timeSlot }}</p>
                </div>
              </div>
              <div class="rating-info">
                <el-rate v-model="review.rating" disabled show-score />
                <span class="date">{{ review.createTime }}</span>
              </div>
            </div>
            <div class="review-content">
              <p>{{ review.content }}</p>

              <div v-if="review.tagList?.length" class="tag-list">
                <el-tag
                  v-for="tag in review.tagList"
                  :key="tag"
                  size="small"
                  effect="light"
                  round
                >
                  {{ tag }}
                </el-tag>
              </div>

              <!-- 医生回复 -->
              <div v-if="review.doctorReply" class="doctor-reply">
                <div class="reply-header">
                  <el-icon color="#52c41a">
                    <ChatDotRound />
                  </el-icon>
                  <span class="reply-label">医生回复：</span>
                  <span class="reply-time">{{ review.doctorReplyTime }}</span>
                </div>
                <div class="reply-content">{{ review.doctorReply }}</div>
              </div>
            </div>
            <div class="review-footer">
              <div class="footer-left">
                <el-tag v-if="review.auditStatus === 1" type="success" size="small">已通过</el-tag>
                <el-tag v-else-if="review.auditStatus === 0" type="warning" size="small">待审核</el-tag>
                <el-tag v-else type="info" size="small">已回复</el-tag>
              </div>
              <div class="footer-right">
                <el-button v-if="!review.doctorReply" type="primary" size="small" @click="openReplyDialog(review)">
                  <el-icon>
                    <ChatDotRound />
                  </el-icon>
                  回复
                </el-button>
              </div>
            </div>
            <el-divider />
          </div>

          <div v-if="reviews.length === 0 && !loading" class="doctor-empty">
            <div class="empty-icon">
              <el-icon>
                <ChatDotRound />
              </el-icon>
            </div>
            <div class="empty-text">暂无评价</div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="doctor-pagination" v-if="total > 0">
          <el-pagination v-model:current-page="queryParams.page" v-model:page-size="queryParams.pageSize" :total="total"
            layout="total, prev, pager, next" @current-change="loadReviews" />
        </div>
      </div>
    </div>

    <!-- 回复弹窗 -->
    <el-dialog v-model="replyDialogVisible" title="回复评价" width="600px">
      <div class="reply-dialog-content">
        <div class="review-info">
          <div class="info-row">
            <span class="label">患者：</span>
            <span class="value">{{ selectedReview.patientName }}</span>
          </div>
          <div class="info-row">
            <span class="label">评分：</span>
            <el-rate v-model="selectedReview.rating" disabled show-score />
          </div>
          <div class="info-row">
            <span class="label">评价内容：</span>
            <div class="value">{{ selectedReview.content }}</div>
          </div>
        </div>
        <el-divider />
        <el-form :model="replyForm" label-width="80px">
          <el-form-item label="回复内容">
            <el-input v-model="replyForm.reply" type="textarea" :rows="5" placeholder="请输入回复内容" maxlength="500"
              show-word-limit />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="replyDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReply" :loading="submitting">
          提交回复
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, onMounted } from 'vue'

import {
  Star,
  ChatDotRound,
  Calendar,
  TrendCharts,
  User
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useDoctorStore } from '@/stores/doctor'
import { getDoctorReviews, replyReview } from '@/api/review'
import { getDoctorReviewStats } from '@/api/statistics'

const userStore = useUserStore()
const doctorStore = useDoctorStore()

const loading = ref(false)
const filterRating = ref(null)
const submitting = ref(false)

// 回复弹窗
const replyDialogVisible = ref(false)
const selectedReview = ref({})
const replyForm = reactive({
  reply: ''
})

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10
})

// 评价统计
const reviewStats = reactive({
  avgRating: 0,
  totalReviews: 0,
  monthlyReviews: 0,
  goodRate: 0
})

// 加载评价统计
const loadReviewStats = async () => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) {

    return
  }

  try {
    const res = await getDoctorReviewStats(doctorId)
    if (res.code === 200) {
      reviewStats.avgRating = res.data.avgRating
      reviewStats.totalReviews = res.data.totalReviews
      reviewStats.monthlyReviews = res.data.monthlyReviews
      reviewStats.goodRate = res.data.goodRate
    }
  } catch (error) {

    message.error('加载评价统计失败')
  }
}

// 数据
const reviews = ref([])
const total = ref(0)

// 加载评价列表
const loadReviews = async () => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) {

    return
  }

  loading.value = true
  try {
    const params = {
      rating: filterRating.value,
      ...queryParams
    }
    const res = await getDoctorReviews(doctorId, params)
    if (res.code === 200) {
      const records = res.data?.records || []
      records.forEach((item) => {
        if (item.tags) {
          try {
            const parsed = JSON.parse(item.tags)
            item.tagList = Array.isArray(parsed) ? parsed : []
          } catch (error) {

            item.tagList = []
          }
        } else {
          item.tagList = []
        }
      })
      reviews.value = records
      // 确保 total 是数字类型
      total.value = Number(res.data?.total) || 0
    }
  } catch (error) {

    message.error('加载评价列表失败')
  } finally {
    loading.value = false
  }
}

// 评分筛选
const handleRatingFilterChange = () => {
  queryParams.page = 1
  loadReviews()
}

// 打开回复弹窗
const openReplyDialog = (review) => {
  selectedReview.value = review
  replyForm.reply = ''
  replyDialogVisible.value = true
}

// 提交回复
const submitReply = async () => {
  if (!replyForm.reply.trim()) {
    message.warning('请输入回复内容')
    return
  }

  submitting.value = true
  try {
    const res = await replyReview(selectedReview.value.id, {
      reply: replyForm.reply
    })

    if (res.code === 200) {
      message.success('回复成功')
      replyDialogVisible.value = false
      // 刷新列表
      loadReviews()
    } else {
      message.error(res.message || '回复失败')
    }
  } catch (error) {

    message.error('回复失败')
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  await doctorStore.fetchDoctorInfo()
  loadReviewStats()
  loadReviews()
})
</script>

<style scoped lang="scss">
.reviews-container {
  max-width: 1200px;
  margin: 0 auto;

  .stats-row {
    margin-bottom: 20px;

    .stat-card {
      margin-bottom: 20px;
      transition: all 0.3s;

      &:hover {
        transform: translateY(-5px);
      }
    }
  }

  .tag-list {
    margin: 10px 0;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
      font-size: 20px;
    }
  }

  .review-item {
    margin-bottom: 20px;

    .review-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;

      .patient-info {
        display: flex;
        gap: 15px;
        align-items: center;

        .info {
          h4 {
            margin: 0 0 5px 0;
            font-size: 16px;
            color: #333;
          }

          p {
            margin: 0;
            font-size: 13px;
            color: #909399;
          }
        }
      }

      .rating-info {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 8px;

        .date {
          font-size: 12px;
          color: #909399;
        }
      }
    }

    .review-content {
      padding: 15px 20px;
      background: #f5f7fa;
      border-radius: 8px;
      margin-bottom: 10px;

      p {
        margin: 0;
        line-height: 1.8;
        color: #606266;
      }

      .doctor-reply {
        margin-top: 15px;
        padding: 15px;
        background: #f0f9ff;
        border-left: 3px solid #52c41a;
        border-radius: 4px;

        .reply-header {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 10px;

          .reply-label {
            font-weight: bold;
            color: #52c41a;
          }

          .reply-time {
            font-size: 12px;
            color: #999;
          }
        }

        .reply-content {
          color: #666;
          line-height: 1.6;
        }
      }
    }

    .review-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .footer-left {
        display: flex;
        gap: 10px;
      }

      .footer-right {
        display: flex;
        gap: 10px;
      }
    }
  }

  .reply-dialog-content {
    .review-info {
      .info-row {
        margin-bottom: 15px;

        .label {
          color: #666;
          font-weight: bold;
          display: inline-block;
          width: 100px;
        }

        .value {
          color: #333;
          line-height: 1.6;
        }
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
