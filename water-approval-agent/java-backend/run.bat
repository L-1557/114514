@echo off
echo ========================================
echo Java Backend Startup
echo ========================================
echo.

echo Checking Java...
java -version
if %errorlevel% neq 0 (
    echo Java not found!
    pause
    exit /b 1
)

echo.
echo Starting Java Backend...
echo.

REM Try Maven first
where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo Maven found! Starting...
    mvn clean spring-boot:run
    goto :end
)

REM Try Maven Wrapper
if exist "mvnw.cmd" (
    echo Using Maven Wrapper...
    call mvnw.cmd clean spring-boot:run
    goto :end
)

echo Maven not found!
echo.
echo Please install Maven or use IDE:
echo   1. choco install maven
echo   2. Download from https://maven.apache.org/download.cgi
echo   3. Use IntelliJ IDEA or Eclipse
echo.
pause

:end
