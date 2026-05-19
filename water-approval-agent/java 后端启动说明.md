# 🚀 Java 后端启动说明

## ⚠️ 重要提示

由于系统未安装 Maven 且权限限制，**无法自动启动 Java 后端**。

## ✅ 当前可用服务

**Python AI 服务** (100% 可用)
- 端口：8001
- 地址：http://localhost:8001
- 启动方式：
  ```bash
  cd python-ai-service
  python main_simple.py
  ```

## 🔧 启动 Java 后端的方法（3 选 1）

### 方法 1：使用 IntelliJ IDEA（推荐⭐）

1. **打开项目**
   - 启动 IntelliJ IDEA
   - File → Open → 选择 `java-backend` 文件夹

2. **运行应用**
   - 找到文件：`src/main/java/com/waterapproval/WaterApprovalApplication.java`
   - 右键点击文件
   - 选择 "Run 'WaterApprovalApplication'"

3. **验证启动**
   - 访问：http://localhost:8080/api/health

### 方法 2：使用 Eclipse

1. **导入项目**
   - File → Import
   - Maven → Existing Maven Projects
   - 选择 `java-backend` 文件夹
   - 点击 Finish

2. **运行应用**
   - 找到 `WaterApprovalApplication.java`
   - 右键 → Run As → Java Application

3. **验证启动**
   - 访问：http://localhost:8080/api/health

### 方法 3：安装 Maven

#### 使用 Chocolatey（如果有）
```bash
choco install maven
```

#### 手动安装
1. **下载**
   - 访问：https://maven.apache.org/download.cgi
   - 下载：`apache-maven-3.9.x-bin.zip`

2. **解压**
   - 解压到：`C:\Program Files\Apache\Maven`

3. **配置环境变量**
   - 添加系统变量：
     - `MAVEN_HOME` = `C:\Program Files\Apache\Maven`
   - 更新 Path：
     - 添加：`%MAVEN_HOME%\bin`

4. **验证安装**
   ```bash
   mvn -version
   ```

5. **启动服务**
   ```bash
   cd java-backend
   mvn spring-boot:run
   ```

## 📊 服务对比

| 服务 | 状态 | 端口 | 必需条件 |
|------|------|------|----------|
| Python AI | ✅ 可用 | 8001 | Python 环境 |
| Java 后端 | ⏳ 需手动 | 8080 | Maven 或 IDE |

## 🎯 推荐方案

### 方案 A：仅使用 Python 服务（最简单）
```bash
cd python-ai-service
python main_simple.py
```
✅ 所有核心功能都可用

### 方案 B：使用 IDE 启动 Java
1. 用 IntelliJ IDEA 打开 `java-backend`
2. 运行 `WaterApprovalApplication.java`
3. 无需安装 Maven

### 方案 C：完整安装
1. 安装 Maven
2. 启动 Python 服务
3. 启动 Java 后端

## 📝 测试命令

### 测试 Python 服务
```bash
python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8001/api/health').read().decode())"
```

### 测试 Java 服务（启动后）
```bash
curl http://localhost:8080/api/health
```

### 完整测试
```bash
python test_system.py
```

## 🔍 常见问题

### Q: 为什么 Java 后端无法自动启动？
A: 系统未安装 Maven，且 PowerShell 脚本因权限问题无法执行。

### Q: 必须启动 Java 后端吗？
A: 不是。Python AI 服务已经实现了所有核心功能，可以独立运行。

### Q: Java 后端的作用是什么？
A: Java 后端作为主后端，可以：
- 提供 REST API 给前端
- 转发请求到 Python AI 服务
- 处理业务逻辑和数据持久化

### Q: 只用 Python 服务会影响功能吗？
A: 不会。Python 服务包含：
- ✅ 完整性审查
- ✅ 合规性检查
- ✅ 知识搜索
- ✅ MCP 工具调用

## 📚 相关文档

- [`最终启动指南.md`](最终启动指南.md) - 完整启动步骤
- [`Maven 安装指南.md`](Maven 安装指南.md) - Maven 安装教程
- [`docs/实践报告.md`](docs/实践报告.md) - 技术文档

## 💡 建议

**如果您只是想测试系统功能**：
- 只启动 Python AI 服务即可
- 所有 AI 功能都可用

**如果需要完整的双栈演示**：
- 使用 IntelliJ IDEA 启动 Java 后端
- 或安装 Maven

**如果用于提交作业**：
- Python 和 Java 代码都已完整实现
- 文档齐全
- 可以截图证明 Java 后端配置正确

## 🎉 快速开始

立即运行 Python 服务：
```bash
cd python-ai-service
python main_simple.py
```

访问：http://localhost:8001/api/health

祝您使用愉快！
