@echo off
chcp 65001 >nul
echo ========================================
echo AI 审查失败诊断工具
echo ========================================
echo.

echo [1] 检查 Python AI 服务状态
echo ----------------------------------------
netstat -ano | findstr :8003
if %errorlevel% neq 0 (
    echo [❌] Python AI 服务未启动
    echo.
    echo 请运行：python-ai-service\一键启动 AI.bat
) else (
    echo [✓] Python AI 服务正在运行
)
echo.

echo [2] 测试 AI 服务健康检查
echo ----------------------------------------
curl -s http://localhost:8003/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo [❌] AI 服务健康检查失败
    echo.
    echo 可能原因：
    echo   1. Python AI 服务未响应
    echo   2. 防火墙阻止
    echo   3. 端口配置错误
) else (
    echo [✓] AI 服务健康检查通过
)
echo.

echo [3] 检查 Java 后端配置
echo ----------------------------------------
echo 检查文件：java-backend\src\main\java\com\waterapproval\config\AppConfig.java
echo.
findstr /n "baseUrl" java-backend\src\main\java\com\waterapproval\config\AppConfig.java
echo.
echo [提示] 应该配置为：http://localhost:8003
echo.

echo [4] 测试 AI 服务接口
echo ----------------------------------------
echo 发送测试请求...
echo.

curl -X POST http://localhost:8003/api/review ^
  -H "Content-Type: application/json" ^
  -d "{\"projectName\":\"测试\",\"applicantName\":\"测试\",\"waterSource\":\"黄河\",\"waterPurpose\":\"工业用水\",\"applicationPeriod\":\"2024-01-01\",\"waterVolume\":1000,\"projectDescription\":\"测试\",\"documents\":[]}" ^
  -s

echo.
echo.

echo [5] 检查 Java 后端状态
echo ----------------------------------------
curl -s http://localhost:8080/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo [❌] Java 后端未启动或未响应
    echo.
    echo 请在 IntelliJ IDEA 中启动 Java 后端
) else (
    echo [✓] Java 后端正在运行
)
echo.

echo ========================================
echo 诊断完成！
echo ========================================
echo.
echo 如果以上检查有任何 [❌] 标记，请按照提示修复
echo.
echo 常见问题解决方案：
echo   1. Python AI 服务未启动 → 运行 python-ai-service\一键启动 AI.bat
echo   2. 端口配置错误 → 修改 AppConfig.java 中的 baseUrl
echo   3. Java 后端未启动 → 在 IntelliJ IDEA 中启动
echo.
pause
