<template>
  <div class="doctor-manage-container">
    <div class="admin-card">
      <div class="card-header">
        <h2>
          <el-icon>
            <User />
          </el-icon>
          医生管理
        </h2>
        <div class="header-actions">
          <div class="admin-search">
            <el-input v-model="searchText" placeholder="搜索中医师姓名" clearable @input="handleSearch">
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
            添加中医师
          </el-button>
        </div>
      </div>
      <div class="card-body">

        <!-- 中医师列表 -->
        <el-table :data="doctors" v-loading="loading" class="admin-table" stripe>
          <el-table-column type="index" label="序号" width="70" align="center" fixed="left" />
          
          <!-- 头像列 -->
          <el-table-column label="头像" width="80" align="center" fixed="left">
            <template #default="{ row }">
              <el-avatar 
                :size="50" 
                :src="getAvatarUrl(row)" 
                @error="handleAvatarError($event, row)"
              >
                <el-icon><User /></el-icon>
              </el-avatar>
            </template>
          </el-table-column>
          
          <!-- 基本信息 -->
          <el-table-column prop="doctorName" label="中医师姓名" min-width="140" align="center" fixed="left">
            <template #default="{ row }">
              <div style="font-weight: 600; color: #303133; text-align: center;">{{ row.doctorName || '未设置' }}</div>
            </template>
          </el-table-column>
          
          <el-table-column prop="phone" label="手机号" width="130" align="center">
            <template #default="{ row }">
              <span style="font-family: monospace; color: #606266;">{{ row.phone || '未设置' }}</span>
            </template>
          </el-table-column>
          
          <!-- 专业信息 -->
          <el-table-column prop="deptName" label="所属分类" min-width="120" align="center">
            <template #default="{ row }">
              <span class="status-tag info">
                <span class="status-dot"></span>
                {{ row.deptName || '未分配' }}
              </span>
            </template>
          </el-table-column>
          
          <el-table-column prop="title" label="职称" width="120" align="center">
            <template #default="{ row }">
              <span class="status-tag warning">
                <span class="status-dot"></span>
                {{ row.title || '未设置' }}
              </span>
            </template>
          </el-table-column>
          
          <el-table-column prop="yearsOfExperience" label="从业年限" width="100" align="center">
            <template #default="{ row }">
              <span style="font-weight: 500; color: #409eff;">{{ row.yearsOfExperience || 0 }}年</span>
            </template>
          </el-table-column>
          
          <!-- 业务信息 -->
          <el-table-column prop="consultationFee" label="挂号费" width="100" align="center">
            <template #default="{ row }">
              <span style="color: #f56c6c; font-weight: 600;">¥{{ row.consultationFee || 0 }}</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="rating" label="评分" width="140" align="center">
            <template #default="{ row }">
              <div style="display: flex; align-items: center; justify-content: center; gap: 6px;">
                <el-rate v-model="row.rating" disabled size="small" />
                <span style="color: #909399; font-size: 12px;">{{ (row.rating || 0).toFixed(1) }}</span>
              </div>
            </template>
          </el-table-column>
          
          <!-- 详细信息 -->
          <el-table-column prop="specialty" label="专长" min-width="200" show-overflow-tooltip align="center">
            <template #default="{ row }">
              <span style="color: #606266; text-align: center;">{{ row.specialty || '暂无专长介绍' }}</span>
            </template>
          </el-table-column>
          
          <!-- 是否推荐首页 -->
          <el-table-column label="推荐首页" width="100" align="center">
            <template #default="{ row }">
              <el-switch
                v-model="row.isRecommended"
                :active-value="true"
                :inactive-value="false"
                @change="toggleRecommended(row)"
              />
            </template>
          </el-table-column>
          
          <!-- 状态信息 -->
          <el-table-column prop="status" label="状态" width="90" align="center">
            <template #default="{ row }">
              <span :class="['status-tag', row.status === 1 ? 'success' : 'danger']">
                <span class="status-dot"></span>
                {{ getStatusText(row.status) }}
              </span>
            </template>
          </el-table-column>
          
          <!-- 操作列 -->
          <el-table-column label="操作" width="320" fixed="right" align="center">
            <template #default="{ row }">
              <el-button size="small" :type="row.status === 1 ? 'warning' : 'success'" @click="toggleStatus(row)">
                <el-icon>
                  <Switch />
                </el-icon>
                {{ row.status === 1 ? '禁用' : '启用' }}
              </el-button>
              <el-button size="small" @click="viewDetail(row)">
                <el-icon>
                  <View />
                </el-icon>
                详情
              </el-button>
              <el-button size="small" type="primary" @click="editDoctor(row)">
                <el-icon>
                  <Edit />
                </el-icon>
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="handleDeleteDoctor(row)">
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
          <el-pagination v-model:current-page="queryParams.page" v-model:page-size="queryParams.pageSize" :total="total"
            :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next" @size-change="loadDoctors"
            @current-change="loadDoctors" />
        </div>
      </div>
    </div>

    <!-- 添加/编辑医生弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="中医师姓名" prop="realName">
              <el-input v-model="form.realName" placeholder="请输入中医师姓名" @blur="handleFieldBlur('realName')" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号" maxlength="11" @blur="handleFieldBlur('phone')" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别">
              <el-radio-group v-model="form.gender">
                <el-radio :label="1">男</el-radio>
                <el-radio :label="2">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="出生日期">
              <el-date-picker v-model="form.birthday" type="date" placeholder="选择出生日期" style="width: 100%"
                format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属分类" prop="deptId">
              <el-select v-model="form.deptId" placeholder="选择分类" style="width: 100%" @change="handleFieldBlur('deptId')">
                <el-option v-for="dept in departments" :key="dept.id" :label="dept.deptName"
                  :value="dept.id.toString()" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="职称" prop="title">
              <el-select v-model="form.title" placeholder="选择职称" style="width: 100%" @change="handleFieldBlur('title')">
                <el-option label="主任中医师" value="主任中医师" />
                <el-option label="副主任中医师" value="副主任中医师" />
                <el-option label="主治中医师" value="主治中医师" />
                <el-option label="中医师" value="中医师" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="从业年限">
              <el-input-number v-model="form.yearsOfExperience" :min="0" :max="50" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学历">
              <el-select v-model="form.education" placeholder="选择学历" style="width: 100%">
                <el-option label="本科" value="本科" />
                <el-option label="硕士" value="硕士" />
                <el-option label="博士" value="博士" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="专长">
          <el-input v-model="form.specialty" placeholder="如：心血管疾病、高血压" />
        </el-form-item>

        <el-form-item label="个人简介">
          <el-input v-model="form.introduction" type="textarea" :rows="3" placeholder="请输入医生简介" />
        </el-form-item>

        <el-form-item label="资质证书">
          <el-input v-model="form.certificates" type="textarea" :rows="2" placeholder="请输入资质证书信息（JSON格式）" />
        </el-form-item>

        <el-form-item label="挂号费" prop="consultationFee">
          <el-input-number v-model="form.consultationFee" :min="0" :step="10" style="width: 100%" @blur="handleFieldBlur('consultationFee')" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveDoctorHandler">保存</el-button>
      </template>
    </el-dialog>

    <!-- 医生详情弹窗 -->
    <el-dialog v-model="detailVisible" title="医生详情" width="700px">
      <div v-if="selectedDoctor">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="医生ID" :span="2">
            <span>{{ selectedDoctor.id }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="用户ID">
            <span>{{ selectedDoctor.userId }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="科室ID">
            <span>{{ selectedDoctor.deptId }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="医生姓名">
            <span style="font-weight: 500;">{{ selectedDoctor.doctorName || '未设置' }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="手机号">
            <span>{{ selectedDoctor.phone || '未设置' }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="性别">
            <el-tag :type="selectedDoctor.gender === 1 ? 'primary' : selectedDoctor.gender === 2 ? 'danger' : 'info'"
              size="small">
              {{ getGenderText(selectedDoctor.gender) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="出生日期">{{ selectedDoctor.birthday || '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="所属科室">
            <el-tag type="info">{{ selectedDoctor.deptName || '未分配' }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="职称">
            <el-tag type="warning">{{ selectedDoctor.title || '未设置' }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="从业年限">
            <span style="color: #409eff; font-weight: 500;">{{ selectedDoctor.yearsOfExperience || 0 }}年</span>
          </el-descriptions-item>
          <el-descriptions-item label="学历">{{ selectedDoctor.education || '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="挂号费">
            <span style="color: #f56c6c; font-weight: 500;">¥{{ selectedDoctor.consultationFee || 0 }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="评分">
            <div style="display: flex; align-items: center;">
              <el-rate v-model="selectedDoctor.rating" disabled size="small" />
              <span style="margin-left: 8px;">{{ selectedDoctor.rating || 0 }}</span>
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="接诊总数">
            <span style="color: #409eff; font-weight: 500;">{{ selectedDoctor.consultationCount || 0 }}次</span>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(selectedDoctor.status)">
              {{ getStatusText(selectedDoctor.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="专长" :span="2">
            <div style="max-height: 60px; overflow-y: auto;">
              {{ selectedDoctor.specialty || '暂无专长介绍' }}
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="个人简介" :span="2">
            <div style="max-height: 80px; overflow-y: auto;">
              {{ selectedDoctor.introduction || '暂无个人简介' }}
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="资质证书" :span="2">
            <div style="max-height: 60px; overflow-y: auto;">
              {{ selectedDoctor.certificates || '暂无资质证书信息' }}
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ selectedDoctor.createTime || '未知' }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ selectedDoctor.updateTime || '未知' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button type="primary" @click="editDoctor(selectedDoctor)">编辑医生</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, onMounted } from 'vue'
import { ElMessageBox } from 'element-plus'
import { Refresh, Delete, User, Search, Plus, Switch, View, Edit } from '@element-plus/icons-vue'
import { getDoctorList, addDoctor, updateDoctor, deleteDoctor as deleteDoctorApi, updateDoctorStatus } from '@/api/doctor'
import { refreshDoctorCache } from '@/api/cache'
import { getDepartmentList } from '@/api/department'
import { useFormValidation } from '@/composables/useFormValidation'

const loading = ref(false)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('添加医生')
const isEdit = ref(false)
const searchText = ref('')
const formRef = ref(null)

// 创建字段失焦处理函数
const { handleFieldBlur } = useFormValidation(formRef)

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10
})

// 表单数据
const form = reactive({
  realName: '',
  phone: '',
  gender: 0,
  birthday: '',
  deptId: null,
  title: '',
  specialty: '',
  introduction: '',
  yearsOfExperience: 0,
  education: '',
  certificates: '',
  consultationFee: 50,
  status: 1
})

// 表单验证规则
const rules = {
  realName: [{ required: true, message: '请输入医生姓名', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  deptId: [{ required: true, message: '请选择科室', trigger: 'change' }],
  title: [{ required: true, message: '请选择职称', trigger: 'change' }],
  consultationFee: [{ required: true, message: '请输入挂号费', trigger: 'blur' }]
}

// 数据
const doctors = ref([])
const departments = ref([])
const selectedDoctor = ref(null)
const total = ref(0)

// 加载医生列表
const loadDoctors = async () => {
  loading.value = true
  try {
    const res = await getDoctorList()

    let filteredDoctors = res.data || []

    // 前端搜索过滤
    if (searchText.value) {
      filteredDoctors = filteredDoctors.filter(d =>
        d.doctorName?.includes(searchText.value) ||
        d.realName?.includes(searchText.value)
      )
    }

    // 确保每个医生都有头像和推荐字段
    doctors.value = filteredDoctors.map(doctor => ({
      ...doctor,
      avatar: doctor.avatar || '',
      isRecommended: doctor.isRecommended !== undefined ? doctor.isRecommended : false
    }))
    total.value = filteredDoctors.length
  } catch (error) {

    message.error('加载医生列表失败')
  } finally {
    loading.value = false
  }
}

// 加载分类列表
const loadDepartments = async () => {
  try {
    const res = await getDepartmentList()
    departments.value = res.data || []
  } catch (error) {

  }
}

// 搜索处理
const handleSearch = () => {
  queryParams.page = 1
  loadDoctors()
}

// 显示添加弹窗
const showAddDialog = () => {
  isEdit.value = false
  dialogTitle.value = '添加中医师'
  resetForm()
  dialogVisible.value = true
}

// 编辑中医师
const editDoctor = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑中医师'
  Object.assign(form, {
    id: row.id, // 保持字符串格式
    realName: row.doctorName,
    phone: row.phone,
    gender: row.gender || 0,
    birthday: row.birthday || '',
    deptId: row.deptId,
    title: row.title,
    specialty: row.specialty,
    introduction: row.introduction,
    yearsOfExperience: row.yearsOfExperience || 0,
    education: row.education || '',
    certificates: row.certificates || '',
    consultationFee: row.consultationFee,
    status: row.status
  })
  dialogVisible.value = true
}

// 查看详情
const viewDetail = (row) => {
  selectedDoctor.value = row
  detailVisible.value = true
}

// 删除中医师
const handleDeleteDoctor = async (row) => {
  // 检查ID是否有效
  if (!row.id || row.id === 0) {
    message.error('中医师ID无效，无法删除')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除中医师 ${row.doctorName || row.realName} 吗？删除后将同时删除关联的用户账号。`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    loading.value = true
    // ID是字符串格式，直接传递给后端
    await deleteDoctorApi(row.id)

    message.success('删除成功')
    
    // 清除缓存并重新加载数据
    try {
      await refreshDoctorCache()
    } catch (e) {

    }
    await loadDoctors()
  } catch (error) {
    if (error !== 'cancel') {

      message.error(error.response?.data?.message || '删除失败')
    }
  } finally {
    loading.value = false
  }
}

// 保存中医师
const saveDoctorHandler = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      // 构造中医师数据
      const doctorData = {
        doctorName: form.realName,
        phone: form.phone,
        gender: form.gender,
        birthday: form.birthday,
        deptId: form.deptId, // 保持原始格式，后端会自动转换
        title: form.title,
        specialty: form.specialty,
        introduction: form.introduction,
        yearsOfExperience: form.yearsOfExperience,
        education: form.education,
        certificates: form.certificates,
        rating: 5.00,
        consultationFee: form.consultationFee,
        status: form.status
      }


      if (isEdit.value) {
        doctorData.id = form.id
        await updateDoctor(doctorData)
      } else {
        await addDoctor(doctorData)
      }

      message.success(isEdit.value ? '编辑成功' : '添加成功')
      dialogVisible.value = false
      
      // 清除缓存并重新加载数据
      try {
        await refreshDoctorCache()
      } catch (e) {

      }
      await loadDoctors()
    } catch (error) {

      message.error(error.response?.data?.message || '保存失败')
    }
  })
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    realName: '',
    phone: '',
    gender: 0,
    birthday: '',
    deptId: null,
    title: '',
    specialty: '',
    introduction: '',
    yearsOfExperience: 0,
    education: '',
    certificates: '',
    consultationFee: 50,
    status: 1
  })
  formRef.value?.clearValidate()
}

// 切换状态
const toggleStatus = async (row) => {
  const newStatus = row.status === 1 ? 0 : 1
  const action = newStatus === 1 ? '启用' : '禁用'

  try {
    await ElMessageBox.confirm(`确定要${action}此医生吗？`, '提示', {
      type: 'warning'
    })

    loading.value = true
    await updateDoctorStatus(row.id, newStatus)
    
    // 立即更新本地数据
    row.status = newStatus
    message.success(`${action}成功`)
    
    // 清除缓存并重新加载数据
    try {
      await refreshDoctorCache()
    } catch (e) {

    }
    await loadDoctors()
  } catch (error) {
    if (error !== 'cancel') {

      message.error(error.response?.data?.message || '状态更新失败')
    }
  } finally {
    loading.value = false
  }
}

// 获取性别文本
const getGenderText = (gender) => {
  const textMap = { 0: '未知', 1: '男', 2: '女' }
  return textMap[gender] || '未知'
}

// 获取默认头像
const getDefaultAvatar = (row) => {
  if (row.avatar) return row.avatar
  // 使用医生ID生成默认头像
  const seed = row.id || row.userId || 'doctor'
  return `https://api.dicebear.com/7.x/thumbs/svg?seed=${seed}`
}

// 获取头像URL（优先使用row.avatar，如果为空则使用默认头像）
const getAvatarUrl = (row) => {
  if (row.avatar && row.avatar.trim() !== '') {
    return row.avatar
  }
  return getDefaultAvatar(row)
}

// 处理头像加载错误
const handleAvatarError = (event, row) => {
  if (!event?.target) return
  const defaultAvatar = getDefaultAvatar(row)
  // 如果当前src不是默认头像，则替换为默认头像
  if (event.target.src !== defaultAvatar) {
    event.target.src = defaultAvatar
  }
}

// 获取状态类型
const getStatusType = (status) => {
  const typeMap = { 0: 'info', 1: 'success' }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = { 0: '离职', 1: '在职' }
  return textMap[status] || '未知'
}

// 刷新缓存并重新加载数据
const handleRefresh = async () => {
  try {
    loading.value = true
    await refreshDoctorCache()
    await loadDoctors()
    message.success('刷新成功')
  } catch (error) {

    message.error('刷新失败')
  } finally {
    loading.value = false
  }
}

// 切换推荐首页状态
const toggleRecommended = async (row) => {
  try {
    // TODO: 调用API更新推荐状态
    // await updateDoctorRecommended(row.id, row.isRecommended)
    message.success(row.isRecommended ? '已推荐到首页' : '已取消推荐')
    
    // 清除缓存并重新加载数据
    try {
      await refreshDoctorCache()
    } catch (e) {
      // 静默失败
    }
  } catch (error) {
    // 如果失败，恢复原状态
    row.isRecommended = !row.isRecommended
    message.error('更新推荐状态失败')
  }
}

onMounted(async () => {
  // 先加载数据，确保页面快速显示
  await loadDepartments()
  await loadDoctors()
  
  // 异步刷新缓存，确保数据最新（不阻塞页面显示）
  setTimeout(async () => {
    try {
      await refreshDoctorCache()
      await loadDoctors()
    } catch (error) {

      // 静默失败，不影响用户体验
    }
  }, 100)
})
</script>

<style scoped lang="scss">
@use '@/styles/admin-variables.scss' as *;
@use '@/styles/admin-common.scss' as *;

.doctor-manage-container {
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
