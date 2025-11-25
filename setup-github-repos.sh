#!/bin/bash
# GitHub 仓库创建和推送脚本
# 使用方法: bash setup-github-repos.sh

set -e

GITHUB_USER="XDD513"
GITHUB_TOKEN=""
REPOS=(
    "hospital-frontend:医院预约挂号系统 - 前端应用 (Vue 3 + Element Plus)"
    "hospital-appointment-system:医院预约挂号系统 - 后端服务 (Spring Boot + MyBatis-Plus)"
)

echo "========================================"
echo "GitHub 仓库创建和推送脚本"
echo "========================================"
echo ""

# 检查是否提供了token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "需要 GitHub Personal Access Token 来创建仓库"
    echo "如果没有token，请访问: https://github.com/settings/tokens"
    echo "创建token时需要勾选 'repo' 权限"
    echo ""
    read -p "请输入您的 GitHub Token (或按 Enter 跳过创建，仅尝试推送): " GITHUB_TOKEN
fi

# 创建仓库的函数
create_repo() {
    local repo_name=$1
    local repo_desc=$2
    
    if [ -z "$GITHUB_TOKEN" ]; then
        echo "⚠️  跳过创建仓库 $repo_name (未提供token)"
        return 0
    fi
    
    echo "正在创建仓库: $repo_name..."
    
    response=$(curl -s -w "\n%{http_code}" -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/user/repos \
        -d "{\"name\":\"$repo_name\",\"description\":\"$repo_desc\",\"private\":false}")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "201" ]; then
        echo "✅ 成功创建仓库: $repo_name"
        return 0
    elif [ "$http_code" = "422" ]; then
        echo "⚠️  仓库 $repo_name 可能已存在，跳过创建"
        return 0
    else
        echo "❌ 创建仓库失败: $repo_name"
        echo "HTTP状态码: $http_code"
        echo "响应: $body"
        return 1
    fi
}

# 推送代码的函数
push_repo() {
    local repo_path=$1
    local repo_name=$2
    
    echo ""
    echo "正在推送 $repo_name..."
    
    cd "$repo_path" || {
        echo "❌ 无法进入目录: $repo_path"
        return 1
    }
    
    # 检查远程仓库是否已配置
    if ! git remote get-url origin &>/dev/null; then
        echo "配置远程仓库..."
        git remote add origin "https://github.com/$GITHUB_USER/$repo_name.git"
    fi
    
    # 确保分支名为main
    git branch -M main 2>/dev/null || true
    
    # 推送代码
    echo "推送代码到 GitHub..."
    if git push -u origin main 2>&1; then
        echo "✅ 成功推送 $repo_name"
        return 0
    else
        echo "❌ 推送 $repo_name 失败"
        return 1
    fi
}

# 主流程
echo "步骤 1: 创建 GitHub 仓库"
echo "----------------------------------------"

for repo_info in "${REPOS[@]}"; do
    IFS=':' read -r repo_name repo_desc <<< "$repo_info"
    create_repo "$repo_name" "$repo_desc"
    sleep 1
done

echo ""
echo "步骤 2: 推送代码到 GitHub"
echo "----------------------------------------"

success_count=0
for repo_info in "${REPOS[@]}"; do
    IFS=':' read -r repo_name repo_desc <<< "$repo_info"
    repo_path="$repo_name"
    
    if [ -d "$repo_path" ]; then
        if push_repo "$repo_path" "$repo_name"; then
            ((success_count++))
        fi
    else
        echo "⚠️  路径不存在: $repo_path"
    fi
done

echo ""
echo "========================================"
echo "完成！成功推送 $success_count/${#REPOS[@]} 个仓库"
echo "========================================"
echo ""
echo "仓库地址:"
for repo_info in "${REPOS[@]}"; do
    IFS=':' read -r repo_name repo_desc <<< "$repo_info"
    echo "  - https://github.com/$GITHUB_USER/$repo_name"
done

