<template>
  <div class="acupoint-detail-container">
    <el-page-header @back="goBack" title="返回">
      <template #content>
        <span class="page-title">穴位详情</span>
      </template>
    </el-page-header>

    <el-card class="detail-card" v-loading="loading">
      <div v-if="acupoint">
        <!-- 基本信息 -->
        <div class="basic-info">
          <div class="info-left">
            <h1>{{ acupoint.acupointName }}</h1>
            <p class="pinyin">{{ acupoint.pinyin }}</p>
            <el-tag type="primary" size="large">{{ acupoint.meridian }}</el-tag>
            <div class="view-count">
              <el-icon><View /></el-icon>
              浏览量：{{ acupoint.viewCount || 0 }}
            </div>
          </div>
          <div class="info-right">
            <img :src="acupoint.image || '/default-acupoint.png'" :alt="acupoint.acupointName" />
          </div>
        </div>

        <el-divider />

        <!-- 详细信息 -->
        <div class="detail-info">
          <!-- 定位 -->
          <div class="info-section">
            <h3><el-icon><Location /></el-icon> 穴位定位</h3>
            <p>{{ acupoint.location }}</p>
          </div>

          <!-- 解剖 -->
          <div class="info-section" v-if="acupoint.anatomy">
            <h3><el-icon><Document /></el-icon> 解剖结构</h3>
            <p>{{ acupoint.anatomy }}</p>
          </div>

          <!-- 主治 -->
          <div class="info-section">
            <h3><el-icon><FirstAidKit /></el-icon> 主治功效</h3>
            <p>{{ acupoint.indications }}</p>
          </div>

          <!-- 按摩方法 -->
          <div class="info-section">
            <h3><el-icon><Operation /></el-icon> 按摩方法</h3>
            <p>{{ acupoint.massageMethod }}</p>
          </div>

          <!-- 注意事项 -->
          <div class="info-section" v-if="acupoint.precautions">
            <h3><el-icon><Warning /></el-icon> 注意事项</h3>
            <el-alert type="warning" :closable="false">
              <p>{{ acupoint.precautions }}</p>
            </el-alert>
          </div>

          <!-- 视频教程 -->
          <div class="info-section" v-if="acupoint.videoUrl">
            <h3><el-icon><VideoPlay /></el-icon> 视频教程</h3>
            <video :src="acupoint.videoUrl" controls style="width: 100%; max-width: 800px;"></video>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { View, Location, Document, FirstAidKit, Operation, Warning, VideoPlay } from '@element-plus/icons-vue'
import { getAcupointDetail } from '@/api/acupoint'

const route = useRoute()
const router = useRouter()

const acupoint = ref(null)
const loading = ref(false)

// 加载穴位详情
const loadDetail = async () => {
  loading.value = true
  try {
    const id = route.params.id
    const res = await getAcupointDetail(id)
    if (res.code === 200) {
      acupoint.value = res.data
    }
  } catch (error) {

    message.error('加载穴位详情失败')
  } finally {
    loading.value = false
  }
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
.acupoint-detail-container {
  padding: 20px;
}

.page-title {
  font-size: 18px;
  font-weight: 500;
}

.detail-card {
  margin-top: 20px;
}

.basic-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 30px;
}

.info-left {
  flex: 1;
}

.info-left h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 10px;
}

.pinyin {
  font-size: 16px;
  color: #999;
  margin-bottom: 15px;
}

.view-count {
  margin-top: 15px;
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 5px;
}

.info-right {
  width: 300px;
  flex-shrink: 0;
}

.info-right img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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

@media (max-width: 768px) {
  .basic-info {
    flex-direction: column;
  }

  .info-right {
    width: 100%;
  }
}
</style>

