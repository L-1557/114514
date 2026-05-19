@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo 知识库系统 - 快速测试
echo ========================================
echo.

echo [步骤 1] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python 环境
    pause
    exit /b 1
)
echo [✓] Python 已安装
echo.

echo [步骤 2] 检查依赖包...
pip show requests >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 安装 requests 库...
    pip install requests -q
)
echo [✓] 依赖包检查完成
echo.

echo [步骤 3] 运行测试脚本...
echo.
python test_knowledge.py

echo.
echo ========================================
echo 测试完成
echo ========================================
echo.

pause
