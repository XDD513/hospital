<template>
  <div class="combination-detail-container">
    <el-page-header @back="goBack" title="返回">
      <template #content>
        <span class="page-title">组合方案详情</span>
      </template>
    </el-page-header>

    <el-card class="detail-card" v-loading="loading">
      <div v-if="combination">
        <!-- 基本信息 -->
        <div class="basic-info">
          <h1>{{ combination.combinationName }}</h1>
          <div class="tags">
            <el-tag type="success">{{ getConstitutionLabel(combination.constitutionType) }}</el-tag>
            <el-tag type="info">{{ combination.frequency }}</el-tag>
            <el-tag type="warning">{{ combination.totalDuration }}分钟</el-tag>
          </div>
          <div class="view-count">
            <el-icon><View /></el-icon>
            浏览量：{{ combination.viewCount || 0 }}
          </div>
        </div>

        <el-divider />

        <!-- 详细信息 -->
        <div class="detail-info">
          <!-- 适用症状 -->
          <div class="info-section">
            <h3><el-icon><FirstAidKit /></el-icon> 适用症状</h3>
            <p>{{ combination.symptom }}</p>
          </div>

          <!-- 方案描述 -->
          <div class="info-section">
            <h3><el-icon><Document /></el-icon> 方案描述</h3>
            <p>{{ combination.description }}</p>
          </div>

          <!-- 穴位列表 -->
          <div class="info-section">
            <h3><el-icon><Location /></el-icon> 包含穴位</h3>
            <el-row :gutter="15">
              <el-col
                v-for="acupoint in acupointList"
                :key="acupoint.id"
                :xs="24"
                :sm="12"
                :md="8"
              >
                <div class="acupoint-card" @click="viewAcupointDetail(acupoint.id)">
                  <div class="acupoint-image">
                    <img :src="acupoint.image || '/default-acupoint.png'" :alt="acupoint.acupointName" />
                  </div>
                  <div class="acupoint-info">
                    <h4>{{ acupoint.acupointName }}</h4>
                    <p>{{ acupoint.pinyin }} ({{ acupoint.code }})</p>
                    <el-tag size="small">{{ acupoint.meridian }}</el-tag>
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>

          <!-- 按摩顺序 -->
          <div class="info-section" v-if="massageSequence.length > 0">
            <h3><el-icon><Operation /></el-icon> 按摩顺序</h3>
            <el-timeline>
              <el-timeline-item
                v-for="(step, index) in massageSequence"
                :key="index"
                :timestamp="`第${index + 1}步`"
                placement="top"
              >
                <el-card>
                  <h4>{{ step.acupointName }}</h4>
                  <p>{{ step.method }}</p>
                  <p class="duration">时长：{{ step.duration }}分钟</p>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </div>

          <!-- 功效说明 -->
          <div class="info-section">
            <h3><el-icon><Star /></el-icon> 功效说明</h3>
            <p>{{ combination.efficacy }}</p>
          </div>

          <!-- 注意事项 -->
          <div class="info-section" v-if="combination.precautions">
            <h3><el-icon><Warning /></el-icon> 注意事项</h3>
            <el-alert type="warning" :closable="false">
              <p>{{ combination.precautions }}</p>
            </el-alert>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { View, FirstAidKit, Document, Location, Operation, Star, Warning } from '@element-plus/icons-vue'
import { getCombinationDetail } from '@/api/acupoint'
import { getAcupointDetail } from '@/api/acupoint'

const route = useRoute()
const router = useRouter()

const combination = ref(null)
const acupointList = ref([])
const loading = ref(false)

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

// 按摩顺序
const massageSequence = computed(() => {
  if (!combination.value?.massageSequence) return []
  try {
    return JSON.parse(combination.value.massageSequence)
  } catch {
    return []
  }
})

// 加载组合详情
const loadDetail = async () => {
  loading.value = true
  try {
    const id = route.params.id
    const res = await getCombinationDetail(id)
    if (res.code === 200) {
      combination.value = res.data
      // 加载穴位列表
      if (res.data.acupointIds) {
        await loadAcupoints(res.data.acupointIds)
      }
    }
  } catch (error) {

    message.error('加载组合详情失败')
  } finally {
    loading.value = false
  }
}

// 加载穴位列表
const loadAcupoints = async (acupointIds) => {
  try {
    // 解析 JSON 数组格式的穴位 ID
    let ids = []
    if (typeof acupointIds === 'string') {
      // 如果是 JSON 字符串，解析为数组
      ids = JSON.parse(acupointIds)
    } else if (Array.isArray(acupointIds)) {
      // 如果已经是数组，直接使用
      ids = acupointIds
    }

    const promises = ids.map(id => getAcupointDetail(id))
    const results = await Promise.all(promises)
    acupointList.value = results
      .filter(res => res.code === 200)
      .map(res => res.data)
  } catch (error) {

  }
}

// 获取体质标签
const getConstitutionLabel = (type) => {
  if (!type) return '通用'
  const types = type.split(',')
  return types.map(t => constitutionMap[t] || t).join('、')
}

// 查看穴位详情
const viewAcupointDetail = (id) => {
  router.push(`/patient/acupoint/detail/${id}`)
}

// 返回
const goBack = () => {
  router.back()
}

onMounted(() => {
  loadDetail()
})
</script>

<style scoped>
.combination-detail-container {
  padding: 20px;
}

.page-title {
  font-size: 18px;
  font-weight: 500;
}

.detail-card {
  margin-top: 20px;
}

.basic-info h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 15px;
}

.tags {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.view-count {
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 5px;
}

.detail-info {
  margin-top: 20px;
}

.info-section {
  margin-bottom: 30px;
}

.info-section h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-section p {
  font-size: 15px;
  color: #666;
  line-height: 1.8;
  text-align: justify;
}

.acupoint-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 15px;
}

.acupoint-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-3px);
}

.acupoint-image {
  width: 100%;
  height: 150px;
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

.acupoint-info h4 {
  font-size: 16px;
  color: #333;
  margin-bottom: 5px;
}

.acupoint-info p {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.duration {
  color: #409eff;
  font-weight: 500;
}
</style>

