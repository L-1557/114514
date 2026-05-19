@echo off
echo ========================================
echo 涉水审批AI服务启动脚本
echo ========================================

echo.
echo [1/3] 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境
    pause
    exit /b 1
)

echo.
echo [2/3] 安装Python依赖...
cd python-ai-service
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 警告: 依赖安装可能有问题，继续尝试启动...
)

echo.
echo [3/3] 启动Python AI服务...
echo 服务将在 http://localhost:8000 启动
echo 按 Ctrl+C 停止服务
echo.

python main.py

pause
