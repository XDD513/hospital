<template>
  <div class="article-list-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>养生知识社区</h2>
      <p>分享养生知识，交流健康经验</p>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card">
      <el-form :inline="true">
        <el-form-item label="关键词">
          <el-input v-model="searchKeyword" placeholder="请输入文章标题或内容" clearable @clear="handleSearch" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="selectedCategory" placeholder="请选择分类" clearable @change="handleSearch"
            style="width: 180px;">
            <el-option label="体质养生" value="CONSTITUTION" />
            <el-option label="饮食养生" value="DIET" />
            <el-option label="运动养生" value="EXERCISE" />
            <el-option label="穴位养生" value="ACUPOINT" />
            <el-option label="季节养生" value="SEASON" />
            <el-option label="其他" value="OTHER" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select 
            v-model="selectedTags" 
            placeholder="请选择标签" 
            clearable 
            multiple 
            collapse-tags
            @change="handleSearch"
            style="width: 300px;"
          >
            <el-option 
              v-for="tag in availableTags" 
              :key="tag" 
              :label="tag" 
              :value="tag" 
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon>
              <Search />
            </el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" @click="goToPublish">
            <el-icon>
              <Edit />
            </el-icon>
            发布文章
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 推荐文章 -->
    <el-card class="recommended-card" v-if="recommendedArticles.length > 0">
      <template #header>
        <div class="card-header">
          <span>推荐文章</span>
        </div>
      </template>
      <el-carousel height="200px" indicator-position="outside">
        <el-carousel-item v-for="article in recommendedArticles" :key="article.id">
          <div class="carousel-item" @click="viewDetail(article.id)">
            <img :src="article.coverImage || '/default-article.png'" :alt="article.title" />
            <div class="carousel-content">
              <h3>{{ article.title }}</h3>
              <p>{{ article.summary }}</p>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </el-card>

    <!-- 文章列表 -->
    <el-card class="list-card">
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="最新" name="latest"></el-tab-pane>
        <el-tab-pane label="热门" name="popular"></el-tab-pane>
      </el-tabs>

      <div class="article-list">
        <template v-if="listLoading">
          <div
            v-for="n in articleSkeletonCount"
            :key="`article-skeleton-${n}`"
            class="article-item"
          >
            <el-skeleton animated>
              <template #template>
                <div class="article-skeleton">
                  <div class="article-skeleton-cover">
                    <el-skeleton-item variant="image" style="width: 100%; height: 100%;" />
                  </div>
                  <div class="article-skeleton-content">
                    <el-skeleton-item variant="text" style="width: 60%;" />
                    <el-skeleton-item variant="text" />
                    <el-skeleton-item variant="text" />
                    <div class="article-skeleton-meta">
                      <el-skeleton-item variant="text" style="width: 120px;" />
                      <el-skeleton-item variant="text" style="width: 180px;" />
                    </div>
                  </div>
                </div>
              </template>
            </el-skeleton>
          </div>
        </template>

        <template v-else>
          <div v-for="article in articleList" :key="article.id" class="article-item" @click="viewDetail(article.id)">
            <div class="article-cover" v-if="article.coverImage">
              <img :src="article.coverImage" :alt="article.title" />
            </div>
            <div class="article-content">
              <h3>{{ article.title }}</h3>
              <p class="summary">{{ article.summary }}</p>
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
                <span class="stats">
                  <el-icon>
                    <View />
                  </el-icon>
                  {{ article.viewCount || 0 }}
                  <el-icon>
                    <Star />
                  </el-icon>
                  {{ article.likeCount || 0 }}
                  <el-icon>
                    <ChatDotRound />
                  </el-icon>
                  {{ article.commentCount || 0 }}
                </span>
                <span class="time">{{ formatTime(article.publishTime) }}</span>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- 空状态 -->
      <EmptyState
        v-if="articleList.length === 0 && !listLoading"
        description="暂无文章"
        tip="试试调整关键词或标签筛选"
      />

      <!-- 分页 -->
      <div class="pagination-container" v-if="total > 0">
        <el-pagination v-model:current-page="queryParams.pageNum" v-model:page-size="queryParams.pageSize"
          :total="total" :page-sizes="[10, 20, 30, 50]" layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadArticles" @current-change="loadArticles" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { Search, Edit, User, View, Star, ChatDotRound } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import {
  getArticleList,
  searchArticles,
  getRecommendedArticles,
  getPopularArticles,
  getAllTags
} from '@/api/article'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()

// 数据
const articleList = ref([])
const recommendedArticles = ref([])
const total = ref(0)
const searchKeyword = ref('')
const selectedCategory = ref('')
const selectedTags = ref([])
const availableTags = ref([])
const activeTab = ref('latest')
const listLoading = ref(false)
const articleSkeletonCount = 4

// 查询参数
const queryParams = ref({
  pageNum: 1,
  pageSize: 10,
  category: '',
  tags: '',
  isRecommend: null
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

// 加载所有标签
const loadAvailableTags = async () => {
  try {
    const res = await getAllTags()
    if (res.code === 200 && res.data) {
      availableTags.value = res.data
    }
  } catch (error) {
    console.error('加载标签列表失败', error)
  }
}

// 加载文章列表
const loadArticles = async () => {
  listLoading.value = true
  try {
    const params = {
      ...queryParams.value,
      category: selectedCategory.value || undefined,
      tags: selectedTags.value.length > 0 ? selectedTags.value.join(',') : undefined
    }
    const res = await getArticleList(params)
    if (res.code === 200) {
      articleList.value = res.data.records || []
      total.value = Number(res.data.total) || 0
    }
  } catch (error) {
    message.error('加载文章列表失败')
  } finally {
    listLoading.value = false
  }
}

// 加载推荐文章
const loadRecommendedArticles = async () => {
  try {
    const res = await getRecommendedArticles(5)
    if (res.code === 200) {
      recommendedArticles.value = res.data || []
    }
  } catch (error) {

  }
}

// 加载热门文章
const loadPopularArticles = async () => {
  listLoading.value = true
  try {
    const res = await getPopularArticles(10)
    if (res.code === 200) {
      articleList.value = res.data || []
      total.value = res.data.length
    }
  } catch (error) {

    message.error('加载热门文章失败')
  } finally {
    listLoading.value = false
  }
}

// 搜索处理
const handleSearch = async () => {
  queryParams.value.pageNum = 1
  if (searchKeyword.value) {
    try {
      listLoading.value = true
      const params = {
        keyword: searchKeyword.value,
        pageNum: queryParams.value.pageNum,
        pageSize: queryParams.value.pageSize
      }
      const res = await searchArticles(params)
      if (res.code === 200) {
        articleList.value = res.data.records || []
        total.value = Number(res.data.total) || 0
      }
    } catch (error) {
      message.error('搜索文章失败')
    } finally {
      listLoading.value = false
    }
  } else {
    loadArticles()
  }
}

// 重置筛选
const handleReset = () => {
  searchKeyword.value = ''
  selectedCategory.value = ''
  selectedTags.value = []
  handleSearch()
}

// 标签页切换
const handleTabChange = (tab) => {
  if (tab === 'popular') {
    loadPopularArticles()
  } else {
    loadArticles()
  }
}

// 查看详情
const viewDetail = (id) => {
  router.push(`/patient/community/article/${id}`)
}

// 发布文章
const goToPublish = () => {
  router.push('/patient/community/publish')
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
  loadAvailableTags()
  loadRecommendedArticles()
  loadArticles()
})
</script>

<style scoped>
.article-list-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
  text-align: center;
}

.page-header h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 14px;
  color: #666;
}

.search-card {
  margin-bottom: 20px;
}

.recommended-card {
  margin-bottom: 20px;
}

.carousel-item {
  width: 100%;
  height: 100%;
  position: relative;
  cursor: pointer;
  overflow: hidden;
}

.carousel-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  color: white;
}

.carousel-content h3 {
  font-size: 20px;
  margin-bottom: 8px;
}

.carousel-content p {
  font-size: 14px;
  opacity: 0.9;
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
}

.article-item:hover {
  background: #f9f9f9;
}

.article-skeleton {
  display: flex;
  gap: 20px;
}

.article-skeleton-cover {
  width: 200px;
  height: 150px;
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
}

.article-skeleton-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.article-skeleton-meta {
  display: flex;
  gap: 15px;
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
}

.author,
.stats,
.time {
  display: flex;
  align-items: center;
  gap: 5px;
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
}
</style>
