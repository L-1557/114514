# AI 审查服务故障排查指南

## ❌ 常见问题及解决方案

### 问题 1：端口不匹配（最常见）

**症状**：
- Java 后端报错：`Connection refused`
- 前端显示：`AI 服务不可用`

**原因**：
- Java 后端配置的端口与 Python AI 服务实际端口不一致

**检查方法**：

1. 查看 Java 后端配置
   ```bash
   # 文件位置
   java-backend/src/main/java/com/waterapproval/config/AppConfig.java
   
   # 查看第 28 行
   .baseUrl("http://localhost:8003")  # 应该为 8003
   ```

2. 查看 Python AI 服务配置
   ```bash
   # 文件位置
   python-ai-service/main_simple.py
   
   # 查看第 12 行
   PORT = 8003  # 应该为 8003
   ```

**解决方案**：
```bash
# 确保两个端口一致（都使用 8003）
Java 后端：8003 ✅
Python AI: 8003 ✅
```

---

### 问题 2：Python AI 服务未启动

**症状**：
- Java 后端报错：`Connection refused`
- 访问 `http://localhost:8003/api/health` 无法访问

**检查方法**：
```bash
# Windows 命令行
netstat -ano | findstr :8003

# 如果没有输出，说明服务未启动
```

**解决方案**：

启动 Python AI 服务：
```bash
# 方法 1：直接启动
cd python-ai-service
python main_simple.py

# 方法 2：使用启动脚本
cd python-ai-service
start.bat
```

**验证启动成功**：
```bash
# 浏览器访问
http://localhost:8003/api/health

# 应该返回
{
  "status": "healthy",
  "service": "water-approval-ai",
  "timestamp": "2024-01-01T12:00:00"
}
```

---

### 问题 3：端口被占用

**症状**：
- Python AI 服务启动失败
- 报错：`OSError: [WinError 10048] 端口已被占用`

**解决方案**：

1. 查看占用端口的进程
   ```bash
   netstat -ano | findstr :8003
   ```

2. 杀死占用端口的进程
   ```bash
   # 假设 PID 为 12345
   taskkill /F /PID 12345
   ```

3. 或者修改 Python AI 服务端口
   ```python
   # 修改 main_simple.py 第 12 行
   PORT = 8004  # 改为其他端口
   ```

4. 同时修改 Java 后端配置
   ```java
   // 修改 AppConfig.java 第 28 行
   .baseUrl("http://localhost:8004")
   ```

---

### 问题 4：CORS 跨域问题

**症状**：
- 浏览器控制台报错：`CORS policy`
- Python AI 服务收到请求但拒绝

**解决方案**：

Python AI 服务已支持 CORS（第 16-21 行）：
```python
def do_OPTIONS(self):
    """处理 CORS 预检请求"""
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.end_headers()
```

---

## 🔧 完整的启动流程

### 步骤 1：启动 Python AI 服务

```bash
# 打开命令行
cd C:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\python-ai-service
python main_simple.py
```

**验证**：
```bash
# 浏览器访问
http://localhost:8003/api/health
```

应该看到：
```json
{
  "status": "healthy",
  "service": "water-approval-ai",
  "timestamp": "2024-01-01T12:00:00"
}
```

---

### 步骤 2：启动 Java 后端

```bash
# 在 IntelliJ IDEA 中运行
WaterApprovalApplication.java
```

**验证**：
```bash
# 浏览器访问
http://localhost:8080/api/health
```

应该看到：
```
Java backend is healthy
```

---

### 步骤 3：测试 AI 审查

```bash
# 使用 curl 测试
curl -X POST http://localhost:8080/api/review \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "测试项目",
    "applicantName": "张三",
    "waterSource": "黄河",
    "waterPurpose": "工业用水",
    "applicationPeriod": "2024-01-01 至 2029-12-31",
    "waterVolume": 50000,
    "projectDescription": "测试项目描述",
    "documents": ["application_form"]
  }'
```

---

## 📊 故障排查流程图

```
AI 审查失败
    ↓
1. 检查 Python AI 服务是否启动
    ↓ 未启动
   启动服务：python main_simple.py
    ↓ 已启动
2. 检查端口是否一致
    ↓ 不一致
   修改 AppConfig.java 第 28 行
    ↓ 一致
3. 检查端口是否被占用
    ↓ 被占用
   杀死进程或修改端口
    ↓ 未占用
4. 测试健康检查
    ↓ 失败
   检查防火墙/杀毒软件
    ↓ 成功
5. 重新测试 AI 审查
```

---

## 🎯 快速检查清单

### Python AI 服务检查
- [ ] Python AI 服务已启动
- [ ] 运行在端口 8003
- [ ] 健康检查通过：http://localhost:8003/api/health
- [ ] 端口未被占用
- [ ] CORS 配置正确

### Java 后端检查
- [ ] Java 后端已启动
- [ ] 运行在端口 8080
- [ ] 健康检查通过：http://localhost:8080/api/health
- [ ] WebClient 配置正确（端口 8003）
- [ ] 错误处理完善

### 网络检查
- [ ] 防火墙未阻止 8003 端口
- [ ] 杀毒软件未阻止 Python
- [ ] localhost 解析正常

---

## 🔍 调试技巧

### 1. 查看 Java 后端日志

启动 Java 后端时，查看控制台输出：
```
AI 服务请求失败：...
AI 服务连接失败：...
```

### 2. 查看 Python AI 服务日志

Python AI 服务启动后，查看控制台输出：
```
127.0.0.1 - - [01/Jan/2024 12:00:00] "POST /api/review HTTP/1.1" 200 -
```

### 3. 使用 Postman/Apifox 测试

直接测试 Python AI 服务：
```
POST http://localhost:8003/api/review
Content-Type: application/json

{
  "projectName": "测试项目",
  ...
}
```

### 4. 使用 telnet 测试端口连通性

```bash
telnet localhost 8003
```

如果连接成功，说明端口正常。

---

## 📝 配置文件位置

### Java 后端配置
📄 [AppConfig.java](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\java-backend\src\main\java\com\waterapproval\config\AppConfig.java)
- 第 28 行：WebClient baseUrl 配置

### Python AI 服务配置
📄 [main_simple.py](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\python-ai-service\main_simple.py)
- 第 12 行：PORT 配置

### 启动脚本
📄 [start.bat](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\python-ai-service\start.bat)
- Python AI 服务一键启动

---

## 🎉 验证成功

### 成功标志

✅ Python AI 服务启动成功
```
Serving at port 8003
```

✅ Java 后端连接成功
```
无错误日志
```

✅ AI 审查返回结果
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

### Q1: Python AI 服务必须启动吗？
A: 是的，AI 审查功能依赖 Python AI 服务。如果不启动，会报错。

### Q2: 可以不用 AI 审查吗？
A: 可以。AI 审查是可选功能，可以手动审查申请。

### Q3: 为什么使用 8003 端口？
A: 8001 和 8002 可能被其他服务占用，8003 是安全的选择。

### Q4: 可以修改端口吗？
A: 可以。同时修改 Python AI 服务的 PORT 和 Java 后端的 baseUrl 即可。

### Q5: AI 审查服务是必须的吗？
A: 如果只需要基本功能，可以不使用 AI 审查。系统支持手动审查。

---

## 🔧 已修复的问题

✅ **端口配置已更新**
- Java 后端：8003（原来是 8001）
- Python AI 服务：8003

✅ **错误处理已增强**
- 添加了详细的错误信息
- 提供了明确的解决方案提示

✅ **日志输出已优化**
- 打印详细的错误原因
- 方便故障排查

---

## 🚀 下一步操作

1. **重启 Java 后端**（应用新配置）
   ```bash
   # 在 IntelliJ IDEA 中重新启动
   WaterApprovalApplication.java
   ```

2. **启动 Python AI 服务**
   ```bash
   cd python-ai-service
   python main_simple.py
   ```

3. **测试 AI 审查**
   - 打开前端：http://localhost:8080
   - 进入申请详情
   - 点击"AI 审查"按钮

现在应该可以正常工作了！🎉
