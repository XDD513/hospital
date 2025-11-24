<template>
  <div class="article-detail-container">
    <el-page-header @back="goBack" title="返回">
      <template #content>
        <span class="page-title">文章详情</span>
      </template>
    </el-page-header>

    <el-card class="detail-card">
      <template v-if="loading">
        <el-skeleton animated>
          <template #template>
            <div class="detail-skeleton">
              <div class="detail-skeleton-header">
                <el-skeleton-item variant="h1" style="width: 70%;" />
                <div class="detail-skeleton-meta">
                  <el-skeleton-item variant="text" style="width: 120px;" />
                  <el-skeleton-item variant="text" style="width: 100px;" />
                  <el-skeleton-item variant="text" style="width: 80px;" />
                </div>
              </div>
              <el-skeleton-item variant="text" style="width: 100%; height: 220px;" />
              <div class="detail-skeleton-actions">
                <el-skeleton-item variant="button" style="width: 120px;" />
                <el-skeleton-item variant="button" style="width: 120px;" />
                <el-skeleton-item variant="button" style="width: 120px;" />
              </div>
              <div class="detail-skeleton-comments">
                <el-skeleton-item variant="text" style="width: 40%;" />
                <div class="detail-skeleton-comment-item" v-for="n in 2" :key="`comment-skeleton-${n}`">
                  <el-skeleton-item variant="text" style="width: 30%;" />
                  <el-skeleton-item variant="text" />
                  <el-skeleton-item variant="text" style="width: 60%;" />
                </div>
              </div>
            </div>
          </template>
        </el-skeleton>
      </template>

      <template v-else-if="article">
        <!-- 文章头部 -->
        <div class="article-header">
          <h1>{{ article.title }}</h1>
          <div class="article-meta">
            <span class="author">
              <el-icon>
                <User />
              </el-icon>
              {{ article.authorName }}
            </span>
            <span class="category">
              <el-tag size="small">{{ getCategoryLabel(article.category) }}</el-tag>
            </span>
            <span class="time">{{ formatTime(article.publishTime) }}</span>
            <span class="stats">
              <el-icon>
                <View />
              </el-icon>
              {{ article.viewCount || 0 }}
            </span>
          </div>
        </div>

        <el-divider />

        <!-- 文章内容 -->
        <div class="article-content" v-html="article.content"></div>

        <el-divider />

        <!-- 文章操作 -->
        <div class="article-actions">
          <el-button :type="isLiked ? 'primary' : 'default'" :icon="Star" @click="handleLike">
            {{ isLiked ? '已点赞' : '点赞' }} ({{ article.likeCount || 0 }})
          </el-button>
          <el-button :type="isFavorited ? 'warning' : 'default'" :icon="Collection" @click="handleFavorite">
            {{ isFavorited ? '已收藏' : '收藏' }} ({{ article.favoriteCount || 0 }})
          </el-button>
          <el-button v-if="isAuthor" type="info" :icon="Edit" @click="handleEdit">
            编辑
          </el-button>
          <el-button v-if="isAuthor" type="danger" :icon="Delete" @click="handleDelete">
            删除
          </el-button>
        </div>

        <el-divider />

        <!-- 评论区 -->
        <div class="comment-section">
          <h3>评论 ({{ article.commentCount || 0 }})</h3>

          <!-- 发表评论 -->
          <div class="comment-form">
            <el-input v-model="commentContent" type="textarea" :rows="3" placeholder="写下你的评论..." />
            <el-button type="primary" @click="handlePublishComment" :disabled="!commentContent.trim()"
              style="margin-top: 10px;">
              发表评论
            </el-button>
          </div>

          <!-- 评论列表 -->
          <div class="comment-list">
            <div v-for="comment in commentList" :key="comment.id" class="comment-item">
              <div class="comment-header">
                <span class="comment-author">{{ comment.userName }}</span>
                <span class="comment-time">{{ formatTime(comment.createdAt) }}</span>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
              <div class="comment-actions">
                <el-button text size="small" :type="comment.isLiked ? 'primary' : ''"
                  @click="handleLikeComment(comment)">
                  <el-icon>
                    <Star />
                  </el-icon>
                  {{ comment.isLiked ? '已点赞' : '点赞' }} ({{ comment.likeCount || 0 }})
                </el-button>
                <el-button v-if="comment.userId === userStore.userInfo?.id" text size="small" type="danger"
                  @click="handleDeleteComment(comment.id)">
                  删除
                </el-button>
              </div>
            </div>
          </div>

          <!-- 评论分页 -->
          <div class="pagination-container" v-if="commentTotal > 0">
            <el-pagination v-model:current-page="commentParams.pageNum" v-model:page-size="commentParams.pageSize"
              :total="commentTotal" layout="prev, pager, next" @current-change="loadComments" />
          </div>
        </div>
      </template>

      <el-empty v-else description="文章不存在或已删除" />
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { User, View, Star, Collection, Edit, Delete } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import dayjs from 'dayjs'
import {
  getArticleDetail,
  likeArticle,
  unlikeArticle,
  favoriteArticle,
  unfavoriteArticle,
  deleteArticle,
  checkLikeStatus,
  checkFavoriteStatus
} from '@/api/article'
import {
  getCommentList,
  publishComment,
  deleteComment,
  likeComment,
  unlikeComment,
  checkCommentLikeStatus
} from '@/api/comment'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const article = ref(null)
const commentList = ref([])
const commentTotal = ref(0)
const loading = ref(false)
const isLiked = ref(false)
const isFavorited = ref(false)
const commentContent = ref('')

const commentParams = ref({
  pageNum: 1,
  pageSize: 10,
  articleId: null
})

// 分类映射
const categoryMap = {
  'CONSTITUTION': '体质养生',
  'DIET': '饮食养生',
  'EXERCISE': '运动养生',
  'ACUPOINT': '穴位养生',
  'SEASON': '季节养生',
  'OTHER': '其他'
}

// 是否是作者
const isAuthor = computed(() => {
  return article.value?.authorId === userStore.userInfo?.id
})

// 加载文章详情
const loadDetail = async () => {
  loading.value = true
  try {
    const id = route.params.id
    const res = await getArticleDetail(id)
    if (res.code === 200) {
      article.value = res.data
      commentParams.value.articleId = id

      // 如果用户已登录，查询点赞和收藏状态
      const userId = userStore.userInfo?.id
      if (userId) {
        checkUserStatus(id, userId)
      }

      loadComments()
    }
  } catch (error) {

    message.error('加载文章详情失败')
  } finally {
    loading.value = false
  }
}

// 检查用户点赞和收藏状态
const checkUserStatus = async (articleId, userId) => {
  try {
    // 检查点赞状态
    const likeRes = await checkLikeStatus(articleId, userId)
    if (likeRes.code === 200) {
      isLiked.value = likeRes.data
    }

    // 检查收藏状态
    const favoriteRes = await checkFavoriteStatus(articleId, userId)
    if (favoriteRes.code === 200) {
      isFavorited.value = favoriteRes.data
    }
  } catch (error) {

  }
}

// 加载评论列表
const loadComments = async () => {
  try {
    const res = await getCommentList(commentParams.value)
    if (res.code === 200) {
      commentList.value = res.data.records || []
      commentTotal.value = res.data.total || 0

      // 检查每条评论的点赞状态
      const userId = userStore.userInfo?.id
      if (userId && commentList.value.length > 0) {
        await checkCommentsLikeStatus(userId)
      }
    }
  } catch (error) {

  }
}

// 检查评论列表的点赞状态
const checkCommentsLikeStatus = async (userId) => {
  try {
    // 为每条评论查询点赞状态
    const promises = commentList.value.map(async (comment) => {
      const res = await checkCommentLikeStatus(comment.id, userId)
      if (res.code === 200) {
        comment.isLiked = res.data
      }
    })
    await Promise.all(promises)
  } catch (error) {

  }
}

// 点赞文章
const handleLike = async () => {
  const userId = userStore.userInfo?.id
  if (!userId) {
    message.warning('请先登录')
    return
  }

  try {
    if (isLiked.value) {
      await unlikeArticle(article.value.id, userId)
      article.value.likeCount--
      isLiked.value = false
      message.success('已取消点赞')
    } else {
      await likeArticle(article.value.id, userId)
      article.value.likeCount++
      isLiked.value = true
      message.success('点赞成功')
    }
  } catch (error) {

  }
}

// 收藏文章
const handleFavorite = async () => {
  const userId = userStore.userInfo?.id
  if (!userId) {
    message.warning('请先登录')
    return
  }

  try {
    if (isFavorited.value) {
      await unfavoriteArticle(article.value.id, userId)
      article.value.favoriteCount--
      isFavorited.value = false
      message.success('已取消收藏')
    } else {
      await favoriteArticle(article.value.id, userId)
      article.value.favoriteCount++
      isFavorited.value = true
      message.success('收藏成功')
    }
  } catch (error) {

  }
}

// 编辑文章
const handleEdit = () => {
  router.push(`/patient/community/edit/${article.value.id}`)
}

// 删除文章
const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const userId = userStore.userInfo?.id
    await deleteArticle(article.value.id, userId)
    message.success('删除成功')
    router.back()
  } catch (error) {
    if (error !== 'cancel') {

    }
  }
}

// 发表评论
const handlePublishComment = async () => {
  const userId = userStore.userInfo?.id
  if (!userId) {
    message.warning('请先登录')
    return
  }

  try {
    const data = {
      articleId: article.value.id,
      userId: userId,
      userName: userStore.userInfo.realName || userStore.userInfo.username,
      content: commentContent.value,
      parentId: 0
    }
    await publishComment(data)
    message.success('评论成功')
    commentContent.value = ''
    article.value.commentCount++
    loadComments()
  } catch (error) {

    message.error('发表评论失败')
  }
}

// 点赞评论
const handleLikeComment = async (comment) => {
  const userId = userStore.userInfo?.id
  if (!userId) {
    message.warning('请先登录')
    return
  }

  try {
    if (comment.isLiked) {
      // 取消点赞
      await unlikeComment(comment.id, userId)
      comment.likeCount--
      comment.isLiked = false
      message.success('已取消点赞')
    } else {
      // 点赞
      await likeComment(comment.id, userId)
      comment.likeCount++
      comment.isLiked = true
      message.success('点赞成功')
    }
  } catch (error) {

    message.error(error.message || '操作失败')
  }
}

// 删除评论
const handleDeleteComment = async (commentId) => {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const userId = userStore.userInfo?.id
    await deleteComment(commentId, userId)
    message.success('删除成功')
    article.value.commentCount--
    loadComments()
  } catch (error) {
    if (error !== 'cancel') {

    }
  }
}

// 获取分类标签
const getCategoryLabel = (category) => {
  return categoryMap[category] || category
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

// 返回
const goBack = () => {
  router.back()
}

onMounted(() => {
  loadDetail()
})
</script>

<style scoped>
.article-detail-container {
  padding: 20px;
}

.page-title {
  font-size: 18px;
  font-weight: 500;
}

.detail-card {
  margin-top: 20px;
}

.detail-skeleton {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-skeleton-meta {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

.detail-skeleton-actions {
  display: flex;
  gap: 15px;
}

.detail-skeleton-comments {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.detail-skeleton-comment-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.article-header h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.4;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 14px;
  color: #999;
}

.author,
.stats,
.time {
  display: flex;
  align-items: center;
  gap: 5px;
}

.article-content {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  min-height: 300px;
}

.article-content :deep(img) {
  max-width: 100%;
  height: auto;
}

.article-actions {
  display: flex;
  gap: 10px;
}

.comment-section h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 20px;
}

.comment-form {
  margin-bottom: 30px;
}

.comment-list {
  margin-top: 20px;
}

.comment-item {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.comment-author {
  font-weight: 500;
  color: #333;
}

.comment-time {
  font-size: 12px;
  color: #999;
}

.comment-content {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 10px;
}

.comment-actions {
  display: flex;
  gap: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
