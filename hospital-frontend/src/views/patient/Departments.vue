<template>
  <div class="departments-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <h2>科室列表</h2>
          <el-input
            v-model="searchText"
            placeholder="搜索科室名称"
            style="width: 300px"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </template>

      <!-- 科室卡片列表 -->
      <el-row :gutter="20" v-loading="loading">
        <el-col
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
          v-for="dept in pagedDepartments"
          :key="dept.id"
        >
          <el-card class="dept-card" shadow="hover">
            <div class="dept-content">
              <div class="dept-icon">
                <el-icon :size="48" :color="dept.color">
                  <OfficeBuilding />
                </el-icon>
              </div>
              <h3>{{ dept.deptName }}</h3>
              <p class="dept-type">{{ dept.deptType }}</p>
              <p class="dept-desc">{{ dept.description }}</p>
              <div class="dept-actions">
                <el-button type="primary" plain size="small" @click="viewDoctors(dept)">
                  查看医生
                </el-button>
                <el-button type="success" size="small" @click="makeAppointment(dept)">
                  立即预约
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 空状态 -->
      <el-empty v-if="filteredDepartments.length === 0" description="暂无科室信息" />

      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.pageSize"
          :total="total"
          :page-sizes="[8, 16, 24, 48]"
          layout="total, sizes, prev, pager, next, jumper"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

import { getEnabledDepartmentList } from '@/api/department'

const router = useRouter()

// 搜索文本
const searchText = ref('')

// 加载状态
const loading = ref(false)

// 科室列表
const departments = ref([])

// 颜色列表（用于给科室分配颜色）
const colors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399']

// 过滤后的科室列表
const filteredDepartments = computed(() => {
  if (!searchText.value) {
    return departments.value
  }
  return departments.value.filter(dept =>
    dept.deptName.includes(searchText.value) ||
    dept.deptType.includes(searchText.value) ||
    dept.description.includes(searchText.value)
  )
})

// 分页参数与分页数据
const queryParams = reactive({ page: 1, pageSize: 8 })
const total = computed(() => filteredDepartments.value.length)
const pagedDepartments = computed(() => {
  const start = (queryParams.page - 1) * queryParams.pageSize
  return filteredDepartments.value.slice(start, start + queryParams.pageSize)
})

// 搜索时重置页码
watch(searchText, () => {
  queryParams.page = 1
})

// 查看医生
const viewDoctors = (dept) => {
  router.push({
    path: '/doctors',
    query: { deptId: dept.id, deptName: dept.deptName }
  })
}

// 预约挂号
const makeAppointment = (dept) => {
  router.push({
    path: '/appointment',
    query: { deptId: dept.id }
  })
}

// 加载科室列表
const loadDepartments = async () => {
  loading.value = true
  try {
    const res = await getEnabledDepartmentList()
    
    // 为每个科室分配颜色
    departments.value = res.data.map((dept, index) => ({
      ...dept,
      color: colors[index % colors.length]
    }))
  } catch (error) {

    message.error('加载科室列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDepartments()
})
</script>

<style scoped lang="scss">
.departments-container {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
      font-size: 20px;
      color: #333;
    }
  }

  .dept-card {
    margin-bottom: 20px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    .dept-content {
      text-align: center;

      .dept-icon {
        margin-bottom: 15px;
      }

      h3 {
        margin: 0 0 8px 0;
        font-size: 18px;
        color: #333;
      }

      .dept-type {
        color: #909399;
        font-size: 13px;
        margin: 0 0 12px 0;
      }

      .dept-desc {
        color: #666;
        font-size: 13px;
        line-height: 1.6;
        margin: 0 0 20px 0;
        min-height: 60px;
      }

      .dept-actions {
        display: flex;
        gap: 10px;
        justify-content: center;
      }
    }
  }

  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
}
</style>

