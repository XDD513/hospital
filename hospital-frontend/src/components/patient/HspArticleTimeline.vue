<template>
  <el-card class="hsp-article-timeline" shadow="never" v-animate-on-scroll>
    <template #header>
      <div class="card-header">
        <span>养生知识</span>
        <el-button text type="success" @click="goToArticles">
          查看更多 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
    </template>
    <el-timeline v-loading="loading">
      <el-timeline-item 
        v-for="article in articles" 
        :key="article.id" 
        :timestamp="article.publishTime"
        placement="top"
      >
        <el-card class="article-item" shadow="hover" @click="goToArticleDetail(article.id)">
          <div class="article-content">
            <h4>{{ article.title }}</h4>
            <p>{{ article.summary }}</p>
            <div class="article-meta">
              <el-tag size="small">{{ article.category }}</el-tag>
              <span class="article-stats">
                <el-icon><View /></el-icon> {{ article.viewCount }}
                <el-icon><ChatDotRound /></el-icon> {{ article.commentCount }}
              </span>
            </div>
          </div>
        </el-card>
      </el-timeline-item>
      <el-empty v-if="articles.length === 0 && !loading" description="暂无文章" />
    </el-timeline>
  </el-card>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ArrowRight, View, ChatDotRound } from '@element-plus/icons-vue'

const props = defineProps({
  articles: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()

// 跳转文章列表
const goToArticles = () => {
  router.push('/patient/community/articles')
}

// 跳转文章详情
const goToArticleDetail = (id) => {
  router.push(`/patient/community/article/${id}`)
}
</script>

<script>
// 滚动动画指令
export default {
  directives: {
    'animate-on-scroll': {
      mounted(el) {
        const observer = new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              if (entry.isIntersecting) {
                entry.target.classList.add('animate-in')
                observer.unobserve(entry.target)
              }
            })
          },
          { threshold: 0.1 }
        )
        observer.observe(el)
      }
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/home-variables.scss';

.hsp-article-timeline {
  margin-bottom: $spacing-lg;
  opacity: 0;
  transform: translateY(20px);

  &.animate-in {
    opacity: 1;
    transform: translateY(0);
    transition: all $transition-normal $ease-out;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
  }

  .article-item {
    cursor: pointer;
    transition: all $transition-normal;

    &:hover {
      box-shadow: $elevation-1;
    }

    .article-content {
      h4 {
        margin: 0 0 $spacing-sm 0;
        color: $text-primary;
        font-size: 15px;
        font-weight: 600;
      }

      p {
        margin: 0 0 $spacing-sm 0;
        color: $text-secondary;
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
          gap: $spacing-md;
          color: $text-tertiary;
          font-size: 13px;

          .el-icon {
            margin-right: 4px;
          }
        }
      }
    }
  }
}
</style>

