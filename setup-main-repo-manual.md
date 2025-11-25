# 主仓库初始化手动步骤

如果脚本有编码问题，可以按照以下步骤手动执行：

## 1. 初始化 Git 仓库（如果还没有）

```powershell
git init
```

## 2. 添加所有文件

```powershell
git add .
```

## 3. 创建初始提交

```powershell
git commit -m "feat: Initialize project`n`n- Hospital appointment system main repository`n- Includes backend, frontend and documentation"
```

## 4. 添加远程仓库

```powershell
git remote add origin https://github.com/你的用户名/hospital.git
```

## 5. 推送到远程仓库

```powershell
git push --set-upstream origin main
```

## 完整命令序列

```powershell
# 初始化
git init

# 添加文件
git add .

# 提交
git commit -m "feat: Initialize project`n`n- Hospital appointment system main repository`n- Includes backend, frontend and documentation"

# 添加远程（替换为你的仓库URL）
git remote add origin https://github.com/你的用户名/hospital.git

# 推送
git push --set-upstream origin main
```

