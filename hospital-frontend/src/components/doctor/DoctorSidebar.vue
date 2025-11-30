<template>
  <div class="doctor-sidebar" :class="{ collapsed: !sidebarOpen }">
    <!-- Logo Area -->
    <div class="sidebar-logo">
      <div class="logo-content">
        <div class="logo-icon">
          <el-icon :size="14">
            <Tools />
          </el-icon>
        </div>
        <span class="logo-text">中医师工作台</span>
      </div>
    </div>

    <!-- Menu Items -->
    <div class="sidebar-menu scrollbar-hide">
      <!-- 工作台 -->
      <div 
        class="menu-item" 
        :class="{ active: activeKey === 'dashboard' }"
        @click="handleMenuClick('dashboard', '工作台')"
      >
        <el-icon class="menu-icon"><DataAnalysis /></el-icon>
        <span class="menu-title">工作台</span>
      </div>

      <!-- 我的排班 -->
      <div 
        class="menu-item" 
        :class="{ active: activeKey === 'schedule' }"
        @click="handleMenuClick('schedule', '我的排班')"
      >
        <el-icon class="menu-icon"><Calendar /></el-icon>
        <span class="menu-title">我的排班</span>
      </div>

      <!-- 患者管理 -->
      <div 
        class="menu-item" 
        :class="{ active: activeKey === 'patients' }"
        @click="handleMenuClick('patients', '患者管理')"
      >
        <el-icon class="menu-icon"><UserFilled /></el-icon>
        <span class="menu-title">患者管理</span>
      </div>

      <!-- 接诊记录 -->
      <div 
        class="menu-item" 
        :class="{ active: activeKey === 'records' }"
        @click="handleMenuClick('records', '接诊记录')"
      >
        <el-icon class="menu-icon"><Document /></el-icon>
        <span class="menu-title">接诊记录</span>
      </div>

      <!-- 患者评价 -->
      <div 
        class="menu-item" 
        :class="{ active: activeKey === 'reviews' }"
        @click="handleMenuClick('reviews', '患者评价')"
      >
        <el-icon class="menu-icon"><ChatDotRound /></el-icon>
        <span class="menu-title">患者评价</span>
      </div>

      <!-- 智能对话 -->
      <div 
        class="menu-item" 
        :class="{ active: activeKey === 'dialogue' }"
        @click="handleMenuClick('dialogue', '智能对话')"
      >
        <el-icon class="menu-icon"><ChatLineRound /></el-icon>
        <span class="menu-title">智能对话</span>
      </div>

      <!-- 个人设置 -->
      <div 
        class="menu-item" 
        :class="{ active: activeKey === 'settings' }"
        @click="handleMenuClick('settings', '个人设置')"
      >
        <el-icon class="menu-icon"><Setting /></el-icon>
        <span class="menu-title">个人设置</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  DataAnalysis, Calendar, UserFilled, Document, 
  ChatDotRound, ChatLineRound, Setting, Tools
} from '@element-plus/icons-vue'

const props = defineProps({
  activeKey: {
    type: String,
    default: 'dashboard'
  },
  sidebarOpen: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['menu-click'])

const handleMenuClick = (key, title) => {
  emit('menu-click', key, title)
}
</script>

<style scoped lang="scss">
.doctor-sidebar {
  width: 210px;
  background: #304156;
  color: white;
  display: flex;
  flex-direction: column;
  height: 100vh;
  flex-shrink: 0;
  transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);

  &.collapsed {
    width: 64px;

    .logo-text {
      opacity: 0;
      width: 0;
      overflow: hidden;
      transition: opacity 0.3s ease-in-out, width 0.3s ease-in-out;
    }

    .menu-title {
      opacity: 0;
      width: 0;
      overflow: hidden;
      transition: opacity 0.3s ease-in-out, width 0.3s ease-in-out;
    }
  }

  .logo-text {
    opacity: 1;
    width: auto;
    transition: opacity 0.35s ease-in-out 0.1s, width 0.35s ease-in-out 0.1s;
  }

  .menu-title {
    opacity: 1;
    width: auto;
    transition: opacity 0.35s ease-in-out 0.1s, width 0.35s ease-in-out 0.1s;
  }

  .sidebar-logo {
    height: 50px;
    background: #2b2f3a;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 16px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 10;
    transition: all 0.3s ease-in-out;

    .logo-content {
      display: flex;
      align-items: center;
      gap: 8px;
      transition: gap 0.3s ease-in-out;

      .logo-icon {
        width: 24px;
        height: 24px;
        background: #10b981;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        flex-shrink: 0;
        transition: all 0.3s ease-in-out;
      }

      .logo-text {
        color: white;
        font-size: 16px;
        white-space: nowrap;
      }
    }
  }

  .sidebar-menu {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;

    .menu-item {
      padding: 12px 16px;
      display: flex;
      align-items: center;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      color: rgb(191, 203, 217);
      position: relative;

      &:hover {
        background: #263445;
        color: white;
      }

      &.active {
        color: #409EFF;
        background: #001528;

        .menu-icon {
          color: #409EFF;
        }
      }

      .menu-icon {
        margin-right: 12px;
        font-size: 18px;
        flex-shrink: 0;
        transition: all 0.3s ease-in-out;
      }

      .menu-title {
        font-size: 14px;
        flex: 1;
        white-space: nowrap;
      }
    }
  }
}

.scrollbar-hide {
  &::-webkit-scrollbar {
    display: none;
  }
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>

