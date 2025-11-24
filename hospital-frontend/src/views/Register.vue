<template>
  <div class="register-container">
    <div class="register-box">
      <!-- 头部 -->
      <div class="register-header">
        <h1>用户注册</h1>
        <p>创建您的账号，开启健康养生之旅</p>
      </div>

      <!-- 注册表单 -->
      <div class="register-form-wrapper">
        <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" label-width="100px"
          @submit.prevent="handleRegister">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="registerForm.username" placeholder="请输入用户名（字母、数字、下划线）" clearable
              @blur="() => handleFieldBlur('username')">
              <template #prefix>
                <el-icon>
                  <User />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input v-model="registerForm.password" type="password" placeholder="请输入密码（至少6位）" show-password clearable
              @blur="handleFieldBlur('password')">
              <template #prefix>
                <el-icon>
                  <Lock />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码" show-password
              clearable @blur="handleFieldBlur('confirmPassword')">
              <template #prefix>
                <el-icon>
                  <Lock />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="真实姓名" prop="realName">
            <el-input v-model="registerForm.realName" placeholder="请输入真实姓名" clearable
              @blur="handleFieldBlur('realName')">
              <template #prefix>
                <el-icon>
                  <Avatar />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="手机号" prop="phone">
            <el-input v-model="registerForm.phone" placeholder="请输入手机号" maxlength="11" clearable
              @blur="() => handleFieldBlur('phone')">
              <template #prefix>
                <el-icon>
                  <Iphone />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="身份证号" prop="idCard">
            <el-input v-model="registerForm.idCard" placeholder="请输入身份证号（选填）" maxlength="18" clearable
              @blur="handleFieldBlur('idCard')">
              <template #prefix>
                <el-icon>
                  <Postcard />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="registerForm.gender" @change="handleFieldBlur('gender')">
              <el-radio :label="1">男</el-radio>
              <el-radio :label="2">女</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="出生日期" prop="birthDate">
            <el-date-picker v-model="registerForm.birthDate" type="date" placeholder="请选择出生日期" format="YYYY-MM-DD"
              value-format="YYYY-MM-DD" style="width: 100%" @blur="handleFieldBlur('birthDate')" />
          </el-form-item>

          <el-form-item>
            <div class="button-group">
              <el-button type="primary" size="large" :loading="loading" @click="handleRegister">
                {{ loading ? '注册中...' : '立即注册' }}
              </el-button>
              <el-button size="large" @click="goToLogin">返回登录</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

import { User, Lock, Avatar, Iphone, Postcard } from '@element-plus/icons-vue'
import { register, checkUsername, checkPhone } from '@/api/user'
import { useFormValidation } from '@/composables/useFormValidation'

const router = useRouter()

// 表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  realName: '',
  phone: '',
  idCard: '',
  gender: 0,
  birthDate: ''
})

// 自定义验证：两次密码一致
const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在3-20个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在6-20个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在2-20个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  idCard: [
    { pattern: /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/, message: '请输入正确的身份证号', trigger: 'blur' }
  ]
}

const registerFormRef = ref(null)
const loading = ref(false)

// 检查用户名是否存在
const checkUsernameExists = async () => {
  if (!registerForm.username) return

  try {
    const res = await checkUsername(registerForm.username)
    if (res.data) {
      message.warning('该用户名已被注册')
    }
  } catch (error) {

  }
}

// 检查手机号是否存在
const checkPhoneExists = async () => {
  if (!registerForm.phone) return

  try {
    const res = await checkPhone(registerForm.phone)
    if (res.data) {
      message.warning('该手机号已被注册')
    }
  } catch (error) {

  }
}

// 创建字段失焦处理函数
const { handleFieldBlur } = useFormValidation(registerFormRef, async (fieldName) => {
  // 根据字段名称执行额外的处理（如检查用户名是否存在）
  if (fieldName === 'username' && registerForm.username) {
    await checkUsernameExists()
  } else if (fieldName === 'phone' && registerForm.phone) {
    await checkPhoneExists()
  }
})

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return

  await registerFormRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true

    try {
      const res = await register(registerForm)

      if (res.code === 200) {
        message.success('注册成功！请登录')

        setTimeout(() => {
          router.push('/login')
        }, 1000)
      }
    } catch (error) {

    } finally {
      loading.value = false
    }
  })
}

// 返回登录
const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped lang="scss">
.register-container {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}

.register-box {
  width: 700px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.register-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 40px 20px;

  h1 {
    font-size: 32px;
    margin-bottom: 10px;
    font-weight: bold;
  }

  p {
    font-size: 16px;
    opacity: 0.9;
  }
}

.register-form-wrapper {
  padding: 40px 60px;
}

.button-group {
  display: flex;
  gap: 15px;
  width: 100%;

  .el-button {
    flex: 1;
    height: 45px;
    font-size: 16px;
  }
}

:deep(.el-form-item) {
  margin-bottom: 22px;
}

:deep(.el-input__wrapper) {
  padding: 10px 15px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #333;
}
</style>
