# 主仓库初始化脚本
# 用于创建主仓库并推送所有代码到 GitHub

# 设置控制台编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

$step1 = "[1/5] 初始化 Git 仓库..."
$step2 = "[2/5] 配置远程仓库..."
$step3 = "[3/5] 添加文件..."
$step4 = "[4/5] 创建提交..."
$step5 = "[5/5] 推送到远程仓库..."

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "主仓库初始化脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 初始化 Git 仓库
Write-Host $step1 -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "Git 仓库初始化完成" -ForegroundColor Green
} else {
    Write-Host "Git 仓库已存在" -ForegroundColor Gray
}
Write-Host ""

# 2. 配置远程仓库
Write-Host $step2 -ForegroundColor Yellow
$remote = git remote -v 2>$null
if ($remote) {
    Write-Host "当前远程仓库:" -ForegroundColor Gray
    Write-Host $remote -ForegroundColor Gray
    $useExisting = Read-Host "使用现有配置? (y/n)"
    if ($useExisting -ne "y" -and $useExisting -ne "Y") {
        Write-Host "请手动配置后重新运行" -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "未配置远程仓库" -ForegroundColor Gray
    Write-Host ""
    Write-Host "请输入 GitHub 仓库 URL" -ForegroundColor Yellow
    Write-Host "示例: https://github.com/username/hospital.git" -ForegroundColor Gray
    $repoUrl = Read-Host "仓库 URL"
    if ($repoUrl) {
        git remote add origin $repoUrl
        Write-Host "远程仓库配置完成" -ForegroundColor Green
    } else {
        Write-Host "跳过远程仓库配置" -ForegroundColor Yellow
        Write-Host "稍后可使用命令配置: git remote add origin [URL]" -ForegroundColor Gray
    }
}
Write-Host ""

# 3. 添加文件
Write-Host $step3 -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    git add .
    Write-Host "文件已添加到暂存区" -ForegroundColor Green
} else {
    Write-Host "没有需要提交的文件" -ForegroundColor Gray
}
Write-Host ""

# 4. 创建提交
Write-Host $step4 -ForegroundColor Yellow
$commitCount = git rev-list --count HEAD 2>$null
if ($commitCount -eq 0 -or $null -eq $commitCount) {
    $line1 = 'feat: 初始化项目'
    $line2 = ''
    $line3 = '- 医院预约挂号系统主仓库'
    $line4 = '- 包含后端、前端和文档'
    $msg = "$line1`n$line2`n$line3`n$line4"
    git commit -m $msg
    if ($LASTEXITCODE -eq 0) {
        Write-Host "初始提交创建成功" -ForegroundColor Green
    } else {
        Write-Host "提交失败" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "已有 $commitCount 个提交" -ForegroundColor Gray
}
Write-Host ""

# 5. 推送到远程
Write-Host $step5 -ForegroundColor Yellow
$remote = git remote -v 2>$null
if ($remote) {
    $branch = git branch --show-current
    if ([string]::IsNullOrWhiteSpace($branch)) {
        $branch = "main"
        git branch -M main
    }
    Write-Host "当前分支: $branch" -ForegroundColor Gray
    Write-Host ""
    Write-Host "正在推送..." -ForegroundColor Yellow
    git push --set-upstream origin $branch
    if ($LASTEXITCODE -eq 0) {
        Write-Host "代码推送成功" -ForegroundColor Green
    } else {
        Write-Host "推送失败，请检查远程仓库配置" -ForegroundColor Red
        Write-Host ""
        Write-Host "可能的原因:" -ForegroundColor Yellow
        Write-Host "1. 远程仓库不存在或 URL 错误" -ForegroundColor Gray
        Write-Host "2. 没有推送权限" -ForegroundColor Gray
        Write-Host "3. 需要配置认证信息" -ForegroundColor Gray
        Write-Host ""
        Write-Host "可手动运行:" -ForegroundColor Yellow
        Write-Host "  git push --set-upstream origin $branch" -ForegroundColor Gray
    }
} else {
    Write-Host "未配置远程仓库，跳过推送" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "稍后可配置并推送:" -ForegroundColor Yellow
    Write-Host "  git remote add origin [仓库URL]" -ForegroundColor Gray
    Write-Host "  git push --set-upstream origin main" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "设置完成！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

