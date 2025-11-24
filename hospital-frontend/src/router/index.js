import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getAppConfig } from '@/config/runtimeConfig'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册' }
  },
  {
    path: '/search',
    name: 'SearchResult',
    component: () => import('@/views/SearchResult.vue'),
    meta: { title: '搜索结果' }
  },

  // ==================== 患者端路由 ====================
  {
    path: '/patient',
    component: () => import('@/layout/PatientLayout.vue'),
    redirect: '/patient/home',
    meta: { roles: [1] },
    children: [
      {
        path: 'home',
        name: 'PatientHome',
        component: () => import('@/views/patient/Home.vue'),
        meta: { title: '首页', roles: [1] }
      },
      {
        path: 'departments',
        name: 'PatientDepartments',
        component: () => import('@/views/patient/Departments.vue'),
        meta: { title: '中医分类', roles: [1] }
      },
      {
        path: 'doctors',
        name: 'PatientDoctors',
        component: () => import('@/views/patient/Doctors.vue'),
        meta: { title: '中医师列表', roles: [1] }
      },
      {
        path: 'appointment',
        name: 'PatientAppointment',
        component: () => import('@/views/patient/Appointment.vue'),
        meta: { title: '中医师预约', roles: [1] }
      },
      {
        path: 'my-appointments',
        name: 'PatientMyAppointments',
        component: () => import('@/views/patient/MyAppointments.vue'),
        meta: { title: '我的预约', roles: [1] }
      },
      {
        path: 'profile',
        name: 'PatientProfile',
        component: () => import('@/views/patient/Profile.vue'),
        meta: { title: '个人中心', roles: [1] }
      },
      {
        path: 'notifications',
        name: 'PatientNotificationCenter',
        component: () => import('@/views/patient/NotificationCenter.vue'),
        meta: { title: '消息中心', roles: [1] }
      },
      {
        path: 'dialogue',
        name: 'PatientDialogue',
        component: () => import('@/views/dialogue/DialogPage.vue'),
        meta: { title: '智能对话', roles: [1] }
      },

      // ==================== 体质测试模块 ====================
      // 体质测试路由保留，但不在菜单中显示，只能通过"就诊中"状态的提醒进入
      {
        path: 'constitution/test',
        name: 'ConstitutionTest',
        component: () => import('@/views/patient/constitution/ConstitutionTest.vue'),
        meta: { title: '体质测试', roles: [1] }
      },
      {
        path: 'constitution/result/:id?',
        name: 'TestResult',
        component: () => import('@/views/patient/constitution/TestResult.vue'),
        meta: { title: '测试结果', roles: [1] }
      },
      {
        path: 'constitution/history',
        name: 'TestHistory',
        component: () => import('@/views/patient/constitution/TestHistory.vue'),
        meta: { title: '测试历史', roles: [1] }
      },

      // ==================== 药膳推荐模块 ====================
      {
        path: 'recipe',
        name: 'RecipeList',
        component: () => import('@/views/patient/recipe/RecipeList.vue'),
        meta: { title: '药膳推荐', roles: [1] }
      },
      {
        path: 'recipe/detail/:id',
        name: 'RecipeDetail',
        component: () => import('@/views/patient/recipe/RecipeDetail.vue'),
        meta: { title: '药膳详情', roles: [1] }
      },
      {
        path: 'recipe/my',
        name: 'MyRecipes',
        component: () => import('@/views/patient/recipe/MyRecipes.vue'),
        meta: { title: '我的药膳', roles: [1] }
      },

      // ==================== 穴位按摩模块 ====================
      {
        path: 'acupoint',
        redirect: '/patient/acupoint/list'
      },
      {
        path: 'acupoint/list',
        name: 'AcupointList',
        component: () => import('@/views/patient/acupoint/AcupointList.vue'),
        meta: { title: '穴位列表', roles: [1] }
      },
      {
        path: 'acupoint/detail/:id',
        name: 'AcupointDetail',
        component: () => import('@/views/patient/acupoint/AcupointDetail.vue'),
        meta: { title: '穴位详情', roles: [1] }
      },
      {
        path: 'acupoint/combination',
        name: 'CombinationList',
        component: () => import('@/views/patient/acupoint/CombinationList.vue'),
        meta: { title: '组合方案', roles: [1] }
      },
      {
        path: 'acupoint/combination/:id',
        name: 'CombinationDetail',
        component: () => import('@/views/patient/acupoint/CombinationDetail.vue'),
        meta: { title: '组合详情', roles: [1] }
      },

      // ==================== 养生知识社区模块 ====================
      {
        path: 'community',
        redirect: '/patient/community/articles'
      },
      {
        path: 'community/articles',
        name: 'ArticleList',
        component: () => import('@/views/patient/community/ArticleList.vue'),
        meta: { title: '养生社区', roles: [1] }
      },
      {
        path: 'community/article/:id',
        name: 'ArticleDetail',
        component: () => import('@/views/patient/community/ArticleDetail.vue'),
        meta: { title: '文章详情', roles: [1] }
      },
      {
        path: 'community/publish',
        name: 'ArticlePublish',
        component: () => import('@/views/patient/community/ArticlePublish.vue'),
        meta: { title: '发布文章', roles: [1] }
      },
      {
        path: 'community/edit/:id',
        name: 'ArticleEdit',
        component: () => import('@/views/patient/community/ArticlePublish.vue'),
        meta: { title: '编辑文章', roles: [1] }
      },
      {
        path: 'community/my-articles',
        name: 'MyArticles',
        component: () => import('@/views/patient/community/MyArticles.vue'),
        meta: { title: '我的文章', roles: [1] }
      },
      {
        path: 'community/favorites',
        name: 'MyFavorites',
        component: () => import('@/views/patient/community/MyFavorites.vue'),
        meta: { title: '我的收藏', roles: [1] }
      },

      // ==================== 个人健康档案模块 ====================
      {
        path: 'health/profile',
        name: 'HealthProfile',
        component: () => import('@/views/patient/health/HealthProfile.vue'),
        meta: { title: '健康档案', roles: [1] }
      },
      {
        path: 'health/plan',
        name: 'HealthPlan',
        component: () => import('@/views/patient/health/HealthPlan.vue'),
        meta: { title: '健康计划', roles: [1] }
      },
      {
        path: 'health/checkin',
        name: 'HealthCheckin',
        component: () => import('@/views/patient/health/HealthCheckin.vue'),
        meta: { title: '健康打卡', roles: [1] }
      },
      {
        path: 'health/statistics',
        name: 'HealthStatistics',
        component: () => import('@/views/patient/health/HealthStatistics.vue'),
        meta: { title: '健康统计', roles: [1] }
      },
      {
        path: 'health/report',
        name: 'HealthReport',
        component: () => import('@/views/patient/health/HealthReport.vue'),
        meta: { title: '健康报告', roles: [1] }
      }
    ]
  },

  // ==================== 医生端路由 ====================
  {
    path: '/doctor',
    component: () => import('@/layout/DoctorLayout.vue'),
    redirect: '/doctor/dashboard',
    meta: { roles: [2] },
    children: [
      {
        path: 'dashboard',
        name: 'DoctorDashboard',
        component: () => import('@/views/doctor/Dashboard.vue'),
        meta: { title: '工作台', roles: [2] }
      },
      {
        path: 'schedule',
        name: 'DoctorSchedule',
        component: () => import('@/views/doctor/Schedule.vue'),
        meta: { title: '我的排班', roles: [2] }
      },
      {
        path: 'patients',
        name: 'DoctorPatients',
        component: () => import('@/views/doctor/Patients.vue'),
        meta: { title: '患者管理', roles: [2] }
      },
      {
        path: 'records',
        name: 'DoctorRecords',
        component: () => import('@/views/doctor/ConsultationRecords.vue'),
        meta: { title: '接诊记录', roles: [2] }
      },
      {
        path: 'reviews',
        name: 'DoctorReviews',
        component: () => import('@/views/doctor/Reviews.vue'),
        meta: { title: '患者评价', roles: [2] }
      },
      {
        path: 'settings',
        name: 'DoctorSettings',
        component: () => import('@/views/doctor/Settings.vue'),
        meta: { title: '个人设置', roles: [2] }
      },
      {
        path: 'dialogue',
        name: 'DoctorDialogue',
        component: () => import('@/views/dialogue/DialogPage.vue'),
        meta: { title: '智能对话', roles: [2] }
      }
    ]
  },

  // ==================== 管理员端路由 ====================
  {
    path: '/admin',
    component: () => import('@/layout/AdminLayout.vue'),
    redirect: '/admin/dashboard',
    meta: { roles: [3] },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '系统概览', roles: [3] }
      },
      {
        path: 'departments',
        name: 'AdminDepartments',
        component: () => import('@/views/admin/DepartmentManage.vue'),
        meta: { title: '中医分类管理', roles: [3] }
      },
      {
        path: 'doctors',
        name: 'AdminDoctors',
        component: () => import('@/views/admin/DoctorManage.vue'),
        meta: { title: '中医师管理', roles: [3] }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/UserManage.vue'),
        meta: { title: '用户管理', roles: [3] }
      },
      {
        path: 'schedules',
        name: 'AdminSchedules',
        component: () => import('@/views/admin/ScheduleManage.vue'),
        meta: { title: '排班管理', roles: [3] }
      },
      {
        path: 'appointments',
        name: 'AdminAppointments',
        component: () => import('@/views/admin/AppointmentManage.vue'),
        meta: { title: '预约管理', roles: [3] }
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/views/admin/SystemSettings.vue'),
        meta: { title: '系统设置', roles: [3] }
      },
      {
        path: 'settings/test',
        name: 'AdminSettingsTest',
        component: () => import('@/views/admin/SystemSettingsTest.vue'),
        meta: { title: '设置生效检测', roles: [3] }
      },
      {
        path: 'statistics',
        name: 'AdminStatistics',
        component: () => import('@/views/admin/Statistics.vue'),
        meta: { title: '数据统计', roles: [3] }
      },
      {
        path: 'logs',
        name: 'AdminLogs',
        component: () => import('@/views/admin/OperationLogs.vue'),
        meta: { title: '操作日志', roles: [3] }
      },
      {
        path: 'dialogue',
        name: 'AdminDialogue',
        component: () => import('@/views/dialogue/DialogPage.vue'),
        meta: { title: '智能对话', roles: [3] }
      },
      {
        path: 'profile',
        name: 'AdminProfile',
        component: () => import('@/views/admin/Profile.vue'),
        meta: { title: '个人信息', roles: [3] }
      }
    ]
  },

  // 默认跳转
  {
    path: '/',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/**
 * 根据角色获取首页路径
 */
function getHomeByRole(roleType) {
  const homeMap = {
    1: '/patient/home',    // 患者
    2: '/doctor/dashboard', // 医生
    3: '/admin/dashboard'   // 管理员
  }
  return homeMap[roleType] || '/login'
}

// 路由守卫
router.beforeEach((to, from, next) => {
  const appConfig = getAppConfig()
  const systemTitle = appConfig?.systemInfo?.name || '中医体质辨识系统'
  document.title = to.meta.title ? `${to.meta.title} - ${systemTitle}` : systemTitle

  const userStore = useUserStore()
  const roleType = userStore.userInfo?.roleType

  // 白名单路由（不需要登录）
  const whiteList = ['/login', '/register']

  // 1. 未登录
  if (!userStore.token) {
    if (whiteList.includes(to.path)) {
      next()
    } else {
      next('/login')
    }
    return
  }

  // 2. 已登录但角色类型无效，清除登录状态并跳转到登录页
  if (!roleType || ![1, 2, 3].includes(roleType)) {
    if (whiteList.includes(to.path)) {
      // 允许访问登录页，但清除无效token
      userStore.logout()
      next()
    } else {
      userStore.logout()
      next('/login')
    }
    return
  }

  // 3. 已登录，访问登录/注册页，跳转到对应角色首页
  if (to.path === '/login' || to.path === '/register') {
    next(getHomeByRole(roleType))
    return
  }

  // 4. 已登录，访问根路径，跳转到对应角色首页
  if (to.path === '/') {
    next(getHomeByRole(roleType))
    return
  }

  // 5. 权限验证：检查当前路由是否允许该角色访问
  if (to.meta.roles && !to.meta.roles.includes(roleType)) {
    // 无权限，跳转到对应角色的首页
    next(getHomeByRole(roleType))
    return
  }

  next()
})

export default router


