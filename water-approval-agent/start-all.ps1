# 涉水审批系统 - 完整安装与启动脚本 (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "涉水审批系统 - 完整安装与启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 步骤 1: 检查 Java
Write-Host "[步骤 1/5] 检查 Java 环境..." -ForegroundColor Yellow
try {
    $javaVersion = java -version 2>&1
    Write-Host "[成功] Java 已安装" -ForegroundColor Green
    $javaVersion | Select-Object -First 1
} catch {
    Write-Host "[错误] 未找到 Java 环境" -ForegroundColor Red
    Write-Host "请先安装 JDK 17+" -ForegroundColor Yellow
    Write-Host "下载地址：https://www.oracle.com/java/technologies/downloads/" -ForegroundColor Cyan
    pause
    exit 1
}
Write-Host ""

# 步骤 2: 检查 Maven
Write-Host "[步骤 2/5] 检查 Maven..." -ForegroundColor Yellow
$mvnCmd = Get-Command mvn -ErrorAction SilentlyContinue
if ($mvnCmd) {
    Write-Host "[成功] Maven 已安装" -ForegroundColor Green
    mvn -version | Select-Object -First 3
    $MAVEN_CMD = "mvn"
} else {
    Write-Host "[信息] Maven 未安装，开始自动安装..." -ForegroundColor Cyan
    
    # 步骤 3: 下载 Maven
    Write-Host "[步骤 3/5] 下载 Maven 3.9.6..." -ForegroundColor Yellow
    $MAVEN_HOME = "$env:USERPROFILE\apache-maven"
    $MAVEN_BIN = "$MAVEN_HOME\bin"
    $MAVEN_ZIP = "$env:TEMP\maven.zip"
    
    if (Test-Path "$MAVEN_BIN\mvn.cmd") {
        Write-Host "[信息] Maven 已存在于用户目录" -ForegroundColor Green
        $MAVEN_CMD = "$MAVEN_BIN\mvn.cmd"
    } else {
        try {
            $downloadUrl = "https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.zip"
            Write-Host "下载链接：$downloadUrl" -ForegroundColor Gray
            Invoke-WebRequest -Uri $downloadUrl -OutFile $MAVEN_ZIP -UseBasicParsing
            Write-Host "[成功] Maven 下载完成" -ForegroundColor Green
        } catch {
            Write-Host "[错误] 下载失败：$_" -ForegroundColor Red
            Write-Host "请手动下载安装 Maven" -ForegroundColor Yellow
            pause
            exit 1
        }
        
        # 步骤 4: 解压
        Write-Host "[步骤 4/5] 解压 Maven..." -ForegroundColor Yellow
        try {
            if (Test-Path $MAVEN_HOME) {
                Remove-Item -Recurse -Force $MAVEN_HOME
            }
            Expand-Archive -Path $MAVEN_ZIP -DestinationPath $env:USERPROFILE -Force
            Rename-Item -Path "$env:USERPROFILE\apache-maven-3.9.6" -NewName "apache-maven" -Force
            Write-Host "[成功] Maven 解压完成" -ForegroundColor Green
            $MAVEN_CMD = "$MAVEN_BIN\mvn.cmd"
        } catch {
            Write-Host "[错误] 解压失败：$_" -ForegroundColor Red
            pause
            exit 1
        }
        
        # 步骤 5: 配置环境变量
        Write-Host "[步骤 5/5] 配置环境变量..." -ForegroundColor Yellow
        try {
            $envPath = [Environment]::GetEnvironmentVariable("Path", "User")
            if ($envPath -notlike "*$MAVEN_BIN*") {
                [Environment]::SetEnvironmentVariable("Path", "$envPath;$MAVEN_BIN", "User")
                $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
            }
            Write-Host "[成功] 环境变量已配置" -ForegroundColor Green
        } catch {
            Write-Host "[警告] 环境变量配置失败，请手动添加：$MAVEN_BIN" -ForegroundColor Yellow
        }
    }
}
Write-Host ""

# 启动服务
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "启动服务" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 启动 Python AI 服务
Write-Host "[服务 1/2] 启动 Python AI 服务..." -ForegroundColor Yellow
$pythonProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*Python AI*" }
if ($pythonProcess) {
    Write-Host "[信息] Python AI 服务已在运行" -ForegroundColor Green
} else {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\python-ai-service'; Write-Host 'Python AI Service Starting...'; python main_simple.py" -WindowStyle Normal
    Write-Host "[成功] Python AI 服务已启动" -ForegroundColor Green
}
Write-Host "访问地址：http://localhost:8001" -ForegroundColor Cyan
Write-Host ""

Start-Sleep -Seconds 3

# 启动 Java 后端
Write-Host "[服务 2/2] 启动 Java 后端..." -ForegroundColor Yellow
try {
    if ($MAVEN_CMD -eq "mvn") {
        Write-Host "[信息] 使用系统 Maven 启动..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\java-backend'; Write-Host 'Java Backend Starting...'; mvn clean spring-boot:run" -WindowStyle Normal
    } else {
        Write-Host "[信息] 使用本地 Maven 启动..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\java-backend'; Write-Host 'Java Backend Starting...'; & '$MAVEN_CMD' clean spring-boot:run" -WindowStyle Normal
    }
    Write-Host "[成功] Java 后端已启动" -ForegroundColor Green
    Write-Host "访问地址：http://localhost:8080" -ForegroundColor Cyan
} catch {
    Write-Host "[警告] Maven 启动失败" -ForegroundColor Yellow
    Write-Host "请使用 IDE 启动 Java 后端：" -ForegroundColor Cyan
    Write-Host "  1. 打开 IntelliJ IDEA" -ForegroundColor Gray
    Write-Host "  2. File -> Open -> 选择 java-backend 文件夹" -ForegroundColor Gray
    Write-Host "  3. 右键 WaterApprovalApplication.java" -ForegroundColor Gray
    Write-Host "  4. 选择 'Run'" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "服务启动完成" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "服务状态:" -ForegroundColor White
Write-Host "  ✓ Python AI 服务：http://localhost:8001" -ForegroundColor Green
Write-Host "  ✓ Java 后端：http://localhost:8080" -ForegroundColor Green
Write-Host ""
Write-Host "测试命令:" -ForegroundColor White
Write-Host "  curl http://localhost:8001/api/health" -ForegroundColor Gray
Write-Host "  curl http://localhost:8080/api/health" -ForegroundColor Gray
Write-Host ""

Start-Sleep -Seconds 5

# 打开浏览器测试
try {
    Start-Process "http://localhost:8001/api/health"
    Start-Sleep -Seconds 2
    Start-Process "http://localhost:8080/api/health"
} catch {
    # 忽略浏览器打开失败
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "所有服务已启动！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "停止服务：关闭对应的 PowerShell 窗口即可" -ForegroundColor Yellow
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
pause | Out-Null
