<template>
  <div class="admin-dashboard">
    <!-- 欢迎横幅 -->
    <el-card class="welcome-card" shadow="never">
      <div class="welcome-content">
        <div>
          <h1>管理后台</h1>
          <p>{{ currentDate }} | 系统运行正常</p>
        </div>
        <el-icon :size="100" color="#e6a23c"><DataAnalysis /></el-icon>
      </div>
    </el-card>

    <!-- 核心数据统计 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card orange" shadow="hover">
          <el-statistic title="科室总数" :value="stats.departments">
            <template #prefix>
              <el-icon><OfficeBuilding /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card green" shadow="hover">
          <el-statistic title="医生总数" :value="stats.doctors">
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card blue" shadow="hover">
          <el-statistic title="用户总数" :value="stats.users">
            <template #prefix>
              <el-icon><UserFilled /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card red" shadow="hover">
          <el-statistic title="今日预约" :value="stats.todayAppointments">
            <template #prefix>
              <el-icon><Calendar /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <!-- 最近预约 -->
      <el-col :xs="24" :md="12">
        <el-card shadow="never">
          <template #header>
            <h3>最近预约</h3>
          </template>
          <el-table :data="recentAppointments" size="small">
            <el-table-column prop="patientName" label="患者" width="100" />
            <el-table-column prop="doctorName" label="医生" width="100" />
            <el-table-column prop="deptName" label="科室" width="100" />
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag size="small" :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 系统信息 -->
      <el-col :xs="24" :md="12">
        <el-card shadow="never">
          <template #header>
            <h3>系统信息</h3>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="系统版本">v1.0.0</el-descriptions-item>
            <el-descriptions-item label="数据库">MySQL 8.0</el-descriptions-item>
            <el-descriptions-item label="后端框架">Spring Boot 2.7.18</el-descriptions-item>
            <el-descriptions-item label="前端框架">Vue 3 + Element Plus</el-descriptions-item>
            <el-descriptions-item label="系统状态">
              <el-tag type="success">运行中</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { getAdminStats, getRecentAppointments } from '@/api/statistics'
import dayjs from 'dayjs'

const router = useRouter()
const userStore = useUserStore()

const currentDate = computed(() => {
  const weekDays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  const dayOfWeek = dayjs().day()
  return dayjs().format('YYYY年MM月DD日') + ' ' + weekDays[dayOfWeek]
})

// 统计数据
const stats = ref({
  departments: 0,
  doctors: 0,
  users: 0,
  todayAppointments: 0
})

// 最近预约
const recentAppointments = ref([])

// 加载统计数据
const loadStats = async () => {
  try {
    const res = await getAdminStats()
    if (res.code === 200) {
      stats.value = res.data
    }
  } catch (error) {
    console.error('加载统计失败:', error)
    ElMessage.error('加载统计失败')
  }
}

// 加载最近预约
const loadRecentAppointments = async () => {
  try {
    const res = await getRecentAppointments()
    if (res.code === 200) {
      recentAppointments.value = res.data || []
    }
  } catch (error) {
    console.error('加载最近预约失败:', error)
    ElMessage.error('加载最近预约失败')
  }
}

const getStatusType = (status) => {
  const map = {
    '待就诊': 'warning',
    '已完成': 'success',
    '已取消': 'info'
  }
  return map[status] || 'info'
}

onMounted(() => {
  loadStats()
  loadRecentAppointments()
})
</script>

<style scoped lang="scss">
.admin-dashboard {
  max-width: 1400px;
  margin: 0 auto;

  .welcome-card {
    margin-bottom: 20px;

    .welcome-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px;

      h1 {
        font-size: 32px;
        color: #333;
        margin-bottom: 10px;
      }

      p {
        color: #666;
        font-size: 16px;
      }
    }
  }

  .stats-row {
    margin-bottom: 20px;
  }

  .stat-card {
    margin-bottom: 20px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    &.orange :deep(.el-icon) { color: #e6a23c; }
    &.green :deep(.el-icon) { color: #67c23a; }
    &.blue :deep(.el-icon) { color: #409eff; }
    &.red :deep(.el-icon) { color: #f56c6c; }
  }

  h3 {
    margin: 0;
    font-size: 16px;
  }
}
</style>

