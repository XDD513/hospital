<template>
  <div class="dept-manage-container">
    <div class="admin-card">
      <div class="card-header">
        <h2>
          <el-icon>
            <OfficeBuilding />
          </el-icon>
          中医分类管理
        </h2>
        <div class="header-actions">
          <el-button @click="handleRefresh">
            <el-icon>
              <Refresh />
            </el-icon>
            刷新
          </el-button>
          <el-button type="danger" :disabled="selectedRows.length === 0" @click="handleBatchDelete">
            <el-icon>
              <Delete />
            </el-icon>
            批量删除
          </el-button>
          <el-button type="primary" @click="showAddDialog">
            <el-icon>
              <Plus />
            </el-icon>
            添加分类
          </el-button>
        </div>
      </div>
      <div class="card-body">

        <el-table :data="pagedDepartments" v-loading="loading" class="admin-table" stripe @selection-change="handleSelectionChange">
          <el-table-column type="selection" width="55" align="center" fixed="left"/>
          <el-table-column type="index" label="序号" width="70" align="center" fixed="left"/>
          <el-table-column prop="deptName" label="分类名称" min-width="150" align="center" fixed="left">
            <template #default="{ row }">
              <div style="font-weight: 600; color: #303133;">{{ row.deptName || '未设置' }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="deptHead" label="负责人" width="120" align="center">
            <template #default="{ row }">
              <span style="font-weight: 500;">{{ row.deptHead || '未指定' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="contactPhone" label="联系电话" width="140" align="center">
            <template #default="{ row }">
              <span style="font-family: monospace;">{{ row.contactPhone || '未设置' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="location" label="位置" min-width="180" align="center">
            <template #default="{ row }">
              <span>
                <el-icon style="margin-right: 4px;">
                  <Location />
                </el-icon>
                {{ row.location || '未设置' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="deptDesc" label="分类描述" min-width="220" show-overflow-tooltip>
            <template #default="{ row }">
              <span>{{ row.deptDesc || '暂无描述' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="sortOrder" label="排序" width="80" align="center">
            <template #default="{ row }">
              <span style="font-weight: 500; color: #e6a23c;">{{ row.sortOrder || 0 }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="90" align="center">
            <template #default="{ row }">
              <span :class="['status-tag', row.status === 1 ? 'success' : 'danger']">
                <span class="status-dot"></span>
                {{ row.status === 1 ? '启用' : '停用' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="180" align="center">
            <template #default="{ row }">
              <span style="font-size: 12px; color: #666;">{{ row.createTime || '未知' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="280" fixed="right" align="center">
            <template #default="{ row }">
              <el-button size="small" :type="row.status === 1 ? 'warning' : 'success'" @click="toggleStatus(row)">
                <el-icon>
                  <Switch />
                </el-icon>
                {{ row.status === 1 ? '禁用' : '启用' }}
              </el-button>
              <el-button size="small" type="primary" @click="editDept(row)">
                <el-icon>
                  <Edit />
                </el-icon>
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="deleteDept(row)">
                <el-icon>
                  <Delete />
                </el-icon>
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页 -->
        <div class="admin-pagination" v-if="total > 0">
          <el-pagination v-model:current-page="page" v-model:page-size="pageSize" :total="total"
            :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next" @size-change="loadDepartments"
            @current-change="loadDepartments" />
        </div>
      </div>
    </div>

    <!-- 添加/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" class="admin-dialog">
      <el-form :model="form" label-width="100px" class="admin-form">
        <el-form-item label="分类名称">
          <el-input v-model="form.deptName" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-select v-model="form.deptHead" placeholder="请选择负责人" clearable filterable @change="handleDeptHeadChange"
            style="width: 100%">
            <el-option v-for="doctor in doctors" :key="doctor.id" :label="doctor.doctorName"
              :value="doctor.doctorName" />
          </el-select>
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="form.contactPhone" placeholder="联系电话" />
        </el-form-item>
        <el-form-item label="位置">
          <el-input v-model="form.location" placeholder="请输入位置">
            <template #prefix>
              <el-icon>
                <Location />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="分类描述">
          <el-input v-model="form.deptDesc" type="textarea" :rows="3" placeholder="请输入分类描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="admin-actions">
          <el-button @click="dialogVisible = false">
            <el-icon>
              <Close />
            </el-icon>
            取消
          </el-button>
          <el-button type="primary" @click="saveDept">
            <el-icon>
              <Check />
            </el-icon>
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessageBox } from 'element-plus'
import { Refresh, Delete } from '@element-plus/icons-vue'
import { getDepartmentList, addDepartment, updateDepartment, deleteDepartment, updateDepartmentStatus } from '@/api/department'
import { refreshDepartmentCache } from '@/api/cache'
import { getDoctorList } from '@/api/doctor'

const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('添加科室')

// 表单
const form = reactive({
  deptName: '',
  deptHead: '',
  contactPhone: '',
  location: '',
  deptDesc: '',
  status: 1
})

// 科室列表与分页
const departments = ref([])
const doctors = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const selectedRows = ref([])

const pagedDepartments = computed(() => {
  const start = (page.value - 1) * pageSize.value
  const end = start + pageSize.value
  return departments.value.slice(start, end)
})

// 加载分类列表
const loadDepartments = async () => {
  loading.value = true
  try {
    const res = await getDepartmentList()
    departments.value = res.data || []
    total.value = departments.value.length
    page.value = 1
  } catch (error) {

    message.error('加载分类列表失败')
  } finally {
    loading.value = false
  }
}

// 加载医生列表
const loadDoctors = async () => {
  try {
    const res = await getDoctorList()
    doctors.value = res.data || []
  } catch (error) {

  }
}

// 显示添加弹窗
const showAddDialog = () => {
  dialogTitle.value = '添加分类'
  Object.assign(form, {
    id: null,
    deptName: '',
    deptHead: '',
    contactPhone: '',
    location: '',
    deptDesc: '',
    status: 1
  })
  dialogVisible.value = true
}

// 编辑分类
const editDept = (row) => {
  dialogTitle.value = '编辑分类'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 处理负责人选择变化
const handleDeptHeadChange = (doctorName) => {
  if (!doctorName) {
    form.contactPhone = ''
    return
  }

  const selectedDoctor = doctors.value.find(d => d.doctorName === doctorName)
  if (selectedDoctor) {
    form.contactPhone = selectedDoctor.phone || ''
  }
}

// 初始化
onMounted(async () => {
  // 先加载数据，确保页面快速显示
  await loadDepartments()
  loadDoctors()
  
  // 异步刷新缓存，确保数据最新（不阻塞页面显示）
  setTimeout(async () => {
    try {
      await refreshDepartmentCache()
      await loadDepartments()
    } catch (error) {

      // 静默失败，不影响用户体验
    }
  }, 100)
})

// 删除分类
const deleteDept = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除此分类吗？', '提示', {
      type: 'warning'
    })

    loading.value = true
    await deleteDepartment(row.id)
    message.success('删除成功')
    
    // 清除缓存并重新加载数据
    try {
      await refreshDepartmentCache()
    } catch (e) {

    }
    await loadDepartments()
  } catch (error) {
    if (error !== 'cancel') {

      message.error('删除失败')
    }
  } finally {
    loading.value = false
  }
}

// 切换状态
const toggleStatus = async (row) => {
  const newStatus = row.status === 1 ? 0 : 1
  const action = newStatus === 1 ? '启用' : '禁用'

  try {
    await ElMessageBox.confirm(`确定要${action}此分类吗？`, '提示', {
      type: 'warning'
    })

    loading.value = true
    await updateDepartmentStatus(row.id, newStatus)
    
    // 立即更新本地数据
    row.status = newStatus
    message.success(`${action}成功`)
    
    // 清除缓存并重新加载数据
    try {
      await refreshDepartmentCache()
    } catch (e) {

    }
    await loadDepartments()
  } catch (error) {
    if (error !== 'cancel') {

      message.error(error.response?.data?.message || '状态更新失败')
    }
  } finally {
    loading.value = false
  }
}

// 保存
const saveDept = async () => {
  try {
    if (form.id) {
      await updateDepartment(form)
    } else {
      await addDepartment(form)
    }

    message.success('保存成功')
    dialogVisible.value = false
    
    // 清除缓存并重新加载数据
    try {
      await refreshDepartmentCache()
    } catch (e) {

    }
    await loadDepartments()
  } catch (error) {

    message.error(error.response?.data?.message || '保存失败')
  }
}

// 刷新缓存并重新加载数据
const handleRefresh = async () => {
  try {
    loading.value = true
    await refreshDepartmentCache()
    await loadDepartments()
    message.success('刷新成功')
  } catch (error) {

    message.error('刷新失败')
  } finally {
    loading.value = false
  }
}

// 处理表格选择变化
const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

// 批量删除
const handleBatchDelete = async () => {
  if (selectedRows.value.length === 0) {
    message.warning('请选择要删除的分类')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedRows.value.length} 个分类吗？删除后不可恢复。`,
      '批量删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    loading.value = true
    const deletePromises = selectedRows.value.map(row => deleteDepartment(row.id))
    await Promise.all(deletePromises)
    
    message.success(`成功删除 ${selectedRows.value.length} 个分类`)
    selectedRows.value = []
    
    // 清除缓存并重新加载数据
    try {
      await refreshDepartmentCache()
    } catch (e) {

    }
    await loadDepartments()
  } catch (error) {
    if (error !== 'cancel') {
      message.error('批量删除失败')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
// 使用全局admin样式
</style>
