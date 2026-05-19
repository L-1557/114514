@echo off
echo ========================================
echo Maven Installation (User Directory)
echo ========================================
echo.

set MAVEN_VERSION=3.9.6
set MAVEN_HOME=%USERPROFILE%\maven
set MAVEN_BIN=%MAVEN_HOME%\bin

echo [Step 1/4] Downloading Maven %MAVEN_VERSION%...
curl -L -o maven.zip "https://dlcdn.apache.org/maven/maven-3/%MAVEN_VERSION%/binaries/apache-maven-%MAVEN_VERSION%-bin.zip"
if %errorlevel% neq 0 (
    echo [ERROR] Download failed
    pause
    exit /b 1
)

echo.
echo [Step 2/4] Extracting Maven to user directory...
powershell -Command "Expand-Archive -Path maven.zip -DestinationPath '%USERPROFILE%' -Force"
powershell -Command "Rename-Item -Path '%USERPROFILE%\apache-maven-%MAVEN_VERSION%' -NewName 'maven' -Force"

echo.
echo [Step 3/4] Setting up user environment variables...
reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "%%PATH%%;%MAVEN_BIN%" /f >nul 2>&1

echo.
echo [Step 4/4] Verifying installation...
call %MAVEN_BIN%\mvn.cmd -version
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Maven installed successfully!
    echo ========================================
    echo Maven Home: %MAVEN_HOME%
    echo.
    echo Next steps:
    echo 1. Close and reopen your terminal
    echo 2. Run: cd java-backend ^&^& mvn spring-boot:run
) else (
    echo.
    echo ========================================
    echo Installation completed
    echo ========================================
    echo Please restart your terminal and run:
    echo   cd java-backend
    echo   mvn spring-boot:run
)

echo.
del maven.zip
echo Temporary files cleaned up
echo.
pause
