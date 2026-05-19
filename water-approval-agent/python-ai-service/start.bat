@echo off
chcp 65001 >nul
echo ========================================
echo Python AI 服务启动脚本
echo ========================================
echo.

echo [步骤 1] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Python 未安装或未配置到 PATH
    echo 请安装 Python 3.8 或更高版本
    pause
    exit /b 1
)
echo [✓] Python 已安装
echo.

echo [步骤 2] 切换到脚本目录...
cd /d "%~dp0"
echo [✓] 目录：%CD%
echo.

echo [步骤 3] 启动 Python AI 服务...
echo.
echo ========================================
python main_simple.py
echo ========================================

echo.
echo [信息] 服务已停止
echo.
pause
