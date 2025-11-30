<template>
  <div class="appointment-manage-container">
    <div class="admin-card">
      <div class="card-header">
        <h2>
          <el-icon>
            <Tickets />
          </el-icon>
          就诊记录
        </h2>
        <div class="header-actions">
          <div class="admin-search">
            <el-input v-model="searchText" placeholder="搜索订单号或患者姓名" clearable @input="handleSearch">
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
            <el-form-item label="预约状态">
              <el-select v-model="queryParams.status" placeholder="全部" clearable style="width: 150px"
                @change="loadAppointments">
                <el-option label="已确认" value="CONFIRMED" />
                <el-option label="就诊中" value="IN_PROGRESS" />
                <el-option label="已完成" value="COMPLETED" />
                <el-option label="已取消" value="CANCELLED" />
                <el-option label="爽约" value="NO_SHOW" />
              </el-select>
            </el-form-item>
            <el-form-item label="日期范围">
              <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期"
                end-placeholder="结束日期" @change="loadAppointments" />
            </el-form-item>
          </el-form>

          <!-- 预约列表 -->
          <el-table :data="appointments" v-loading="loading" class="admin-table" stripe>
            <el-table-column type="index" label="序号" width="60" align="center" fixed="left"/>
            <el-table-column prop="id" label="订单号" width="160" align="center">
              <template #default="{ row }">
                <span style="font-weight: 500; color: #303133;">{{ row.id }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="patientName" label="患者姓名" width="120" align="center">
              <template #default="{ row }">
                <div style="font-weight: 500; color: #303133;">{{ row.patientName || '未知患者' }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="doctorName" label="医生姓名" width="120" align="center">
              <template #default="{ row }">
                <div style="font-weight: 500;">{{ row.doctorName || '未知医生' }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="deptName" label="科室" width="120" align="center">
              <template #default="{ row }">
                <el-tag type="info" size="small">{{ row.deptName || '未知科室' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="appointmentDate" label="就诊日期" width="120" align="center">
              <template #default="{ row }">
                <span style="font-family: monospace; color: #409eff;">{{ row.appointmentDate || '未设置' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="timeSlot" label="时段" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="getTimeSlotType(row.timeSlot)" size="small">{{ formatTimeSlot(row.timeSlot) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="queueNumber" label="排队号" width="80" align="center" />
            <el-table-column prop="consultationFee" label="挂号费" width="100" align="center">
              <template #default="{ row }">
                <span style="color: #f56c6c; font-weight: 500;">¥{{ row.consultationFee }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createTime" label="创建时间" width="160" align="center">
              <template #default="{ row }">
                <span style="font-size: 12px; color: #666;">{{ row.createTime || '未知' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right" align="center">
              <template #default="{ row }">
                <el-button size="small" @click="viewDetail(row)">详情</el-button>
                <el-button v-if="row.status === 'CONFIRMED'" size="small" type="danger" @click="handleCancelAppointment(row)">
                  取消
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="admin-pagination" v-if="total > 0">
            <el-pagination v-model:current-page="queryParams.page" v-model:page-size="queryParams.pageSize" :total="total"
              :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next" @size-change="loadAppointments"
              @current-change="loadAppointments" />
          </div>
        </div>

        <!-- 详情弹窗 -->
          <el-dialog v-model="detailVisible" title="预约详情" width="600px">
            <el-descriptions :column="2" border v-if="selectedAppointment">
              <el-descriptions-item label="订单号" :span="2">
                <span>{{ selectedAppointment.id }}</span>
              </el-descriptions-item>
              <el-descriptions-item label="患者姓名">{{ selectedAppointment.patientName }}</el-descriptions-item>
              <el-descriptions-item label="患者电话">{{ selectedAppointment.patientPhone }}</el-descriptions-item>
              <el-descriptions-item label="医生姓名">{{ selectedAppointment.doctorName }}</el-descriptions-item>
              <el-descriptions-item label="科室">{{ selectedAppointment.deptName }}</el-descriptions-item>
              <el-descriptions-item label="就诊日期">{{ selectedAppointment.appointmentDate }}</el-descriptions-item>
              <el-descriptions-item label="就诊时段">{{ formatTimeSlot(selectedAppointment.timeSlot)
              }}</el-descriptions-item>
              <el-descriptions-item label="排队号">{{ selectedAppointment.queueNumber }}</el-descriptions-item>
              <el-descriptions-item label="挂号费">¥{{ selectedAppointment.consultationFee }}</el-descriptions-item>
              <el-descriptions-item label="预约状态">
                <el-tag :type="getStatusType(selectedAppointment.status)">
                  {{ getStatusText(selectedAppointment.status) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="创建时间" :span="2">
                {{ selectedAppointment.createTime }}
              </el-descriptions-item>
            </el-descriptions>
            <template #footer>
              <el-button @click="detailVisible = false">关闭</el-button>
            </template>
          </el-dialog>
      </div>
    </div>
  </div>
</template>

  <script setup>
  import message from '@/plugins/message'
import { ref, reactive, onMounted } from 'vue'
  import { ElMessageBox } from 'element-plus'
  import { Refresh } from '@element-plus/icons-vue'
  import { getAppointmentList, cancelAppointment, updateAppointmentStatus, deleteAppointment } from '@/api/appointment'
  import { refreshAppointmentCache } from '@/api/cache'
  import dayjs from 'dayjs'

  const loading = ref(false)
  const detailVisible = ref(false)
  const searchText = ref('')
  const dateRange = ref([])
  const selectedAppointment = ref(null)

  // 查询参数
  const queryParams = reactive({
    page: 1,
    pageSize: 10,
    status: ''
  })

  // 数据
  const appointments = ref([])
  const total = ref(0)

  // 加载预约列表
  const loadAppointments = async () => {
    loading.value = true
    try {
      const keyword = String(searchText.value || '').trim()
      const params = {
        ...queryParams
      }
      // 自动判断：纯数字按订单号查询，否则按患者姓名查询
      if (keyword) {
        if (/^\d+$/.test(keyword)) {
          params.id = keyword
        } else {
          params.patientName = keyword
        }
      }
      // 处理日期范围
      if (dateRange.value && dateRange.value.length === 2) {
        params.startDate = dateRange.value[0]
        params.endDate = dateRange.value[1]
      }
      const res = await getAppointmentList(params)
      if (res.code === 200) {
        appointments.value = res.data?.records || []
        // 兜底：将接口 total 强制为数字，若缺失则使用 records.length
        const apiTotal = Number(res.data?.total)
        total.value = apiTotal > 0 ? apiTotal : (Array.isArray(res.data?.records) ? res.data.records.length : 0)
      }
    } catch (error) {

      message.error('加载预约列表失败')
    } finally {
      loading.value = false
    }
  }

  // 搜索处理
  const handleSearch = () => {
    queryParams.page = 1
    loadAppointments()
  }

  // 查看详情
  const viewDetail = (row) => {
    selectedAppointment.value = row
    detailVisible.value = true
  }

  // 取消预约
  const handleCancelAppointment = async (row) => {
    try {
      await ElMessageBox.confirm('确定要取消此预约吗？', '确认操作', {
        type: 'warning'
      })

      loading.value = true
      const res = await cancelAppointment(row.id)
      
      if (res.code === 200) {
        message.success('取消成功')
        
        // 清除缓存并重新加载数据
        try {
          await refreshAppointmentCache()
        } catch (e) {

        }
        await loadAppointments()
      } else {
        message.error(res.message || '取消失败')
      }
    } catch (error) {
      if (error !== 'cancel') {
        message.error('取消失败')
      }
    } finally {
      loading.value = false
    }
  }

  // 格式化时段
  const formatTimeSlot = (slot) => {
    const slotMap = {
      'MORNING': '上午',
      'AFTERNOON': '下午',
      'EVENING': '晚间'
    }
    return slotMap[slot] || slot
  }

  // 时段标签类型
  const getTimeSlotType = (slot) => {
    const typeMap = {
      'MORNING': 'success',
      'AFTERNOON': 'warning',
      'EVENING': 'danger'
    }
    return typeMap[slot] || 'info'
  }

  // 获取状态类型
  const getStatusType = (status) => {
    const typeMap = {
      'CONFIRMED': 'primary',
      'IN_PROGRESS': 'info',
      'COMPLETED': 'success',
      'CANCELLED': 'info',
      'NO_SHOW': 'danger'
    }
    return typeMap[status] || 'info'
  }

  // 获取状态文本
  const getStatusText = (status) => {
    const textMap = {
      'CONFIRMED': '已确认',
      'IN_PROGRESS': '就诊中',
      'COMPLETED': '已完成',
      'CANCELLED': '已取消',
      'NO_SHOW': '爽约'
    }
    return textMap[status] || '未知'
  }

  // 刷新缓存并重新加载数据
  const handleRefresh = async () => {
    try {
      loading.value = true
      await refreshAppointmentCache()
      await loadAppointments()
      message.success('刷新成功')
    } catch (error) {

      message.error('刷新失败')
    } finally {
      loading.value = false
    }
  }

  onMounted(async () => {
    // 先加载数据，确保页面快速显示
    await loadAppointments()
    
    // 异步刷新缓存，确保数据最新（不阻塞页面显示）
    setTimeout(async () => {
      try {
        await refreshAppointmentCache()
        await loadAppointments()
      } catch (error) {

        // 静默失败，不影响用户体验
      }
    }, 100)
  })
</script>

<style scoped lang="scss">
.appointment-manage-container {
  // 使用全局admin样式
}
</style>