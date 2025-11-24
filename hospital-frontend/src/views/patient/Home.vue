<template>
  <div class="home-container">
    <!-- 欢迎横幅 -->
    <el-card class="welcome-card" shadow="never">
      <div class="welcome-content">
        <div class="welcome-left">
          <h1>欢迎使用{{ systemName }}，{{ userStore.userInfo.realName || userStore.userInfo.username }}！</h1>
          <p>{{ currentDate }} · {{ healthTip }}</p>
          <div class="action-buttons">
            <el-button type="success" size="large" @click="goToConstitutionHistory">
              <el-icon>
                <Document />
              </el-icon>
              查看测试历史
            </el-button>
            <el-button type="primary" size="large" plain @click="goToRecipes">
              <el-icon>
                <Food />
              </el-icon>
              浏览药膳推荐
            </el-button>
          </div>
        </div>
        <div class="welcome-right">
          <el-icon :size="120" color="#52c41a">
            <Van />
          </el-icon>
        </div>
      </div>
    </el-card>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <div class="patient-stat-card green" @click="router.push('/patient/constitution/history')">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Document />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.testCount || 0 }}</div>
              <div class="stat-label">体质测试次数</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="patient-stat-card orange" @click="router.push('/patient/recipe/my')">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <Food />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.recipeCount || 0 }}</div>
              <div class="stat-label">收藏药膳</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="patient-stat-card blue" @click="router.push('/patient/community/my-articles')">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <ChatDotRound />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.articleCount || 0 }}</div>
              <div class="stat-label">发布文章</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="patient-stat-card red" @click="router.push('/patient/health/checkin')">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon>
                <CircleCheck />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.checkinDays || 0 }}</div>
              <div class="stat-label">连续打卡天数</div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>


    <!-- 我的体质 -->
    <el-card class="constitution-card" shadow="never" v-if="latestConstitution">
      <template #header>
        <div class="card-header">
          <span>我的体质</span>
          <el-button text type="success" @click="router.push('/patient/constitution/history')">
            查看详情 <el-icon>
              <ArrowRight />
            </el-icon>
          </el-button>
        </div>
      </template>
      <div class="constitution-content">
        <div class="constitution-main">
          <el-tag size="large" type="success" effect="dark">{{ latestConstitution.type }}</el-tag>
          <p class="constitution-desc">{{ latestConstitution.description }}</p>
          <div class="constitution-date">测试时间：{{ latestConstitution.testDate }}</div>
        </div>
        <div class="constitution-suggestions">
          <h4>养生建议</h4>
          <ul>
            <li v-for="(tip, index) in latestConstitution.tips" :key="index">{{ tip }}</li>
          </ul>
        </div>
      </div>
    </el-card>

    <!-- 健康趋势 -->
    <el-card class="health-trend-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>健康趋势（最近7天）</span>
          <el-button text type="success" @click="router.push('/patient/health/statistics')">
            查看详情 <el-icon>
              <ArrowRight />
            </el-icon>
          </el-button>
        </div>
      </template>
      <div ref="healthTrendChartRef" style="width: 100%; height: 300px;"></div>
    </el-card>

    <!-- 推荐药膳 -->
    <el-card class="recommended-recipes" shadow="never">
      <template #header>
        <div class="card-header">
          <span>推荐药膳</span>
          <el-button text type="success" @click="router.push('/patient/recipe')">
            查看更多 <el-icon>
              <ArrowRight />
            </el-icon>
          </el-button>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" v-for="recipe in recommendedRecipes" :key="recipe.id">
          <el-card class="recipe-card" shadow="hover" @click="goToRecipeDetail(recipe.id)">
            <div class="recipe-image">
              <el-image :src="getRecipeImage(recipe.image)" fit="cover" :lazy="true">
                <template #error>
                  <div class="image-slot">
                    <el-icon>
                      <Picture />
                    </el-icon>
                  </div>
                </template>
              </el-image>
            </div>
            <div class="recipe-info">
              <h4>{{ recipe.name }}</h4>
              <p class="recipe-effect">{{ recipe.effect }}</p>
              <!-- AI推荐理由 -->
              <p v-if="recipe.recommendationReason" class="recipe-recommendation">
                <el-icon><InfoFilled /></el-icon>
                {{ recipe.recommendationReason }}
              </p>
              <div class="recipe-meta">
                <el-tag size="small">{{ getSeasonName(recipe.season) }}</el-tag>
                <el-tag size="small" type="success">{{ getConstitutionName(recipe.constitution) }}</el-tag>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>

    <!-- 养生知识 -->
    <el-card class="health-articles" shadow="never">
      <template #header>
        <div class="card-header">
          <span>养生知识</span>
          <el-button text type="success" @click="router.push('/patient/community/articles')">
            查看更多 <el-icon>
              <ArrowRight />
            </el-icon>
          </el-button>
        </div>
      </template>
      <el-timeline>
        <el-timeline-item v-for="article in healthArticles" :key="article.id" :timestamp="article.publishTime"
          placement="top">
          <el-card class="article-item" shadow="hover" @click="goToArticleDetail(article.id)">
            <div class="article-content">
              <h4>{{ article.title }}</h4>
              <p>{{ article.summary }}</p>
              <div class="article-meta">
                <el-tag size="small">{{ article.category }}</el-tag>
                <span class="article-stats">
                  <el-icon>
                    <View />
                  </el-icon> {{ article.viewCount }}
                  <el-icon>
                    <ChatDotRound />
                  </el-icon> {{ article.commentCount }}
                </span>
              </div>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { usePatientStore } from '@/stores/patient'
import dayjs from 'dayjs'
import * as echarts from 'echarts'
import {
  Document,
  Van,
  Food,
  ChatDotRound,
  CircleCheck,
  ArrowRight,
  View,
  Picture,
  InfoFilled
} from '@element-plus/icons-vue'
import { getLatestTestResult } from '@/api/constitution'
import { getRecommendedRecipes } from '@/api/recipe'
import { getRecommendedArticles } from '@/api/article'
import { getHealthStatistics } from '@/api/health'
import { getCheckinList } from '@/api/health'
import { getPatientStats } from '@/api/statistics'
import { getAppConfig } from '@/config/runtimeConfig'

const router = useRouter()
const userStore = useUserStore()
const patientStore = usePatientStore()
const appConfig = inject('appConfig', getAppConfig())
const systemName = computed(() => appConfig?.systemInfo?.name || '中医体质辨识系统')

// ECharts实例引用
const healthTrendChartRef = ref(null)
let healthTrendChartInstance = null

// 当前日期
const currentDate = computed(() => {
  const weekDays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  const dayOfWeek = dayjs().day()
  return dayjs().format('YYYY年MM月DD日') + ' ' + weekDays[dayOfWeek]
})

// 养生小贴士
const healthTips = [
  '春养肝，夏养心，秋养肺，冬养肾',
  '早睡早起，顺应自然',
  '饮食有节，起居有常',
  '心平气和，情志调畅',
  '适度运动，强身健体'
]
const healthTip = computed(() => {
  const index = dayjs().day()
  return healthTips[index % healthTips.length]
})

// 统计数据
const stats = ref({
  testCount: 0,
  recipeCount: 0,
  articleCount: 0,
  checkinDays: 0
})

const formatDateTime = (value) => {
  if (!value) return ''
  return dayjs(value).format('YYYY-MM-DD HH:mm')
}

// 加载统计数据
const loadStats = async () => {
  try {
    const userId = userStore.userInfo?.id
    if (!userId) {

      return
    }

    // 调用患者统计API
    const res = await getPatientStats()

    if (res.code === 200 && res.data) {
      stats.value = {
        testCount: res.data.testCount || 0,
        recipeCount: res.data.recipeCount || 0,
        articleCount: res.data.articleCount || 0,
        checkinDays: res.data.checkinDays || 0
      }
    } else {

      // 使用默认值
      stats.value = {
        testCount: 0,
        recipeCount: 0,
        articleCount: 0,
        checkinDays: 0
      }
    }

  } catch (error) {


    // 使用默认值
    stats.value = {
      testCount: 0,
      recipeCount: 0,
      articleCount: 0,
      checkinDays: 0
    }
  }
}


// 最新体质测试结果
const latestConstitution = ref(null)

// 加载最新体质测试结果
const loadLatestConstitution = async () => {
  try {
    const res = await getLatestTestResult()
    if (res.code === 200 && res.data) {
      const result = res.data
      const primaryDetail = result.primaryConstitutionDetail || {}

      // 提取养生建议
      const tips = []
      if (primaryDetail.healthAdvice) tips.push(primaryDetail.healthAdvice)
      if (primaryDetail.dietAdvice) tips.push(primaryDetail.dietAdvice)
      if (primaryDetail.exerciseAdvice) tips.push(primaryDetail.exerciseAdvice)

      latestConstitution.value = {
        type: result.primaryConstitutionName || primaryDetail.typeName || result.primaryConstitution,
        description: primaryDetail.description || primaryDetail.characteristics || '',
        testDate: dayjs(result.testDate).format('YYYY-MM-DD'),
        tips: tips
      }
    } else {
      latestConstitution.value = null
    }
  } catch (error) {

    // 如果没有测试结果，不显示该区块
    latestConstitution.value = null
  }
}

// 推荐药膳
const recommendedRecipes = ref([])

// 获取药膳图片URL
const getRecipeImage = (imagePath) => {
  // 如果没有图片路径，返回占位图（使用data URL避免404请求）
  if (!imagePath) {
    return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LXNpemU9IjE4IiBmaWxsPSIjY2NjIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+6I2v6IaA5Zu+54mHPC90ZXh0Pjwvc3ZnPg=='
  }

  // 如果是完整URL，直接返回
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath
  }

  // 如果是相对路径，从public/uploads目录加载
  return `/uploads/${imagePath}`
}

// 季节名称映射
const seasonNames = {
  'SPRING': '春季',
  'SUMMER': '夏季',
  'AUTUMN': '秋季',
  'WINTER': '冬季',
  'ALL': '四季'
}

// 体质名称映射
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

// 获取季节名称
const getSeasonName = (season) => {
  if (!season) return '四季'
  return seasonNames[season] || season
}

// 获取体质名称
const getConstitutionName = (type) => {
  if (!type) return ''
  // 处理多个体质（逗号分隔）
  if (type.includes(',')) {
    return type.split(',').map(t => constitutionNames[t.trim()] || t.trim()).join('、')
  }
  return constitutionNames[type] || type
}

// 加载推荐药膳
const loadRecommendedRecipes = async () => {
  try {
    const res = await getRecommendedRecipes({ pageNum: 1, pageSize: 3 })
    if (res.code === 200 && res.data) {
      // 后端返回分页数据，需要从 records 中获取
      const records = res.data.records || res.data.list || res.data || []
      recommendedRecipes.value = records.slice(0, 3).map(recipe => ({
        id: recipe.id,
        name: recipe.recipeName,  // 后端字段是 recipeName
        effect: recipe.efficacy || '',  // 后端字段是 efficacy
        season: recipe.season || 'ALL',
        constitution: recipe.constitutionType || '',
        image: recipe.image || '',
        recommendationReason: recipe.recommendationReason || ''  // AI推荐理由
      }))
    } else if (res.code === 404 || res.message?.includes('体质测试')) {
      // 用户未完成体质测试，显示提示信息
      recommendedRecipes.value = []
    } else {
      recommendedRecipes.value = []
    }
  } catch (error) {

    // 使用空数组
    recommendedRecipes.value = []
  }
}

// 养生文章
const healthArticles = ref([])

// 加载养生文章
const loadHealthArticles = async () => {
  try {
    const res = await getRecommendedArticles(3)
    if (res.code === 200 && res.data) {
      // 后端返回的是 List，不是分页对象
      const articles = Array.isArray(res.data) ? res.data : (res.data.records || res.data.list || [])
      healthArticles.value = articles.slice(0, 3).map(article => ({
        id: article.id,
        title: article.title,
        summary: article.summary || (article.content ? article.content.substring(0, 100) + '...' : ''),
        category: article.category || '养生知识',
        publishTime: dayjs(article.publishTime || article.createdAt).format('YYYY-MM-DD HH:mm'),
        viewCount: article.viewCount || 0,
        commentCount: article.commentCount || 0
      }))
    } else {
      healthArticles.value = []
    }
  } catch (error) {

    // 使用空数组
    healthArticles.value = []
  }
}


// 跳转测试历史
const goToConstitutionHistory = () => {
  router.push('/patient/constitution/history')
}

// 跳转药膳列表
const goToRecipes = () => {
  router.push('/patient/recipe')
}

// 跳转药膳详情
const goToRecipeDetail = (id) => {
  router.push(`/patient/recipe/${id}`)
}

// 跳转文章详情
const goToArticleDetail = (id) => {
  router.push(`/patient/community/article/${id}`)
}

// 初始化健康趋势图表
const initHealthTrendChart = async () => {
  const userId = userStore.userInfo?.id
  if (!userId || !healthTrendChartRef.value) return

  try {
    // 获取最近7天的打卡数据
    const endDate = dayjs().format('YYYY-MM-DD')
    const startDate = dayjs().subtract(6, 'day').format('YYYY-MM-DD')

    const res = await getCheckinList({
      userId: userId,
      startDate: startDate,
      endDate: endDate,
      pageNum: 1,
      pageSize: 100
    })

    if (res.code === 200) {
      healthTrendChartInstance = echarts.init(healthTrendChartRef.value)

      const checkinData = res.data?.records || res.data?.list || []

      // 生成最近7天的日期数组
      const dates = []
      for (let i = 6; i >= 0; i--) {
        dates.push(dayjs().subtract(i, 'day').format('YYYY-MM-DD'))
      }

      // 创建日期到数据的映射
      const dataMap = {}
      checkinData.forEach(item => {
        const dateKey = dayjs(item.checkinDate).format('YYYY-MM-DD')
        dataMap[dateKey] = item
      })

      // 提取各项数据（适配后端字段名）
      const weights = dates.map(date => dataMap[date]?.weight || null)
      const sleepHours = dates.map(date => dataMap[date]?.sleepDuration || null)
      const exerciseMinutes = dates.map(date => dataMap[date]?.exerciseDuration || null)
      const moodScores = dates.map(date => dataMap[date]?.moodScore || null)

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        legend: {
          data: ['体重(kg)', '睡眠(小时)', '运动(分钟)', '心情(分)'],
          bottom: 0
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: dates.map(date => dayjs(date).format('MM-DD')),
          axisLabel: {
            color: '#666'
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            color: '#666'
          }
        },
        series: [
          {
            name: '体重(kg)',
            type: 'line',
            data: weights,
            smooth: true,
            itemStyle: {
              color: '#1890ff'
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(24, 144, 255, 0.3)' },
                  { offset: 1, color: 'rgba(24, 144, 255, 0.05)' }
                ]
              }
            }
          },
          {
            name: '睡眠(小时)',
            type: 'line',
            data: sleepHours,
            smooth: true,
            itemStyle: {
              color: '#52c41a'
            }
          },
          {
            name: '运动(分钟)',
            type: 'line',
            data: exerciseMinutes,
            smooth: true,
            itemStyle: {
              color: '#faad14'
            }
          },
          {
            name: '心情(分)',
            type: 'line',
            data: moodScores,
            smooth: true,
            itemStyle: {
              color: '#f5222d'
            }
          }
        ]
      }

      healthTrendChartInstance.setOption(option)

      // 响应式调整
      window.addEventListener('resize', () => {
        healthTrendChartInstance?.resize()
      })
    }
  } catch (error) {

  }
}

// 页面加载时执行
onMounted(async () => {
  loadStats()
  loadLatestConstitution()
  loadRecommendedRecipes()
  loadHealthArticles()

  // 加载患者端数据
  await patientStore.fetchHealthStats({
    startDate: dayjs().subtract(30, 'day').format('YYYY-MM-DD'),
    endDate: dayjs().format('YYYY-MM-DD')
  })

  // 初始化图表
  await nextTick()
  initHealthTrendChart()
})
</script>

<style scoped lang="scss">
.home-container {
  max-width: 1400px;
  margin: 0 auto;
}

.welcome-card {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);

  .welcome-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;

    .welcome-left {
      flex: 1;

      h1 {
        font-size: 28px;
        color: #333;
        margin-bottom: 10px;
        font-weight: 600;
      }

      p {
        color: #52c41a;
        margin-bottom: 20px;
        font-size: 16px;
        font-weight: 500;
      }

      .action-buttons {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
      }
    }

    .welcome-right {
      opacity: 0.2;
    }
  }
}

.stats-row {
  margin-bottom: 20px;
}

.patient-stat-card {
  padding: 24px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  }

  &.green {
    background: linear-gradient(135deg, #f6ffed 0%, #d9f7be 100%);
    border: 1px solid #b7eb8f;

    .stat-icon {
      background: #52c41a;
    }
  }

  &.orange {
    background: linear-gradient(135deg, #fff7e6 0%, #ffe7ba 100%);
    border: 1px solid #ffd591;

    .stat-icon {
      background: #fa8c16;
    }
  }

  &.blue {
    background: linear-gradient(135deg, #e6f7ff 0%, #bae7ff 100%);
    border: 1px solid #91d5ff;

    .stat-icon {
      background: #1890ff;
    }
  }

  &.red {
    background: linear-gradient(135deg, #fff1f0 0%, #ffccc7 100%);
    border: 1px solid #ffa39e;

    .stat-icon {
      background: #f5222d;
    }
  }

  .stat-content {
    display: flex;
    align-items: center;
    gap: 20px;

    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 28px;
      flex-shrink: 0;
    }

    .stat-info {
      flex: 1;

      .stat-number {
        font-size: 32px;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
        line-height: 1;
      }

      .stat-label {
        color: #666;
        font-size: 14px;
      }
    }
  }
}


.constitution-card {
  margin-bottom: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
  }

  .constitution-content {
    .constitution-main {
      margin-bottom: 20px;
      padding: 20px;
      background: #f6ffed;
      border-radius: 8px;
      border: 1px solid #b7eb8f;

      .constitution-desc {
        margin: 15px 0;
        color: #333;
        font-size: 15px;
        line-height: 1.6;
      }

      .constitution-date {
        color: #999;
        font-size: 13px;
      }
    }

    .constitution-suggestions {
      h4 {
        margin: 0 0 15px 0;
        color: #333;
        font-size: 15px;
      }

      ul {
        margin: 0;
        padding-left: 20px;

        li {
          color: #666;
          line-height: 2;
          font-size: 14px;
        }
      }
    }
  }
}

.recommended-recipes {
  margin-bottom: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
  }

  .recipe-card {
    margin-bottom: 20px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .recipe-image {
      height: 180px;
      overflow: hidden;
      border-radius: 4px;
      margin-bottom: 15px;

      .el-image {
        width: 100%;
        height: 100%;
      }
    }

    .recipe-info {
      h4 {
        margin: 0 0 8px 0;
        color: #333;
        font-size: 16px;
        font-weight: 600;
      }

      .recipe-recommendation {
        font-size: 12px;
        color: #409EFF;
        line-height: 1.6;
        margin: 8px 0;
        padding: 8px;
        background: #ecf5ff;
        border-radius: 4px;
        border-left: 3px solid #409EFF;
        display: flex;
        align-items: flex-start;
        gap: 6px;
      }

      .recipe-recommendation .el-icon {
        margin-top: 2px;
        flex-shrink: 0;
      }

      .recipe-effect {
        margin: 0 0 10px 0;
        color: #666;
        font-size: 14px;
        line-height: 1.5;
      }

      .recipe-meta {
        display: flex;
        gap: 8px;
      }
    }
  }
}

.health-articles {
  margin-bottom: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
  }

  .article-item {
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .article-content {
      h4 {
        margin: 0 0 10px 0;
        color: #333;
        font-size: 15px;
        font-weight: 600;
      }

      p {
        margin: 0 0 12px 0;
        color: #666;
        font-size: 14px;
        line-height: 1.6;
      }

      .article-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;

        .article-stats {
          display: flex;
          align-items: center;
          gap: 15px;
          color: #999;
          font-size: 13px;

          .el-icon {
            margin-right: 4px;
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .welcome-card {
    .welcome-content {
      .welcome-left {
        h1 {
          font-size: 22px;
        }

        .action-buttons {
          flex-direction: column;

          .el-button {
            width: 100%;
          }
        }
      }

      .welcome-right {
        display: none;
      }
    }
  }

  .stat-card {
    .stat-content {
      .stat-info {
        .stat-number {
          font-size: 24px;
        }
      }
    }
  }

  .recipe-card {
    .recipe-image {
      height: 150px;

      .image-slot {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        background: #f5f7fa;
        color: #909399;
        font-size: 30px;
      }
    }
  }
}
</style>
