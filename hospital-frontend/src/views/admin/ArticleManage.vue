<template>
  <div class="article-manage-container">
    <div class="admin-card">
      <div class="card-header">
        <h2>
          <el-icon>
            <ChatLineRound />
          </el-icon>
          资讯管理
        </h2>
        <div class="header-actions">
          <div class="admin-search">
            <el-input v-model="searchText" placeholder="搜索文章标题" clearable @input="handleSearch">
              <template #prefix>
                <el-icon>
                  <Search />
                </el-icon>
              </template>
            </el-input>
          </div>
          <el-button @click="handleRefresh">
            <el-icon>
              <Refresh />
            </el-icon>
            刷新
          </el-button>
          <el-button type="primary" @click="showAddDialog">
            <el-icon>
              <Plus />
            </el-icon>
            发布资讯
          </el-button>
        </div>
      </div>
      <div class="card-body">
        <!-- 筛选条件 -->
        <div class="admin-filter">
          <el-form inline>
            <el-form-item label="状态">
              <el-select v-model="queryParams.status" placeholder="全部" clearable @change="loadArticles">
                <el-option label="已发布" value="PUBLISHED" />
                <el-option label="草稿" value="DRAFT" />
                <el-option label="已下架" value="OFFLINE" />
              </el-select>
            </el-form-item>
          </el-form>
        </div>

        <!-- 文章列表 -->
        <el-table :data="articles" v-loading="loading" class="admin-table" stripe>
          <el-table-column type="index" label="序号" width="70" align="center" />
          <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip align="center">
            <template #default="{ row }">
              <span style="text-align: center;">{{ row.title || '未设置' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="author" label="作者" width="100" align="center" />
          <el-table-column prop="category" label="分类" width="100" align="center" />
          <el-table-column prop="status" label="状态" width="100" align="center">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="publishTime" label="发布时间" width="160" align="center" />
          <el-table-column label="操作" width="200" fixed="right" align="center">
            <template #default="{ row }">
              <el-button size="small" @click="viewArticle(row)">查看</el-button>
              <el-button size="small" @click="editArticle(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteArticle(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="admin-pagination" v-if="total > 0">
          <el-pagination v-model:current-page="queryParams.page" v-model:page-size="queryParams.pageSize" :total="total"
            :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next" @size-change="loadArticles"
            @current-change="loadArticles" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ChatLineRound, Search, Refresh, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const searchText = ref('')
const articles = ref([])
const total = ref(0)

const queryParams = reactive({
  page: 1,
  pageSize: 10,
  status: ''
})

const loadArticles = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取文章列表
    // const res = await getArticles(queryParams)
    // articles.value = res.data?.records || []
    // total.value = res.data?.total || 0
    articles.value = []
    total.value = 0
  } catch (error) {
    console.error('加载文章列表失败:', error)
    ElMessage.error('加载文章列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  queryParams.page = 1
  loadArticles()
}

const handleRefresh = () => {
  loadArticles()
}

const showAddDialog = () => {
  // TODO: 显示添加文章对话框
}

const viewArticle = (row) => {
  // TODO: 查看文章
}

const editArticle = (row) => {
  // TODO: 编辑文章
}

const deleteArticle = (row) => {
  // TODO: 删除文章
}

const getStatusType = (status) => {
  const map = {
    'PUBLISHED': 'success',
    'DRAFT': 'warning',
    'OFFLINE': 'info'
  }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = {
    'PUBLISHED': '已发布',
    'DRAFT': '草稿',
    'OFFLINE': '已下架'
  }
  return map[status] || '未知'
}

onMounted(() => {
  loadArticles()
})
</script>

<style scoped lang="scss">
@use '@/styles/admin-variables.scss' as *;
@use '@/styles/admin-common.scss' as *;

.article-manage-container {
  // 使用全局admin样式
  
  // 确保表格所有单元格内容居中
  :deep(.el-table) {
    .el-table__cell {
      text-align: center;
      
      .cell {
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
      }
    }
    
    // 表头也居中
    .el-table__header-wrapper {
      .el-table__header {
        th {
          text-align: center;
          
          .cell {
            text-align: center;
            justify-content: center;
          }
        }
      }
    }
  }
}
</style>

