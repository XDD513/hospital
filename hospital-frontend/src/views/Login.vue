<template>
  <div class="login-container">
    <div class="login-box">
      <!-- 左侧图片区域 -->
      <div class="login-left">
        <div class="hospital-info">
          <h1>{{ systemTitle }}</h1>
          <p>辨识体质 · 科学养生 · 健康生活</p>
          <div class="features">
            <div class="feature-item">
              <el-icon>
                <CircleCheck />
              </el-icon>
              <span>体质测试辨识</span>
            </div>
            <div class="feature-item">
              <el-icon>
                <Calendar />
              </el-icon>
              <span>个性化养生方案</span>
            </div>
            <div class="feature-item">
              <el-icon>
                <Document />
              </el-icon>
              <span>健康档案管理</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="login-right">
        <div class="login-form-wrapper">
          <h2>欢迎登录</h2>
          <p class="subtitle">请输入您的账号和密码</p>

          <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" @submit.prevent="handleLogin">
            <el-form-item prop="username">
              <el-input v-model="loginForm.username" placeholder="请输入用户名" size="large" :prefix-icon="User" clearable
                @blur="handleFieldBlur('username')" />
            </el-form-item>

            <el-form-item prop="password">
              <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" size="large"
                :prefix-icon="Lock" show-password clearable @keyup.enter="handleLogin" @blur="handleFieldBlur('password')" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" size="large" :loading="loading" @click="handleLogin" class="login-button">
                {{ loading ? '登录中...' : '登 录' }}
              </el-button>
            </el-form-item>

            <div class="form-footer">
              <span>还没有账号？</span>
              <el-link type="primary" @click="goToRegister">立即注册</el-link>
            </div>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject, computed } from 'vue'
import { useRouter } from 'vue-router'
import message from '@/plugins/message'
import { User, Lock, CircleCheck, Calendar, Document } from '@element-plus/icons-vue'
import { login, getUserInfo } from '@/api/user'
import { useUserStore } from '@/stores/user'
import { getAppConfig } from '@/config/runtimeConfig'
import { useFormValidation } from '@/composables/useFormValidation'

const router = useRouter()
const userStore = useUserStore()
const appConfig = inject('appConfig', getAppConfig())
const systemTitle = computed(() => appConfig?.systemInfo?.name || '中医体质辨识系统')

// 表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

const loginFormRef = ref(null)
const loading = ref(false)

// 创建字段失焦处理函数
const { handleFieldBlur } = useFormValidation(loginFormRef)

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true

    try {
      const res = await login(loginForm)

      if (res.code === 200) {
        // 保存Token和用户信息
        userStore.setToken(res.data.token)
        userStore.setUserInfo(res.data)

        // 登录后立即刷新一次用户信息，获取签名后的头像等动态字段
        try {
          const infoRes = await getUserInfo()
          if (infoRes.code === 200 && infoRes.data) {
            userStore.setUserInfo(infoRes.data)
          }
        } catch (error) {

        }

        message.success('登录成功！')

        // 根据角色跳转到对应首页
        const roleType = res.data.roleType
        let homePath = '/patient/home'

        // roleType 0 或 1 都跳转到患者端
        if (roleType === 2) {
          homePath = '/doctor/dashboard'
        } else if (roleType === 3) {
          homePath = '/admin/dashboard'
        } else if (roleType === 0 || roleType === 1) {
          homePath = '/patient/home'
        }

        // 立即跳转，不使用setTimeout
        router.push(homePath)
      }
    } catch (error) {

    } finally {
      loading.value = false
    }
  })
}

// 跳转注册页
const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped lang="scss">
.login-container {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.login-box {
  width: 1000px;
  height: 600px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  overflow: hidden;
}

.login-left {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
  color: white;
}

.hospital-info {
  h1 {
    font-size: 36px;
    margin-bottom: 15px;
    font-weight: bold;
  }

  p {
    font-size: 18px;
    margin-bottom: 50px;
    opacity: 0.9;
  }
}

.features {
  .feature-item {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    font-size: 16px;

    .el-icon {
      font-size: 24px;
      margin-right: 12px;
    }
  }
}

.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 50px;
}

.login-form-wrapper {
  width: 100%;
  max-width: 380px;

  h2 {
    font-size: 28px;
    color: #333;
    margin-bottom: 10px;
    font-weight: bold;
  }

  .subtitle {
    color: #666;
    margin-bottom: 40px;
  }
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: bold;
  margin-top: 10px;
}

.form-footer {
  text-align: center;
  color: #666;
  margin-top: 20px;

  .el-link {
    margin-left: 5px;
    font-weight: bold;
  }
}

:deep(.el-input__wrapper) {
  padding: 12px 15px;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}
</style>
