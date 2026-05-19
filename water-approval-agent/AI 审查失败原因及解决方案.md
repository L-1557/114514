# 🔍 AI 审查失败原因及解决方案

## 📋 快速诊断（3 步）

### 步骤 1：运行诊断工具

**双击运行**：
```
诊断 AI 审查.bat
```

自动检查：
- ✅ Python AI 服务是否启动
- ✅ AI 服务是否可访问
- ✅ Java 后端配置是否正确
- ✅ Java 后端是否运行

---

### 步骤 2：查看错误信息

**重启 Java 后端**，查看控制台输出：

启动后，当 AI 审查失败时，控制台会显示：
```
AI 审查失败：[具体错误信息]
```

**常见错误**：
- `Connection refused` - Python AI 服务未启动
- `Connection timeout` - 服务响应超时
- `404 Not Found` - 接口路径错误

---

### 步骤 3：根据错误码排查

| 错误码 | 错误信息 | 原因 | 解决方案 |
|--------|---------|------|---------|
| 500 | AI 审查失败：Connection refused | Python AI 服务未启动 | 启动 Python AI 服务 |
| 500 | AI 审查失败：Connection timeout | 服务响应超时 | 检查网络/防火墙 |
| 500 | AI 审查失败：404 Not Found | 接口路径错误 | 检查配置 |
| 500 | AI 审查失败：500 Internal Server Error | Python 服务内部错误 | 查看 Python 日志 |

---

## 🔍 详细排查步骤

### 排查 1：检查 Python AI 服务

#### 方法 1：查看进程
```bash
netstat -ano | findstr :8003
```

**成功**：看到 `LISTENING` 状态  
**失败**：无输出

#### 方法 2：访问健康检查
```bash
# 浏览器访问
http://localhost:8003/api/health
```

**成功**：
```json
{
  "status": "healthy",
  "service": "water-approval-ai"
}
```

**失败**：无法访问或报错

#### 方法 3：启动服务
```bash
cd python-ai-service
python main_simple.py
```

---

### 排查 2：检查 Java 后端配置

#### 查看配置文件
📄 [AppConfig.java](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\java-backend\src\main\java\com\waterapproval\config\AppConfig.java#L28)

**检查第 28 行**：
```java
.baseUrl("http://localhost:8003")  // ✅ 应该是 8003
```

**错误配置**：
```java
.baseUrl("http://localhost:8001")  // ❌ 错误端口
```

#### 修改配置
如果端口不正确：
1. 修改 `AppConfig.java` 第 28 行
2. 重启 Java 后端

---

### 排查 3：检查网络连接

#### 测试端口连通性
```bash
telnet localhost 8003
```

**成功**：连接建立  
**失败**：连接失败

#### 检查防火墙
```bash
# Windows 防火墙
netsh advfirewall show allprofiles
```

如果防火墙开启，需要添加例外规则。

---

### 排查 4：查看日志

#### Python AI 服务日志
启动后查看命令行输出：
```
127.0.0.1 - - [01/Jan/2024 12:00:00] "POST /api/review HTTP/1.1" 200 -
```

**正常**：看到请求日志  
**异常**：看到错误堆栈

#### Java 后端日志
查看 IntelliJ IDEA 控制台：
```
AI 审查失败：Connection refused
```

---

## 🎯 常见失败场景

### 场景 1：Python AI 服务未启动

**症状**：
- 前端显示 "AI 审查失败"
- Java 控制台显示 "Connection refused"

**诊断**：
```bash
netstat -ano | findstr :8003
# 无输出
```

**解决**：
```bash
# 启动 Python AI 服务
cd python-ai-service
python main_simple.py
```

---

### 场景 2：端口配置错误

**症状**：
- Python AI 服务运行在 8003
- Java 后端连接 8001

**诊断**：
```bash
# 查看 Python AI 服务端口
python-ai-service\main_simple.py 第 12 行
PORT = 8003

# 查看 Java 后端配置
java-backend\config\AppConfig.java 第 28 行
.baseUrl("http://localhost:8001")  # ❌ 不一致
```

**解决**：
修改 `AppConfig.java` 第 28 行：
```java
.baseUrl("http://localhost:8003")
```

重启 Java 后端。

---

### 场景 3：端口被占用

**症状**：
- Python AI 服务启动失败
- 报错：`OSError: [WinError 10048]`

**诊断**：
```bash
netstat -ano | findstr :8003
# 看到其他进程占用
```

**解决**：

**方案 A**：杀死占用进程
```bash
# 假设 PID 为 12345
taskkill /F /PID 12345
```

**方案 B**：修改端口
```python
# 修改 main_simple.py 第 12 行
PORT = 8004

# 修改 AppConfig.java 第 28 行
.baseUrl("http://localhost:8004")
```

---

### 场景 4：Python 代码错误

**症状**：
- Python AI 服务启动成功
- 收到请求后报错

**诊断**：
查看 Python 控制台错误堆栈

**解决**：
根据错误信息修复 Python 代码

---

### 场景 5：请求数据格式错误

**症状**：
- Python AI 服务返回 400 错误
- Java 后端显示请求失败

**诊断**：
检查请求 JSON 格式

**解决**：
确保请求数据包含所有必需字段：
```json
{
  "projectName": "项目名称",
  "applicantName": "申请人",
  "waterSource": "水源",
  "waterPurpose": "用途",
  "applicationPeriod": "期限",
  "waterVolume": 1000,
  "projectDescription": "项目描述",
  "documents": []
}
```

---

## 🔧 解决方案汇总

### 问题 1：Python AI 服务未启动

```bash
# 启动服务
cd python-ai-service
python main_simple.py

# 或使用一键启动
双击：python-ai-service\一键启动 AI.bat
```

---

### 问题 2：端口配置不一致

```bash
# 1. 修改 Java 后端配置
编辑：java-backend\config\AppConfig.java
修改第 28 行：.baseUrl("http://localhost:8003")

# 2. 重启 Java 后端
在 IntelliJ IDEA 中重新启动
```

---

### 问题 3：端口被占用

```bash
# 1. 查找占用进程
netstat -ano | findstr :8003

# 2. 杀死进程
taskkill /F /PID [进程 ID]

# 3. 或修改端口
修改 main_simple.py 第 12 行：PORT = 8004
修改 AppConfig.java 第 28 行：.baseUrl("http://localhost:8004")
```

---

### 问题 4：防火墙阻止

```bash
# Windows 防火墙添加例外
netsh advfirewall firewall add rule name="Python AI" dir=in action=allow program="C:\Python\python.exe" enable=yes
```

---

### 问题 5：Java 后端未重启

```bash
# 修改配置后必须重启
在 IntelliJ IDEA 中：
1. 停止当前运行
2. 重新运行 WaterApprovalApplication.java
```

---

## 📊 完整的检查清单

### Python AI 服务检查
- [ ] Python AI 服务已启动
- [ ] 运行在端口 8003
- [ ] 健康检查通过
- [ ] 端口未被占用
- [ ] 无 Python 代码错误

### Java 后端检查
- [ ] Java 后端已启动
- [ ] 运行在端口 8080
- [ ] WebClient 配置正确（端口 8003）
- [ ] 错误处理完善
- [ ] 控制台无错误日志

### 网络检查
- [ ] localhost 解析正常
- [ ] 防火墙未阻止
- [ ] 端口连通性正常

---

## 🎯 快速修复流程

```
AI 审查失败
    ↓
1. 运行诊断工具
   双击：诊断 AI 审查.bat
    ↓
2. 根据诊断结果修复
   - Python AI 服务未启动 → 启动服务
   - 端口配置错误 → 修改配置
   - Java 后端未启动 → 启动后端
    ↓
3. 重新测试
   前端点击"AI 审查"按钮
    ↓
4. 查看结果
   - 成功 → 完成
   - 失败 → 查看 Java 控制台错误信息
```

---

## 📝 调试技巧

### 技巧 1：查看详细错误

修改 `ReviewController.java` 后，重启 Java 后端，控制台会显示详细错误信息。

---

### 技巧 2：直接测试 Python AI 服务

```bash
# 使用 curl 测试
curl -X POST http://localhost:8003/api/review \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "测试项目",
    "applicantName": "测试",
    "waterSource": "黄河",
    "waterPurpose": "工业用水",
    "applicationPeriod": "2024-01-01",
    "waterVolume": 1000,
    "projectDescription": "测试",
    "documents": []
  }'
```

---

### 技巧 3：使用 Postman/Apifox

创建测试请求：
```
POST http://localhost:8003/api/review
Content-Type: application/json
Body: { ... }
```

---

## 🎉 成功标志

### Python AI 服务正常
```
Serving at port 8003
127.0.0.1 - - [...] "POST /api/review HTTP/1.1" 200 -
```

### Java 后端正常
```
无错误日志
```

### AI 审查成功
```json
{
  "status": "success",
  "data": {
    "approved": true,
    "remarks": "材料齐全，符合要求"
  }
}
```

---

## 📞 常见问题 FAQ

### Q1: AI 审查失败，如何查看详细错误？
A: 查看 Java 后端控制台，会显示 "AI 审查失败：[详细信息]"

### Q2: Python AI 服务必须一直运行吗？
A: 是的，使用 AI 审查功能时需要保持运行。

### Q3: 修改配置后需要重启吗？
A: 需要，修改任何配置后都要重启 Java 后端。

### Q4: 可以禁用 AI 审查吗？
A: 可以，AI 审查是可选功能，可以手动审查。

### Q5: 为什么健康检查通过但审查失败？
A: 可能是请求数据格式错误或 Python 代码内部错误。

---

## 🚀 现在就开始

**最简单的排查方法**：

1. 双击运行 [诊断 AI 审查.bat](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\诊断 AI 审查.bat)
2. 根据诊断结果修复
3. 重启 Java 后端
4. 重新测试 AI 审查

**就这么简单！** 🎉

---

## 📂 相关工具

- 📄 [诊断 AI 审查.bat](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\诊断 AI 审查.bat) - 自动诊断工具
- 📄 [一键启动 AI.bat](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\python-ai-service\一键启动 AI.bat) - Python AI 服务启动
- 📄 [启动指南.md](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\python-ai-service\启动指南.md) - 详细启动说明
- 📄 [AI 审查故障排查指南.md](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\AI 审查故障排查指南.md) - 完整排查指南
