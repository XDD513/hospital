# GitHub 仓库创建和推送脚本
# 使用方法: .\create-and-push-repos.ps1 -GitHubToken "your_token_here"

param(
    [Parameter(Mandatory=$false)]
    [string]$GitHubToken = "",
    
    [Parameter(Mandatory=$false)]
    [string]$GitHubUsername = "XDD513"
)

$ErrorActionPreference = "Stop"

# 如果没有提供token，尝试从环境变量获取
if ([string]::IsNullOrEmpty($GitHubToken)) {
    $GitHubToken = $env:GITHUB_TOKEN
}

# 如果还是没有token，提示用户输入
if ([string]::IsNullOrEmpty($GitHubToken)) {
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "GitHub 仓库创建和推送脚本" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "需要 GitHub Personal Access Token 来创建仓库" -ForegroundColor Cyan
    Write-Host "如果没有token，请访问: https://github.com/settings/tokens" -ForegroundColor Cyan
    Write-Host "创建token时需要勾选 'repo' 权限" -ForegroundColor Cyan
    Write-Host ""
    $GitHubToken = Read-Host "请输入您的 GitHub Token (或按 Enter 跳过创建，仅尝试推送)"
}

# 仓库配置
$repos = @(
    @{
        Name = "hospital-frontend"
        Path = "hospital-frontend"
        Description = "医院预约挂号系统 - 前端应用 (Vue 3 + Element Plus)"
    },
    @{
        Name = "hospital-appointment-system"
        Path = "hospital-appointment-system"
        Description = "医院预约挂号系统 - 后端服务 (Spring Boot + MyBatis-Plus)"
    }
)

# 创建仓库的函数
function Create-GitHubRepository {
    param(
        [string]$Name,
        [string]$Description,
        [string]$Token,
        [string]$Username
    )
    
    $headers = @{
        "Authorization" = "token $Token"
        "Accept" = "application/vnd.github.v3+json"
    }
    
    $body = @{
        name = $Name
        description = $Description
        private = $false
        auto_init = $false
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
        Write-Host "✅ 成功创建仓库: $Name" -ForegroundColor Green
        return $true
    }
    catch {
        if ($_.Exception.Response.StatusCode -eq 422) {
            Write-Host "⚠️  仓库 $Name 可能已存在，跳过创建" -ForegroundColor Yellow
            return $true
        }
        else {
            Write-Host "❌ 创建仓库失败: $Name" -ForegroundColor Red
            Write-Host "错误信息: $($_.Exception.Message)" -ForegroundColor Red
            return $false
        }
    }
}

# 推送代码的函数
function Push-Repository {
    param(
        [string]$RepoPath,
        [string]$RepoName
    )
    
    Write-Host ""
    Write-Host "正在推送 $RepoName..." -ForegroundColor Cyan
    
    Push-Location $RepoPath
    
    try {
        # 检查远程仓库是否已配置
        $remote = git remote get-url origin 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "配置远程仓库..." -ForegroundColor Yellow
            git remote add origin "https://github.com/XDD513/$RepoName.git"
        }
        
        # 确保分支名为main
        git branch -M main 2>$null
        
        # 推送代码
        Write-Host "推送代码到 GitHub..." -ForegroundColor Yellow
        git push -u origin main 2>&1 | ForEach-Object {
            if ($_ -match "error|fatal") {
                Write-Host $_ -ForegroundColor Red
            }
            else {
                Write-Host $_
            }
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ 成功推送 $RepoName" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ 推送 $RepoName 失败" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ 推送过程中出错: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    finally {
        Pop-Location
    }
}

# 主流程
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "开始创建和推送仓库" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 如果有token，先创建仓库
if (-not [string]::IsNullOrEmpty($GitHubToken)) {
    Write-Host "步骤 1: 创建 GitHub 仓库" -ForegroundColor Cyan
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    
    foreach ($repo in $repos) {
        Create-GitHubRepository -Name $repo.Name -Description $repo.Description -Token $GitHubToken -Username $GitHubUsername
        Start-Sleep -Seconds 1
    }
    
    Write-Host ""
}

# 推送代码
Write-Host "步骤 2: 推送代码到 GitHub" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

$successCount = 0
foreach ($repo in $repos) {
    if (Test-Path $repo.Path) {
        if (Push-Repository -RepoPath $repo.Path -RepoName $repo.Name) {
            $successCount++
        }
    }
    else {
        Write-Host "⚠️  路径不存在: $($repo.Path)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "完成！成功推送 $successCount/$($repos.Count) 个仓库" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "仓库地址:" -ForegroundColor Cyan
foreach ($repo in $repos) {
    Write-Host "  - https://github.com/XDD513/$($repo.Name)" -ForegroundColor White
}

