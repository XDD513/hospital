<template>
  <div class="my-favorites-container">
    <div class="page-header">
      <h2>我的收藏</h2>
    </div>

    <el-card class="list-card">
      <div class="article-list">
        <div
          v-for="favorite in favoriteList"
          :key="favorite.id"
          class="article-item"
          @click="viewDetail(favorite.articleId)"
        >
          <div class="article-cover" v-if="favorite.article?.coverImage">
            <img :src="favorite.article.coverImage" :alt="favorite.article.title" />
          </div>
          <div class="article-content">
            <h3>{{ favorite.article?.title }}</h3>
            <p class="summary">{{ favorite.article?.summary }}</p>
            <div class="article-meta">
              <span class="author">
                <el-icon><User /></el-icon>
                {{ favorite.article?.authorName }}
              </span>
              <span class="category">
                <el-tag size="small">{{ getCategoryLabel(favorite.article?.category) }}</el-tag>
              </span>
              <span class="stats">
                <el-icon><View /></el-icon>
                {{ favorite.article?.viewCount || 0 }}
                <el-icon><Star /></el-icon>
                {{ favorite.article?.likeCount || 0 }}
              </span>
              <span class="time">收藏于：{{ formatTime(favorite.createdAt) }}</span>
            </div>
            <div class="remark" v-if="favorite.remark">
              <el-icon><Document /></el-icon>
              备注：{{ favorite.remark }}
            </div>
          </div>
          <div class="article-actions">
            <el-button
              type="danger"
              size="small"
              @click.stop="handleUnfavorite(favorite.articleId)"
            >
              取消收藏
            </el-button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <el-empty v-if="favoriteList.length === 0 && !loading" description="暂无收藏" />

      <!-- 分页 -->
      <div class="pagination-container" v-if="total > 0">
        <el-pagination
          v-model:current-page="queryParams.pageNum"
          v-model:page-size="queryParams.pageSize"
          :total="total"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadFavorites"
          @current-change="loadFavorites"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { User, View, Star, Document } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import dayjs from 'dayjs'
import { getFavoriteArticles, unfavoriteArticle } from '@/api/article'

const router = useRouter()
const userStore = useUserStore()

const favoriteList = ref([])
const total = ref(0)
const loading = ref(false)

const queryParams = ref({
  pageNum: 1,
  pageSize: 10,
  userId: null
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

// 加载收藏列表
const loadFavorites = async () => {
  const userId = userStore.userInfo?.id
  if (!userId) {
    message.warning('请先登录')
    return
  }

  loading.value = true
  try {
    queryParams.value.userId = userId
    const res = await getFavoriteArticles(queryParams.value)
    if (res.code === 200) {
      const records = res.data.records || []
      // 将扁平化的数据转换为嵌套结构，以匹配前端模板
      favoriteList.value = records.map(favorite => ({
        ...favorite,
        article: {
          id: favorite.articleId,
          title: favorite.title,
          summary: favorite.summary,
          coverImage: favorite.coverImage,
          authorName: favorite.authorName,
          category: favorite.category,
          viewCount: favorite.viewCount || 0,
          likeCount: favorite.likeCount || 0
        }
      }))
      total.value = Number(res.data.total) || 0
    }
  } catch (error) {

    message.error('加载收藏列表失败')
  } finally {
    loading.value = false
  }
}

// 查看详情
const viewDetail = (articleId) => {
  router.push(`/patient/community/article/${articleId}`)
}

// 取消收藏
const handleUnfavorite = async (articleId) => {
  try {
    await ElMessageBox.confirm('确定要取消收藏吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const userId = userStore.userInfo?.id
    await unfavoriteArticle(articleId, userId)
    message.success('已取消收藏')
    loadFavorites()
  } catch (error) {
    if (error !== 'cancel') {

      message.error('取消收藏失败')
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

onMounted(() => {
  loadFavorites()
})
</script>

<style scoped>
.my-favorites-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.list-card {
  margin-bottom: 20px;
}

.article-list {
  margin-top: 20px;
}

.article-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.article-item:hover {
  background: #f9f9f9;
}

.article-cover {
  width: 200px;
  height: 150px;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: 8px;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.article-content h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 10px;
}

.summary {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
  flex: 1;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 13px;
  color: #999;
  margin-bottom: 10px;
}

.author,
.stats,
.time {
  display: flex;
  align-items: center;
  gap: 5px;
}

.remark {
  font-size: 13px;
  color: #409eff;
  display: flex;
  align-items: center;
  gap: 5px;
}

.article-actions {
  display: flex;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .article-item {
    flex-direction: column;
  }

  .article-cover {
    width: 100%;
  }

  .article-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>

