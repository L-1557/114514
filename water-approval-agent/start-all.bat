@echo off
chcp 65001 >nul
echo ========================================
echo 涉水审批系统 - 自动启动脚本
echo ========================================

echo.
echo [步骤 1/4] 检查 Java 环境...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Java 环境，请先安装 JDK 17+
    pause
    exit /b 1
) else (
    echo [成功] Java 环境已安装
)

echo.
echo [步骤 2/4] 检查 Maven...
where mvn >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 未找到 Maven，将使用 Maven Wrapper
    if not exist "java-backend\mvnw.cmd" (
        echo [信息] 正在下载 Maven Wrapper...
        cd java-backend
        curl -o mvnw.cmd https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.2.0/maven-wrapper-3.2.0.jar
        echo [提示] 请手动下载 Maven Wrapper 或使用以下方式之一：
        echo   1. 安装 Maven: https://maven.apache.org/download.cgi
        echo   2. 使用 IDE (IntelliJ IDEA / Eclipse) 运行
        cd ..
    )
) else (
    echo [成功] Maven 已安装
)

echo.
echo [步骤 3/4] 启动 Python AI 服务...
start "Python AI 服务" cmd /k "cd python-ai-service && python main_simple.py"
echo [信息] Python AI 服务正在启动 (端口 8001)...
timeout /t 3 >nul

echo.
echo [步骤 4/4] 启动 Java 后端...
where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo [信息] 使用系统 Maven 启动 Java 后端...
    start "Java 后端" cmd /k "cd java-backend && mvn spring-boot:run"
) else if exist "java-backend\mvnw.cmd" (
    echo [信息] 使用 Maven Wrapper 启动 Java 后端...
    start "Java 后端" cmd /k "cd java-backend && mvnw.cmd spring-boot:run"
) else (
    echo [错误] 无法启动 Java 后端，请先安装 Maven 或使用 IDE 运行
    echo.
    echo 替代方案:
    echo 1. 安装 Maven: https://maven.apache.org/download.cgi
    echo 2. 使用 IntelliJ IDEA 或 Eclipse 打开 java-backend 项目并运行
    echo 3. 只使用 Python AI 服务 (已启动)
    pause
    exit /b 1
)

echo.
echo ========================================
echo 服务启动中...
echo ========================================
echo Python AI 服务：http://localhost:8001
echo Java 后端：http://localhost:8080
echo.
echo 测试服务:
echo   - 访问 http://localhost:8001/api/health
echo   - 访问 http://localhost:8080/api/health
echo.
echo 按任意键打开浏览器测试...
pause >nul

start http://localhost:8001/api/health
start http://localhost:8080/api/health

echo.
echo ========================================
echo 所有服务已启动！
echo ========================================
echo.
echo 要停止服务：
echo   1. 关闭打开的命令行窗口
echo   2. 或在任务管理器中结束 java.exe 和 python.exe 进程
echo.
pause
