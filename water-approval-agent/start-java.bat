@echo off
echo ========================================
echo 涉水审批Java后端启动脚本
echo ========================================

echo.
echo [1/2] 检查Java环境...
java -version
if %errorlevel% neq 0 (
    echo 错误: 未找到Java环境
    pause
    exit /b 1
)

echo.
echo [2/2] 启动Java后端服务...
cd java-backend
echo 服务将在 http://localhost:8080 启动
echo 按 Ctrl+C 停止服务
echo.

call mvn spring-boot:run

pause
