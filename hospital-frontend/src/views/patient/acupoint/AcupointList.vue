<template>
  <div class="acupoint-list-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>穴位按摩指导</h2>
      <p>了解中医穴位，掌握按摩方法，改善身体健康</p>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card">
      <el-form :inline="true">
        <el-form-item label="关键词">
          <el-input v-model="searchKeyword" placeholder="请输入穴位名称或拼音" clearable @clear="handleSearch" />
        </el-form-item>
        <el-form-item label="经络">
          <el-select v-model="selectedMeridian" placeholder="请选择经络" clearable @change="handleSearch"
            style="width: 200px;">
            <el-option v-for="meridian in meridians" :key="meridian" :label="meridian" :value="meridian" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon>
              <Search />
            </el-icon>
            搜索
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 热门穴位 -->
    <el-card class="popular-card" v-if="popularAcupoints.length > 0">
      <template #header>
        <div class="card-header">
          <span>热门穴位</span>
        </div>
      </template>
      <div class="popular-list">
        <el-tag v-for="acupoint in popularAcupoints" :key="acupoint.id" class="popular-tag"
          @click="viewDetail(acupoint.id)">
          {{ acupoint.acupointName }}
        </el-tag>
      </div>
    </el-card>

    <!-- 穴位列表 -->
    <el-card class="list-card">
      <el-row :gutter="20">
        <el-col v-for="acupoint in acupointList" :key="acupoint.id" :xs="24" :sm="12" :md="8" :lg="6">
          <div class="acupoint-item" @click="viewDetail(acupoint.id)">
            <div class="acupoint-image">
              <img :src="acupoint.image || '/default-acupoint.png'" :alt="acupoint.acupointName" />
            </div>
            <div class="acupoint-info">
              <h3>{{ acupoint.acupointName }}</h3>
              <p class="pinyin">{{ acupoint.pinyin }} ({{ acupoint.code }})</p>
              <p class="meridian">
                <el-tag size="small">{{ acupoint.meridian }}</el-tag>
              </p>
              <p class="indications">{{ truncate(acupoint.indications, 50) }}</p>
              <div class="acupoint-footer">
                <span class="view-count">
                  <el-icon>
                    <View />
                  </el-icon>
                  {{ acupoint.viewCount || 0 }}
                </span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>

      <!-- 空状态 -->
      <el-empty v-if="acupointList.length === 0" description="暂无穴位数据" />

      <!-- 分页 -->
      <div class="pagination-container" v-if="total > 0">
        <el-pagination v-model:current-page="queryParams.pageNum" v-model:page-size="queryParams.pageSize"
          :total="total" :page-sizes="[12, 24, 36, 48]" layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadAcupoints" @current-change="loadAcupoints" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { Search, View } from '@element-plus/icons-vue'
import {
  getAcupointList,
  searchAcupoints,
  getAllMeridians,
  getPopularAcupoints
} from '@/api/acupoint'

const router = useRouter()

// 数据
const acupointList = ref([])
const popularAcupoints = ref([])
const meridians = ref([])
const total = ref(0)
const searchKeyword = ref('')
const selectedMeridian = ref('')

// 查询参数
const queryParams = ref({
  pageNum: 1,
  pageSize: 12,
  meridian: '',
  constitutionType: ''
})

// 加载穴位列表
const loadAcupoints = async () => {
  try {
    const params = {
      ...queryParams.value,
      meridian: selectedMeridian.value
    }
    const res = await getAcupointList(params)
    if (res.code === 200) {
      acupointList.value = res.data.records || []
      total.value = Number(res.data.total) || 0
    }
  } catch (error) {

    message.error('加载穴位列表失败')
  }
}

// 加载经络列表
const loadMeridians = async () => {
  try {
    const res = await getAllMeridians()
    if (res.code === 200) {
      meridians.value = res.data || []
    }
  } catch (error) {

  }
}

// 加载热门穴位
const loadPopularAcupoints = async () => {
  try {
    const res = await getPopularAcupoints(10)
    if (res.code === 200) {
      popularAcupoints.value = res.data || []
    }
  } catch (error) {

  }
}

// 搜索处理
const handleSearch = async () => {
  if (searchKeyword.value) {
    try {
      const params = {
        keyword: searchKeyword.value,
        pageNum: queryParams.value.pageNum,
        pageSize: queryParams.value.pageSize
      }
      const res = await searchAcupoints(params)
      if (res.code === 200) {
        acupointList.value = res.data.records || []
        total.value = res.data.total || 0
      }
    } catch (error) {

      message.error('搜索穴位失败')
    }
  } else {
    queryParams.value.pageNum = 1
    loadAcupoints()
  }
}

// 查看详情
const viewDetail = (id) => {
  router.push(`/patient/acupoint/detail/${id}`)
}

// 文本截断
const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

onMounted(() => {
  loadMeridians()
  loadPopularAcupoints()
  loadAcupoints()
})
</script>

<style scoped>
.acupoint-list-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
  text-align: center;
}

.page-header h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 14px;
  color: #666;
}

.search-card {
  margin-bottom: 20px;
}

.popular-card {
  margin-bottom: 20px;
}

.popular-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.popular-tag {
  cursor: pointer;
  transition: all 0.3s;
}

.popular-tag:hover {
  transform: scale(1.05);
}

.list-card {
  margin-bottom: 20px;
}

.acupoint-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 20px;
  height: 100%;
}

.acupoint-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-5px);
}

.acupoint-image {
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: #f5f5f5;
}

.acupoint-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.acupoint-info {
  padding: 15px;
}

.acupoint-info h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 5px;
}

.pinyin {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.meridian {
  margin-bottom: 10px;
}

.indications {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 10px;
  min-height: 40px;
}

.acupoint-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.view-count {
  font-size: 12px;
  color: #999;
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
