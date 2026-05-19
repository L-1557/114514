@echo off
echo ========================================
echo Java Backend Quick Start
echo ========================================
echo.

echo Checking for IntelliJ IDEA...
if exist "C:\Program Files\JetBrains\IntelliJ IDEA*\bin\idea.exe" (
    echo [INFO] IntelliJ IDEA found
    echo [ACTION] Please open this folder in IntelliJ IDEA:
    echo   %CD%
    echo.
    echo Then run WaterApprovalApplication.java
) else (
    echo [INFO] IntelliJ IDEA not found
    echo.
    echo Please install Maven or use IDE:
    echo   1. Download IntelliJ IDEA: https://www.jetbrains.com/idea/
    echo   2. Open this folder in IDE
    echo   3. Run WaterApprovalApplication.java
    echo.
    echo Or install Maven:
    echo   choco install maven
)
echo.
echo Current directory:
echo   %CD%
echo.
echo Main class:
echo   src\main\java\com\waterapproval\WaterApprovalApplication.java
echo.
pause
