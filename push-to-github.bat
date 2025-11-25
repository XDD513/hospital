@echo off
chcp 65001 >nul
echo ========================================
echo GitHub 仓库推送脚本
echo ========================================
echo.

echo 请确保您已经：
echo 1. 在 GitHub 上创建了以下仓库：
echo    - hospital-frontend
echo    - hospital-appointment-system
echo 2. 已配置 Git 认证（用户名和密码/token）
echo.

pause

echo.
echo 正在推送前端仓库...
cd hospital-frontend
git push -u origin main
if %errorlevel% equ 0 (
    echo ✅ 前端仓库推送成功！
) else (
    echo ❌ 前端仓库推送失败，请检查：
    echo    - 仓库是否已创建
    echo    - 网络连接是否正常
    echo    - Git 认证是否正确
)
cd ..

echo.
echo 正在推送后端仓库...
cd hospital-appointment-system
git push -u origin main
if %errorlevel% equ 0 (
    echo ✅ 后端仓库推送成功！
) else (
    echo ❌ 后端仓库推送失败，请检查：
    echo    - 仓库是否已创建
    echo    - 网络连接是否正常
    echo    - Git 认证是否正确
)
cd ..

echo.
echo ========================================
echo 完成！
echo ========================================
echo.
echo 仓库地址：
echo   - https://github.com/XDD513/hospital-frontend
echo   - https://github.com/XDD513/hospital-appointment-system
echo.
pause

