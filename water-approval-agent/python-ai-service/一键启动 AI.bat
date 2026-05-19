@echo off
chcp 65001 >nul
echo ========================================
echo Python AI 服务一键启动
echo ========================================
echo.

echo [1] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Python 未安装或未配置到 PATH
    echo.
    echo 请安装 Python 3.8 或更高版本
    echo 下载地址：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [✓] Python 已安装
echo.

echo [2] 切换到 AI 服务目录...
cd /d "%~dp0"
echo [✓] 目录：%CD%
echo.

echo [3] 启动 Python AI 服务...
echo [提示] 服务运行在端口 8003
echo [提示] 按 Ctrl+C 停止服务
echo.
echo ========================================
echo 服务已启动！
echo ========================================
echo.
echo AI 服务地址：http://localhost:8003
echo 健康检查：http://localhost:8003/api/health
echo.
echo 按 Ctrl+C 可停止服务
echo ========================================
echo.

python main_simple.py

pause
