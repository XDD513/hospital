# 第一阶段功能完善实施计划

## 一、数据可视化增强

### 1.1 患者健康趋势图表

**后端实现**：

- 在 `HealthProfileService` 接口中添加方法：`getHealthTrendData(Long userId, LocalDate startDate, LocalDate endDate)`
- 在 `HealthProfileServiceImpl` 中实现：从 `health_checkin` 表查询指定日期范围的打卡数据，按日期分组统计体重、睡眠、运动、心情
- 在 `HealthProfileController` 中添加接口：`GET /api/health/statistics/trend?startDate=xxx&endDate=xxx&period=7/30/90`
- 返回数据格式：`List<HealthTrendData>`，包含日期、体重、睡眠时长、运动时长、心情评分

**前端实现**：

- 修改 `hospital-frontend/src/views/patient/health/HealthStatistics.vue`
- 添加时间周期选择器（7天/30天/90天）
- 使用 ECharts 绘制折线图展示体重、睡眠、运动趋势
- 使用柱状图展示心情分布
- 调用新接口 `getHealthTrendData` 获取数据

**文件位置**：

- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/HealthProfileService.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/impl/HealthProfileServiceImpl.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/controller/HealthProfileController.java`
- 前端：`hospital-frontend/src/views/patient/health/HealthStatistics.vue`
- 前端：`hospital-frontend/src/api/health.js`

### 1.2 体质测试历史对比雷达图

**后端实现**：

- 在 `ConstitutionTestService` 接口中添加方法：`getTestComparison(Long userId, List<Long> testIds)`
- 在 `ConstitutionTestServiceImpl` 中实现：查询多个测试记录的得分，返回对比数据
- 在 `ConstitutionController` 中添加接口：`GET /api/constitution/test/comparison?testIds=1,2,3`
- 返回数据格式：包含各测试记录的9种体质得分

**前端实现**：

- 修改 `hospital-frontend/src/views/patient/constitution/TestHistory.vue`
- 添加测试记录多选功能
- 使用 ECharts 雷达图展示多个测试结果的对比
- 调用新接口 `getTestComparison` 获取数据

**文件位置**：

- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/ConstitutionTestService.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/impl/ConstitutionTestServiceImpl.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/controller/ConstitutionController.java`
- 前端：`hospital-frontend/src/views/patient/constitution/TestHistory.vue`
- 前端：`hospital-frontend/src/api/constitution.js`

### 1.3 管理员数据大屏

**后端实现**：

- 在 `StatisticsService` 接口中添加方法：`getRealtimeStats()` 返回实时预约数据
- 在 `StatisticsServiceImpl` 中实现：查询今日预约数、待处理数、完成数、取消数
- 在 `StatisticsController` 中添加接口：`GET /api/statistics/admin/realtime`
- 添加方法：`getDoctorWorkloadStats(Map<String, Object> params)` 返回医生工作量统计
- 添加接口：`GET /api/statistics/doctor/workload?startDate=xxx&endDate=xxx`
- 添加方法：`getDepartmentHeatmapData(Map<String, Object> params)` 返回科室预约热力图数据
- 添加接口：`GET /api/statistics/department/heatmap?startDate=xxx&endDate=xxx`

**前端实现**：

- 修改 `hospital-frontend/src/views/admin/Dashboard.vue`
- 添加实时预约数据看板：使用 ECharts 仪表盘、饼图展示今日预约状态分布
- 修改 `hospital-frontend/src/views/admin/Statistics.vue`
- 添加医生工作量统计图表：柱状图展示医生接诊量、预约量、评价统计
- 添加科室预约热力图：使用 ECharts 热力图展示各科室在不同时段的预约热度

**文件位置**：

- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/StatisticsService.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/impl/StatisticsServiceImpl.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/controller/StatisticsController.java`
- 前端：`hospital-frontend/src/views/admin/Dashboard.vue`
- 前端：`hospital-frontend/src/views/admin/Statistics.vue`
- 前端：`hospital-frontend/src/api/statistics.js`

## 二、消息通知系统完善

### 2.1 站内消息中心

**后端实现**：

- 在 `NotificationService` 接口中添加方法：`queryNotificationsByType(Long userId, Page<UserNotification> page, String type, Integer readStatus)`
- 在 `NotificationServiceImpl` 中实现：支持按类型筛选消息
- 在 `NotificationController` 中修改接口：`GET /api/patient/notifications?type=xxx&readStatus=xxx` 支持类型筛选
- 添加接口：`PUT /api/patient/notifications/read-all` 批量标记已读
- 在 `NotificationService` 中添加方法：`markAllAsRead(Long userId)`

**前端实现**：

- 新建 `hospital-frontend/src/views/patient/NotificationCenter.vue`
- 实现消息分类标签（系统通知、预约提醒、评价反馈等）
- 实现消息筛选功能（全部/未读/已读）
- 实现消息列表展示（分页）
- 实现单个消息标记已读
- 实现批量标记已读功能（全选、批量操作）
- 在路由中添加：`/patient/notifications` 路由

**文件位置**：

- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/NotificationService.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/impl/NotificationServiceImpl.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/controller/NotificationController.java`
- 前端：`hospital-frontend/src/views/patient/NotificationCenter.vue` (新建)
- 前端：`hospital-frontend/src/api/notification.js`
- 前端：`hospital-frontend/src/router/index.js`

### 2.2 消息推送优化

**后端实现**：

- 在 `AppointmentServiceImpl` 中，预约状态变更时调用 `NotificationService.createAndSendNotification` 发送通知
- 在 `ConversationServiceImpl` 中，医生回复消息时调用 `NotificationService.createAndSendNotification` 发送通知
- 通知类型定义：
- `APPOINTMENT_SUCCESS`: 预约成功
- `APPOINTMENT_CANCELLED`: 预约取消
- `APPOINTMENT_REMINDER`: 预约提醒
- `DOCTOR_REPLY`: 医生回复

**文件位置**：

- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/impl/AppointmentServiceImpl.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/impl/ConversationServiceImpl.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/impl/NotificationServiceImpl.java`

## 三、搜索功能增强

### 3.1 全局搜索

**后端实现**：

- 新建 `SearchController.java`：`/api/search`
- 新建 `SearchService.java` 接口和 `SearchServiceImpl.java` 实现
- 实现全局搜索方法：`searchAll(String keyword, String type, Integer pageNum, Integer pageSize)`
- 支持搜索类型：`all`（全部）、`doctor`（医生）、`recipe`（药膳）、`article`（文章）、`acupoint`（穴位）
- 返回统一格式的搜索结果：`SearchResultDTO`，包含类型、标题、描述、链接等
- 添加热门搜索词接口：`GET /api/search/hot-keywords`，从 Redis 统计搜索次数

**前端实现**：

- 新建 `hospital-frontend/src/components/SearchBox.vue` 全局搜索组件
- 实现搜索框、搜索历史（LocalStorage）、热门搜索词展示
- 新建 `hospital-frontend/src/views/SearchResults.vue` 搜索结果页
- 实现搜索结果分类展示（医生、药膳、文章、穴位）
- 在路由中添加：`/search?keyword=xxx` 路由
- 在 `hospital-frontend/src/api/search.js` 中添加搜索相关 API

**文件位置**：

- 后端：`hospital-appointment-system/src/main/java/com/hospital/controller/SearchController.java` (新建)
- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/SearchService.java` (新建)
- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/impl/SearchServiceImpl.java` (新建)
- 前端：`hospital-frontend/src/components/SearchBox.vue` (新建)
- 前端：`hospital-frontend/src/views/SearchResults.vue` (新建)
- 前端：`hospital-frontend/src/api/search.js` (新建)
- 前端：`hospital-frontend/src/router/index.js`

### 3.2 高级筛选

**后端实现**：

- 修改 `HerbalRecipeController` 的搜索接口：`GET /api/recipe/search`
- 添加筛选参数：`constitution`（体质）、`season`（季节）、`effect`（功效）
- 在 `HerbalRecipeService` 中实现多条件筛选逻辑
- 修改 `HealthArticleController` 的搜索接口：`GET /api/article/search`
- 添加筛选参数：`category`（分类）、`tag`（标签）

**前端实现**：

- 修改 `hospital-frontend/src/views/patient/recipe/RecipeList.vue`
- 添加筛选器组件：体质选择、季节选择、功效选择
- 修改 `hospital-frontend/src/views/patient/community/ArticleList.vue`
- 添加筛选器组件：分类选择、标签选择

**文件位置**：

- 后端：`hospital-appointment-system/src/main/java/com/hospital/controller/HerbalRecipeController.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/service/HerbalRecipeService.java`
- 后端：`hospital-appointment-system/src/main/java/com/hospital/controller/HealthArticleController.java`
- 前端：`hospital-frontend/src/views/patient/recipe/RecipeList.vue`
- 前端：`hospital-frontend/src/views/patient/community/ArticleList.vue`

## 四、项目文档完善

### 4.1 需求分析文档

- 新建 `docs/需求分析文档.md`
- 包含：项目背景、功能需求、非功能需求、用户故事、用例描述

### 4.2 系统设计文档

- 新建 `docs/系统架构设计.md`
- 包含：整体架构图、技术选型说明、模块划分、数据库设计
- 新建 `docs/数据库设计.md`
- 包含：数据库 ER 图、表结构说明、索引设计

### 4.3 部署文档

- 新建 `docs/环境搭建指南.md`
- 包含：开发环境搭建、依赖安装、配置说明
- 新建 `docs/部署文档.md`
- 包含：生产环境部署步骤、数据库初始化、Nginx 配置

**文件位置**：

- `docs/需求分析文档.md` (新建)
- `docs/系统架构设计.md` (新建)
- `docs/数据库设计.md` (新建)
- `docs/环境搭建指南.md` (新建)
- `docs/部署文档.md` (新建)

## 实施顺序

1. 数据可视化增强（预计 5-6 天）

- 先完成后端接口
- 再完成前端图表

2. 消息通知系统完善（预计 3-4 天）

- 先完成后端接口
- 再完成前端页面

3. 搜索功能增强（预计 4-5 天）

- 先完成全局搜索
- 再完成高级筛选

4. 项目文档完善（预计 4-5 天）

- 并行编写各类文档

## 验收标准

- 数据可视化：图表能正确展示数据，支持时间周期切换
- 消息通知：消息中心功能完整，能分类筛选、批量操作
- 搜索功能：全局搜索能搜索所有类型内容，高级筛选能多条件组合
- 项目文档：文档内容完整，结构清晰，包含必要的图表