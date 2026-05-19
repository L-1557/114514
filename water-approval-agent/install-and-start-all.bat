@echo off
chcp 65001 >nul
echo ========================================
echo 涉水审批系统 - 完整安装与启动
echo ========================================
echo.

echo [步骤 1/5] 检查 Java 环境...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Java 环境
    echo.
    echo 请先安装 JDK 17+：
    echo   下载地址：https://www.oracle.com/java/technologies/downloads/
    pause
    exit /b 1
)
echo [成功] Java 已安装
java -version
echo.

echo [步骤 2/5] 检查 Maven...
where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo [成功] Maven 已安装
    mvn -version
    goto :START_SERVICES
)

echo [信息] Maven 未安装，开始自动安装...
echo.

echo [步骤 3/5] 下载 Maven 3.9.6...
set MAVEN_HOME=%USERPROFILE%\apache-maven
set MAVEN_BIN=%MAVEN_HOME%\bin

if exist "%MAVEN_BIN%\mvn.cmd" (
    echo [信息] Maven 已存在于用户目录
    goto :START_SERVICES
)

echo 正在下载 Maven...
powershell -Command "Invoke-WebRequest -Uri 'https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.zip' -OutFile '%TEMP%\maven.zip' -UseBasicParsing"
if %errorlevel% neq 0 (
    echo [错误] 下载失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo [步骤 4/5] 解压 Maven...
powershell -Command "if (Test-Path '%MAVEN_HOME%') { Remove-Item -Recurse -Force '%MAVEN_HOME%' }; Expand-Archive -Path '%TEMP%\maven.zip' -DestinationPath '%USERPROFILE%' -Force; Rename-Item -Path '%USERPROFILE%\apache-maven-3.9.6' -NewName 'apache-maven' -Force"

echo.
echo [步骤 5/5] 配置环境变量...
setx PATH "%PATH%;%MAVEN_BIN%"
echo [成功] Maven 已安装到：%MAVEN_HOME%
echo.

:START_SERVICES
echo ========================================
echo 启动服务
echo ========================================
echo.

echo [服务 1/2] 启动 Python AI 服务...
tasklist /FI "WINDOWTITLE eq Python AI*" 2>nul | find "python" >nul
if %errorlevel% equ 0 (
    echo [信息] Python AI 服务已在运行
) else (
    start "Python AI 服务" cmd /k "cd python-ai-service && echo Python AI Service Starting... && python main_simple.py"
    echo [成功] Python AI 服务已启动
)
echo 访问地址：http://localhost:8001
echo.

timeout /t 3 >nul

echo [服务 2/2] 启动 Java 后端...
where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo [信息] 使用系统 Maven 启动...
    start "Java 后端" cmd /k "cd java-backend && echo Java Backend Starting... && mvn clean spring-boot:run"
    echo [成功] Java 后端已启动
    echo 访问地址：http://localhost:8080
) else if exist "%MAVEN_BIN%\mvn.cmd" (
    echo [信息] 使用用户目录 Maven 启动...
    start "Java 后端" cmd /k "cd java-backend && echo Java Backend Starting... && call %MAVEN_BIN%\mvn.cmd clean spring-boot:run"
    echo [成功] Java 后端已启动
    echo 访问地址：http://localhost:8080
) else (
    echo [警告] Maven 不可用，使用 IDE 启动 Java 后端
    echo.
    echo 请手动启动 Java 后端：
    echo   1. 打开 IntelliJ IDEA
    echo   2. File -> Open -> 选择 java-backend 文件夹
    echo   3. 右键 WaterApprovalApplication.java
    echo   4. 选择 "Run"
    echo.
)

echo.
echo ========================================
echo 服务启动完成
echo ========================================
echo.
echo 服务状态:
echo   ✓ Python AI 服务：http://localhost:8001
echo   ✓ Java 后端：http://localhost:8080
echo.
echo 测试命令:
echo   curl http://localhost:8001/api/health
echo   curl http://localhost:8080/api/health
echo.
echo 按任意键打开浏览器测试...
pause >nul

start http://localhost:8001/api/health
timeout /t 2 >nul
start http://localhost:8080/api/health

echo.
echo ========================================
echo 所有服务已启动！
echo ========================================
echo.
echo 停止服务：关闭对应的命令行窗口即可
echo.
pause
