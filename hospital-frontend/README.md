# 医院前端项目（hospital-frontend）

## 项目简介
基于 Vue 3 + Vite 的单页应用，提供患者、医生、管理员三个端的交互界面，包括预约挂号、体质测试、健康打卡、文章社区、消息通知、后台管理等模块。

## 技术栈
- Vue 3
- Vite
- Vue Router
- Pinia
- SCSS
- Vitest

## 本地开发
1. 安装 Node.js（建议 18+）
2. 在项目根目录执行：
   - `npm install`
   - `npm run dev`
3. 浏览器打开 `http://localhost:5173/`

## 生产构建
- `npm run build` 生成产物到 `dist/`
- `npm run preview` 本地预览构建结果

## 目录结构
- `src/api` 后端接口封装
- `src/views` 页面视图
- `src/components` 组件库
- `src/stores` 状态管理
- `src/router` 路由配置
- `src/styles` 样式文件
- `public/uploads` 静态资源示例

## 环境变量
在 `src/config/runtimeConfig.js` 中按需调整运行时配置（如后端 API 地址）。

## 测试
- `npm run test` 运行单元测试（Vitest）

## 常见问题
- 若接口请求失败，请检查后端服务是否启动以及跨域配置（后端已提供 `CorsConfig`）。

