<template>
  <div class="feedback-manage-container">
    <div class="admin-card">
      <div class="card-header">
        <h2>
          <el-icon>
            <ChatLineRound />
          </el-icon>
          反馈管理
        </h2>
        <div class="header-actions">
          <div class="admin-search">
            <el-input v-model="searchText" placeholder="搜索反馈内容" clearable @input="handleSearch">
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
        </div>
      </div>
      <div class="card-body">
        <!-- 筛选条件 -->
        <div class="admin-filter">
          <el-form inline>
            <el-form-item label="状态">
              <el-select v-model="queryParams.status" placeholder="全部" clearable @change="loadFeedbacks">
                <el-option label="待处理" value="PENDING" />
                <el-option label="已处理" value="PROCESSED" />
                <el-option label="已关闭" value="CLOSED" />
              </el-select>
            </el-form-item>
          </el-form>
        </div>

        <!-- 反馈列表 -->
        <el-table :data="feedbacks" v-loading="loading" class="admin-table" stripe>
          <el-table-column type="index" label="序号" width="70" align="center" />
          <el-table-column prop="userName" label="反馈人" width="100" align="center" />
          <el-table-column prop="content" label="反馈内容" min-width="200" show-overflow-tooltip align="center">
            <template #default="{ row }">
              <span style="text-align: center;">{{ row.content || '暂无内容' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="type" label="反馈类型" width="100" align="center" />
          <el-table-column prop="status" label="状态" width="100" align="center">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="createTime" label="反馈时间" width="160" align="center" />
          <el-table-column label="操作" width="200" fixed="right" align="center">
            <template #default="{ row }">
              <el-button size="small" @click="viewFeedback(row)">查看</el-button>
              <el-button size="small" type="primary" @click="handleFeedback(row)">处理</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="admin-pagination" v-if="total > 0">
          <el-pagination v-model:current-page="queryParams.page" v-model:page-size="queryParams.pageSize" :total="total"
            :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next" @size-change="loadFeedbacks"
            @current-change="loadFeedbacks" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ChatLineRound, Search, Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const searchText = ref('')
const feedbacks = ref([])
const total = ref(0)

const queryParams = reactive({
  page: 1,
  pageSize: 10,
  status: ''
})

const loadFeedbacks = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取反馈列表
    // const res = await getFeedbacks(queryParams)
    // feedbacks.value = res.data?.records || []
    // total.value = res.data?.total || 0
    feedbacks.value = []
    total.value = 0
  } catch (error) {
    console.error('加载反馈列表失败:', error)
    ElMessage.error('加载反馈列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  queryParams.page = 1
  loadFeedbacks()
}

const handleRefresh = () => {
  loadFeedbacks()
}

const viewFeedback = (row) => {
  // TODO: 查看反馈详情
}

const handleFeedback = (row) => {
  // TODO: 处理反馈
}

const getStatusType = (status) => {
  const map = {
    'PENDING': 'warning',
    'PROCESSED': 'success',
    'CLOSED': 'info'
  }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = {
    'PENDING': '待处理',
    'PROCESSED': '已处理',
    'CLOSED': '已关闭'
  }
  return map[status] || '未知'
}

onMounted(() => {
  loadFeedbacks()
})
</script>

<style scoped lang="scss">
@use '@/styles/admin-variables.scss' as *;
@use '@/styles/admin-common.scss' as *;

.feedback-manage-container {
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

