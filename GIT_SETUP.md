# Git 仓库设置说明

## 📋 已完成的工作

1. ✅ 更新了前端 README 文件 (`hospital-frontend/README.md`)
2. ✅ 更新了后端 README 文件 (`hospital-appointment-system/README.md`)
3. ✅ 更新了外层 README 文件 (`README.md`)
4. ✅ 为前端项目初始化了独立的 Git 仓库
5. ✅ 为后端项目初始化了独立的 Git 仓库
6. ✅ 提交了所有代码到本地仓库

## 🚀 下一步操作：创建 GitHub 仓库并推送代码

由于网络连接问题，需要您手动创建 GitHub 仓库并推送代码。请按照以下步骤操作：

### 方法一：使用 GitHub 网页创建仓库（推荐）

#### 1. 创建前端仓库

1. 访问 https://github.com/new
2. 仓库名称填写：`hospital-frontend`
3. 选择 **Private** 或 **Public**（根据您的需求）
4. **不要**勾选 "Initialize this repository with a README"
5. 点击 "Create repository"

#### 2. 创建后端仓库

1. 访问 https://github.com/new
2. 仓库名称填写：`hospital-appointment-system`
3. 选择 **Private** 或 **Public**（根据您的需求）
4. **不要**勾选 "Initialize this repository with a README"
5. 点击 "Create repository"

### 方法二：使用 Git Bash 推送代码

#### 推送前端代码

```bash
cd hospital-frontend
git remote add origin https://github.com/XDD513/hospital-frontend.git
git branch -M main
git push -u origin main
```

#### 推送后端代码

```bash
cd hospital-appointment-system
git remote add origin https://github.com/XDD513/hospital-appointment-system.git
git branch -M main
git push -u origin main
```

### 方法三：使用 SSH 方式（如果已配置 SSH 密钥）

#### 推送前端代码

```bash
cd hospital-frontend
git remote set-url origin git@github.com:XDD513/hospital-frontend.git
git push -u origin main
```

#### 推送后端代码

```bash
cd hospital-appointment-system
git remote set-url origin git@github.com:XDD513/hospital-appointment-system.git
git push -u origin main
```

## 📦 仓库结构说明

```
hospital/                              # 外层仓库（主仓库）
├── .git/                              # 外层 Git 仓库
├── hospital-frontend/                  # 前端子项目
│   ├── .git/                          # 前端独立 Git 仓库
│   ├── README.md                      # 前端项目说明
│   └── ...
├── hospital-appointment-system/        # 后端子项目
│   ├── .git/                          # 后端独立 Git 仓库
│   ├── README.md                      # 后端项目说明
│   └── ...
└── README.md                           # 外层项目说明
```

## 🔗 仓库地址

- **外层仓库**: https://github.com/XDD513/hospital
- **前端仓库**: https://github.com/XDD513/hospital-frontend
- **后端仓库**: https://github.com/XDD513/hospital-appointment-system

## ⚠️ 注意事项

1. **如果仓库已存在**：如果 GitHub 上已经存在同名仓库，您需要先删除或重命名现有仓库，或者使用不同的仓库名称。

2. **认证问题**：如果推送时遇到认证问题，请：
   - 使用 Personal Access Token（推荐）
   - 或配置 SSH 密钥
   - 或使用 GitHub Desktop 等工具

3. **网络问题**：如果遇到网络连接问题，可以：
   - 检查网络连接
   - 使用代理或 VPN
   - 稍后重试

## 🎯 验证推送成功

推送成功后，您可以访问以下地址验证：

- 前端：https://github.com/XDD513/hospital-frontend
- 后端：https://github.com/XDD513/hospital-appointment-system

## 📝 后续操作

推送成功后，您可以：

1. 在 GitHub 上查看代码
2. 设置仓库描述和标签
3. 配置 GitHub Actions 进行 CI/CD
4. 邀请协作者
5. 创建 Issues 和 Pull Requests

## 🆘 遇到问题？

如果遇到任何问题，请检查：

1. GitHub 账户是否已登录
2. 仓库名称是否正确
3. 网络连接是否正常
4. Git 配置是否正确（用户名和邮箱）

```bash
# 检查 Git 配置
git config --global user.name
git config --global user.email

# 如果未配置，请设置
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

