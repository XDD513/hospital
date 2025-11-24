# 医院预约挂号系统 - 后端服务

## 📖 项目简介

基于 Spring Boot 的医院预约挂号系统后端服务，提供完整的预约挂号、医患对话、健康管理等功能。系统集成了中医体质辨识、在线咨询、消息推送等特色功能。

## ✨ 核心功能

### 1. 用户管理模块
- 用户注册、登录、权限控制
- JWT Token 认证授权
- 用户信息管理
- 多角色支持（患者、医生、管理员）

### 2. 预约挂号模块
- 在线预约挂号
- 医生排班管理
- 号源管理
- 预约状态跟踪
- 支付管理

### 3. 医患对话模块
- 实时对话（WebSocket）
- 消息推送（RabbitMQ）
- 会话管理
- 文件上传支持

### 4. 健康管理模块
- 中医体质辨识
- 体质测试问卷
- 健康档案管理
- 健康打卡

### 5. 养生知识模块
- 养生文章管理
- 药膳推荐
- 穴位指导
- 用户收藏、点赞

### 6. 评价反馈模块
- 医生评价
- 评价回复
- 评分统计

### 7. 系统管理模块
- 科室管理
- 医生管理
- 操作日志
- 数据字典
- 系统配置

## 🏗️ 技术架构

### 核心技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Java | 17 | 编程语言 |
| Spring Boot | 2.7.18 | 核心框架 |
| MyBatis-Plus | 3.5.5 | ORM框架 |
| MySQL | 8.0+ | 关系型数据库 |
| Redis | 6.0+ | 缓存中间件 |
| RabbitMQ | - | 消息队列 |
| Spring Security | 2.7.x | 安全框架 |
| JWT | 0.11.5 | Token认证 |

### 主要依赖

```xml
<!-- 核心框架 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>

<!-- 数据访问 -->
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-boot-starter</artifactId>
    <version>3.5.5</version>
</dependency>
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>

<!-- 缓存与消息 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>

<!-- WebSocket -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>

<!-- 工具类 -->
<dependency>
    <groupId>cn.hutool</groupId>
    <artifactId>hutool-all</artifactId>
    <version>5.8.23</version>
</dependency>
```

## 📁 项目结构

```
hospital-appointment-system/
├── src/main/java/com/hospital/
│   ├── HospitalApplication.java           # 启动类
│   ├── annotation/                        # 自定义注解
│   │   └── OperationLog.java             # 操作日志注解
│   ├── aspect/                           # AOP切面
│   │   └── OperationLogAspect.java       # 日志切面
│   ├── common/                           # 公共模块
│   │   ├── constant/                     # 常量类
│   │   │   ├── SystemConstants.java      # 系统常量
│   │   │   ├── CacheConstants.java       # 缓存常量
│   │   │   ├── DefaultConstants.java     # 默认值常量
│   │   │   └── AppointmentStatus.java    # 预约状态枚举
│   │   ├── exception/                    # 异常处理
│   │   │   ├── BusinessException.java    # 业务异常
│   │   │   └── GlobalExceptionHandler.java # 全局异常处理器
│   │   └── result/                       # 统一返回结果
│   │       ├── Result.java               # 返回结果封装
│   │       └── ResultCode.java           # 状态码枚举
│   ├── config/                           # 配置类
│   │   ├── SecurityConfig.java           # 安全配置
│   │   ├── RedisConfig.java              # Redis配置
│   │   ├── RabbitMQConfig.java           # RabbitMQ配置
│   │   ├── WebSocketConfig.java          # WebSocket配置
│   │   ├── MybatisPlusConfig.java        # MyBatis-Plus配置
│   │   ├── CorsConfig.java               # 跨域配置
│   │   └── OssConfig.java                # OSS对象存储配置
│   ├── controller/                       # 控制层（21个Controller）
│   │   ├── UserController.java           # 用户管理
│   │   ├── AppointmentController.java    # 预约管理
│   │   ├── DoctorController.java         # 医生管理
│   │   ├── ConversationController.java   # 对话管理
│   │   ├── ConstitutionController.java   # 体质辨识
│   │   └── ...
│   ├── service/                          # 业务层
│   │   ├── impl/                         # 服务实现（42个Service）
│   │   └── *.java                        # 服务接口
│   ├── mapper/                           # 数据访问层（33个Mapper）
│   ├── entity/                           # 实体类（31个Entity）
│   ├── dto/                              # 数据传输对象
│   │   ├── request/                      # 请求DTO
│   │   └── response/                     # 响应DTO
│   ├── messaging/                        # 消息处理
│   │   ├── ConversationMessagePublisher.java   # 消息发布
│   │   ├── ConversationMessageListener.java    # 消息监听
│   │   └── dto/                          # 消息DTO
│   ├── util/                             # 工具类
│   │   ├── JwtUtil.java                  # JWT工具
│   │   └── RedisUtil.java                # Redis工具
│   └── interceptor/                      # 拦截器
│       └── JwtInterceptor.java           # JWT拦截器
├── src/main/resources/
│   ├── application.yml                   # 主配置文件
│   ├── application-dev.yml               # 开发环境配置
│   ├── application-prod.yml              # 生产环境配置
│   └── mapper/                           # MyBatis XML映射文件
│       ├── ConsultationRecordMapper.xml
│       ├── DepartmentMapper.xml
│       ├── PatientMapper.xml
│       ├── ReviewMapper.xml
│       └── StatisticsMapper.xml
├── sql/                                  # 数据库脚本
│   ├── tcm_health_system.sql            # 主数据库脚本
│   ├── conversation.sql                  # 对话表脚本
│   ├── migrations/                       # 数据库迁移脚本
│   └── test-data/                        # 测试数据
├── pom.xml                               # Maven配置
└── README.md                             # 项目说明
```

## 🚀 快速开始

### 环境要求

- JDK 17+
- Maven 3.6+
- MySQL 8.0+
- Redis 6.0+
- RabbitMQ 3.8+（可选，用于消息推送）

### 1. 克隆项目

```bash
git clone <repository-url>
cd hospital-appointment-system
```

### 2. 数据库初始化

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE hospital_appointment_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入数据
mysql -u root -p hospital_appointment_system < sql/tcm_health_system.sql
mysql -u root -p hospital_appointment_system < sql/conversation.sql

# 执行迁移脚本（如有）
mysql -u root -p hospital_appointment_system < sql/migrations/*.sql
```

### 3. 配置中心（Nacos）

项目已改为由 Nacos 统一管理所有敏感配置， `.env` 仅用于兼容性示例。请按以下流程操作：

1. 启动 Nacos 并创建命名空间（推荐 `dev`/`staging`/`prod`），详见 `docs/NACOS_SETUP.md`。
2. 依据示例导入配置：
   - `docs/nacos/hospital-appointment-system-dev.yaml`
   - `docs/nacos/hospital-frontend-dev.yaml`
3. 启动应用时通过环境变量或 JVM 参数提供 Nacos 地址：

```bash
export NACOS_SERVER_ADDR=127.0.0.1:8848
export NACOS_NAMESPACE=dev
```

4. 其余数据库、Redis、RabbitMQ、OSS、JWT、前端运行时配置均由 Nacos dataId 下发，应用会自动读取并支持热刷新。

如需手动调试，可在 `application-*.yml` 中保留的默认值或 `.env.example` 中填写，但正式环境建议以 Nacos 为唯一配置源。

### 4. 编译运行

```bash
# 编译打包
mvn clean package -DskipTests

# 运行项目
java -jar target/hospital-appointment-system-1.0.0.jar

# 或者使用Maven运行
mvn spring-boot:run
```

### 5. 访问接口文档

启动后访问 Swagger 文档：
- http://localhost:8080/doc.html

## 📊 数据库设计

### 核心数据表

#### 用户相关
- `user` - 用户表
- `doctor` - 医生表
- `patient` - 患者扩展表

#### 预约相关
- `appointment` - 预约表
- `schedule` - 排班表
- `department` - 科室表
- `payment` - 支付表

#### 对话相关
- `conversation` - 会话表
- `conversation_message` - 消息表
- `user_notification` - 通知表

#### 健康管理
- `constitution_type` - 体质类型表（9种体质）
- `constitution_questionnaire` - 体质问卷表
- `user_constitution_test` - 用户测试记录
- `user_health_profile` - 健康档案
- `health_checkin` - 健康打卡

#### 养生知识
- `health_article` - 养生文章
- `herbal_recipe` - 药膳食谱
- `acupoint` - 穴位信息
- `article_comment` - 文章评论

#### 评价反馈
- `review` - 评价表
- `consultation_record` - 咨询记录

#### 系统管理
- `system_config` - 系统配置
- `operation_log` - 操作日志
- `dictionary` - 数据字典

## 🔧 核心特性

### 1. 统一响应格式

```java
Result<T> result = Result.success(data);
Result<T> error = Result.error(ResultCode.SYSTEM_ERROR);
```

### 2. 全局异常处理

所有异常统一由 `GlobalExceptionHandler` 处理，返回统一格式的错误响应。

### 3. 操作日志记录

使用 `@OperationLog` 注解自动记录操作日志：

```java
@OperationLog(module = "USER", type = "INSERT", description = "创建用户")
public boolean addUser(User user) {
    // ...
}
```

### 4. 缓存策略

- Redis 缓存热点数据
- 缓存键统一管理（`CacheConstants`）
- 支持缓存过期时间配置

### 5. 消息队列

- RabbitMQ 处理异步消息
- WebSocket 实时推送
- 支持消息持久化

### 6. 常量管理

所有常量统一在 `com.hospital.common.constant` 包下：
- `SystemConstants` - 系统级常量
- `CacheConstants` - 缓存相关常量
- `DefaultConstants` - 默认值常量

## 🔐 安全认证

### JWT Token 认证流程

1. 用户登录获取 Token
2. Token 存储在 Redis（可配置过期时间）
3. 请求时通过 `Authorization` 请求头传递 Token
4. `JwtInterceptor` 拦截并验证 Token
5. 验证通过后设置用户上下文

### 权限控制

- 基于 Spring Security
- 支持角色权限控制（ROLE_PATIENT, ROLE_DOCTOR, ROLE_ADMIN）
- URL 级别的权限配置

## 📝 API 规范

### 请求格式

- Content-Type: `application/json`
- 认证：`Authorization: Bearer <token>`

### 响应格式

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {},
  "timestamp": "2025-12-19T10:00:00"
}
```

### 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## 🧪 测试

```bash
# 运行单元测试
mvn test

# 运行集成测试
mvn verify
```

## 📦 部署

### Docker 部署

```dockerfile
FROM openjdk:17-jre-slim
COPY target/hospital-appointment-system-1.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

### 生产环境配置

修改 `application-prod.yml` 配置生产环境参数，包括：
- 数据库连接池配置
- Redis 集群配置
- 日志级别
- JVM 参数优化

## 📚 开发规范

### 代码规范
- 遵循阿里巴巴 Java 开发规范
- 使用 Lombok 简化代码
- 统一异常处理
- 统一返回结果格式

### 命名规范
- Controller: `*Controller`
- Service: `*Service` / `*ServiceImpl`
- Mapper: `*Mapper`
- Entity: 实体名
- DTO: `*Request` / `*Response`

### Git 提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License

## 👥 作者

医院预约挂号系统开发团队

## 📧 联系方式

- 项目地址: [GitHub Repository]
- 问题反馈: [GitHub Issues]
