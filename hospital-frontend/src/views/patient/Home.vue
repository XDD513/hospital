<template>
  <div class="home-container">
    <!-- 欢迎横幅 -->
    <HspHeroBanner 
      :system-name="systemName" 
      :user-name="userStore.userInfo.realName || userStore.userInfo.username"
    />

    <!-- 统计卡片 -->
    <HspStatGrid :stats="stats" />

    <!-- 我的体质 -->
    <HspConstitutionPanel :constitution="latestConstitution" />

    <!-- 健康趋势 -->
    <HspHealthTrend :user-id="userStore.userInfo?.id" />

    <!-- 推荐药膳 -->
    <HspRecipeList :recipes="recommendedRecipes" :loading="recipesLoading" />

    <!-- 养生知识 -->
    <HspArticleTimeline :articles="healthArticles" :loading="articlesLoading" />
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { usePatientStore } from '@/stores/patient'
import dayjs from 'dayjs'
import { getLatestTestResult } from '@/api/constitution'
import { getRecommendedRecipes } from '@/api/recipe'
import { getRecommendedArticles } from '@/api/article'
import { getPatientStats } from '@/api/statistics'
import { getAppConfig } from '@/config/runtimeConfig'
import HspHeroBanner from '@/components/patient/HspHeroBanner.vue'
import HspStatGrid from '@/components/patient/HspStatGrid.vue'
import HspConstitutionPanel from '@/components/patient/HspConstitutionPanel.vue'
import HspHealthTrend from '@/components/patient/HspHealthTrend.vue'
import HspRecipeList from '@/components/patient/HspRecipeList.vue'
import HspArticleTimeline from '@/components/patient/HspArticleTimeline.vue'

const router = useRouter()
const userStore = useUserStore()
const patientStore = usePatientStore()
const appConfig = inject('appConfig', getAppConfig())
const systemName = computed(() => appConfig?.systemInfo?.name || '中医体质辨识系统')

// 统计数据
const stats = ref({
  testCount: 0,
  recipeCount: 0,
  articleCount: 0,
  checkinDays: 0
})

// 最新体质测试结果
const latestConstitution = ref(null)

// 推荐药膳
const recommendedRecipes = ref([])
const recipesLoading = ref(false)

// 养生文章
const healthArticles = ref([])
const articlesLoading = ref(false)

// 并行加载所有数据
const loadAllData = async () => {
  const userId = userStore.userInfo?.id
  if (!userId) {
    return
  }

  // 使用 Promise.allSettled 并行请求，即使部分失败也不影响其他数据
  const results = await Promise.allSettled([
    // 统计数据
    getPatientStats().then(res => {
      if (res.code === 200 && res.data) {
        stats.value = {
          testCount: res.data.testCount || 0,
          recipeCount: res.data.recipeCount || 0,
          articleCount: res.data.articleCount || 0,
          checkinDays: res.data.checkinDays || 0
        }
      }
    }).catch(() => {
      // 使用默认值
      stats.value = { testCount: 0, recipeCount: 0, articleCount: 0, checkinDays: 0 }
    }),

    // 最新体质测试结果
    getLatestTestResult().then(res => {
      if (res.code === 200 && res.data) {
        const result = res.data
        const primaryDetail = result.primaryConstitutionDetail || {}
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
    }).catch(() => {
      latestConstitution.value = null
    }),

    // 推荐药膳
    (async () => {
      recipesLoading.value = true
      try {
        const res = await getRecommendedRecipes({ pageNum: 1, pageSize: 3 })
        if (res.code === 200 && res.data) {
          const records = res.data.records || res.data.list || res.data || []
          recommendedRecipes.value = records.slice(0, 3).map(recipe => ({
            id: recipe.id,
            name: recipe.recipeName,
            effect: recipe.efficacy || '',
            season: recipe.season || 'ALL',
            constitution: recipe.constitutionType || '',
            image: recipe.image || '',
            recommendationReason: recipe.recommendationReason || ''
          }))
        } else {
          recommendedRecipes.value = []
        }
      } catch (error) {
        recommendedRecipes.value = []
      } finally {
        recipesLoading.value = false
      }
    })(),

    // 养生文章
    (async () => {
      articlesLoading.value = true
      try {
        const res = await getRecommendedArticles(3)
        if (res.code === 200 && res.data) {
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
        healthArticles.value = []
      } finally {
        articlesLoading.value = false
      }
    })()
  ])
}

// 页面加载时执行
onMounted(async () => {
  await loadAllData()
  
  // 加载患者端数据（不影响首屏）
  patientStore.fetchHealthStats({
    startDate: dayjs().subtract(30, 'day').format('YYYY-MM-DD'),
    endDate: dayjs().format('YYYY-MM-DD')
  }).catch(() => {
    // 静默失败
  })
})
</script>

<style scoped lang="scss">
@import '@/styles/home-variables.scss';

.home-container {
  max-width: $breakpoint-xl;
  margin: 0 auto;
  padding: 0 $spacing-md;
}
</style>
