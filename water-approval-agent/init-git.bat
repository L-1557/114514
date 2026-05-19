@echo off
echo ========================================
echo Git仓库初始化脚本
echo ========================================

echo.
echo [1/3] 初始化Git仓库...
git init
if %errorlevel% neq 0 (
    echo 错误: Git初始化失败
    pause
    exit /b 1
)

echo.
echo [2/3] 添加所有文件...
git add .

echo.
echo [3/3] 创建初始提交...
git commit -m "Initial commit: 涉水审批材料合规性审查Agent系统"

echo.
echo Git仓库初始化完成!
echo 可以使用 git status 查看状态
echo 使用 git log 查看提交历史

pause
