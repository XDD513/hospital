# 中医体质辨识与养生方案推荐系统

## 📖 项目简介

基于 **SpringBoot + Vue3** 的中医体质辨识与养生方案推荐系统，融合传统中医理论，提供个性化养生方案，区别于西医健康管理系统。

### 🎯 核心功能

1. **体质测试** - 基于中医九种体质分类的在线测试问卷
2. **药膳推荐** - 根据体质推荐个性化药膳食谱
3. **穴位按摩指导** - 穴位图谱、按摩手法视频教学
4. **中医预约** - 中医师在线预约咨询服务
5. **养生知识社区** - 用户分享养生经验、专家答疑

### ✨ 创新点

- 🌿 **融合传统中医理论** - 基于《中医体质分类与判定》标准
- 🎯 **个性化养生方案** - 根据体质自动生成养生建议
- 🤝 **知识社区互动** - 用户分享养生经验
- 🏥 **中医特色服务** - 区别于西医健康管理

---

## 🏗️ 技术架构

### 后端技术栈

```
Spring Boot 2.7.x          - 核心框架
MyBatis-Plus 3.5.x         - ORM框架
MySQL 8.0+                 - 关系型数据库
Redis 6.0+                 - 缓存中间件
Spring Security + JWT      - 认证授权
Swagger 3.0                - API文档
```

### 前端技术栈

```
Vue 3.3.x                  - 前端框架
Element Plus 2.4.x         - UI组件库
Vite 4.4.x                 - 构建工具
Pinia 2.1.x                - 状态管理
Axios 1.5.x                - HTTP客户端
ECharts 5.4.x              - 数据可视化
Quill Editor               - 富文本编辑器
```

---

## 📊 数据库设计

### 核心表结构（24张表）

#### 1. 基础表（5张）
- `user` - 用户表
- `tcm_category` - 中医分类表
- `tcm_doctor` - 中医师表
- `schedule` - 排班表
- `appointment` - 预约表

#### 2. 体质测试（4张）
- `constitution_type` - 体质类型表（9种体质）
- `constitution_questionnaire` - 测试问卷表（66题）
- `questionnaire_option` - 问卷选项表
- `user_constitution_test` - 用户测试记录表

#### 3. 药膳推荐（3张）
- `herbal_recipe` - 药膳食谱表
- `ingredient` - 食材库表
- `user_recipe_favorite` - 用户收藏表

#### 4. 穴位指导（2张）
- `acupoint` - 穴位信息表
- `acupoint_combination` - 穴位组合方案表

#### 5. 养生社区（4张）
- `health_article` - 养生文章表
- `article_comment` - 文章评论表
- `user_like` - 用户点赞表
- `user_article_favorite` - 文章收藏表

#### 6. 个人档案（3张）
- `user_health_profile` - 用户养生档案表
- `health_plan_record` - 养生方案记录表
- `health_checkin` - 健康打卡记录表

#### 7. 系统管理（3张）
- `system_config` - 系统配置表
- `operation_log` - 操作日志表
- `dictionary` - 数据字典表

---

## 🎨 中医九种体质

| 体质类型 | 代码 | 主要特征 | 养生重点 |
|---------|------|---------|---------|
| 平和质 | PINGHE | 阴阳气血调和 | 保持良好习惯 |
| 气虚质 | QIXU | 元气不足 | 益气健脾 |
| 阳虚质 | YANGXU | 阳气不足 | 温阳散寒 |
| 阴虚质 | YINXU | 阴液亏少 | 滋阴降火 |
| 痰湿质 | TANSHI | 痰湿凝聚 | 健脾化痰 |
| 湿热质 | SHIRE | 湿热内蕴 | 清热利湿 |
| 血瘀质 | XUEYU | 血行不畅 | 活血化瘀 |
| 气郁质 | QIYU | 气机郁滞 | 疏肝理气 |
| 特禀质 | TEBING | 先天失常 | 防止过敏 |

---

## 📁 项目结构

```
tcm-health-system/
├── hospital-appointment-system/          # 后端项目
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/hospital/
│   │   │   │   ├── controller/          # 控制层
│   │   │   │   │   ├── ConstitutionController.java
│   │   │   │   │   ├── HerbalRecipeController.java
│   │   │   │   │   ├── AcupointController.java
│   │   │   │   │   ├── HealthArticleController.java
│   │   │   │   │   └── ...
│   │   │   │   ├── service/             # 业务层
│   │   │   │   │   ├── ConstitutionService.java
│   │   │   │   │   ├── HerbalRecipeService.java
│   │   │   │   │   └── ...
│   │   │   │   ├── mapper/              # 数据访问层
│   │   │   │   ├── entity/              # 实体类
│   │   │   │   ├── dto/                 # 数据传输对象
│   │   │   │   ├── config/              # 配置类
│   │   │   │   ├── common/              # 公共模块
│   │   │   │   └── util/                # 工具类
│   │   │   └── resources/
│   │   │       ├── application.yml
│   │   │       └── mapper/              # MyBatis XML
│   │   └── test/                        # 测试代码
│   ├── sql/                             # SQL脚本
│   │   ├── tcm_constitution_system.sql  # 建表脚本
│   │   └── constitution_questionnaire_data.sql  # 问卷数据
│   └── pom.xml
│
├── hospital-frontend/                    # 前端项目
│   ├── src/
│   │   ├── views/                       # 页面
│   │   │   ├── constitution/            # 体质测试
│   │   │   │   ├── ConstitutionIntro.vue
│   │   │   │   ├── ConstitutionTest.vue
│   │   │   │   ├── TestResult.vue
│   │   │   │   └── TestHistory.vue
│   │   │   ├── recipe/                  # 药膳推荐
│   │   │   │   ├── RecipeList.vue
│   │   │   │   ├── RecipeDetail.vue
│   │   │   │   └── RecipeFavorites.vue
│   │   │   ├── acupoint/                # 穴位指导
│   │   │   │   ├── AcupointList.vue
│   │   │   │   ├── AcupointDetail.vue
│   │   │   │   └── AcupointCombination.vue
│   │   │   ├── community/               # 养生社区
│   │   │   │   ├── CommunityHome.vue
│   │   │   │   ├── ArticleList.vue
│   │   │   │   ├── ArticleDetail.vue
│   │   │   │   └── ArticlePublish.vue
│   │   │   └── user/                    # 个人中心
│   │   │       ├── UserProfile.vue
│   │   │       ├── HealthProfile.vue
│   │   │       └── HealthPlan.vue
│   │   ├── components/                  # 组件
│   │   ├── api/                         # API接口
│   │   ├── stores/                      # 状态管理
│   │   ├── router/                      # 路由
│   │   └── assets/                      # 静态资源
│   └── package.json
│
├── 中医体质辨识系统改造方案.md            # 改造方案
├── 项目改造实施计划.md                   # 实施计划
└── README_TCM_SYSTEM.md                 # 本文件
```

---

## 🚀 快速开始

### 环境要求

- JDK 8+
- Node.js 16+
- MySQL 8.0+
- Redis 6.0+
- Maven 3.6+

### 后端启动

```bash
# 1. 创建数据库
mysql -u root -p
CREATE DATABASE tcm_health_system DEFAULT CHARACTER SET utf8mb4;

# 2. 执行建表脚本
mysql -u root -p tcm_health_system < sql/tcm_constitution_system.sql
mysql -u root -p tcm_health_system < sql/constitution_questionnaire_data.sql

# 3. 修改配置文件
vim src/main/resources/application-dev.yml
# 修改数据库连接信息和Redis配置

# 4. 启动后端服务
cd hospital-appointment-system
mvn clean install
mvn spring-boot:run
```

### 前端启动

```bash
# 1. 安装依赖
cd hospital-frontend
npm install

# 2. 启动开发服务器
npm run dev

# 3. 访问系统
浏览器打开: http://localhost:3000
```

### 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |

---

## 📋 API接口文档

### 体质测试模块（7个接口）

```
GET  /api/constitution/types              - 获取体质类型列表
GET  /api/constitution/type/{code}        - 获取体质详情
GET  /api/constitution/questionnaire      - 获取测试问卷
POST /api/constitution/test/submit        - 提交测试
GET  /api/constitution/test/history       - 测试历史
GET  /api/constitution/test/report/{id}   - 测试报告
GET  /api/constitution/test/latest        - 最新测试结果
```

### 药膳推荐模块（9个接口）

```
GET    /api/recipe/recommend              - 推荐药膳
GET    /api/recipe/list                   - 药膳列表
GET    /api/recipe/{id}                   - 药膳详情
GET    /api/recipe/search                 - 搜索药膳
POST   /api/recipe/favorite/{id}          - 收藏药膳
DELETE /api/recipe/favorite/{id}          - 取消收藏
GET    /api/recipe/favorites              - 我的收藏
GET    /api/recipe/popular                - 热门药膳
GET    /api/recipe/seasonal               - 时令药膳
```

### 穴位指导模块（7个接口）

```
GET /api/acupoint/recommend               - 推荐穴位
GET /api/acupoint/list                    - 穴位列表
GET /api/acupoint/{id}                    - 穴位详情
GET /api/acupoint/search                  - 搜索穴位
GET /api/acupoint/meridian/{name}         - 按经络查询
GET /api/acupoint/combination/list        - 组合方案列表
GET /api/acupoint/combination/{id}        - 方案详情
```

### 养生社区模块（15个接口）

```
POST   /api/article/publish               - 发布文章
PUT    /api/article/{id}                  - 更新文章
DELETE /api/article/{id}                  - 删除文章
GET    /api/article/{id}                  - 文章详情
GET    /api/article/list                  - 文章列表
GET    /api/article/featured              - 精选文章
GET    /api/article/search                - 搜索文章
POST   /api/article/{id}/like             - 点赞文章
POST   /api/article/{id}/favorite         - 收藏文章
GET    /api/article/my-articles           - 我的文章
GET    /api/article/my-favorites          - 我的收藏

POST   /api/comment/add                   - 添加评论
DELETE /api/comment/{id}                  - 删除评论
GET    /api/comment/list/{articleId}      - 评论列表
POST   /api/comment/{id}/like             - 点赞评论
```

**完整API文档**: 启动后访问 http://localhost:8080/doc.html

---

## 🎨 UI设计风格

### 主题色调

- **主色**: 中国红 `#C8102E`
- **辅色**: 墨绿 `#2F5233`
- **点缀色**: 金黄 `#F0C239`
- **背景色**: 米白 `#F5F5DC`

### 设计元素

- 中国风图案装饰
- 水墨画风格背景
- 传统纹样边框
- 书法字体标题

---

## 📅 开发进度

### ✅ 已完成

- [x] 项目改造方案设计
- [x] 数据库表结构设计
- [x] 体质测试问卷数据准备
- [x] 实施计划制定

### 🔄 进行中

- [ ] 后端API开发
- [ ] 前端页面开发
- [ ] 数据准备

### 📝 待开始

- [ ] 系统测试
- [ ] 性能优化
- [ ] 部署上线

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 📞 联系方式

- **项目负责人**: 开发团队
- **技术支持**: dev@tcm-health.com
- **项目地址**: [GitHub Repository]

---

**最后更新**: 2025-11-03  
**版本**: v1.0.0

