<template>
  <div class="my-articles-container">
    <div class="page-header">
      <h2>我的文章</h2>
      <el-button type="primary" @click="goToPublish">
        <el-icon><Edit /></el-icon>
        发布新文章
      </el-button>
    </div>

    <el-card class="list-card">
      <el-table :data="articleList" v-loading="loading">
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="category" label="分类" width="120">
          <template #default="{ row }">
            <el-tag size="small">{{ getCategoryLabel(row.category) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="viewCount" label="浏览" width="80" />
        <el-table-column prop="likeCount" label="点赞" width="80" />
        <el-table-column prop="commentCount" label="评论" width="80" />
        <el-table-column prop="publishTime" label="发布时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.publishTime) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetail(row.id)">查看</el-button>
            <el-button size="small" type="primary" @click="handleEdit(row.id)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态 -->
      <el-empty v-if="articleList.length === 0 && !loading" description="暂无文章" />

      <!-- 分页 -->
      <div class="pagination-container" v-if="total > 0">
        <el-pagination
          v-model:current-page="queryParams.pageNum"
          v-model:page-size="queryParams.pageSize"
          :total="total"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadArticles"
          @current-change="loadArticles"
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
import { Edit } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import dayjs from 'dayjs'
import { getMyArticles, deleteArticle } from '@/api/article'

const router = useRouter()
const userStore = useUserStore()

const articleList = ref([])
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

// 加载文章列表
const loadArticles = async () => {
  const userId = userStore.userInfo?.id
  if (!userId) {
    message.warning('请先登录')
    return
  }

  loading.value = true
  try {
    queryParams.value.userId = userId
    const res = await getMyArticles(queryParams.value)
    if (res.code === 200) {
      articleList.value = res.data.records || []
      total.value = Number(res.data.total) || 0
    }
  } catch (error) {

    message.error('加载文章列表失败')
  } finally {
    loading.value = false
  }
}

// 查看详情
const viewDetail = (id) => {
  router.push(`/patient/community/article/${id}`)
}

// 编辑文章
const handleEdit = (id) => {
  router.push(`/patient/community/edit/${id}`)
}

// 删除文章
const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const userId = userStore.userInfo?.id
    await deleteArticle(id, userId)
    message.success('删除成功')
    loadArticles()
  } catch (error) {
    if (error !== 'cancel') {

      message.error('删除文章失败')
    }
  }
}

// 发布新文章
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
  loadArticles()
})
</script>

<style scoped>
.my-articles-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>

