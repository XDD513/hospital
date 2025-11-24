<template>
  <div class="settings-container">
    <el-row :gutter="20">
      <!-- 个人信息 -->
      <el-col :xs="24" :md="8">
        <div class="doctor-card">
          <div class="card-header">
            <h3>
              <el-icon>
                <User />
              </el-icon>
              个人信息
            </h3>
          </div>
          <div class="card-body">
            <div class="profile-info">
              <el-avatar :size="100" :src="doctorStore.doctorInfo?.avatar">
                <el-icon :size="50">
                  <User />
                </el-icon>
              </el-avatar>
              <h2>{{ doctorStore.doctorInfo?.doctorName || userStore.userInfo.realName }}</h2>
              <p>{{ doctorStore.doctorInfo?.title }} | {{ doctorStore.doctorInfo?.deptName }}</p>
              <el-button type="primary" @click="showEditDialog" style="margin-top: 15px">
                <el-icon>
                  <Edit />
                </el-icon>
                编辑资料
              </el-button>
            </div>
          </div>
        </div>

        <!-- 统计信息 -->
        <div class="doctor-card" style="margin-top: 20px">
          <div class="card-body">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="累计接诊">
                {{ doctorStore.doctorInfo?.consultationCount || 0 }} 人次
              </el-descriptions-item>
              <el-descriptions-item label="平均评分">
                <el-rate :model-value="doctorStore.doctorInfo?.rating || 0" disabled />
              </el-descriptions-item>
              <el-descriptions-item label="挂号费">
                ¥{{ doctorStore.doctorInfo?.consultationFee || 0 }}
              </el-descriptions-item>
              <el-descriptions-item label="从业年限">
                {{ doctorStore.doctorInfo?.yearsOfExperience || 0 }} 年
              </el-descriptions-item>
              <el-descriptions-item label="账号状态">
                <span :class="['status-tag', doctorStore.doctorInfo?.status === 1 ? 'success' : 'warning']">
                  <span class="status-dot"></span>
                  {{ doctorStore.doctorInfo?.status === 1 ? '在职' : '休假' }}
                </span>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </div>
      </el-col>

      <!-- 设置选项 -->
      <el-col :xs="24" :md="16">
        <!-- 基本设置 -->
        <div class="doctor-card">
          <div class="card-header">
            <h3>
              <el-icon>
                <Setting />
              </el-icon>
              基本设置
            </h3>
          </div>
          <div class="card-body">
            <el-form label-width="120px">
              <el-form-item label="专长">
                <el-input v-model="basicForm.specialty" type="textarea" :rows="2" placeholder="请输入您的专长领域" />
              </el-form-item>
              <el-form-item label="个人简介">
                <el-input v-model="basicForm.introduction" type="textarea" :rows="4" placeholder="请输入个人简介" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveBasicInfo" :loading="doctorStore.loading">
                  <el-icon>
                    <Check />
                  </el-icon>
                  保存基本信息
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>

        <!-- 通知设置 -->
        <el-card shadow="never" style="margin-top: 20px">
          <template #header>
            <h3>通知设置</h3>
          </template>
          <el-form label-width="120px">
            <el-form-item label="预约提醒">
              <el-switch v-model="notificationSettings.appointmentReminder" />
              <span style="margin-left: 10px; color: #909399">新预约时通知</span>
            </el-form-item>
            <el-form-item label="短信提醒">
              <el-switch v-model="notificationSettings.smsReminder" />
              <span style="margin-left: 10px; color: #909399">就诊前短信提醒</span>
            </el-form-item>
            <el-form-item label="评价通知">
              <el-switch v-model="notificationSettings.reviewNotification" />
              <span style="margin-left: 10px; color: #909399">新评价时通知</span>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveNotificationSettings">保存通知设置</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 安全设置 -->
        <el-card shadow="never" style="margin-top: 20px">
          <template #header>
            <h3>安全设置</h3>
          </template>
          <el-form label-width="120px">
            <el-form-item label="修改密码">
              <el-button type="primary" @click="changePasswordVisible = true">
                <el-icon>
                  <Lock />
                </el-icon>
                修改密码
              </el-button>
            </el-form-item>
            <el-form-item label="手机号">
              <span>{{ userStore.userInfo.phone }}</span>
              <el-button link type="primary" style="margin-left: 15px">修改</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <!-- 编辑资料弹窗 -->
    <el-dialog v-model="editDialogVisible" title="编辑个人资料" width="600px">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="头像">
          <div class="avatar-upload">
            <el-avatar :size="80" :src="avatarPreview || editForm.avatar || doctorStore.doctorInfo?.avatar">
              <el-icon :size="40">
                <User />
              </el-icon>
            </el-avatar>
            <div class="upload-tip">
              <el-upload class="avatar-uploader-inline" :action="uploadAction" :headers="uploadHeaders"
                :show-file-list="false" :before-upload="beforeAvatarUpload" :on-success="handleAvatarSuccess"
                :on-error="handleAvatarError">
                <el-button type="primary" size="small">上传头像</el-button>
              </el-upload>
            </div>
          </div>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名">
              <el-input v-model="editForm.doctorName" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号">
              <el-input v-model="editForm.phone" placeholder="请输入手机号" maxlength="11" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别">
              <el-radio-group v-model="editForm.gender">
                <el-radio :label="1">男</el-radio>
                <el-radio :label="2">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="从业年限">
              <el-input-number v-model="editForm.yearsOfExperience" :min="0" :max="50" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="职称">
          <el-select v-model="editForm.title" style="width: 100%" placeholder="请选择职称">
            <el-option label="主任中医师" value="主任中医师" />
            <el-option label="副主任中医师" value="副主任中医师" />
            <el-option label="主治中医师" value="主治中医师" />
            <el-option label="中医师" value="中医师" />
          </el-select>
        </el-form-item>
        <el-form-item label="专长">
          <el-input v-model="editForm.specialty" type="textarea" :rows="2" placeholder="请输入您的专长领域" />
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input v-model="editForm.introduction" type="textarea" :rows="3" placeholder="请输入个人简介" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProfile" :loading="doctorStore.loading">保存</el-button>
      </template>
    </el-dialog>

    <!-- 修改密码弹窗 -->
    <el-dialog v-model="changePasswordVisible" title="修改密码" width="450px">
      <el-form :model="passwordForm" label-width="100px">
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="changePasswordVisible = false">取消</el-button>
        <el-button type="primary" @click="handleChangePassword">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useDoctorStore } from '@/stores/doctor'

import { User, Lock, Edit, Setting, Check, Bell } from '@element-plus/icons-vue'
import request from '@/api/request'
import { getUserInfo, changePassword, getUserSettings, updateUserSettings } from '@/api/user'
import { generatePresignedUrl } from '@/api/oss'
import { useAvatarUpload } from '@/composables/useAvatarUpload'

const router = useRouter()
const userStore = useUserStore()
const doctorStore = useDoctorStore()

// 弹窗状态
const editDialogVisible = ref(false)
const changePasswordVisible = ref(false)

// 头像预览
const avatarPreview = ref('')

// 上传配置
const uploadAction = computed(() => {
  const baseURL = request.defaults.baseURL || '/api'
  return baseURL + '/upload/avatar'
})

const uploadHeaders = computed(() => {
  const token = userStore.token
  return token
    ? {
        Authorization: `Bearer ${token}`
      }
    : {}
})

// 基础信息表单
const basicForm = reactive({
  specialty: '',
  introduction: ''
})

// 通知设置
const notificationSettings = reactive({
  appointmentReminder: true,
  smsReminder: true,
  reviewNotification: true
})

// 编辑表单
const editForm = reactive({
  avatar: '',
  doctorName: '',
  phone: '',
  gender: 1,
  title: '',
  specialty: '',
  introduction: '',
  yearsOfExperience: 0
})

// 密码表单
const passwordForm = reactive({
  newPassword: '',
  confirmPassword: ''
})

// 清理头像URL，移除OSS签名参数
const sanitizeAvatarUrl = (avatarUrl) => {
  if (!avatarUrl) return ''
  // 移除?号及其后面的所有参数（OSS签名参数）
  const questionIndex = avatarUrl.indexOf('?')
  if (questionIndex > 0) {
    return avatarUrl.substring(0, questionIndex)
  }
  return avatarUrl
}

// 显示编辑对话框
const showEditDialog = async () => {
  const info = doctorStore.doctorInfo || {}
  // 清理头像URL，移除签名参数，只保存原始URL
  const rawAvatarUrl = sanitizeAvatarUrl(info.avatar || '')
  editForm.avatar = rawAvatarUrl
  editForm.doctorName = info.doctorName || userStore.userInfo.realName || ''
  editForm.phone = info.phone || userStore.userInfo.phone || ''
  editForm.gender = info.gender || 1
  editForm.title = info.title || ''
  editForm.specialty = info.specialty || ''
  editForm.introduction = info.introduction || ''
  editForm.yearsOfExperience = info.yearsOfExperience || 0
  
  // 如果有原始URL，生成签名URL用于预览
  if (rawAvatarUrl) {
    try {
      const signedUrlResponse = await generatePresignedUrl(rawAvatarUrl, 60)
      if (signedUrlResponse && signedUrlResponse.code === 200) {
        const signedUrl = signedUrlResponse.data || signedUrlResponse.message
        if (signedUrl && signedUrl.startsWith('http')) {
          avatarPreview.value = signedUrl
        } else {
          avatarPreview.value = rawAvatarUrl
        }
      } else {
        avatarPreview.value = rawAvatarUrl
      }
    } catch (e) {
      // 如果生成签名URL失败，使用原始URL或info中的URL
      avatarPreview.value = info.avatar || rawAvatarUrl
    }
  } else {
    avatarPreview.value = ''
  }
  
  editDialogVisible.value = true
}

// 保存基本信息
const saveBasicInfo = async () => {
  const success = await doctorStore.updateInfo({
    specialty: basicForm.specialty,
    introduction: basicForm.introduction
  })
  if (success) {
    if (doctorStore.doctorInfo) {
      doctorStore.doctorInfo.specialty = basicForm.specialty
      doctorStore.doctorInfo.introduction = basicForm.introduction
    }
    message.success('保存成功')
  }
}

// 保存通知设置
const saveNotificationSettings = async () => {
  try {
    await updateUserSettings({
      appointmentReminder: notificationSettings.appointmentReminder,
      smsReminder: notificationSettings.smsReminder,
      reviewNotification: notificationSettings.reviewNotification
    })
    message.success('通知设置保存成功')
  } catch (error) {
    message.error('保存通知设置失败')
  }
}

// 保存资料
const saveProfile = async () => {
  const success = await doctorStore.updateInfo(editForm)
  if (success) {
    editDialogVisible.value = false
    avatarPreview.value = ''
    basicForm.specialty = doctorStore.doctorInfo?.specialty || ''
    basicForm.introduction = doctorStore.doctorInfo?.introduction || ''
    await refreshUserInfo()
  }
}

// 使用头像上传composable
const { beforeAvatarUpload, handleAvatarSuccess, handleAvatarError } = useAvatarUpload(avatarPreview, editForm)

// 修改密码
const handleChangePassword = async () => {
  if (!passwordForm.newPassword) {
    message.warning('请填写新密码')
    return
  }

  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    message.warning('两次密码输入不一致')
    return
  }

  if (passwordForm.newPassword.length < 6) {
    message.warning('新密码长度至少6位')
    return
  }

  try {
    const response = await changePassword({
      newPassword: passwordForm.newPassword
    })
    
    if (response.code === 200) {
      message.success('密码修改成功，请重新登录')
      changePasswordVisible.value = false
      
      // 清空表单
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
      
      setTimeout(() => {
        userStore.clearUserInfo()
        router.push('/login')
      }, 1500)
    } else {
      message.error(response.message || '修改失败')
    }
  } catch (error) {
    message.error(error?.response?.data?.message || error?.message || '修改失败')
  }
}

// 初始化时加载数据
const loadDoctorInfo = async () => {
  const info = await doctorStore.fetchDoctorInfo()
  if (info) {
    basicForm.specialty = info.specialty || ''
    basicForm.introduction = info.introduction || ''
  } else {
    basicForm.specialty = ''
    basicForm.introduction = ''
  }
}

const refreshUserInfo = async () => {
  try {
    const response = await getUserInfo()
    if (response.code === 200 && response.data) {
      userStore.setUserInfo(response.data)
      if (doctorStore.doctorInfo) {
        doctorStore.doctorInfo.avatar = response.data.avatar
        doctorStore.doctorInfo.phone = response.data.phone
        doctorStore.doctorInfo.gender = response.data.gender
      }
    }
  } catch (error) {

  }
}

// 加载用户设置
const loadSettings = async () => {
  try {
    const response = await getUserSettings()
    if (response.code === 200 && response.data) {
      notificationSettings.appointmentReminder = response.data.appointmentReminder !== false
      notificationSettings.smsReminder = response.data.smsReminder !== false
      notificationSettings.reviewNotification = response.data.reviewNotification !== false
    }
  } catch (error) {
    // 静默失败
  }
}

onMounted(() => {
  loadDoctorInfo()
  refreshUserInfo()
  loadSettings()
})
</script>

<style scoped lang="scss">
.settings-container {
  max-width: 1200px;
  margin: 0 auto;

  h3 {
    margin: 0;
    font-size: 16px;
    color: #333;
  }

  .profile-info {
    text-align: center;
    padding: 20px;

    h2 {
      margin: 15px 0 5px 0;
      font-size: 22px;
      color: #333;
    }

    p {
      margin: 0;
      color: #909399;
      font-size: 14px;
    }
  }

  .stats-row {
    margin-bottom: 20px;

    .stat-card {
      margin-bottom: 20px;
    }
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .avatar-upload {
    display: flex;
    align-items: flex-start;
    gap: 20px;

    .upload-tip {
      flex: 1;
    }

    .avatar-uploader-inline {
      margin-top: 10px;
    }

    .upload-hint {
      font-size: 12px;
      color: #999;
      margin-top: 6px;
    }
  }

  .status-tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: currentColor;
    }

    &.success {
      color: #52c41a;
    }

    &.warning {
      color: #faad14;
    }
  }
}
</style>
