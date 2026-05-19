@echo off
echo ========================================
echo Water Approval System - Auto Start
echo ========================================

echo.
echo [Step 1/3] Check Java Environment...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Java not found, please install JDK 17+
    pause
    exit /b 1
) else (
    echo [OK] Java is installed
)

echo.
echo [Step 2/3] Start Python AI Service...
start "Python AI Service" cmd /k "cd python-ai-service && python main_simple.py"
echo [INFO] Python AI Service starting on port 8001...
timeout /t 3 >nul

echo.
echo [Step 3/3] Start Java Backend...
where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Starting Java Backend with Maven...
    start "Java Backend" cmd /k "cd java-backend && mvn spring-boot:run"
) else (
    echo [WARNING] Maven not found, Java Backend will not start automatically
    echo [INFO] You can start Java Backend manually using:
    echo   1. Install Maven and run: mvn spring-boot:run
    echo   2. Or use IDE (IntelliJ IDEA / Eclipse)
)

echo.
echo ========================================
echo Services Starting...
echo ========================================
echo Python AI Service: http://localhost:8001
if %errorlevel% equ 0 (
    echo Java Backend: http://localhost:8080
)
echo.
echo Testing services...
timeout /t 5 >nul

python -c "import urllib.request; print('Python Service:', urllib.request.urlopen('http://localhost:8001/api/health').read().decode())"

echo.
echo ========================================
echo All services started!
echo ========================================
echo.
echo To stop services:
echo   1. Close the command windows
echo   2. Or end java.exe and python.exe in Task Manager
echo.
pause
