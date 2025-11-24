<template>
  <div class="operation-logs-container">
    <div class="admin-card">
      <div class="card-header">
        <h2>
          <el-icon>
            <Document />
          </el-icon>
          操作日志
        </h2>
        <div class="header-actions">
          <el-button type="success" :icon="Download" @click="handleExport" :loading="exportLoading">
            导出Excel
          </el-button>
          <div class="admin-search">
            <el-input v-model="searchText" placeholder="搜索用户名或操作模块" clearable @input="handleSearch">
              <template #prefix>
                <el-icon>
                  <Search />
                </el-icon>
              </template>
            </el-input>
          </div>
        </div>
      </div>
      <div class="card-body">

        <!-- 筛选条件 -->
        <el-form inline style="margin-bottom: 15px">
          <el-form-item label="操作模块">
            <el-select v-model="queryParams.operationModule" placeholder="全部" clearable style="width: 150px"
              @change="handleFilterChange">
              <el-option label="用户管理" value="USER" />
              <el-option label="医生管理" value="DOCTOR" />
              <el-option label="预约管理" value="APPOINTMENT" />
              <el-option label="系统设置" value="SYSTEM" />
            </el-select>
          </el-form-item>
          <el-form-item label="操作类型">
            <el-select v-model="queryParams.operationType" placeholder="全部" clearable style="width: 150px"
              @change="handleFilterChange">
              <el-option label="新增" value="INSERT" />
              <el-option label="修改" value="UPDATE" />
              <el-option label="删除" value="DELETE" />
              <el-option label="查询" value="SELECT" />
            </el-select>
          </el-form-item>
          <el-form-item label="操作状态">
            <el-select v-model="queryParams.status" placeholder="全部" clearable style="width: 150px"
              @change="handleFilterChange">
              <el-option label="成功" :value="1" />
              <el-option label="失败" :value="0" />
            </el-select>
          </el-form-item>
          <el-form-item label="时间范围">
            <el-date-picker v-model="dateRange" type="datetimerange" range-separator="至" start-placeholder="开始时间"
              end-placeholder="结束时间" @change="handleDateChange" />
          </el-form-item>
        </el-form>

        <!-- 日志列表 -->
        <el-table :data="logs" v-loading="loading" stripe>
          <el-table-column type="index" label="序号" width="70"
            :index="(index) => (queryParams.page - 1) * queryParams.pageSize + index + 1" />
          <el-table-column prop="username" label="操作用户" width="120" />
          <el-table-column prop="operationModule" label="操作模块" width="120">
            <template #default="{ row }">
              <el-tag size="small">{{ row.operationModule }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="operationType" label="操作类型" width="100">
            <template #default="{ row }">
              <el-tag size="small" :type="getOperationType(row.operationType)">
                {{ row.operationType }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="requestMethod" label="请求方法" width="100" />
          <el-table-column prop="requestUrl" label="请求URL" show-overflow-tooltip width="200" />
          <el-table-column prop="ipAddress" label="IP地址" width="130" />
          <el-table-column prop="executionTime" label="耗时(ms)" width="100">
            <template #default="{ row }">
              <span :style="{ color: row.executionTime > 1000 ? '#f56c6c' : '#67c23a' }">
                {{ row.executionTime }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="80">
            <template #default="{ row }">
              <el-tag :type="row.status === 1 ? 'success' : 'danger'" size="small">
                {{ row.status === 1 ? '成功' : '失败' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="createdAt" label="操作时间" width="160" />
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="viewDetail(row)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <AdminPagination v-model:current-page="queryParams.page" v-model:page-size="queryParams.pageSize" :total="total"
          @size-change="handlePageSizeChange" @current-change="handlePageChange" />
      </div>

      <!-- 日志详情弹窗 -->
      <el-dialog v-model="detailVisible" title="日志详情" width="700px">
        <el-descriptions :column="2" border v-if="selectedLog">
          <el-descriptions-item label="日志ID">{{ selectedLog.id }}</el-descriptions-item>
          <el-descriptions-item label="操作用户">{{ selectedLog.username }}</el-descriptions-item>
          <el-descriptions-item label="操作模块">{{ selectedLog.operationModule }}</el-descriptions-item>
          <el-descriptions-item label="操作类型">{{ selectedLog.operationType }}</el-descriptions-item>
          <el-descriptions-item label="请求方法">{{ selectedLog.requestMethod }}</el-descriptions-item>
          <el-descriptions-item label="IP地址">{{ selectedLog.ipAddress }}</el-descriptions-item>
          <el-descriptions-item label="请求URL" :span="2">{{ selectedLog.requestUrl }}</el-descriptions-item>
          <el-descriptions-item label="请求参数" :span="2">
            <el-input type="textarea" :value="selectedLog.requestParams" :rows="3" readonly />
          </el-descriptions-item>
          <el-descriptions-item label="响应数据" :span="2" v-if="selectedLog.status === 1">
            <el-input type="textarea" :value="selectedLog.responseData" :rows="3" readonly />
          </el-descriptions-item>
          <el-descriptions-item label="错误信息" :span="2" v-if="selectedLog.status === 0">
            <el-input type="textarea" :value="selectedLog.errorMsg" :rows="3" readonly />
          </el-descriptions-item>
          <el-descriptions-item label="执行时长">{{ selectedLog.executionTime }} ms</el-descriptions-item>
          <el-descriptions-item label="操作状态">
            <el-tag :type="selectedLog.status === 1 ? 'success' : 'danger'">
              {{ selectedLog.status === 1 ? '成功' : '失败' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="操作时间" :span="2">
            {{ selectedLog.createdAt }}
          </el-descriptions-item>
        </el-descriptions>
        <template #footer>
          <el-button @click="detailVisible = false">关闭</el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, onMounted } from 'vue'
import dayjs from 'dayjs'

import { Search, Download } from '@element-plus/icons-vue'
import { getOperationLogs, exportOperationLogs } from '@/api/system'
import AdminPagination from '@/components/AdminPagination.vue'

const loading = ref(false)
const exportLoading = ref(false)
const detailVisible = ref(false)
const searchText = ref('')
const dateRange = ref([])
const selectedLog = ref(null)

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10,
  operationModule: '',
  operationType: '',
  status: null
})

// 数据
const logs = ref([])
const total = ref(0)

// 这些统计数据已移除，因为它们不属于操作日志页面

// 加载日志列表
const buildQueryParams = () => {
  const params = {
    page: queryParams.page,
    pageSize: queryParams.pageSize,
    operationModule: queryParams.operationModule || undefined,
    operationType: queryParams.operationType || undefined,
    status: queryParams.status !== null ? queryParams.status : undefined,
    keyword: searchText.value || undefined
  }

  if (dateRange.value && dateRange.value.length === 2) {
    params.startDate = dayjs(dateRange.value[0]).format('YYYY-MM-DD HH:mm:ss')
    params.endDate = dayjs(dateRange.value[1]).format('YYYY-MM-DD HH:mm:ss')
  }

  return params
}

const loadLogs = async () => {
  loading.value = true
  try {
    const params = buildQueryParams()
    const res = await getOperationLogs(params)

    if (res.code === 200) {
      logs.value = res.data?.records || []
      const apiTotal = Number(res.data?.total)
      total.value = Number.isFinite(apiTotal) && apiTotal > 0
        ? apiTotal
        : (Array.isArray(res.data?.records) ? res.data.records.length : 0)
    } else {

      message.error(res.message || '获取操作日志失败')
    }
  } catch (error) {

    message.error(error.response?.data?.message || '加载日志列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  queryParams.page = 1
  loadLogs()
}

// 筛选变化时重置页码
const handleFilterChange = () => {
  queryParams.page = 1
  loadLogs()
}

const handleDateChange = () => {
  queryParams.page = 1
  loadLogs()
}

// 分页事件
const handlePageChange = (page) => {
  queryParams.page = page
  loadLogs()
}

const handlePageSizeChange = (size) => {
  queryParams.pageSize = size
  queryParams.page = 1
  loadLogs()
}

// 查看详情
const viewDetail = (row) => {
  selectedLog.value = row
  detailVisible.value = true
}

// 获取操作类型颜色
const getOperationType = (type) => {
  const typeMap = {
    'INSERT': 'success',
    'UPDATE': 'warning',
    'DELETE': 'danger',
    'SELECT': 'info'
  }
  return typeMap[type] || ''
}

// 导出操作日志
const handleExport = async () => {
  try {
    exportLoading.value = true

    const exportParams = buildQueryParams()
    const res = await exportOperationLogs(exportParams)

    // 创建下载链接
    const blob = new Blob([res], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url

    // 生成文件名（包含时间戳）
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-')
    link.download = `操作日志_${timestamp}.xlsx`

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    message.success('导出成功')
  } catch (error) {

    message.error('导出失败，请稍后重试')
  } finally {
    exportLoading.value = false
  }
}

onMounted(() => {
  loadLogs()
})
</script>

<style scoped lang="scss">
.pagination {
  margin-top: 15px;
  display: flex;
  justify-content: center;
}
</style>

<style scoped lang="scss">
.operation-logs-container {
  max-width: 1600px;
  margin: 0 auto;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
      font-size: 20px;
    }
  }
}
</style>

<style scoped lang="scss">
@use '@/styles/admin-variables.scss' as *;
@use '@/styles/admin-common.scss' as *;

.operation-logs-container {
  max-width: 1400px;
  margin: 0 auto;
}
</style>
