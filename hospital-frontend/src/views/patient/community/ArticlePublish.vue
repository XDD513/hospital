<template>
  <div class="article-publish-container">
    <el-page-header @back="goBack" title="返回">
      <template #content>
        <span class="page-title">{{ isEdit ? '编辑文章' : '发布文章' }}</span>
      </template>
    </el-page-header>

    <el-card class="publish-card">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="文章标题" prop="title">
          <el-input
            v-model="formData.title"
            placeholder="请输入文章标题"
            maxlength="100"
            show-word-limit
            @blur="handleFieldBlur('title')"
          />
        </el-form-item>

        <el-form-item label="文章分类" prop="category">
          <el-select v-model="formData.category" placeholder="请选择分类" @change="handleFieldBlur('category')">
            <el-option label="体质养生" value="CONSTITUTION" />
            <el-option label="饮食养生" value="DIET" />
            <el-option label="运动养生" value="EXERCISE" />
            <el-option label="穴位养生" value="ACUPOINT" />
            <el-option label="季节养生" value="SEASON" />
            <el-option label="其他" value="OTHER" />
          </el-select>
        </el-form-item>

        <el-form-item label="文章摘要" prop="summary">
          <el-input
            v-model="formData.summary"
            type="textarea"
            :rows="3"
            placeholder="请输入文章摘要"
            maxlength="200"
            show-word-limit
            @blur="handleFieldBlur('summary')"
          />
        </el-form-item>

        <el-form-item label="封面图片" prop="coverImage">
          <el-input
            v-model="formData.coverImage"
            placeholder="请输入封面图片URL"
          />
          <div class="cover-preview" v-if="formData.coverImage">
            <img :src="formData.coverImage" alt="封面预览" />
          </div>
        </el-form-item>

        <el-form-item label="文章内容" prop="content">
          <el-input
            v-model="formData.content"
            type="textarea"
            :rows="15"
            placeholder="请输入文章内容（支持HTML格式）"
            @blur="handleFieldBlur('content')"
          />
        </el-form-item>

        <el-form-item label="标签">
          <el-input
            v-model="formData.tags"
            placeholder="请输入标签，多个标签用逗号分隔"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ isEdit ? '更新文章' : '发布文章' }}
          </el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useUserStore } from '@/stores/user'
import {
  publishArticle,
  updateArticle,
  getArticleDetail
} from '@/api/article'
import { useFormValidation } from '@/composables/useFormValidation'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)

// 创建字段失焦处理函数
const { handleFieldBlur } = useFormValidation(formRef)
const submitting = ref(false)
const isEdit = ref(false)

const formData = ref({
  title: '',
  category: '',
  summary: '',
  coverImage: '',
  content: '',
  tags: '',
  authorId: null,
  authorName: ''
})

const rules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' },
    { min: 5, max: 100, message: '标题长度在 5 到 100 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择文章分类', trigger: 'change' }
  ],
  summary: [
    { required: true, message: '请输入文章摘要', trigger: 'blur' },
    { min: 10, max: 200, message: '摘要长度在 10 到 200 个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文章内容', trigger: 'blur' },
    { min: 50, message: '内容至少 50 个字符', trigger: 'blur' }
  ]
}

// 加载文章详情（编辑模式）
const loadArticle = async () => {
  try {
    const id = route.params.id
    const res = await getArticleDetail(id)
    if (res.code === 200) {
      const article = res.data
      formData.value = {
        title: article.title,
        category: article.category,
        summary: article.summary,
        coverImage: article.coverImage,
        content: article.content,
        tags: article.tags,
        authorId: article.authorId,
        authorName: article.authorName
      }
    }
  } catch (error) {

    message.error('加载文章失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    const userId = userStore.userInfo?.id
    if (!userId) {
      message.warning('请先登录')
      return
    }

    submitting.value = true
    try {
      const data = {
        ...formData.value,
        authorId: userId,
        authorName: userStore.userInfo.username
      }

      if (isEdit.value) {
        const id = route.params.id
        await updateArticle(id, data)
        message.success('更新成功')
      } else {
        await publishArticle(data)
        message.success('发布成功')
      }

      router.push('/patient/community/my-articles')
    } catch (error) {

      message.error(isEdit.value ? '更新失败' : '发布失败')
    } finally {
      submitting.value = false
    }
  })
}

// 返回
const goBack = () => {
  router.back()
}

onMounted(() => {
  // 检查是否是编辑模式
  if (route.params.id) {
    isEdit.value = true
    loadArticle()
  }
})
</script>

<style scoped>
.article-publish-container {
  padding: 20px;
}

.page-title {
  font-size: 18px;
  font-weight: 500;
}

.publish-card {
  margin-top: 20px;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

.cover-preview {
  margin-top: 10px;
  width: 300px;
  height: 200px;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.cover-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>

