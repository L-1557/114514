@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo Python AI 服务 - 知识库版本
echo ========================================
echo.

echo [步骤 1] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python 环境
    echo.
    echo 请安装 Python 3.8 或更高版本
    echo 下载地址：https://www.python.org/
    echo.
    pause
    exit /b 1
)
echo [✓] Python 已安装
for /f "tokens=3" %%i in ('python --version 2^>^&1 ^| findstr /i "version"') do echo [信息] %%i
echo.

echo [步骤 2] 检查依赖包...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 检测到缺少依赖包，正在安装...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo [错误] 依赖包安装失败
        echo.
        pause
        exit /b 1
    )
    echo [✓] 依赖包安装完成
) else (
    echo [✓] 依赖包已安装
)
echo.

echo [步骤 3] 检查端口占用...
netstat -ano | findstr :8003 >nul 2>&1
if %errorlevel% equ 0 (
    echo [警告] 端口 8003 已被占用
    echo.
    echo 请选择：
    echo   1. 杀死占用端口的进程并继续
    echo   2. 退出
    echo.
    set /p choice="请输入选项 (1/2): "
    
    if "!choice!"=="1" (
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8003') do (
            echo [信息] 杀死进程 %%a
            taskkill /F /PID %%a >nul 2>&1
        )
        echo [✓] 端口已释放
    ) else (
        exit /b 0
    )
)
echo.

echo [步骤 4] 启动 Python AI 服务...
echo [提示] 服务运行在端口 8003
echo [提示] 按 Ctrl+C 停止服务
echo.
echo ========================================
echo 服务已启动！
echo ========================================
echo.
echo 服务地址：http://localhost:8003
echo 健康检查：http://localhost:8003/api/health
echo 知识库管理：http://localhost:8003/knowledge_manager.html
echo.
echo 可用接口:
echo   GET  /api/health              - 健康检查
echo   GET  /api/knowledge/stats     - 知识库统计
echo   POST /api/knowledge/search    - 知识检索
echo   POST /api/knowledge/upload    - 文档上传
echo   POST /api/knowledge/delete    - 删除文档
echo.
echo MCP 服务:
echo   python mcp_service.py
echo.
echo 按 Ctrl+C 可停止服务
echo ========================================
echo.

python main_knowledge.py

pause
