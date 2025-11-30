<template>
  <div class="admin-layout">
    <AdminSidebar 
      :active-key="activeKey"
      :sidebar-open="sidebarOpen"
      @menu-click="handleMenuClick"
    />
    <div class="layout-content">
      <AdminHeader 
        :breadcrumbs="breadcrumbs"
        :sidebar-open="sidebarOpen"
        @toggle-sidebar="toggleSidebar"
      />
      <AdminTagsView 
        :tabs="tabs"
        :active-key="activeKey"
        @tab-click="handleTabClick"
        @tab-close="handleTabClose"
        @close-all="handleCloseAll"
      />
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminSidebar from '@/components/admin/AdminSidebar.vue'
import AdminHeader from '@/components/admin/AdminHeader.vue'
import AdminTagsView from '@/components/admin/AdminTagsView.vue'

const route = useRoute()
const router = useRouter()

const sidebarOpen = ref(true)
const activeKey = ref('home')
const tabs = ref([
  { key: 'home', title: '首页', closable: false }
])

const titleMap = {
  home: '首页',
  system: '系统管理',
  doctor: '医生管理',
  role: '角色管理',
  menu: '菜单管理',
  patient: '患者管理',
  department: '科室管理',
  schedule: '排班管理',
  appointment: '预约管理',
  record: '就诊记录',
  news: '资讯管理',
  feedback: '反馈管理',
  notice: '公告管理',
  settings: '系统设置',
  settingsTest: '设置生效检测',
  statistics: '数据统计',
  logs: '操作日志',
  dialogue: '智能对话',
  profile: '个人信息'
}

const breadcrumbs = computed(() => {
  if (activeKey.value === 'home') {
    return ['首页']
  }
  if (['doctor', 'role', 'patient'].includes(activeKey.value)) {
    return ['首页', '用户管理', titleMap[activeKey.value]]
  }
  if (['menu', 'settings', 'settingsTest', 'statistics', 'logs'].includes(activeKey.value)) {
    return ['首页', '系统管理', titleMap[activeKey.value]]
  }
  if (['department', 'schedule', 'appointment', 'record'].includes(activeKey.value)) {
    return ['首页', '业务管理', titleMap[activeKey.value]]
  }
  if (['news', 'feedback', 'notice'].includes(activeKey.value)) {
    return ['首页', '内容管理', titleMap[activeKey.value]]
  }
  return ['首页', titleMap[activeKey.value]]
})

const handleMenuClick = (key, title) => {
  activeKey.value = key
  
  // 添加到标签页
  if (!tabs.value.find(t => t.key === key)) {
    tabs.value.push({ 
      key, 
      title, 
      closable: key !== 'home' 
    })
  }

  // 路由跳转
  const routeMap = {
    home: '/admin/dashboard',
    doctor: '/admin/doctors',
    role: '/admin/role',
    menu: '/admin/menu',
    patient: '/admin/patients',
    department: '/admin/departments',
    schedule: '/admin/schedules',
    appointment: '/admin/appointments',
    record: '/admin/records',
    news: '/admin/news',
    feedback: '/admin/feedback',
    notice: '/admin/notice',
    settings: '/admin/settings',
    settingsTest: '/admin/settings/test',
    statistics: '/admin/statistics',
    logs: '/admin/logs',
    dialogue: '/admin/dialogue',
    profile: '/admin/profile'
  }

  if (routeMap[key]) {
    router.push(routeMap[key])
  }
}

const handleTabClick = (key) => {
  activeKey.value = key
  const routeMap = {
    home: '/admin/dashboard',
    doctor: '/admin/doctors',
    role: '/admin/role',
    menu: '/admin/menu',
    patient: '/admin/patients',
    department: '/admin/departments',
    schedule: '/admin/schedules',
    appointment: '/admin/appointments',
    record: '/admin/records',
    news: '/admin/news',
    feedback: '/admin/feedback',
    notice: '/admin/notice',
    settings: '/admin/settings',
    settingsTest: '/admin/settings/test',
    statistics: '/admin/statistics',
    logs: '/admin/logs',
    dialogue: '/admin/dialogue',
    profile: '/admin/profile'
  }

  if (routeMap[key]) {
    router.push(routeMap[key])
  }
}

const handleTabClose = (key) => {
  const newTabs = tabs.value.filter(t => t.key !== key)
  tabs.value = newTabs
  
  // 如果关闭的是当前激活的标签，切换到最后一个
  if (activeKey.value === key && newTabs.length > 0) {
    const lastTab = newTabs[newTabs.length - 1]
    activeKey.value = lastTab.key
    handleTabClick(lastTab.key)
  }
}

const handleCloseAll = () => {
  // 只保留首页标签
  tabs.value = tabs.value.filter(t => !t.closable)
  activeKey.value = 'home'
  router.push('/admin/dashboard')
}

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

// 监听路由变化，更新激活的标签
watch(() => route.path, (newPath) => {
  const pathKeyMap = {
    '/admin/dashboard': 'home',
    '/admin/doctors': 'doctor',
    '/admin/role': 'role',
    '/admin/menu': 'menu',
    '/admin/patients': 'patient',
    '/admin/departments': 'department',
    '/admin/schedules': 'schedule',
    '/admin/appointments': 'appointment',
    '/admin/records': 'record',
    '/admin/news': 'news',
    '/admin/feedback': 'feedback',
    '/admin/notice': 'notice',
    '/admin/settings': 'settings',
    '/admin/settings/test': 'settingsTest',
    '/admin/statistics': 'statistics',
    '/admin/logs': 'logs',
    '/admin/dialogue': 'dialogue',
    '/admin/profile': 'profile'
  }
  
  if (pathKeyMap[newPath]) {
    activeKey.value = pathKeyMap[newPath]
    
    // 如果标签页不存在，添加它
    if (!tabs.value.find(t => t.key === activeKey.value)) {
      tabs.value.push({
        key: activeKey.value,
        title: titleMap[activeKey.value],
        closable: activeKey.value !== 'home'
      })
    }
  }
}, { immediate: true })
</script>

<style scoped lang="scss">
.admin-layout {
  display: flex;
  height: 100vh;
  width: 100%;
  background: #f0f2f5;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif;

  .layout-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    overflow: hidden;
    transition: margin-left 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .main-content {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    background: #f0f2f5;
  }
}
</style>

