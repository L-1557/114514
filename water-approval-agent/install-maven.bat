@echo off
echo ========================================
echo Maven Installation Script for Windows
echo ========================================
echo.

set MAVEN_VERSION=3.9.6
set MAVEN_HOME=C:\Program Files\Apache\Maven
set MAVEN_BIN=%MAVEN_HOME%\bin

echo [Step 1/4] Downloading Maven %MAVEN_VERSION%...
curl -L -o maven.zip "https://dlcdn.apache.org/maven/maven-3/%MAVEN_VERSION%/binaries/apache-maven-%MAVEN_VERSION%-bin.zip"
if %errorlevel% neq 0 (
    echo [ERROR] Download failed, trying alternative mirror...
    curl -L -o maven.zip "https://mirrors.aliyun.com/apache/maven/maven-3/%MAVEN_VERSION%/binaries/apache-maven-%MAVEN_VERSION%-bin.zip"
)

echo.
echo [Step 2/4] Extracting Maven...
powershell -Command "Expand-Archive -Path maven.zip -DestinationPath '%MAVEN_HOME%' -Force"

echo.
echo [Step 3/4] Setting up environment variables...
setx /M PATH "%PATH%;%MAVEN_BIN%"
if %errorlevel% neq 0 (
    echo [WARNING] Failed to set system PATH. Please add manually:
    echo   %MAVEN_BIN%
) else (
    echo [SUCCESS] PATH environment variable updated
)

echo.
echo [Step 4/4] Verifying installation...
refreshenv >nul 2>&1
call mvn -version
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Maven installed successfully!
    echo ========================================
    echo Maven Home: %MAVEN_HOME%
    echo.
    echo Next steps:
    echo 1. Close and reopen your terminal
    echo 2. Run: mvn -version
    echo 3. Start Java backend: cd java-backend ^&^& mvn spring-boot:run
) else (
    echo.
    echo ========================================
    echo Installation completed but verification failed
    echo ========================================
    echo Please add Maven to PATH manually:
    echo   %MAVEN_BIN%
    echo.
    echo Then restart your terminal and run: mvn -version
)

echo.
del maven.zip
echo Temporary files cleaned up
echo.
pause
