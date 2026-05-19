@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Java Backend Startup Script
echo ========================================
echo.

REM Check if Java is installed
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Java not found. Please install JDK 17+
    pause
    exit /b 1
)

echo [OK] Java is installed
echo.

REM Check if Maven is installed
where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Maven is installed
    echo [INFO] Starting Java Backend with Maven...
    mvn spring-boot:run
) else (
    echo [WARNING] Maven not found
    echo.
    echo Please install Maven using one of these methods:
    echo.
    echo Method 1: Using Chocolatey (if installed)
    echo   choco install maven
    echo.
    echo Method 2: Manual installation
    echo   1. Download from: https://maven.apache.org/download.cgi
    echo   2. Extract to: C:\Program Files\Apache\Maven
    echo   3. Add to PATH: C:\Program Files\Apache\Maven\bin
    echo.
    echo Method 3: Use IDE
    echo   - Open this project in IntelliJ IDEA or Eclipse
    echo   - Run WaterApprovalApplication.java
    echo.
    
    REM Try to use Maven Wrapper if it exists
    if exist "mvnw.cmd" (
        echo [INFO] Using Maven Wrapper...
        call mvnw.cmd spring-boot:run
    ) else (
        echo [INFO] Maven Wrapper not found
        pause
        exit /b 1
    )
)

pause
