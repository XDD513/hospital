<template>
  <div class="doctor-layout">
    <DoctorSidebar 
      :active-key="activeKey"
      :sidebar-open="sidebarOpen"
      @menu-click="handleMenuClick"
    />
    <div class="layout-content">
      <DoctorHeader 
        :breadcrumbs="breadcrumbs"
        :sidebar-open="sidebarOpen"
        @toggle-sidebar="toggleSidebar"
      />
      <DoctorTagsView 
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
import DoctorSidebar from '@/components/doctor/DoctorSidebar.vue'
import DoctorHeader from '@/components/doctor/DoctorHeader.vue'
import DoctorTagsView from '@/components/doctor/DoctorTagsView.vue'

const route = useRoute()
const router = useRouter()

const sidebarOpen = ref(true)
const activeKey = ref('dashboard')
const tabs = ref([
  { key: 'dashboard', title: '工作台', closable: false }
])

const titleMap = {
  dashboard: '工作台',
  schedule: '我的排班',
  patients: '患者管理',
  records: '接诊记录',
  reviews: '患者评价',
  dialogue: '智能对话',
  settings: '个人设置'
}

const breadcrumbs = computed(() => {
  if (activeKey.value === 'dashboard') {
    return ['工作台']
  }
  return ['工作台', titleMap[activeKey.value]]
})

const handleMenuClick = (key, title) => {
  activeKey.value = key
  
  // 添加到标签页
  if (!tabs.value.find(t => t.key === key)) {
    tabs.value.push({ 
      key, 
      title, 
      closable: key !== 'dashboard' 
    })
  }

  // 路由跳转
  const routeMap = {
    dashboard: '/doctor/dashboard',
    schedule: '/doctor/schedule',
    patients: '/doctor/patients',
    records: '/doctor/records',
    reviews: '/doctor/reviews',
    dialogue: '/doctor/dialogue',
    settings: '/doctor/settings'
  }

  if (routeMap[key]) {
    router.push(routeMap[key])
  }
}

const handleTabClick = (key) => {
  activeKey.value = key
  const routeMap = {
    dashboard: '/doctor/dashboard',
    schedule: '/doctor/schedule',
    patients: '/doctor/patients',
    records: '/doctor/records',
    reviews: '/doctor/reviews',
    dialogue: '/doctor/dialogue',
    settings: '/doctor/settings'
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
  // 只保留工作台标签
  tabs.value = tabs.value.filter(t => !t.closable)
  activeKey.value = 'dashboard'
  router.push('/doctor/dashboard')
}

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

// 监听路由变化，更新激活的标签
watch(() => route.path, (newPath) => {
  const pathKeyMap = {
    '/doctor/dashboard': 'dashboard',
    '/doctor/schedule': 'schedule',
    '/doctor/patients': 'patients',
    '/doctor/records': 'records',
    '/doctor/reviews': 'reviews',
    '/doctor/dialogue': 'dialogue',
    '/doctor/settings': 'settings'
  }
  
  if (pathKeyMap[newPath]) {
    activeKey.value = pathKeyMap[newPath]
    
    // 如果标签页不存在，添加它
    if (!tabs.value.find(t => t.key === activeKey.value)) {
      tabs.value.push({
        key: activeKey.value,
        title: titleMap[activeKey.value],
        closable: activeKey.value !== 'dashboard'
      })
    }
  }
}, { immediate: true })
</script>

<style scoped lang="scss">
.doctor-layout {
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
