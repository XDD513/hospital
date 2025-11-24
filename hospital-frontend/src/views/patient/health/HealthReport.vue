<template>
  <div class="health-report-container">
    <div class="page-header">
      <h2>健康报告</h2>
      <el-button type="primary" @click="generateReport" :loading="generating">
        <el-icon><Document /></el-icon>
        生成报告
      </el-button>
    </div>

    <el-card class="report-card" v-loading="loading">
      <div v-if="report" ref="reportContentRef" class="report-content">
        <!-- 报告头部 -->
        <div class="report-header">
          <h1>个人健康评估报告</h1>
          <div class="report-meta">
            <span>报告编号：{{ report.id }}</span>
            <span>生成时间：{{ formatTime(report.createdAt) }}</span>
          </div>
        </div>

        <el-divider />

        <!-- 基本信息 -->
        <div class="report-section">
          <h3>一、基本信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="姓名">{{ report.userName }}</el-descriptions-item>
            <el-descriptions-item label="性别">{{ report.gender === 1 ? '男' : '女' }}</el-descriptions-item>
            <el-descriptions-item label="年龄">{{ report.age }}岁</el-descriptions-item>
            <el-descriptions-item label="体质类型">
              <el-tag type="success">{{ getConstitutionLabel(report.constitutionType) }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="BMI">
              <el-tag :type="getBMIType(report.bmi)">{{ report.bmi }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="健康评分">
              <el-tag :type="getScoreType(report.healthScore)">{{ report.healthScore }}分</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 健康指标 -->
        <div class="report-section">
          <h3>二、健康指标分析</h3>
          <div class="indicators">
            <div class="indicator-item">
              <div class="indicator-label">体重指数</div>
              <el-progress
                :percentage="getIndicatorPercentage(report.weightIndicator)"
                :status="getIndicatorStatus(report.weightIndicator)"
              />
              <div class="indicator-desc">{{ report.weightIndicator?.description }}</div>
            </div>

            <div class="indicator-item">
              <div class="indicator-label">睡眠质量</div>
              <el-progress
                :percentage="getIndicatorPercentage(report.sleepIndicator)"
                :status="getIndicatorStatus(report.sleepIndicator)"
              />
              <div class="indicator-desc">{{ report.sleepIndicator?.description }}</div>
            </div>

            <div class="indicator-item">
              <div class="indicator-label">运动水平</div>
              <el-progress
                :percentage="getIndicatorPercentage(report.exerciseIndicator)"
                :status="getIndicatorStatus(report.exerciseIndicator)"
              />
              <div class="indicator-desc">{{ report.exerciseIndicator?.description }}</div>
            </div>

            <div class="indicator-item">
              <div class="indicator-label">情绪状态</div>
              <el-progress
                :percentage="getIndicatorPercentage(report.moodIndicator)"
                :status="getIndicatorStatus(report.moodIndicator)"
              />
              <div class="indicator-desc">{{ report.moodIndicator?.description }}</div>
            </div>
          </div>
        </div>

        <!-- 健康建议 -->
        <div class="report-section">
          <h3>三、健康建议</h3>
          <div class="suggestions">
            <div class="suggestion-item" v-for="(suggestion, index) in report.suggestions" :key="index">
              <div class="suggestion-title">
                <el-icon><Star /></el-icon>
                {{ suggestion.title }}
              </div>
              <div class="suggestion-content">{{ suggestion.content }}</div>
            </div>
          </div>
        </div>

        <!-- 风险提示 -->
        <div class="report-section" v-if="report.risks && report.risks.length > 0">
          <h3>四、风险提示</h3>
          <el-alert
            v-for="(risk, index) in report.risks"
            :key="index"
            :title="risk.title"
            :description="risk.description"
            type="warning"
            :closable="false"
            style="margin-bottom: 10px;"
          />
        </div>

        <!-- 总结 -->
        <div class="report-section">
          <h3>五、总结</h3>
          <p class="summary">{{ report.summary }}</p>
        </div>

        <!-- 报告操作 -->
        <div class="report-actions">
          <el-button type="primary" @click="handlePrint">
            <el-icon><Printer /></el-icon>
            打印报告
          </el-button>
          <el-button @click="handleExport" :loading="exporting">
            <el-icon><Download /></el-icon>
            导出PDF
          </el-button>
        </div>
      </div>

      <el-empty v-else description="暂无健康报告，请点击生成报告" />
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, onMounted, nextTick } from 'vue'

import { Document, Star, Printer, Download } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import dayjs from 'dayjs'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'
import { generateHealthReport } from '@/api/health'

const userStore = useUserStore()

const report = ref(null)
const loading = ref(false)
const generating = ref(false)
const exporting = ref(false)
const reportContentRef = ref(null)

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

// 生成报告
const generateReport = async () => {
  const userId = userStore.userInfo?.id
  if (!userId) {
    message.warning('请先登录')
    return
  }

  generating.value = true
  try {
    const res = await generateHealthReport(userId)
    if (res.code === 200) {
      report.value = res.data
      message.success('报告生成成功')
    }
  } catch (error) {

    message.error('生成报告失败')
  } finally {
    generating.value = false
  }
}

// 获取BMI类型
const getBMIType = (bmi) => {
  if (!bmi) return 'info'
  if (bmi < 18.5) return 'warning'
  if (bmi < 24) return 'success'
  if (bmi < 28) return 'warning'
  return 'danger'
}

// 获取评分类型
const getScoreType = (score) => {
  if (!score) return 'info'
  if (score >= 90) return 'success'
  if (score >= 70) return ''
  if (score >= 60) return 'warning'
  return 'danger'
}

// 获取指标百分比
const getIndicatorPercentage = (indicator) => {
  if (!indicator || !indicator.score) return 0
  return indicator.score
}

// 获取指标状态
const getIndicatorStatus = (indicator) => {
  if (!indicator || !indicator.score) return ''
  if (indicator.score >= 80) return 'success'
  if (indicator.score >= 60) return ''
  return 'exception'
}

// 获取体质标签
const getConstitutionLabel = (type) => {
  return constitutionMap[type] || type || '未测试'
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

// 打印报告
const handlePrint = () => {
  window.print()
}

// 导出PDF
const handleExport = async () => {
  if (!report.value) {
    message.warning('请先生成健康报告')
    return
  }
  if (!reportContentRef.value) {
    message.error('未找到报告内容，导出失败')
    return
  }

  exporting.value = true
  try {
    await nextTick()
    const canvas = await html2canvas(reportContentRef.value, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#ffffff'
    })
    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF('p', 'mm', 'a4')
    const pdfWidth = pdf.internal.pageSize.getWidth()
    const pdfHeight = (canvas.height * pdfWidth) / canvas.width
    let heightLeft = pdfHeight
    let position = 0
    const pageHeight = pdf.internal.pageSize.getHeight()

    pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, pdfHeight)
    heightLeft -= pageHeight

    while (heightLeft > 0) {
      position = heightLeft - pdfHeight
      pdf.addPage()
      pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, pdfHeight)
      heightLeft -= pageHeight
    }

    const fileName = `健康报告_${report.value?.userName || '用户'}_${dayjs().format('YYYYMMDDHHmm')}.pdf`
    pdf.save(fileName)
    message.success('PDF 导出成功')
  } catch (error) {
    console.error('导出PDF失败', error)
    message.error('导出PDF失败，请稍后重试')
  } finally {
    exporting.value = false
  }
}

onMounted(() => {
  // 可以在这里加载最新的报告
})
</script>

<style scoped>
.health-report-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.report-card {
  max-width: 1000px;
  margin: 0 auto;
}

.report-content {
  background: #fff;
  padding: 10px;
}

.report-header {
  text-align: center;
  margin-bottom: 30px;
}

.report-header h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 15px;
}

.report-meta {
  display: flex;
  justify-content: center;
  gap: 30px;
  font-size: 14px;
  color: #999;
}

.report-section {
  margin-bottom: 30px;
}

.report-section h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 15px;
  padding-left: 10px;
  border-left: 4px solid #409eff;
}

.indicators {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.indicator-item {
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.indicator-label {
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
  font-weight: 500;
}

.indicator-desc {
  font-size: 13px;
  color: #666;
  margin-top: 10px;
}

.suggestions {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.suggestion-item {
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
}

.suggestion-title {
  font-size: 16px;
  color: #333;
  font-weight: 500;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.suggestion-content {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.summary {
  font-size: 15px;
  color: #666;
  line-height: 1.8;
  text-align: justify;
}

.report-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
  padding-top: 30px;
  border-top: 1px solid #e0e0e0;
}

@media print {
  .page-header,
  .report-actions {
    display: none;
  }
}
</style>

