@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo 涉水审批系统 - Java 后端启动脚本
echo ========================================
echo.

echo [步骤 1] 检查 Java 环境...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Java 环境
    echo.
    echo 请安装 JDK 17 或更高版本
    echo 下载地址：https://adoptium.net/
    echo.
    pause
    exit /b 1
)
echo [✓] Java 已安装
for /f "tokens=3" %%i in ('java -version 2^>^&1 ^| findstr /i "version"') do echo [信息] %%i
echo.

echo [步骤 2] 检查 Maven...
where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Maven 已安装
    set MAVEN_CMD=mvn
) else (
    echo [提示] Maven 未安装，使用内置的 Maven Wrapper
    echo.
    
    if exist ".mvn\wrapper\maven-wrapper.jar" (
        echo [✓] 找到 Maven Wrapper
        set MAVEN_CMD=mvnw.cmd
    ) else (
        echo [警告] Maven Wrapper 不存在
        echo.
        echo 请选择以下任一方法：
        echo   1. 安装 Maven: https://maven.apache.org/download.cgi
        echo   2. 使用 IntelliJ IDEA 直接运行
        echo   3. 使用 VS Code 运行
        echo.
        pause
        exit /b 1
    )
)
echo.

echo [步骤 3] 切换到项目目录...
cd /d "%~dp0"
echo [✓] 当前目录：%CD%
echo.

echo [步骤 4] 清理并编译项目...
echo [提示] 首次运行需要下载依赖，请耐心等待...
echo.

%MAVEN_CMD% clean compile -q
if %errorlevel% neq 0 (
    echo.
    echo [错误] 编译失败
    echo.
    echo 可能的原因：
    echo   1. 网络连接问题，无法下载依赖
    echo   2. Maven 配置问题
    echo   3. 项目文件损坏
    echo.
    echo 建议：使用 IntelliJ IDEA 直接运行项目
    echo.
    pause
    exit /b 1
)
echo [✓] 编译成功
echo.

echo [步骤 5] 启动 Java 后端...
echo [提示] 服务运行在端口 8080
echo [提示] 按 Ctrl+C 停止服务
echo.
echo ========================================
echo 服务已启动！
echo ========================================
echo.
echo 前端地址：http://localhost:8080
echo API 地址：http://localhost:8080/api
echo 健康检查：http://localhost:8080/api/health
echo.
echo 按 Ctrl+C 可停止服务
echo ========================================
echo.

%MAVEN_CMD% spring-boot:run

pause
