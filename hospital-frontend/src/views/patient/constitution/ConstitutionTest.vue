<template>
  <div class="constitution-test">
    <!-- 测试说明 -->
    <el-card v-if="!testStarted" class="intro-card">
      <template #header>
        <div class="card-header">
          <span>中医体质辨识测试</span>
        </div>
      </template>

      <div class="intro-content">
        <el-alert title="测试说明" type="info" :closable="false" show-icon>
          <p>本测试基于中医体质学理论，通过66道题目的问答，帮助您了解自己的体质类型。</p>
          <p>请根据近一年的体验和感觉回答问题，每题选择最符合您情况的选项。</p>
        </el-alert>

        <div class="constitution-types">
          <h3>九种体质类型</h3>
          <el-row :gutter="20">
            <el-col :span="8" v-for="type in constitutionTypes" :key="type.typeCode">
              <div class="type-card">
                <div class="type-icon" :style="{ backgroundColor: type.color }">
                  {{ type.icon || type.typeName.charAt(0) }}
                </div>
                <div class="type-name">{{ type.typeName }}</div>
                <div class="type-desc">{{ type.description }}</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="test-info">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="题目数量">66题</el-descriptions-item>
            <el-descriptions-item label="预计时间">10-15分钟</el-descriptions-item>
            <el-descriptions-item label="评分方式">5级评分</el-descriptions-item>
            <el-descriptions-item label="结果类型">主要体质 + 次要体质</el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="start-button">
          <el-button type="primary" size="large" @click="startTest" :loading="loading">
            开始测试
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 测试问卷 -->
    <div v-else class="test-content">
      <!-- 进度条 -->
      <el-card class="progress-card">
        <el-progress :percentage="progress" :stroke-width="20" :text-inside="true">
          <span>{{ answeredCount }}/{{ totalQuestions }}</span>
        </el-progress>
      </el-card>

      <!-- 问题列表 -->
      <el-card class="question-card">
        <div class="question-item" v-for="question in questions" :key="question.id">
          <div class="question-header">
            <span class="question-number">{{ question.questionOrder }}.</span>
            <span class="question-text">{{ question.questionText }}</span>
            <el-tag v-if="answers[question.id]" type="success" size="small">已答</el-tag>
          </div>

          <el-radio-group v-model="answers[question.id]" class="question-options" @change="onAnswerChange">
            <el-radio v-for="option in question.options" :key="option.id" :label="option.id" border>
              {{ option.optionText }}
            </el-radio>
          </el-radio-group>
        </div>
      </el-card>

      <!-- 提交按钮 -->
      <el-card class="submit-card">
        <el-button type="primary" size="large" @click="submitTest" :disabled="!isAllAnswered" :loading="submitting">
          {{ isAllAnswered ? '提交测试' : `还有 ${totalQuestions - answeredCount} 题未完成` }}
        </el-button>
        <el-button size="large" @click="cancelTest">取消测试</el-button>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { getConstitutionTypes, getQuestionnaire, submitTest as submitTestApi } from '@/api/constitution'

const router = useRouter()
const route = useRoute()

// 获取预约ID（如果是通过预约提醒进入的）
const appointmentId = ref(route.query.appointmentId ? Number(route.query.appointmentId) : null)

// 数据
const loading = ref(false)
const submitting = ref(false)
const testStarted = ref(false)
const constitutionTypes = ref([])
const questions = ref([])
const answers = ref({})

// 计算属性
const totalQuestions = computed(() => questions.value.length)
const answeredCount = computed(() => Object.keys(answers.value).length)
const progress = computed(() => {
  if (totalQuestions.value === 0) return 0
  return Math.round((answeredCount.value / totalQuestions.value) * 100)
})
const isAllAnswered = computed(() => answeredCount.value === totalQuestions.value)

// 加载体质类型
const loadConstitutionTypes = async () => {
  try {
    loading.value = true
    const res = await getConstitutionTypes()
    if (res.code === 200) {
      constitutionTypes.value = res.data
    }
  } catch (error) {

    message.error('加载体质类型失败')
  } finally {
    loading.value = false
  }
}

// 开始测试
const startTest = async () => {
  try {
    loading.value = true
    const res = await getQuestionnaire()
    if (res.code === 200) {
      questions.value = res.data
      testStarted.value = true
      // 滚动到顶部
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  } catch (error) {

    message.error('加载问卷失败')
  } finally {
    loading.value = false
  }
}

// 答案改变
const onAnswerChange = () => {
  // 可以在这里保存答案到本地存储，防止意外关闭
  localStorage.setItem('constitution_test_answers', JSON.stringify(answers.value))
}

// 提交测试
const submitTest = async () => {
  if (!isAllAnswered.value) {
    message.warning('请完成所有题目后再提交')
    return
  }

  try {
    await ElMessageBox.confirm('确认提交测试？提交后将无法修改答案。', '提示', {
      confirmButtonText: '确认提交',
      cancelButtonText: '继续答题',
      type: 'warning'
    })

    submitting.value = true
    // 提交测试时，如果有预约ID，一起提交
    const submitData = {
      answers: answers.value
    }
    if (appointmentId.value) {
      submitData.appointmentId = appointmentId.value
    }

    const res = await submitTestApi(submitData)

    if (res.code === 200) {
      message.success('测试提交成功')
      // 清除本地存储的答案
      localStorage.removeItem('constitution_test_answers')
      // 跳转到结果页面
      router.push({
        name: 'TestResult',
        params: { id: res.data.id }
      })
    }
  } catch (error) {
    if (error !== 'cancel') {

      message.error('提交测试失败')
    }
  } finally {
    submitting.value = false
  }
}

// 取消测试
const cancelTest = async () => {
  try {
    await ElMessageBox.confirm('确认取消测试？当前答题进度将会丢失。', '提示', {
      confirmButtonText: '确认取消',
      cancelButtonText: '继续答题',
      type: 'warning'
    })

    // 清除答案
    answers.value = {}
    localStorage.removeItem('constitution_test_answers')
    testStarted.value = false
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (error) {
    // 用户取消操作
  }
}

// 页面加载
onMounted(() => {
  loadConstitutionTypes()

  // 尝试恢复之前的答题进度
  const savedAnswers = localStorage.getItem('constitution_test_answers')
  if (savedAnswers) {
    try {
      answers.value = JSON.parse(savedAnswers)
    } catch (error) {

    }
  }
})
</script>

<style scoped>
.constitution-test {
  padding: 20px;
}

.intro-card {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  font-size: 20px;
  font-weight: bold;
}

.intro-content {
  padding: 20px 0;
}

.intro-content .el-alert {
  margin-bottom: 30px;
}

.intro-content .el-alert p {
  margin: 5px 0;
  line-height: 1.8;
}

.constitution-types {
  margin: 30px 0;
}

.constitution-types h3 {
  margin-bottom: 20px;
  font-size: 18px;
  color: #303133;
}

.type-card {
  text-align: center;
  padding: 20px;
  border: 1px solid #EBEEF5;
  border-radius: 4px;
  margin-bottom: 20px;
  transition: all 0.3s;
}

.type-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.type-icon {
  width: 60px;
  height: 60px;
  line-height: 60px;
  margin: 0 auto 10px;
  border-radius: 50%;
  color: white;
  font-size: 24px;
  font-weight: bold;
}

.type-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #303133;
}

.type-desc {
  font-size: 13px;
  color: #909399;
  line-height: 1.6;
}

.test-info {
  margin: 30px 0;
}

.start-button {
  text-align: center;
  margin-top: 30px;
}

.start-button .el-button {
  width: 200px;
}

.progress-card {
  margin-bottom: 20px;
}

.question-card {
  margin-bottom: 20px;
}

.question-item {
  padding: 20px 0;
  border-bottom: 1px solid #EBEEF5;
}

.question-item:last-child {
  border-bottom: none;
}

.question-header {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.question-number {
  font-weight: bold;
  color: #409EFF;
  font-size: 16px;
}

.question-text {
  flex: 1;
  font-size: 15px;
  color: #303133;
  line-height: 1.6;
}

.question-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-left: 30px;
}

.question-options .el-radio {
  margin-right: 0;
  width: 100%;
}

.submit-card {
  text-align: center;
  position: sticky;
  bottom: 20px;
  z-index: 100;
}

.submit-card .el-button {
  min-width: 200px;
  margin: 0 10px;
}
</style>
