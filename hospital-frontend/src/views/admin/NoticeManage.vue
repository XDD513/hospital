<template>
  <div class="notice-manage-container">
    <div class="admin-card">
      <div class="card-header">
        <h2>
          <el-icon>
            <Bell />
          </el-icon>
          公告管理
        </h2>
        <div class="header-actions">
          <div class="admin-search">
            <el-input v-model="searchText" placeholder="搜索公告标题" clearable @input="handleSearch">
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
            发布公告
          </el-button>
        </div>
      </div>
      <div class="card-body">
        <!-- 筛选条件 -->
        <div class="admin-filter">
          <el-form inline>
            <el-form-item label="状态">
              <el-select v-model="queryParams.status" placeholder="全部" clearable @change="loadNotices">
                <el-option label="已发布" value="PUBLISHED" />
                <el-option label="草稿" value="DRAFT" />
                <el-option label="已下架" value="OFFLINE" />
              </el-select>
            </el-form-item>
          </el-form>
        </div>

        <!-- 公告列表 -->
        <el-table :data="notices" v-loading="loading" class="admin-table" stripe>
          <el-table-column type="index" label="序号" width="70" align="center" />
          <el-table-column prop="title" label="公告标题" min-width="200" show-overflow-tooltip align="center">
            <template #default="{ row }">
              <span style="text-align: center;">{{ row.title || '未设置' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="type" label="公告类型" width="100" align="center" />
          <el-table-column prop="status" label="状态" width="100" align="center">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="publishTime" label="发布时间" width="160" align="center" />
          <el-table-column prop="expireTime" label="过期时间" width="160" align="center" />
          <el-table-column label="操作" width="200" fixed="right" align="center">
            <template #default="{ row }">
              <el-button size="small" @click="viewNotice(row)">查看</el-button>
              <el-button size="small" @click="editNotice(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteNotice(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="admin-pagination" v-if="total > 0">
          <el-pagination v-model:current-page="queryParams.page" v-model:page-size="queryParams.pageSize" :total="total"
            :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next" @size-change="loadNotices"
            @current-change="loadNotices" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Bell, Search, Refresh, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const searchText = ref('')
const notices = ref([])
const total = ref(0)

const queryParams = reactive({
  page: 1,
  pageSize: 10,
  status: ''
})

const loadNotices = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取公告列表
    // const res = await getNotices(queryParams)
    // notices.value = res.data?.records || []
    // total.value = res.data?.total || 0
    notices.value = []
    total.value = 0
  } catch (error) {
    console.error('加载公告列表失败:', error)
    ElMessage.error('加载公告列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  queryParams.page = 1
  loadNotices()
}

const handleRefresh = () => {
  loadNotices()
}

const showAddDialog = () => {
  // TODO: 显示添加公告对话框
}

const viewNotice = (row) => {
  // TODO: 查看公告
}

const editNotice = (row) => {
  // TODO: 编辑公告
}

const deleteNotice = (row) => {
  // TODO: 删除公告
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
  loadNotices()
})
</script>

<style scoped lang="scss">
@use '@/styles/admin-variables.scss' as *;
@use '@/styles/admin-common.scss' as *;

.notice-manage-container {
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

