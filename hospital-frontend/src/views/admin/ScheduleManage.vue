<template>
  <div class="schedule-manage-container">
    <div class="admin-card">
      <div class="card-header">
        <h2>
          <el-icon>
            <Calendar />
          </el-icon>
          排班管理
        </h2>
        <div class="header-actions">
          <el-button @click="handleRefresh">
            <el-icon>
              <Refresh />
            </el-icon>
            刷新
          </el-button>
          <el-button type="primary" @click="showBatchAddDialog">
            <el-icon>
              <Plus />
            </el-icon>
            批量添加排班
          </el-button>
        </div>
      </div>
      <div class="card-body">

        <!-- 筛选条件 -->
        <div class="admin-filter">
          <el-form inline>
            <el-form-item label="选择科室">
              <el-select v-model="queryParams.deptId" placeholder="全部科室" clearable style="width: 150px" @change="handleDeptChange">
                <el-option v-for="dept in departments" :key="dept.id" :label="dept.deptName" :value="dept.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="选择医生">
              <el-select v-model="queryParams.doctorId" placeholder="全部医生" clearable style="width: 150px" @change="loadSchedules">
                <el-option v-for="doctor in doctors" :key="doctor.id" :label="doctor.doctorName" :value="doctor.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="日期范围">
              <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期"
                end-placeholder="结束日期" format="YYYY-MM-DD" value-format="YYYY-MM-DD" @change="loadSchedules" />
            </el-form-item>
          </el-form>
        </div>

        <!-- 排班列表 -->
        <el-table :data="schedules" v-loading="loading" class="admin-table" stripe>
          <el-table-column type="index" label="序号" width="60" align="center" fixed="left"/>
          <el-table-column prop="doctorName" label="医生姓名" width="120" align="center" fixed="left">
            <template #default="{ row }">
              <div style="font-weight: 600; color: #303133;">{{ row.doctorName || '未知医生' }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="deptName" label="中医分类" width="120" align="center">
            <template #default="{ row }">
              <span class="status-tag info">
                <span class="status-dot"></span>
                {{ row.deptName || '未知分类' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="scheduleDate" label="排班日期" width="120" align="center">
            <template #default="{ row }">
              <span style="font-family: monospace; color: #409eff; font-weight: 500;">{{ row.scheduleDate || '未设置'
              }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="timeSlot" label="时段" width="100" align="center">
            <template #default="{ row }">
              <span :class="['status-tag', getTimeSlotType(row.timeSlot)]">
                <span class="status-dot"></span>
                {{ formatTimeSlot(row.timeSlot) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="startTime" label="开始时间" width="100" align="center">
            <template #default="{ row }">
              <span style="font-family: monospace; color: #67c23a; font-weight: 500;">{{ row.startTime || '未设置'
              }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="endTime" label="结束时间" width="100" align="center">
            <template #default="{ row }">
              <span style="font-family: monospace; color: #f56c6c; font-weight: 500;">{{ row.endTime || '未设置' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="totalQuota" label="总号源" width="80" align="center">
            <template #default="{ row }">
              <span style="color: #909399; font-weight: 600;">{{ row.totalQuota || 0 }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="bookedQuota" label="已预约" width="80" align="center">
            <template #default="{ row }">
              <span style="color: #e6a23c; font-weight: 600;">{{ row.bookedQuota || 0 }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="remainingQuota" label="剩余" width="80" align="center">
            <template #default="{ row }">
              <span :style="{ color: (row.remainingQuota || 0) > 0 ? '#67c23a' : '#f56c6c', fontWeight: '600' }">
                {{ row.remainingQuota || 0 }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100" align="center">
            <template #default="{ row }">
              <span :class="['status-tag', getStatusType(row.status)]">
                <span class="status-dot"></span>
                {{ getStatusText(row.status) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="note" label="备注" min-width="120" show-overflow-tooltip>
            <template #default="{ row }">
              <span>{{ row.note || '无备注' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="160" align="center">
            <template #default="{ row }">
              <span style="font-size: 12px; color: #666;">{{ row.createTime || '未知' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" fixed="right" align="center">
            <template #default="{ row }">
              <div class="admin-actions">
                <el-button size="small" type="primary" @click="editSchedule(row)">
                  <el-icon>
                    <Edit />
                  </el-icon>
                  编辑
                </el-button>
                <el-button size="small" type="danger" @click="deleteSchedule(row)">
                  <el-icon>
                    <Delete />
                  </el-icon>
                  删除
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="admin-pagination" v-if="total > 0">
          <el-pagination v-model:current-page="queryParams.page" v-model:page-size="queryParams.pageSize" :total="total"
            :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next" @size-change="loadSchedules"
            @current-change="loadSchedules" />
        </div>
      </div>
    </div>

    <!-- 批量添加排班弹窗 -->
    <el-dialog v-model="dialogVisible" title="批量添加排班" width="650px">
      <el-form :model="form" :rules="scheduleRules" ref="formRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="选择医生" prop="doctorIds">
              <el-select v-model="form.doctorIds" placeholder="请选择医生（可多选）" multiple style="width: 100%" filterable @change="handleFieldBlur('doctorIds')">
                <el-option v-for="doctor in doctors" :key="doctor.id"
                  :label="`${doctor.doctorName} - ${doctor.deptName || '未知科室'}`" :value="doctor.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="日期范围" prop="dateRange">
              <el-date-picker v-model="form.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期"
                end-placeholder="结束日期" style="width: 100%" format="YYYY-MM-DD" value-format="YYYY-MM-DD" @change="handleFieldBlur('dateRange')" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="排班时段" prop="timeSlots">
              <el-checkbox-group v-model="form.timeSlots" @change="handleFieldBlur('timeSlots')">
                <el-checkbox label="MORNING">
                  <span style="color: #67c23a;">上午 (08:00-12:00)</span>
                </el-checkbox>
                <el-checkbox label="AFTERNOON">
                  <span style="color: #e6a23c;">下午 (14:00-18:00)</span>
                </el-checkbox>
                <el-checkbox label="EVENING">
                  <span style="color: #f56c6c;">晚间 (19:00-22:00)</span>
                </el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="号源数量" prop="totalQuota">
              <el-input-number v-model="form.totalQuota" :min="1" :max="100" style="width: 100%" @blur="handleFieldBlur('totalQuota')" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="排班状态">
              <el-select v-model="form.status" style="width: 100%">
                <el-option label="可预约" value="AVAILABLE" />
                <el-option label="已满" value="FULL" />
                <el-option label="停诊" value="CLOSED" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注">
          <el-input v-model="form.note" type="textarea" :rows="2" placeholder="请输入备注信息（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveBatchSchedule" :loading="loading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessageBox } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import { getScheduleList, addSchedule, updateSchedule, deleteSchedule as deleteScheduleApi, createSchedulesBatch } from '@/api/schedule'
import { refreshScheduleCache } from '@/api/cache'
import { getDepartmentList } from '@/api/department'
import { getDoctorList, getDoctorListByDept } from '@/api/doctor'
import dayjs from 'dayjs'
import { useFormValidation } from '@/composables/useFormValidation'

const loading = ref(false)
const dialogVisible = ref(false)
const dateRange = ref([])

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10,
  deptId: null,
  doctorId: null
})

// 表单
const form = reactive({
  doctorIds: [],
  dateRange: [],
  timeSlots: [],
  totalQuota: 20,
  status: 'AVAILABLE',
  note: ''
})

// 表单验证规则
const scheduleRules = {
  doctorIds: [{ type: 'array', required: true, message: '请选择至少一位医生', trigger: 'change' }],
  dateRange: [{ required: true, message: '请选择日期范围', trigger: 'change' }],
  timeSlots: [{ type: 'array', required: true, message: '请选择至少一个时段', trigger: 'change' }],
  totalQuota: [{ required: true, message: '请设置号源数量', trigger: 'blur' }]
}

const formRef = ref(null)

// 创建字段失焦处理函数
const { handleFieldBlur } = useFormValidation(formRef)

// 数据
const schedules = ref([])
const departments = ref([])
const doctors = ref([])
const total = ref(0)

// 加载排班列表
const loadSchedules = async () => {
  loading.value = true
  try {
    const params = {
      ...queryParams
    }
    // 处理日期范围筛选
    if (dateRange.value && dateRange.value.length === 2) {
      params.startDate = dateRange.value[0]
      params.endDate = dateRange.value[1]
    }
    const res = await getScheduleList(params)

    if (res.code === 200) {
      schedules.value = res.data?.records || []
      // 兜底：将接口 total 强制为数字，若缺失则使用 records.length
      const apiTotal = Number(res.data?.total)
      total.value = apiTotal > 0 ? apiTotal : (Array.isArray(res.data?.records) ? res.data.records.length : 0)
    } else {

      message.error(res.message || '获取排班列表失败')
    }
  } catch (error) {

    message.error(error.response?.data?.message || '加载排班列表失败')
  } finally {
    loading.value = false
  }
}

// 显示批量添加弹窗
const showBatchAddDialog = () => {
  resetForm()
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    doctorIds: [],
    dateRange: [],
    timeSlots: [],
    totalQuota: 20,
    status: 'AVAILABLE',
    note: ''
  })
  formRef.value?.clearValidate()
}

// 编辑排班
const editSchedule = (row) => {
  message.info('编辑排班功能')
}

// 删除排班
const deleteSchedule = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除此排班吗？', '删除确认', {
      type: 'warning'
    })

    loading.value = true
    const res = await deleteScheduleApi(row.id)

    if (res.code === 200) {
      message.success('删除成功')
      
      // 清除缓存并重新加载数据
      try {
        await refreshScheduleCache()
      } catch (e) {

      }
      await loadSchedules()
    } else {
      message.error(res.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {

      message.error(error.response?.data?.message || '删除失败')
    }
  } finally {
    loading.value = false
  }
}

// 批量保存排班
const saveBatchSchedule = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      const [startDate, endDate] = form.dateRange
      const payload = {
        doctorIds: form.doctorIds,
        startDate: dayjs(startDate).format('YYYY-MM-DD'),
        endDate: dayjs(endDate).format('YYYY-MM-DD'),
        timeSlots: form.timeSlots,
        totalQuota: form.totalQuota,
        status: form.status || 'AVAILABLE',
        note: form.note || ''
      }

      const res = await createSchedulesBatch(payload)
      if (res.code === 200) {
        const created = res.data?.created || 0
        const skipped = res.data?.skipped || 0
        message.success(`成功创建 ${created} 个排班，跳过 ${skipped} 个（已存在）`)
        dialogVisible.value = false
        
        // 清除缓存并重新加载数据
        try {
          await refreshScheduleCache()
        } catch (e) {

        }
        await loadSchedules()
      } else {
        message.error(res.message || '批量创建失败')
      }
    } catch (error) {

      message.error('添加失败：' + (error.response?.data?.message || error.message))
    }
  })
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

// 获取时段标签类型
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
    'AVAILABLE': 'success',
    'FULL': 'warning',
    'CLOSED': 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = {
    'AVAILABLE': '可预约',
    'FULL': '已满',
    'CLOSED': '停诊'
  }
  return textMap[status] || '未知'
}

// 加载科室和医生列表
const loadDepartments = async () => {
  try {
    const res = await getDepartmentList()
    departments.value = res.data || []
  } catch (error) {

  }
}

const loadDoctors = async () => {
  try {
    let res
    if (queryParams.deptId) {
      res = await getDoctorListByDept(queryParams.deptId)
    } else {
      res = await getDoctorList()
    }
    if (res.code === 200) {
      doctors.value = res.data || []
    }
  } catch (error) {

    message.error('加载医生失败')
  }
}

// 处理科室变化
const handleDeptChange = async () => {
  // 清空医生选择
  queryParams.doctorId = null
  // 重新加载医生列表
  await loadDoctors()
  // 重新加载排班列表
  await loadSchedules()
}

// 刷新缓存并重新加载数据
const handleRefresh = async () => {
  try {
    loading.value = true
    await refreshScheduleCache()
    await loadSchedules()
    message.success('刷新成功')
  } catch (error) {

    message.error('刷新失败')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    // 先加载数据，确保页面快速显示
    await loadDepartments()
    await loadDoctors()
    await loadSchedules()
    
    // 异步刷新缓存，确保数据最新（不阻塞页面显示）
    setTimeout(async () => {
      try {
        await refreshScheduleCache()
        await loadSchedules()
      } catch (error) {

        // 静默失败，不影响用户体验
      }
    }, 100)
  } catch (error) {

  }
})
</script>

<style scoped lang="scss">
// 使用全局admin样式
</style>
