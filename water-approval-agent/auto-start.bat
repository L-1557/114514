@echo off
echo ========================================
echo Complete System Auto-Startup Script
echo ========================================
echo.

echo [Step 1/3] Checking Python AI Service...
tasklist /FI "WINDOWTITLE eq Python AI Service*" 2>nul | find "python" >nul
if %errorlevel% equ 0 (
    echo [OK] Python AI Service is already running
) else (
    echo [INFO] Starting Python AI Service...
    start "Python AI Service" cmd /k "cd python-ai-service && python main_simple.py"
    timeout /t 3 >nul
)

echo.
echo [Step 2/3] Checking Java Environment...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Java not found! Please install JDK 17+
    echo Download from: https://www.oracle.com/java/technologies/downloads/
    pause
    exit /b 1
)
echo [OK] Java is installed

echo.
echo [Step 3/3] Starting Java Backend...
where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Maven found, starting Java Backend...
    start "Java Backend" cmd /k "cd java-backend && mvn spring-boot:run"
    echo.
    echo ========================================
    echo All services starting...
    echo ========================================
    echo Python AI Service: http://localhost:8001
    echo Java Backend: http://localhost:8080
    echo.
) else (
    echo [WARNING] Maven not found
    echo.
    echo Python AI Service is running: http://localhost:8001
    echo.
    echo To start Java Backend, please install Maven:
    echo   1. Download: https://maven.apache.org/download.cgi
    echo   2. Install to: C:\Program Files\Apache\Maven
    echo   3. Add to PATH: C:\Program Files\Apache\Maven\bin
    echo.
    echo Or use IDE to run WaterApprovalApplication.java
    echo.
)

timeout /t 5 >nul

REM Test Python service
python -c "import urllib.request; print('Python Service Status:', urllib.request.urlopen('http://localhost:8001/api/health').read().decode())"

echo.
echo ========================================
echo Startup Complete
echo ========================================
echo.
pause
