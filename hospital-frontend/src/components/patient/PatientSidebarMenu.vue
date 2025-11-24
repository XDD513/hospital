<template>
  <el-menu
    :default-active="activeMenu"
    router
    class="patient-menu"
    @select="handleSelect"
  >
    <el-menu-item index="/patient/home">
      <el-icon>
        <HomeFilled />
      </el-icon>
      <span>首页</span>
    </el-menu-item>

    <el-sub-menu index="appointment">
      <template #title>
        <el-icon>
          <Calendar />
        </el-icon>
        <span>预约挂号</span>
      </template>
      <el-menu-item index="/patient/appointment">
        <el-icon>
          <Plus />
        </el-icon>
        <span>预约挂号</span>
      </el-menu-item>
      <el-menu-item index="/patient/my-appointments">
        <el-icon>
          <Tickets />
        </el-icon>
        <span>我的预约</span>
      </el-menu-item>
      <el-menu-item index="/patient/doctors">
        <el-icon>
          <User />
        </el-icon>
        <span>中医师列表</span>
      </el-menu-item>
    </el-sub-menu>

    <el-menu-item index="/patient/constitution/history">
      <el-icon>
        <Document />
      </el-icon>
      <span>测试历史</span>
    </el-menu-item>

    <el-sub-menu index="recipe">
      <template #title>
        <el-icon>
          <Food />
        </el-icon>
        <span>药膳推荐</span>
      </template>
      <el-menu-item index="/patient/recipe">
        <el-icon>
          <List />
        </el-icon>
        <span>药膳列表</span>
      </el-menu-item>
      <el-menu-item index="/patient/recipe/my">
        <el-icon>
          <Star />
        </el-icon>
        <span>我的收藏</span>
      </el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="acupoint">
      <template #title>
        <el-icon>
          <Pointer />
        </el-icon>
        <span>穴位按摩</span>
      </template>
      <el-menu-item index="/patient/acupoint/list">
        <el-icon>
          <Location />
        </el-icon>
        <span>穴位列表</span>
      </el-menu-item>
      <el-menu-item index="/patient/acupoint/combination">
        <el-icon>
          <Connection />
        </el-icon>
        <span>组合方案</span>
      </el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="community">
      <template #title>
        <el-icon>
          <ChatDotRound />
        </el-icon>
        <span>养生社区</span>
      </template>
      <el-menu-item index="/patient/community/articles">
        <el-icon>
          <Reading />
        </el-icon>
        <span>文章列表</span>
      </el-menu-item>
      <el-menu-item index="/patient/community/my-articles">
        <el-icon>
          <EditPen />
        </el-icon>
        <span>我的文章</span>
      </el-menu-item>
      <el-menu-item index="/patient/community/favorites">
        <el-icon>
          <CollectionTag />
        </el-icon>
        <span>我的收藏</span>
      </el-menu-item>
    </el-sub-menu>

    <el-menu-item index="/patient/dialogue">
      <el-icon>
        <ChatLineRound />
      </el-icon>
      <span>智能对话</span>
    </el-menu-item>

    <el-sub-menu index="health">
      <template #title>
        <el-icon>
          <Notebook />
        </el-icon>
        <span>健康档案</span>
      </template>
      <el-menu-item index="/patient/health/profile">
        <el-icon>
          <User />
        </el-icon>
        <span>健康档案</span>
      </el-menu-item>
      <el-menu-item index="/patient/health/plan">
        <el-icon>
          <Calendar />
        </el-icon>
        <span>养生计划</span>
      </el-menu-item>
      <el-menu-item index="/patient/health/checkin">
        <el-icon>
          <CircleCheck />
        </el-icon>
        <span>健康打卡</span>
      </el-menu-item>
      <el-menu-item index="/patient/health/statistics">
        <el-icon>
          <DataAnalysis />
        </el-icon>
        <span>数据统计</span>
      </el-menu-item>
    </el-sub-menu>

    <el-menu-item index="/patient/profile">
      <el-icon>
        <Setting />
      </el-icon>
      <span>个人中心</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import {
  Calendar,
  ChatDotRound,
  ChatLineRound,
  CircleCheck,
  CollectionTag,
  Connection,
  DataAnalysis,
  Document,
  EditPen,
  Food,
  HomeFilled,
  List,
  Location,
  Notebook,
  Pointer,
  Reading,
  Setting,
  Star,
  Tickets,
  User,
  Plus
} from '@element-plus/icons-vue'

const props = defineProps({
  activeMenu: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['select'])

const handleSelect = (index) => {
  emit('select', index)
}
</script>

<style scoped>
.patient-menu {
  border-right: none;
}
</style>


