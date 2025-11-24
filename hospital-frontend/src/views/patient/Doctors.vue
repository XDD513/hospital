<template>
  <div class="doctors-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <h2>医生列表</h2>
          <div class="header-actions">
            <el-select
              v-model="queryParams.deptId"
              placeholder="选择科室"
              clearable
              style="width: 200px; margin-right: 10px"
              @change="loadDoctors"
            >
              <el-option
                v-for="dept in departments"
                :key="dept.id"
                :label="dept.deptName"
                :value="dept.id"
              />
            </el-select>
            <el-input
              v-model="queryParams.searchText"
              placeholder="搜索医生姓名"
              style="width: 250px"
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </div>
      </template>

      <!-- 医生列表 -->
      <el-row :gutter="20">
        <template v-if="loading">
          <el-col :xs="24" :sm="12" :md="8" v-for="n in skeletonCount" :key="`doctor-skeleton-${n}`">
            <el-card class="doctor-card" shadow="never">
              <el-skeleton animated :rows="4">
                <template #template>
                  <div class="doctor-skeleton">
                    <div class="skeleton-avatar">
                      <el-skeleton-item variant="image" style="width: 80px; height: 80px;" />
                    </div>
                    <div class="skeleton-info">
                      <el-skeleton-item variant="text" style="width: 120px;" />
                      <el-skeleton-item variant="text" style="width: 60px;" />
                      <el-skeleton-item variant="text" />
                      <el-skeleton-item variant="text" />
                      <el-skeleton-item variant="text" style="width: 80%;" />
                      <div class="skeleton-actions">
                        <el-skeleton-item variant="button" style="width: 90px;" />
                        <el-skeleton-item variant="button" style="width: 90px;" />
                      </div>
                    </div>
                  </div>
                </template>
              </el-skeleton>
            </el-card>
          </el-col>
        </template>

        <template v-else>
          <el-col
            :xs="24"
            :sm="12"
            :md="8"
            v-for="doctor in doctors"
            :key="doctor.id"
          >
            <el-card class="doctor-card" shadow="hover">
              <div class="doctor-content">
                <el-avatar :size="80" :src="doctor.avatar">
                  <el-icon :size="40"><User /></el-icon>
                </el-avatar>
                
                <div class="doctor-info">
                  <h3>{{ doctor.doctorName }}</h3>
                  <el-tag type="warning" size="small">{{ doctor.title }}</el-tag>
                  
                  <div class="info-item">
                    <el-icon><OfficeBuilding /></el-icon>
                    <span>{{ doctor.deptName }}</span>
                  </div>
                  
                  <div class="info-item">
                    <el-icon><Star /></el-icon>
                    <span>评分：{{ doctor.rating || '暂无' }}</span>
                  </div>
                  
                  <div class="info-item">
                    <el-icon><User /></el-icon>
                    <span>接诊量：{{ doctor.consultationCount || 0 }}</span>
                  </div>
                  
                  <div class="specialty">
                    <strong>擅长：</strong>{{ doctor.specialty || '暂无' }}
                  </div>
                  
                  <div class="doctor-actions">
                    <el-button type="primary" size="small" @click="viewDetail(doctor)">
                      查看详情
                    </el-button>
                    <el-button type="success" size="small" @click="makeAppointment(doctor)">
                      立即预约
                    </el-button>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </template>
      </el-row>

      <!-- 空状态 -->
      <EmptyState
        v-if="doctors.length === 0 && !loading"
        description="暂无医生信息"
        tip="尝试切换科室或调整搜索条件"
      />

      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.pageSize"
          :total="total"
          :page-sizes="[6, 12, 24, 48]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadDoctors"
          @current-change="loadDoctors"
        />
      </div>
    </el-card>

    <!-- 医生详情弹窗 -->
    <el-dialog
      v-model="detailVisible"
      title="医生详情"
      width="600px"
    >
      <div v-if="selectedDoctor" class="doctor-detail">
        <div class="detail-header">
          <el-avatar :size="100" :src="selectedDoctor.avatar">
            <el-icon :size="50"><User /></el-icon>
          </el-avatar>
          <div class="detail-basic">
            <h2>{{ selectedDoctor.doctorName }}</h2>
            <el-tag type="warning">{{ selectedDoctor.title }}</el-tag>
            <p>{{ selectedDoctor.deptName }}</p>
          </div>
        </div>
        
        <el-divider />
        
        <div class="detail-content">
          <div class="detail-item">
            <strong>擅长领域：</strong>
            <p>{{ selectedDoctor.specialty || '暂无' }}</p>
          </div>
          <div class="detail-item">
            <strong>医生简介：</strong>
            <p>{{ selectedDoctor.introduction || '暂无' }}</p>
          </div>
          <div class="detail-item">
            <strong>挂号费：</strong>
            <p class="fee">¥{{ selectedDoctor.consultationFee }}</p>
          </div>
          <div class="detail-item">
            <strong>评分：</strong>
            <el-rate v-model="selectedDoctor.rating" disabled />
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button type="primary" @click="makeAppointment(selectedDoctor)">
          立即预约
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import { getEnabledDoctorList, getDoctorListByDept } from '@/api/doctor'
import { getEnabledDepartmentList } from '@/api/department'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()
const route = useRoute()

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 6,
  deptId: route.query.deptId || null,
  searchText: ''
})

// 数据
const loading = ref(false)
const doctors = ref([])
const total = ref(0)
const departments = ref([])
const detailVisible = ref(false)
const selectedDoctor = ref(null)
const skeletonCount = 6


// 加载医生列表
const loadDoctors = async () => {
  loading.value = true
  try {
    let res
    
    // 按科室筛选
    if (queryParams.deptId) {
      res = await getDoctorListByDept(queryParams.deptId)
    } else {
      res = await getEnabledDoctorList()
    }
    
    let doctorList = res.data || []
    
    // 按名字搜索（前端过滤）
    if (queryParams.searchText) {
      doctorList = doctorList.filter(d => 
        d.doctorName?.includes(queryParams.searchText) ||
        d.realName?.includes(queryParams.searchText)
      )
    }
    
    doctors.value = doctorList
    total.value = doctorList.length
    
  } catch (error) {

    message.error('加载医生列表失败')
  } finally {
    loading.value = false
  }
}

// 加载科室列表
const loadDepartments = async () => {
  try {
    const res = await getEnabledDepartmentList()
    departments.value = res.data || []
  } catch (error) {

  }
}

// 搜索处理
const handleSearch = () => {
  queryParams.page = 1
  loadDoctors()
}

// 查看医生详情
const viewDetail = (doctor) => {
  selectedDoctor.value = doctor
  detailVisible.value = true
}

// 预约挂号
const makeAppointment = (doctor) => {
  detailVisible.value = false
  router.push({
    path: '/appointment',
    query: {
      doctorId: doctor.id,
      deptId: doctor.deptId
    }
  })
}

onMounted(() => {
  loadDepartments()
  loadDoctors()
})
</script>

<style scoped lang="scss">
.doctors-container {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;

    h2 {
      margin: 0;
      font-size: 20px;
      color: #333;
    }

    .header-actions {
      display: flex;
      gap: 10px;
    }
  }

  .doctor-card {
    margin-bottom: 20px;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    .doctor-content {
      display: flex;
      gap: 20px;

      .doctor-info {
        flex: 1;

        h3 {
          margin: 0 0 10px 0;
          font-size: 18px;
          color: #333;
        }

        .info-item {
          display: flex;
          align-items: center;
          gap: 5px;
          color: #666;
          font-size: 14px;
          margin: 8px 0;

          .el-icon {
            color: #909399;
          }
        }

        .specialty {
          margin: 12px 0;
          font-size: 13px;
          color: #666;
          line-height: 1.6;

          strong {
            color: #333;
          }
        }

        .doctor-actions {
          display: flex;
          gap: 10px;
          margin-top: 15px;
        }
      }
    }

    .doctor-skeleton {
      display: flex;
      gap: 20px;

      .skeleton-avatar {
        display: flex;
        align-items: flex-start;
      }

      .skeleton-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 10px;

        .skeleton-actions {
          display: flex;
          gap: 12px;
          margin-top: 10px;
        }
      }
    }
  }

  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
}

.doctor-detail {
  .detail-header {
    display: flex;
    gap: 20px;
    align-items: center;

    .detail-basic {
      flex: 1;

      h2 {
        margin: 0 0 10px 0;
      }

      p {
        margin: 10px 0 0 0;
        color: #666;
      }
    }
  }

  .detail-content {
    .detail-item {
      margin-bottom: 20px;

      strong {
        display: block;
        margin-bottom: 8px;
        color: #333;
      }

      p {
        margin: 0;
        color: #666;
        line-height: 1.6;
      }

      .fee {
        font-size: 24px;
        color: #f56c6c;
        font-weight: bold;
      }
    }
  }
}
</style>

