@echo off
chcp 65001 >nul
echo ========================================
echo Java 后端编译和运行检查
echo ========================================
echo.

echo [步骤 1] 检查 Java 环境...
java -version
if %errorlevel% neq 0 (
    echo [错误] Java 未安装或未配置到 PATH
    echo 请安装 JDK 17 或更高版本
    pause
    exit /b 1
)
echo.

echo [步骤 2] 检查 Maven...
where mvn >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] Maven 未安装，将使用 IDE 编译
    echo.
    echo 请使用 IntelliJ IDEA 打开此项目并运行：
    echo   src/main/java/com/waterapproval/WaterApprovalApplication.java
    echo.
    echo 或者安装 Maven:
    echo   choco install maven
    pause
    exit /b 1
) else (
    echo [信息] Maven 已安装
)
echo.

echo [步骤 3] 清理并编译...
cd /d "%~dp0"
call mvn clean compile -DskipTests
if %errorlevel% neq 0 (
    echo.
    echo [错误] 编译失败，请检查错误信息
    pause
    exit /b 1
)
echo.

echo [步骤 4] 编译成功！
echo ========================================
echo 编译完成，可以运行项目了
echo.
echo 下一步：
echo 1. 在 IDE 中运行 WaterApprovalApplication.java
echo 2. 或者运行：mvn spring-boot:run
echo ========================================
pause
