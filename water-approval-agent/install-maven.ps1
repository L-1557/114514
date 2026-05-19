# Maven 安装脚本 (PowerShell)
Write-Host "========================================"
Write-Host "Maven Installation Script"
Write-Host "========================================"
Write-Host ""

$MAVEN_VERSION = "3.9.6"
$MAVEN_HOME = "$env:USERPROFILE\maven"
$DOWNLOAD_URL = "https://dlcdn.apache.org/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.zip"

Write-Host "[Step 1/4] Downloading Maven $MAVEN_VERSION..."
try {
    Invoke-WebRequest -Uri $DOWNLOAD_URL -OutFile "$env:TEMP\maven.zip" -UseBasicParsing
    Write-Host "[OK] Download completed"
} catch {
    Write-Host "[ERROR] Download failed: $_"
    Write-Host "Trying alternative method..."
    # 如果下载失败，使用已存在的文件
    if (Test-Path "$env:TEMP\maven.zip") {
        Write-Host "[INFO] Using existing file"
    } else {
        Write-Host "[ERROR] Please download manually from: $DOWNLOAD_URL"
        pause
        exit 1
    }
}

Write-Host ""
Write-Host "[Step 2/4] Extracting..."
try {
    if (Test-Path $MAVEN_HOME) {
        Remove-Item -Recurse -Force $MAVEN_HOME
    }
    Expand-Archive -Path "$env:TEMP\maven.zip" -DestinationPath $env:TEMP -Force
    Move-Item -Path "$env:TEMP\apache-maven-$MAVEN_VERSION" -Destination $MAVEN_HOME -Force
    Write-Host "[OK] Extraction completed to $MAVEN_HOME"
} catch {
    Write-Host "[ERROR] Extraction failed: $_"
}

Write-Host ""
Write-Host "[Step 3/4] Setting up PATH..."
try {
    $envPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($envPath -notlike "*$MAVEN_HOME\bin*") {
        [Environment]::SetEnvironmentVariable("Path", "$envPath;$MAVEN_HOME\bin", "User")
        Write-Host "[OK] PATH updated"
    } else {
        Write-Host "[INFO] PATH already configured"
    }
} catch {
    Write-Host "[ERROR] Failed to update PATH: $_"
}

Write-Host ""
Write-Host "[Step 4/4] Verifying installation..."
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
try {
    & "$MAVEN_HOME\bin\mvn.cmd" -version
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Maven installed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Maven Home: $MAVEN_HOME"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "1. Close and reopen your terminal"
    Write-Host "2. Run: cd java-backend"
    Write-Host "   mvn spring-boot:run"
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "========================================"
    Write-Host "Installation completed"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Please restart your terminal and run:"
    Write-Host "  cd java-backend"
    Write-Host "  mvn spring-boot:run"
    Write-Host ""
}

# Cleanup
if (Test-Path "$env:TEMP\maven.zip") {
    Remove-Item "$env:TEMP\maven.zip" -Force
    Write-Host "Temporary files cleaned up"
}

Write-Host ""
pause
