# 创建 GitHub 仓库并推送代码

## 方法一：使用 GitHub 网页创建（最简单）

### 1. 创建前端仓库

1. 访问 https://github.com/new
2. 仓库名称：`hospital-frontend`
3. 描述：`医院预约挂号系统 - 前端应用 (Vue 3 + Element Plus)`
4. 选择 Public 或 Private
5. **不要**勾选任何初始化选项（README、.gitignore、license）
6. 点击 "Create repository"

### 2. 创建后端仓库

1. 访问 https://github.com/new
2. 仓库名称：`hospital-appointment-system`
3. 描述：`医院预约挂号系统 - 后端服务 (Spring Boot + MyBatis-Plus)`
4. 选择 Public 或 Private
5. **不要**勾选任何初始化选项
6. 点击 "Create repository"

### 3. 推送代码

创建完仓库后，在 Git Bash 中执行：

```bash
# 推送前端
cd hospital-frontend
git push -u origin main

# 推送后端
cd ../hospital-appointment-system
git push -u origin main
```

## 方法二：使用脚本自动创建（需要 GitHub Token）

### 1. 创建 GitHub Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" -> "Generate new token (classic)"
3. 填写 Note：`创建仓库脚本`
4. 勾选权限：`repo`（完整仓库权限）
5. 点击 "Generate token"
6. **复制并保存token**（只显示一次）

### 2. 使用 PowerShell 脚本

```powershell
# 设置执行策略（如果需要）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 运行脚本（会提示输入token）
.\create-and-push-repos.ps1

# 或者直接提供token
.\create-and-push-repos.ps1 -GitHubToken "your_token_here"
```

### 3. 使用 Bash 脚本（Git Bash）

```bash
# 设置token环境变量
export GITHUB_TOKEN="your_token_here"

# 运行脚本
bash setup-github-repos.sh
```

## 方法三：使用 GitHub CLI（如果已安装）

```bash
# 安装 GitHub CLI (如果未安装)
# Windows: winget install GitHub.cli
# 或访问: https://cli.github.com/

# 登录
gh auth login

# 创建前端仓库
gh repo create hospital-frontend --public --description "医院预约挂号系统 - 前端应用 (Vue 3 + Element Plus)" --source=hospital-frontend --remote=origin --push

# 创建后端仓库
gh repo create hospital-appointment-system --public --description "医院预约挂号系统 - 后端服务 (Spring Boot + MyBatis-Plus)" --source=hospital-appointment-system --remote=origin --push
```

## 方法四：使用 curl 命令（需要 Token）

```bash
# 设置变量
GITHUB_USER="XDD513"
GITHUB_TOKEN="your_token_here"

# 创建前端仓库
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{"name":"hospital-frontend","description":"医院预约挂号系统 - 前端应用 (Vue 3 + Element Plus)","private":false}'

# 创建后端仓库
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{"name":"hospital-appointment-system","description":"医院预约挂号系统 - 后端服务 (Spring Boot + MyBatis-Plus)","private":false}'

# 然后推送代码
cd hospital-frontend
git push -u origin main

cd ../hospital-appointment-system
git push -u origin main
```

## 验证推送成功

推送成功后，访问以下地址验证：

- 前端：https://github.com/XDD513/hospital-frontend
- 后端：https://github.com/XDD513/hospital-appointment-system

## 常见问题

### 1. 认证失败

如果遇到认证问题：

```bash
# 使用 Personal Access Token
git remote set-url origin https://YOUR_TOKEN@github.com/XDD513/hospital-frontend.git

# 或配置 Git Credential Manager
git config --global credential.helper manager-core
```

### 2. 仓库已存在

如果仓库已存在，直接推送即可：

```bash
cd hospital-frontend
git push -u origin main
```

### 3. 网络连接问题

如果遇到网络问题：

1. 检查网络连接
2. 使用代理或 VPN
3. 尝试使用 SSH 方式：

```bash
# 配置 SSH
git remote set-url origin git@github.com:XDD513/hospital-frontend.git
git push -u origin main
```

## 推荐方案

**最简单的方式**：使用方法一（GitHub 网页创建），然后直接推送代码。

如果经常需要创建仓库，建议使用方法二（脚本自动化）。

