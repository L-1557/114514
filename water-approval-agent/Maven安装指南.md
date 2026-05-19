# Maven 安装指南

## 方法一：使用 Chocolatey（最简单）

如果您的系统已安装 Chocolatey，只需运行：

```bash
choco install maven
```

安装完成后，重启终端并验证：
```bash
mvn -version
```

## 方法二：手动安装（推荐）

### 步骤 1：下载 Maven

访问官方下载页面：
https://maven.apache.org/download.cgi

或直接下载：
- **Apache 官方**: https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.zip
- **清华镜像**: https://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.zip

### 步骤 2：解压到本地

建议解压到以下目录之一：
- `C:\Program Files\Apache\Maven`
- `C:\maven`
- `%USERPROFILE%\maven`

### 步骤 3：配置环境变量

1. **打开环境变量设置**
   - 右键"此电脑" → "属性"
   - "高级系统设置" → "环境变量"

2. **添加系统变量**
   - 新建系统变量：
     - 变量名：`MAVEN_HOME`
     - 变量值：`C:\Program Files\Apache\Maven`（根据实际安装路径）

3. **更新 PATH 变量**
   - 在"系统变量"中找到 `Path`
   - 点击"编辑"
   - 添加：`%MAVEN_HOME%\bin`

### 步骤 4：验证安装

打开新的命令行窗口，运行：
```bash
mvn -version
```

如果看到类似输出，说明安装成功：
```
Apache Maven 3.9.6
Maven home: C:\Program Files\Apache\Maven
Java version: 17.x.x
```

## 方法三：使用脚本安装

### Windows PowerShell（管理员）

```powershell
# 下载并安装 Maven
$MAVEN_VERSION = "3.9.6"
$MAVEN_HOME = "C:\Program Files\Apache\Maven"
$DOWNLOAD_URL = "https://dlcdn.apache.org/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.zip"

# 下载
Invoke-WebRequest -Uri $DOWNLOAD_URL -OutFile "$env:TEMP\maven.zip"

# 解压
Expand-Archive -Path "$env:TEMP\maven.zip" -DestinationPath "$env:TEMP"
Move-Item -Path "$env:TEMP\apache-maven-$MAVEN_VERSION" -Destination $MAVEN_HOME -Force

# 添加到 PATH
$envPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
[Environment]::SetEnvironmentVariable("Path", "$envPath;$MAVEN_HOME\bin", "Machine")

Write-Host "Maven installed successfully!"
```

## 安装后配置

### 配置 Maven 镜像（可选，加速下载）

编辑 `%MAVEN_HOME%\conf\settings.xml`，添加：

```xml
<mirrors>
    <mirror>
        <id>aliyun</id>
        <name>Aliyun Maven</name>
        <url>https://maven.aliyun.com/repository/public</url>
        <mirrorOf>central</mirrorOf>
    </mirror>
</mirrors>
```

### 启动 Java 后端

安装完成后，运行：

```bash
cd java-backend
mvn spring-boot:run
```

或使用 IDE：
- **IntelliJ IDEA**: 打开项目，运行 `WaterApprovalApplication.java`
- **Eclipse**: Import → Maven Project，运行 `WaterApprovalApplication.java`

## 常见问题

### Q: 安装后 `mvn` 命令无效？
A: 重启终端或重新登录 Windows

### Q: 下载速度慢？
A: 使用国内镜像源

### Q: 权限不足？
A: 使用管理员身份运行 PowerShell 或安装到用户目录

## 快速验证

安装完成后，运行以下命令验证：

```bash
# 检查 Maven 版本
mvn -version

# 启动 Java 后端
cd java-backend
mvn spring-boot:run

# 测试服务
curl http://localhost:8080/api/health
```

## 当前服务状态

- ✅ Python AI 服务：http://localhost:8001
- ⏳ Java 后端：等待 Maven 安装后启动

祝您安装顺利！
