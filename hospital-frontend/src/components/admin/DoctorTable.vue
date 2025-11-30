<template>
  <div class="doctor-table-container">
    <!-- Filter Bar -->
    <div class="filter-bar">
      <el-input 
        v-model="filters.name" 
        placeholder="请输入姓名" 
        class="filter-input"
        clearable
      />
      <el-input 
        v-model="filters.phone" 
        placeholder="请输入电话" 
        class="filter-input"
        clearable
      />
      
      <el-button @click="handleSearch">
        <el-icon><Search /></el-icon>
        搜索
      </el-button>
      
      <el-button @click="handleReset">
        <el-icon><Refresh /></el-icon>
        重置
      </el-button>

      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>
        新增
      </el-button>
    </div>

    <!-- Table -->
    <div class="table-wrapper">
      <table class="doctor-table">
        <thead>
          <tr>
            <th class="col-avatar">头像</th>
            <th class="col-name">姓名</th>
            <th class="col-dept">科室</th>
            <th class="col-gender">性别</th>
            <th class="col-username">账户</th>
            <th class="col-phone">电话</th>
            <th class="col-email">邮箱</th>
            <th class="col-location">出诊地址</th>
            <th class="col-recommended">推荐首页</th>
            <th class="col-status">启用状态</th>
            <th class="col-actions">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="doctor in filteredDoctors" 
            :key="doctor.id"
            class="table-row"
          >
            <td class="col-avatar">
              <el-avatar :size="40" :src="doctor.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
            </td>
            <td class="col-name">{{ doctor.name }}</td>
            <td class="col-dept">{{ doctor.department }}</td>
            <td class="col-gender">
              <AdminTag 
                :type="doctor.gender === '男' ? 'blue' : 'red'" 
                :text="doctor.gender"
              />
            </td>
            <td class="col-username">{{ doctor.username }}</td>
            <td class="col-phone">{{ doctor.phone }}</td>
            <td class="col-email">{{ doctor.email }}</td>
            <td class="col-location">{{ doctor.location }}</td>
            <td class="col-recommended">
              <AdminTag type="blue" text="推荐" />
            </td>
            <td class="col-status">
              <AdminToggleSwitch 
                :checked="doctor.isEnabled"
                @change="handleToggleStatus(doctor)"
              />
            </td>
            <td class="col-actions">
              <div class="action-buttons">
                <AdminButton variant="primary" @click="handleEdit(doctor)">
                  <el-icon><Edit /></el-icon>
                  编辑
                </AdminButton>
                <AdminButton variant="warning" @click="handleResetPassword(doctor)">
                  <el-icon><Lock /></el-icon>
                  重置密码
                </AdminButton>
                <AdminButton variant="danger" @click="handleDelete(doctor)">
                  <el-icon><Delete /></el-icon>
                  删除
                </AdminButton>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="pagination-wrapper">
      <div class="pagination-left">
        <span>共 {{ total }} 条</span>
        <el-select v-model="pageSize" class="page-size-select">
          <el-option label="10条/页" :value="10" />
          <el-option label="20条/页" :value="20" />
        </el-select>
      </div>
      
      <div class="pagination-right">
        <button 
          class="page-btn" 
          :disabled="currentPage === 1"
          @click="handlePrevPage"
        >
          &lt;
        </button>
        <button 
          class="page-btn active"
        >
          {{ currentPage }}
        </button>
        <button 
          class="page-btn" 
          :disabled="currentPage >= totalPages"
          @click="handleNextPage"
        >
          &gt;
        </button>
        <div class="page-jump">
          <span>前往</span>
          <input 
            type="text" 
            v-model.number="jumpPage"
            class="page-input"
            @keyup.enter="handleJumpPage"
          />
          <span>页</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { Search, Refresh, Plus, Edit, Lock, Delete, User } from '@element-plus/icons-vue'
import AdminTag from './AdminTag.vue'
import AdminToggleSwitch from './AdminToggleSwitch.vue'
import AdminButton from './AdminButton.vue'

const props = defineProps({
  doctors: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['add', 'edit', 'delete', 'reset-password', 'toggle-status'])

const filters = reactive({
  name: '',
  phone: ''
})

const currentPage = ref(1)
const pageSize = ref(10)
const jumpPage = ref(1)

const filteredDoctors = computed(() => {
  let result = props.doctors

  if (filters.name) {
    result = result.filter(d => d.name?.includes(filters.name))
  }
  if (filters.phone) {
    result = result.filter(d => d.phone?.includes(filters.phone))
  }

  return result
})

const total = computed(() => filteredDoctors.value.length)
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

const handleSearch = () => {
  currentPage.value = 1
  emit('search', filters)
}

const handleReset = () => {
  filters.name = ''
  filters.phone = ''
  currentPage.value = 1
}

const handleAdd = () => {
  emit('add')
}

const handleEdit = (doctor) => {
  emit('edit', doctor)
}

const handleDelete = (doctor) => {
  emit('delete', doctor)
}

const handleResetPassword = (doctor) => {
  emit('reset-password', doctor)
}

const handleToggleStatus = (doctor) => {
  emit('toggle-status', doctor)
}

const handlePrevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const handleNextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const handleJumpPage = () => {
  const page = Math.max(1, Math.min(jumpPage.value, totalPages.value))
  currentPage.value = page
  jumpPage.value = page
}
</script>

<style scoped lang="scss">
.doctor-table-container {
  background: white;
  padding: 20px;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  min-height: 100%;

  .filter-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;

    .filter-input {
      width: 200px;
    }
  }

  .table-wrapper {
    overflow-x: auto;
    border: 1px solid #e5e7eb;
    border-radius: 2px;

    .doctor-table {
      width: 100%;
      font-size: 14px;
      text-align: left;
      border-collapse: collapse;

      thead {
        background: #f8f8f9;
        color: #606266;
        font-weight: bold;
        border-bottom: 1px solid #e5e7eb;

        th {
          padding: 12px 16px;
          text-align: center;
          font-weight: bold;

          &.col-avatar {
            width: 80px;
          }
          &.col-name {
            width: 96px;
          }
          &.col-gender {
            width: 80px;
          }
          &.col-recommended {
            width: 96px;
          }
          &.col-status {
            width: 96px;
          }
          &.col-actions {
            width: 280px;
          }
        }
      }

      tbody {
        .table-row {
          border-bottom: 1px solid #e5e7eb;
          transition: background-color 0.2s;

          &:hover {
            background: #f5f5f5;
          }

          td {
            padding: 12px 16px;
            color: #606266;
            text-align: center;

            &.col-avatar {
              display: flex;
              justify-content: center;
            }

            &.col-email {
              max-width: 150px;
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
            }

            &.col-actions {
              .action-buttons {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
              }
            }
          }
        }
      }
    }
  }

  .pagination-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 20px;
    font-size: 13px;
    color: #606266;

    .pagination-left {
      display: flex;
      align-items: center;
      gap: 8px;

      .page-size-select {
        width: 100px;
      }
    }

    .pagination-right {
      display: flex;
      align-items: center;
      gap: 8px;

      .page-btn {
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #dcdfe6;
        border-radius: 2px;
        background: white;
        cursor: pointer;
        transition: all 0.2s;

        &:hover:not(:disabled) {
          color: #409EFF;
          border-color: #409EFF;
        }

        &:disabled {
          background: #f5f7fa;
          color: #c0c4cc;
          cursor: not-allowed;
        }

        &.active {
          background: #409EFF;
          color: white;
          border-color: #409EFF;
        }
      }

      .page-jump {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-left: 8px;

        .page-input {
          width: 40px;
          text-align: center;
          border: 1px solid #dcdfe6;
          border-radius: 2px;
          padding: 4px;
          outline: none;

          &:focus {
            border-color: #409EFF;
          }
        }
      }
    }
  }
}
</style>






