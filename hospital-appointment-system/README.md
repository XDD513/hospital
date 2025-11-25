# 医院后端项目（hospital-appointment-system）

## 项目简介
基于 Spring Boot + MyBatis-Plus 的后端服务，提供预约挂号、体质测试、健康档案、文章社区、消息通知、统计分析等业务能力，支持 JWT 安全认证与 WebSocket 通讯。

## 技术栈
- Java 17
- Spring Boot
- MyBatis-Plus
- Spring Security（JWT）
- Redis / RabbitMQ
- MySQL

## 本地运行
1. 安装 JDK 17 与 Maven 3.8+
2. 配置数据库与中间件连接（参考 `src/main/resources/application-dev.yml`）
3. 构建与运行：
   - `mvn clean package -DskipTests`
   - `java -jar target/hospital-appointment-system-*.jar`

## 配置说明
- `application.yml` 全局配置
- `application-dev.yml` 开发环境配置
- `bootstrap.yml` Nacos 等外部配置
- 重要配置类位于 `com.hospital.config` 包（如 `CorsConfig`、`SecurityConfig`、`RedisConfig`、`RabbitMQConfig` 等）

## 目录结构
- `src/main/java/com/hospital/controller` 控制器层
- `src/main/java/com/hospital/service` 业务层与实现
- `src/main/java/com/hospital/entity` 实体定义
- `src/main/java/com/hospital/mapper` Mapper 接口与 XML 映射
- `src/main/resources/mapper` MyBatis XML 文件
- `sql/` 数据初始化与迁移脚本

## 测试
- `mvn test` 运行单元与集成测试
- 测试示例位于 `src/test/java/com/hospital`（如 `UserAuthIntegrationTest`）

## 常见问题
- 若接口 401，请确认 `SecurityConfig` 与 JWT 的签名密钥配置
- 若跨域失败，请检查 `CorsConfig` 与前端请求来源

