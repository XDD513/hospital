# Main Repository Setup Script
# Create main repository and push all code to GitHub

# Set console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Main Repository Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Initialize Git repository
Write-Host "[1/5] Initialize Git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "Git repository already exists" -ForegroundColor Gray
}
Write-Host ""

# Step 2: Configure remote repository
Write-Host "[2/5] Configure remote repository..." -ForegroundColor Yellow
$remote = git remote -v 2>$null
if ($remote) {
    Write-Host "Current remote:" -ForegroundColor Gray
    Write-Host $remote -ForegroundColor Gray
    $useExisting = Read-Host "Use existing remote? (y/n)"
    if ($useExisting -ne "y" -and $useExisting -ne "Y") {
        Write-Host "Please configure remote manually and run again" -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "No remote repository configured" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Please enter your GitHub repository URL" -ForegroundColor Yellow
    Write-Host "Example: https://github.com/username/hospital.git" -ForegroundColor Gray
    $repoUrl = Read-Host "Repository URL"
    if ($repoUrl) {
        git remote add origin $repoUrl
        Write-Host "Remote repository configured" -ForegroundColor Green
    } else {
        Write-Host "Skipping remote configuration" -ForegroundColor Yellow
        Write-Host "You can configure it later with: git remote add origin [URL]" -ForegroundColor Gray
    }
}
Write-Host ""

# Step 3: Add files
Write-Host "[3/5] Add files..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    git add .
    Write-Host "Files added to staging area" -ForegroundColor Green
} else {
    Write-Host "No files to commit" -ForegroundColor Gray
}
Write-Host ""

# Step 4: Create commit
Write-Host "[4/5] Create commit..." -ForegroundColor Yellow
$commitCount = git rev-list --count HEAD 2>$null
if ($commitCount -eq 0 -or $null -eq $commitCount) {
    $msg = "feat: Initialize project`n`n- Hospital appointment system main repository`n- Includes backend, frontend and documentation"
    git commit -m $msg
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Initial commit created successfully" -ForegroundColor Green
    } else {
        Write-Host "Commit failed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Already have $commitCount commit(s)" -ForegroundColor Gray
}
Write-Host ""

# Step 5: Push to remote
Write-Host "[5/5] Push to remote repository..." -ForegroundColor Yellow
$remote = git remote -v 2>$null
if ($remote) {
    $branch = git branch --show-current
    if ([string]::IsNullOrWhiteSpace($branch)) {
        $branch = "main"
        git branch -M main
    }
    Write-Host "Current branch: $branch" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Pushing to remote..." -ForegroundColor Yellow
    git push --set-upstream origin $branch
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Code pushed successfully" -ForegroundColor Green
    } else {
        Write-Host "Push failed. Please check remote repository configuration" -ForegroundColor Red
        Write-Host ""
        Write-Host "Possible reasons:" -ForegroundColor Yellow
        Write-Host "1. Remote repository does not exist or URL is incorrect" -ForegroundColor Gray
        Write-Host "2. No push permission" -ForegroundColor Gray
        Write-Host "3. Authentication required" -ForegroundColor Gray
        Write-Host ""
        Write-Host "You can manually run:" -ForegroundColor Yellow
        Write-Host "  git push --set-upstream origin $branch" -ForegroundColor Gray
    }
} else {
    Write-Host "No remote repository configured, skipping push" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To configure and push later, run:" -ForegroundColor Yellow
    Write-Host "  git remote add origin [repository URL]" -ForegroundColor Gray
    Write-Host "  git push --set-upstream origin main" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup completed!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

