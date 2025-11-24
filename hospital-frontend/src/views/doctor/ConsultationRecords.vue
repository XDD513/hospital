<template>
  <div class="consultation-records-container">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="8">
        <div class="doctor-stat-card blue">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Document />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ total }}</div>
              <div class="stat-label">总接诊数</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="8">
        <div class="doctor-stat-card green">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Calendar />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ monthlyCount }}</div>
              <div class="stat-label">本月接诊</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="8">
        <div class="doctor-stat-card orange">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Clock />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ avgDuration }}</div>
              <div class="stat-label">平均时长(分钟)</div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <div class="doctor-card">
      <div class="card-header">
        <h3>
          <el-icon>
            <Document />
          </el-icon>
          接诊记录
        </h3>
        <div class="header-actions">
          <el-input v-model="patientName" placeholder="搜索患者姓名" class="doctor-search" style="width: 250px" clearable
            @keyup.enter="handleSearch">
            <template #prefix>
              <el-icon>
                <Search />
              </el-icon>
            </template>
          </el-input>
        </div>
      </div>

      <div class="card-body">
        <!-- 筛选条件 -->
        <el-form inline style="margin-bottom: 15px">
          <el-form-item label="日期范围">
            <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期"
              end-placeholder="结束日期" value-format="YYYY-MM-DD" @change="handleSearch" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon>
                <Search />
              </el-icon>
              查询
            </el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="exportRecords" :loading="exportLoading">
              <el-icon>
                <Download />
              </el-icon>
              导出记录
            </el-button>
          </el-form-item>
        </el-form>

        <!-- 接诊记录列表 -->
        <div class="doctor-table">
          <el-table :data="records" v-loading="loading" stripe>
            <el-table-column type="index" label="序号" width="70"
              :index="(index) => (queryParams.page - 1) * queryParams.pageSize + index + 1" />
            <el-table-column prop="appointmentDate" label="就诊日期" width="120" />
            <el-table-column prop="timeSlot" label="时段" width="80">
              <template #default="{ row }">
                <el-tag size="small">{{ row.timeSlot }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="queueNumber" label="排队号" width="70" />
            <el-table-column prop="patientName" label="患者姓名" width="100" />
            <el-table-column prop="gender" label="性别" width="60">
              <template #default="{ row }">
                <span v-if="row.gender == 1">男</span>
                <span v-else-if="row.gender == 2">女</span>
              </template>
            </el-table-column>
            <el-table-column prop="age" label="年龄" width="60" />
            <el-table-column prop="diagnosis" label="诊断" show-overflow-tooltip />
            <el-table-column prop="prescription" label="处方" show-overflow-tooltip />
            <el-table-column prop="consultationDateTime" label="接诊时间" width="160" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="viewDetail(row)">详情</el-button>
                <el-button size="small" type="primary" @click="printRecord(row)">
                  打印
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 空状态 -->
          <div v-if="records.length === 0 && !loading" class="doctor-empty">
            <div class="empty-icon">
              <el-icon>
                <Document />
              </el-icon>
            </div>
            <div class="empty-text">暂无接诊记录</div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="doctor-pagination" v-if="total > 0">
          <el-pagination v-model:current-page="queryParams.page" v-model:page-size="queryParams.pageSize" :total="total"
            :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next" @size-change="loadRecords"
            @current-change="loadRecords" />
        </div>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <RecordDetailDialog v-model="detailVisible" :record-id="selectedRecordId" />
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, onMounted, computed } from 'vue'

import { Search, Download, Document, Calendar, Clock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useDoctorStore } from '@/stores/doctor'
import { getConsultationRecords, exportConsultationRecords } from '@/api/consultation'
import RecordDetailDialog from '@/components/doctor/RecordDetailDialog.vue'
import dayjs from 'dayjs'

const userStore = useUserStore()
const doctorStore = useDoctorStore()

const loading = ref(false)
const exportLoading = ref(false)
const detailVisible = ref(false)
const dateRange = ref([])
const patientName = ref('')
const selectedRecordId = ref(null)

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10
})

// 数据
const records = ref([])
const total = ref(0)

// 统计数据
const monthlyCount = computed(() => {
  const now = dayjs()
  return records.value.filter(r => {
    const recordDate = dayjs(r.consultationDate)
    return recordDate.year() === now.year() && recordDate.month() === now.month()
  }).length
})

const avgDuration = computed(() => {
  if (records.value.length === 0) return 0
  const totalDuration = records.value.reduce((sum, r) => sum + (r.durationMinutes || 0), 0)
  return Math.round(totalDuration / records.value.length)
})

// 加载接诊记录
const loadRecords = async () => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) {

    return
  }

  loading.value = true
  try {
    const params = {
      patientName: patientName.value,
      startDate: dateRange.value?.[0],
      endDate: dateRange.value?.[1],
      ...queryParams
    }
    const res = await getConsultationRecords(doctorId, params)
    if (res.code === 200) {
      records.value = res.data?.records || []
      // 确保 total 是数字类型
      total.value = Number(res.data?.total) || 0
    }
  } catch (error) {

    message.error('加载接诊记录失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  queryParams.page = 1
  loadRecords()
}

// 查看详情
const viewDetail = (row) => {
  selectedRecordId.value = row.id
  detailVisible.value = true
}

// 打印记录
const printRecord = (record) => {
  selectedRecordId.value = record.id
  detailVisible.value = true
}

// 导出记录
const exportRecords = async () => {
  const doctorId = doctorStore.getDoctorId()
  if (!doctorId) {
    message.warning('医生ID未获取到')
    return
  }

  try {
    exportLoading.value = true
    const params = {
      patientName: patientName.value,
      startDate: dateRange.value?.[0],
      endDate: dateRange.value?.[1]
    }
    const res = await exportConsultationRecords(doctorId, params)

    // 检查文件大小，如果为0则提示错误
    if (res instanceof Blob && res.size === 0) {
      message.error('导出失败：文件为空，请检查是否有数据')
      return
    }

    // 创建下载链接
    const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `接诊记录_${dayjs().format('YYYY-MM-DD')}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    message.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    message.error(error?.message || '导出失败，请稍后重试')
  } finally {
    exportLoading.value = false
  }
}

onMounted(async () => {
  await doctorStore.fetchDoctorInfo()
  loadRecords()
})
</script>

<style scoped lang="scss">
.consultation-records-container {
  .stats-row {
    margin-bottom: 20px;
  }
}
</style>
