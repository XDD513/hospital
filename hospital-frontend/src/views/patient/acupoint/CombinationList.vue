<template>
  <div class="combination-list-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>穴位组合方案</h2>
      <p>科学搭配穴位，增强按摩效果</p>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card">
      <el-form :inline="true">
        <el-form-item label="关键词">
          <el-input
            v-model="searchKeyword"
            placeholder="请输入组合名称或症状"
            clearable
            @clear="handleSearch"
          />
        </el-form-item>
        <el-form-item label="症状">
          <el-input
            v-model="selectedSymptom"
            placeholder="请输入症状"
            clearable
            @change="handleSearch"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="loadRecommended" v-if="userStore.userInfo?.id">
            <el-icon><Star /></el-icon>
            为我推荐
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 热门组合 -->
    <el-card class="popular-card" v-if="popularCombinations.length > 0">
      <template #header>
        <div class="card-header">
          <span>热门组合</span>
        </div>
      </template>
      <div class="popular-list">
        <el-tag
          v-for="combination in popularCombinations"
          :key="combination.id"
          class="popular-tag"
          type="success"
          @click="viewDetail(combination.id)"
        >
          {{ combination.combinationName }}
        </el-tag>
      </div>
    </el-card>

    <!-- 组合列表 -->
    <el-card class="list-card">
      <el-row :gutter="20">
        <el-col
          v-for="combination in combinationList"
          :key="combination.id"
          :xs="24"
          :sm="12"
          :md="8"
        >
          <div class="combination-item" @click="viewDetail(combination.id)">
            <div class="combination-header">
              <h3>{{ combination.combinationName }}</h3>
              <el-tag size="small" type="success">{{ getConstitutionLabel(combination.constitutionType) }}</el-tag>
            </div>
            <div class="combination-body">
              <p class="symptom">
                <el-icon><FirstAidKit /></el-icon>
                <span>{{ combination.symptom }}</span>
              </p>
              <p class="description">{{ truncate(combination.description, 80) }}</p>
              <div class="combination-meta">
                <span class="duration">
                  <el-icon><Timer /></el-icon>
                  {{ combination.totalDuration }}分钟
                </span>
                <span class="frequency">{{ combination.frequency }}</span>
              </div>
            </div>
            <div class="combination-footer">
              <span class="view-count">
                <el-icon><View /></el-icon>
                {{ combination.viewCount || 0 }}
              </span>
              <el-button type="primary" size="small" @click.stop="viewDetail(combination.id)">
                查看详情
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>

      <!-- 空状态 -->
      <el-empty v-if="combinationList.length === 0" description="暂无组合方案" />

      <!-- 分页 -->
      <div class="pagination-container" v-if="total > 0">
        <el-pagination
          v-model:current-page="queryParams.pageNum"
          v-model:page-size="queryParams.pageSize"
          :total="total"
          :page-sizes="[9, 18, 27, 36]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadCombinations"
          @current-change="loadCombinations"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { Search, Star, FirstAidKit, Timer, View } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import {
  getCombinationList,
  searchCombinations,
  getRecommendedCombinations,
  getPopularCombinations
} from '@/api/acupoint'

const router = useRouter()
const userStore = useUserStore()

// 数据
const combinationList = ref([])
const popularCombinations = ref([])
const total = ref(0)
const searchKeyword = ref('')
const selectedSymptom = ref('')

// 查询参数
const queryParams = ref({
  pageNum: 1,
  pageSize: 9,
  constitutionType: '',
  symptom: ''
})

// 体质类型映射
const constitutionMap = {
  'PINGHE': '平和质',
  'QIXU': '气虚质',
  'YANGXU': '阳虚质',
  'YINXU': '阴虚质',
  'TANSHI': '痰湿质',
  'SHIRE': '湿热质',
  'XUEYU': '血瘀质',
  'QIYU': '气郁质',
  'TEBING': '特禀质'
}

// 加载组合列表
const loadCombinations = async () => {
  try {
    const params = {
      ...queryParams.value,
      symptom: selectedSymptom.value
    }
    const res = await getCombinationList(params)
    if (res.code === 200) {
      combinationList.value = res.data.records || []
      total.value = Number(res.data.total) || 0
    }
  } catch (error) {

    message.error('加载组合列表失败')
  }
}

// 加载热门组合
const loadPopularCombinations = async () => {
  try {
    const res = await getPopularCombinations(10)
    if (res.code === 200) {
      popularCombinations.value = res.data || []
    }
  } catch (error) {

  }
}

// 加载推荐组合
const loadRecommended = async () => {
  try {
    const userId = userStore.userInfo?.id
    if (!userId) {
      message.warning('请先登录')
      return
    }
    const res = await getRecommendedCombinations(userId, 20)
    if (res.code === 200) {
      combinationList.value = res.data || []
      total.value = res.data.length
      message.success('已为您推荐适合的组合方案')
    }
  } catch (error) {

    message.error('加载推荐组合失败')
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
      const res = await searchCombinations(params)
      if (res.code === 200) {
        combinationList.value = res.data.records || []
        total.value = res.data.total || 0
      }
    } catch (error) {

      message.error('搜索组合失败')
    }
  } else {
    queryParams.value.pageNum = 1
    loadCombinations()
  }
}

// 查看详情
const viewDetail = (id) => {
  router.push(`/patient/acupoint/combination/${id}`)
}

// 获取体质标签
const getConstitutionLabel = (type) => {
  if (!type) return '通用'
  const types = type.split(',')
  return types.map(t => constitutionMap[t] || t).join('、')
}

// 文本截断
const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

onMounted(() => {
  loadPopularCombinations()
  loadCombinations()
})
</script>

<style scoped>
.combination-list-container {
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

.combination-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.combination-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-5px);
}

.combination-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.combination-header h3 {
  font-size: 18px;
  color: #333;
  margin: 0;
}

.combination-body {
  flex: 1;
}

.symptom {
  font-size: 14px;
  color: #409eff;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.description {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
  min-height: 60px;
}

.combination-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #999;
  margin-bottom: 15px;
}

.duration,
.frequency {
  display: flex;
  align-items: center;
  gap: 4px;
}

.combination-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
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

