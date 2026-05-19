@echo off
chcp 65001 >nul
echo ========================================
echo Java 后端启动诊断工具
echo ========================================
echo.

REM 检查 1: Java 环境
echo [检查 1/4] Java 环境...
where java >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Java 已安装
    java -version
) else (
    echo [✗] Java 未安装或未配置到 PATH
    echo     请安装 JDK 17+ 或检查环境变量
)
echo.

REM 检查 2: Maven
echo [检查 2/4] Maven 环境...
where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Maven 已安装
    mvn -version
) else (
    echo [✗] Maven 未安装
    echo     可选安装方式:
    echo     1. choco install maven
    echo     2. 手动下载：https://maven.apache.org/download.cgi
    echo     3. 使用 IDE (IntelliJ IDEA/Eclipse)
)
echo.

REM 检查 3: Maven Wrapper
echo [检查 3/4] Maven Wrapper...
if exist "mvnw.cmd" (
    echo [✓] Maven Wrapper 存在
) else (
    echo [✗] Maven Wrapper 不存在
)

if exist ".mvn\wrapper\maven-wrapper.jar" (
    echo [✓] Maven Wrapper JAR 存在
) else (
    echo [✗] Maven Wrapper JAR 不存在
)
echo.

REM 检查 4: 项目文件
echo [检查 4/4] 项目文件完整性...
if exist "pom.xml" (
    echo [✓] pom.xml 存在
) else (
    echo [✗] pom.xml 缺失
)

if exist "src\main\java\com\waterapproval\WaterApprovalApplication.java" (
    echo [✓] 主应用文件存在
) else (
    echo [✗] 主应用文件缺失
)
echo.

echo ========================================
echo 诊断结果
echo ========================================
echo.

REM 综合判断
where java >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Java 未安装
    echo 解决方案：
    echo   1. 下载 JDK 17+: https://www.oracle.com/java/technologies/downloads/
    echo   2. 安装后配置 JAVA_HOME 环境变量
    echo   3. 将 %%JAVA_HOME%%\bin 添加到 PATH
    goto :end
)

where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo [成功] 环境配置完整，可以启动
    echo.
    echo 启动命令:
    echo   mvn spring-boot:run
    goto :end
)

if exist "mvnw.cmd" (
    echo [提示] 可以使用 Maven Wrapper 启动
    echo.
    echo 启动命令:
    echo   call mvnw.cmd spring-boot:run
    goto :end
)

echo [警告] Maven 未安装且无 Maven Wrapper
echo.
echo 推荐方案 (选择其一):
echo.
echo 方案 1: 使用 IntelliJ IDEA (最简单)
echo   1. 打开 IntelliJ IDEA
echo   2. File -> Open -> 选择此文件夹
echo   3. 右键 WaterApprovalApplication.java
echo   4. 选择 "Run"
echo.
echo 方案 2: 安装 Maven
echo   1. choco install maven
echo   2. 或手动下载安装
echo.
echo 方案 3: 仅使用 Python 服务
echo   cd ..\python-ai-service
echo   python main_simple.py
echo.

:end
pause
