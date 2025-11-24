<template>
  <div class="test-result">
    <el-page-header @back="goBack" content="测试结果" />

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>

    <div v-else-if="result" class="result-content">
      <!-- 体质类型卡片 -->
      <el-card class="constitution-card">
        <template #header>
          <div class="card-header">
            <span>您的体质类型</span>
            <el-tag type="info">{{ result.testDate }}</el-tag>
          </div>
        </template>

        <el-row :gutter="20">
          <!-- 主要体质 -->
          <el-col :span="result.secondaryConstitution ? 12 : 24">
            <div class="constitution-type primary">
              <div class="type-badge">主要体质</div>
              <div class="type-icon" :style="{ backgroundColor: result.primaryConstitutionDetail?.color || '#409EFF' }">
                {{ result.primaryConstitutionDetail?.icon || result.primaryConstitutionName?.charAt(0) }}
              </div>
              <h2>{{ result.primaryConstitutionName }}</h2>
              <div class="type-score">
                得分: {{ result.scores[result.primaryConstitution]?.toFixed(1) }}
              </div>
              <p class="type-description">
                {{ result.primaryConstitutionDetail?.description }}
              </p>
            </div>
          </el-col>

          <!-- 次要体质 -->
          <el-col :span="12" v-if="result.secondaryConstitution">
            <div class="constitution-type secondary">
              <div class="type-badge secondary-badge">次要体质</div>
              <div class="type-icon"
                :style="{ backgroundColor: result.secondaryConstitutionDetail?.color || '#67C23A' }">
                {{ result.secondaryConstitutionDetail?.icon || result.secondaryConstitutionName?.charAt(0) }}
              </div>
              <h2>{{ result.secondaryConstitutionName }}</h2>
              <div class="type-score">
                得分: {{ result.scores[result.secondaryConstitution]?.toFixed(1) }}
              </div>
              <p class="type-description">
                {{ result.secondaryConstitutionDetail?.description }}
              </p>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 体质得分雷达图 -->
      <el-card class="score-card">
        <template #header>
          <span>各体质得分分布</span>
        </template>
        <div ref="chartRef" class="chart-container"></div>
      </el-card>

      <!-- 体质特征 -->
      <el-card class="characteristics-card">
        <template #header>
          <span>体质特征</span>
        </template>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="主要特征">
            {{ result.primaryConstitutionDetail?.characteristics }}
          </el-descriptions-item>
          <el-descriptions-item label="易患疾病">
            {{ result.primaryConstitutionDetail?.susceptibleDiseases }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 养生建议 -->
      <el-card class="advice-card">
        <template #header>
          <span>养生建议</span>
        </template>

        <el-tabs>
          <el-tab-pane label="综合建议">
            <div class="advice-content" v-html="result.healthSuggestion"></div>
          </el-tab-pane>

          <el-tab-pane label="饮食调养">
            <div class="advice-content">
              {{ result.primaryConstitutionDetail?.dietAdvice }}
            </div>
          </el-tab-pane>

          <el-tab-pane label="运动调养">
            <div class="advice-content">
              {{ result.primaryConstitutionDetail?.exerciseAdvice }}
            </div>
          </el-tab-pane>

          <el-tab-pane label="情志调节">
            <div class="advice-content">
              {{ result.primaryConstitutionDetail?.emotionAdvice }}
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>

      <!-- 测试报告 -->
      <el-card class="report-card">
        <template #header>
          <span>详细报告</span>
        </template>
        <div class="report-content" v-html="result.report"></div>
      </el-card>

      <!-- 操作按钮 -->
      <el-card class="action-card">
        <el-button type="primary" @click="viewRecommendations">查看推荐药膳</el-button>
        <el-button type="success" @click="viewAcupoints">查看推荐穴位</el-button>
        <el-button @click="viewHistory">查看历史记录</el-button>
      </el-card>
    </div>

    <el-empty v-else description="未找到测试结果" />
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getTestReport, getLatestTestResult } from '@/api/constitution'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()

// 数据
const loading = ref(false)
const result = ref(null)
const chartRef = ref(null)
let chartInstance = null

// 加载测试结果
const loadTestResult = async () => {
  try {
    loading.value = true

    let res
    if (route.params.id) {
      // 根据测试ID获取结果
      res = await getTestReport(route.params.id)
    } else {
      // 获取最新测试结果
      res = await getLatestTestResult()
    }

    if (res.code === 200) {
      result.value = res.data
      // 等待DOM更新后初始化图表
      setTimeout(() => {
        initChart()
      }, 100)
    }
  } catch (error) {

    message.error('加载测试结果失败')
  } finally {
    loading.value = false
  }
}

// 初始化雷达图
const initChart = () => {
  if (!chartRef.value || !result.value) return

  chartInstance = echarts.init(chartRef.value)

  const constitutionNames = {
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

  const indicator = Object.keys(constitutionNames).map(code => ({
    name: constitutionNames[code],
    max: 100
  }))

  const data = Object.keys(constitutionNames).map(code =>
    result.value.scores[code] || 0
  )

  const option = {
    tooltip: {
      trigger: 'item'
    },
    radar: {
      indicator: indicator,
      radius: '60%'
    },
    series: [{
      type: 'radar',
      data: [{
        value: data,
        name: '体质得分',
        areaStyle: {
          color: 'rgba(64, 158, 255, 0.3)'
        },
        lineStyle: {
          color: '#409EFF',
          width: 2
        },
        itemStyle: {
          color: '#409EFF'
        }
      }]
    }]
  }

  chartInstance.setOption(option)

  // 响应式
  window.addEventListener('resize', handleResize)
}

// 处理窗口大小变化
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// 返回
const goBack = () => {
  router.back()
}

// 查看推荐药膳
const viewRecommendations = () => {
  router.push('/patient/recipe')
}

// 查看推荐穴位
const viewAcupoints = () => {
  router.push('/patient/acupoint/combinations')
}

// 查看历史记录
const viewHistory = () => {
  router.push('/patient/constitution/history')
}

// 页面加载
onMounted(() => {
  loadTestResult()
})

// 页面卸载
onUnmounted(() => {
  if (chartInstance) {
    window.removeEventListener('resize', handleResize)
    chartInstance.dispose()
  }
})
</script>

<style scoped>
.test-result {
  padding: 20px;
}

.el-page-header {
  margin-bottom: 20px;
}

.loading-container {
  padding: 40px;
}

.result-content {
  max-width: 1200px;
  margin: 0 auto;
}

.result-content .el-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.constitution-card .constitution-type {
  text-align: center;
  padding: 30px 20px;
  border-radius: 8px;
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
}

.constitution-type.primary {
  border: 2px solid #409EFF;
}

.constitution-type.secondary {
  border: 2px solid #67C23A;
}

.type-badge {
  display: inline-block;
  padding: 4px 12px;
  background: #409EFF;
  color: white;
  border-radius: 12px;
  font-size: 12px;
  margin-bottom: 15px;
}

.secondary-badge {
  background: #67C23A;
}

.type-icon {
  width: 80px;
  height: 80px;
  line-height: 80px;
  margin: 0 auto 15px;
  border-radius: 50%;
  color: white;
  font-size: 32px;
  font-weight: bold;
}

.constitution-type h2 {
  margin: 10px 0;
  font-size: 24px;
  color: #303133;
}

.type-score {
  font-size: 18px;
  color: #409EFF;
  font-weight: bold;
  margin: 10px 0;
}

.type-description {
  color: #606266;
  line-height: 1.8;
  margin-top: 15px;
}

.chart-container {
  height: 400px;
}

.advice-content {
  padding: 20px;
  line-height: 2;
  color: #606266;
  white-space: pre-wrap;
}

.report-content {
  padding: 20px;
  line-height: 2;
  color: #606266;
  white-space: pre-wrap;
}

.action-card {
  text-align: center;
}

.action-card .el-button {
  margin: 0 10px;
}
</style>
