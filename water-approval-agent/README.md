# 涉水审批材料合规性审查 Agent 系统

## 项目简介

本项目是一个基于双栈架构（Java + Python）的涉水审批材料合规性审查智能系统，利用 LangChain Agent 和 RAG 技术实现对取水申请材料的自动化合规性审查。

系统支持：
- ✅ MCP 协议调用知识库工具
- ✅ 结构化文档处理（docx、pdf 等）
- ✅ 非结构化文档 OCR 处理（扫描件识别）
- ✅ 基于知识库的合规审查和修改建议
- ✅ 审查结果稳定性保证
- ✅ Java-Python 完整集成
- ✅ 规则可手动增减

## 技术架构

### 双栈架构
- **Java 后端**：Spring Boot 3.2.0 + WebFlux，作为主后端提供 REST API
- **Python AI 服务**：FastAPI + LangChain + ChromaDB，提供 AI 智能审查能力

### 核心技术
- **LangChain**：构建 Agent 智能体，实现合规审查逻辑
- **ChromaDB**：向量数据库，存储法规知识
- **MCP 协议**：Model Context Protocol，实现标准化工具调用
- **RAG 技术**：检索增强生成，用于合规性判断
- **OCR**：pytesseract + pdf2image，处理扫描件
- **多语言嵌入**：Sentence Transformers，支持中文语义理解

## 项目结构

```
water-approval-agent/
├── java-backend/                     # Java Spring Boot 后端
│   ├── src/main/java/
│   │   └── com/waterapproval/
│   │       ├── WaterApprovalApplication.java
│   │       ├── config/
│   │       │   └── AppConfig.java           # 配置类（WebClient、CORS）
│   │       ├── controller/
│   │       │   ├── ReviewController.java    # 审查接口
│   │       │   └── FileUploadController.java
│   │       ├── model/
│   │       │   ├── ReviewRequest.java
│   │       │   └── ReviewResponse.java
│   │       ├── service/
│   │       │   ├── ReviewService.java       # 审查服务（含重试机制）
│   │       │   ├── ApplicationService.java
│   │       │   └── FileService.java
│   │       └── repository/
│   ├── src/main/resources/
│   │   └── application.properties
│   └── pom.xml
├── python-ai-service/                  # Python AI 服务
│   ├── main_enhanced.py                # 增强版主服务
│   ├── main.py                         # 简化版服务
│   ├── mcp_service.py                  # MCP 服务
│   ├── vector_db.py                    # 向量数据库
│   ├── document_parser.py              # 文档解析器
│   ├── requirements.txt
│   └── src/
│       ├── services/
│       │   ├── compliance_agent.py     # 合规审查 Agent
│       │   └── agent_service.py
│       └── tools/
│           ├── mcp_tools.py            # MCP 工具执行器
│           └── ocr_tool.py             # OCR 工具
├── test_integration.py                 # 集成测试脚本
├── test_stability.py                   # 稳定性测试脚本
└── docs/                               # 文档目录
```

## 核心功能

### 1. MCP 协议调用 ⭐
- `knowledge_search`：知识检索工具，支持语义搜索
- `check_completeness`：材料完整性检查工具
- `upload_document`：文档上传工具
- `get_knowledge_stats`：知识库统计信息

### 2. 结构化文档处理 ⭐
- **PDF 文档**：使用 pdfplumber 精确解析
- **Word 文档**：使用 python-docx 解析
- **智能分块**：RecursiveCharacterTextSplitter
- **向量嵌入**：paraphrase-multilingual-MiniLM-L12-v2

### 3. 非结构化文档 OCR 处理 ⭐
- **图片 OCR**：支持 jpg、png、bmp 等格式
- **PDF 扫描件**：pdf2image + pytesseract
- **中文识别**：chi_sim+eng 双语言模型
- **置信度评估**：自动计算识别可信度

### 4. 合规审查 ⭐
- **形式审查**：完整性检查
- **内容审查**：逻辑一致性检查
- **实质审查**：基于 RAG 的合规判断
- **修改建议**：针对不合规项给出具体建议
- **规则管理**：支持手动增减审查规则

### 5. 审查结果稳定性 ⭐
- **固定随机种子**：确保多次调用结果一致
- **重试机制**：Java 端自动重试 3 次
- **超时控制**：60 秒超时保护
- **稳定性接口**：`/api/review/stable` 专用接口

## 快速开始

### 方式一：一键启动（推荐）

```bash
# Windows
cd water-approval-agent
.\auto-start.bat

# 或手动启动
.\start-java.bat
.\start-python.bat
```

### 方式二：分步启动

#### 1. Python AI 服务

```bash
cd python-ai-service
pip install -r requirements.txt
python main_enhanced.py
```

服务将在 `http://localhost:8000` 启动

#### 2. Java 后端

```bash
cd java-backend
mvn clean install
mvn spring-boot:run
```

服务将在 `http://localhost:8080` 启动

### 3. 测试系统

```bash
# 集成测试
python test_integration.py

# 稳定性测试
python test_stability.py
```

## API 接口

### Python AI 服务

#### 审查接口
- `POST /api/review` - 提交审查请求
- `POST /api/review/stable` - 稳定性审查（固定随机种子）

#### 知识库接口
- `POST /api/knowledge/search` - 搜索知识库
- `POST /api/knowledge/upload` - 上传知识文档
- `POST /api/knowledge/stats` - 获取统计信息

#### MCP 工具接口
- `POST /api/mcp/tools` - MCP 工具调用
  - `knowledge_search`：知识检索
  - `check_completeness`：材料检查
  - `upload_document`：文档上传

#### 规则管理接口
- `GET /api/rules/list` - 获取规则列表
- `POST /api/rules/update` - 更新规则

#### 文件处理接口
- `POST /api/upload` - 上传并处理文件（支持 OCR）

#### 健康检查
- `GET /api/health` - 健康检查

### Java 后端

- `POST /api/review` - 提交审查请求（转发到 Python 服务）
- `POST /api/review/stable` - 稳定性审查
- `GET /api/health` - 健康检查
- `POST /api/upload` - 文件上传

## 配置说明

### Python 服务

环境变量（可选）：
```bash
OPENAI_API_KEY=your_key  # 如果使用 OpenAI
```

配置文件：无需额外配置，默认使用本地嵌入模型

### Java 服务

配置文件：`src/main/resources/application.properties`

```properties
# Python AI 服务地址
python.ai.service.url=http://localhost:8000

# 服务器端口
server.port=8080

# 文件上传大小限制
spring.servlet.multipart.max-file-size=100MB
spring.servlet.multipart.max-request-size=100MB
```

## 使用示例

### 1. 提交审查请求

```python
import requests

data = {
    "application_data": {
        "project_name": "某取水项目",
        "applicant_name": "某某公司",
        "water_source": "地表水",
        "water_purpose": "工业用水",
        "application_period": "2024-01-01 至 2034-12-31",
        "water_volume": 1000
    },
    "documents": ["application_form", "business_license"],
    "check_type": "full"  # full, completeness, compliance
}

response = requests.post("http://localhost:8000/api/review", json=data)
result = response.json()

print(f"审查状态：{result['status']}")
print(f"问题数量：{result['results']['total_issues']}")
for issue in result['issues']:
    print(f"  - {issue['message']}")
```

### 2. 调用 MCP 工具

```python
# 知识检索
response = requests.post("http://localhost:8000/api/mcp/tools", json={
    "tool_name": "knowledge_search",
    "parameters": {
        "query": "取水许可申请需要什么材料？",
        "top_k": 5
    }
})

# 材料检查
response = requests.post("http://localhost:8000/api/mcp/tools", json={
    "tool_name": "check_completeness",
    "parameters": {
        "submitted_documents": ["申请书", "身份证明", "水资源论证报告"],
        "check_type": "required"
    }
})
```

### 3. 上传扫描件（OCR）

```python
import requests

files = {"file": open("scan.pdf", "rb")}
response = requests.post(
    "http://localhost:8000/api/upload",
    files=files,
    data={"is_scan": "true", "process_type": "both"}
)
result = response.json()

print(f"OCR 识别置信度：{result['ocr']['confidence']:.2f}%")
```

### 4. 更新审查规则

```python
new_rules = [
    {
        "id": "rule_006",
        "name": "环境保护",
        "description": "取水项目必须符合环境保护要求",
        "check_points": ["是否进行环评", "是否有环保措施"],
        "severity": "high"
    }
]

response = requests.post(
    "http://localhost:8000/api/rules/update",
    json={"rules": new_rules}
)
```

## 测试

### 集成测试

```bash
python test_integration.py
```

测试项目：
1. Python 服务健康检查
2. Java 服务健康检查
3. MCP 知识检索工具
4. MCP 材料完整性检查
5. AI 审查接口
6. Java-Python 集成
7. 知识库上传
8. 规则管理

### 稳定性测试

```bash
python test_stability.py
```

测试项目：
1. 多次调用结果一致性
2. 审查状态稳定性
3. 问题数量稳定性
4. 修改建议稳定性

## 创新性功能

### 1. LangChain Agent 集成 ⭐
- 使用 LangChain 构建智能审查 Agent
- ReAct 模式进行推理和工具调用
- 可解释的审查过程

### 2. RAG 增强生成 ⭐
- 检索相关法规条款
- 基于检索结果进行合规判断
- 引用法规来源

### 3. 双栈架构优势 ⭐
- Java：企业级后端，稳定可靠
- Python：AI 能力强，生态丰富
- HTTP 解耦，独立部署

### 4. 规则可配置 ⭐
- 支持动态添加审查规则
- 规则可手动增减
- 适应不同地区政策

## 常见问题

### Q: Python 服务无法启动？
A: 检查端口 8000 是否被占用，或修改 `main_enhanced.py` 中的端口配置

### Q: Java 后端连接不上 Python 服务？
A: 检查 `application.properties` 中的 `python.ai.service.url` 配置

### Q: OCR 识别不准确？
A: 确保安装了 Tesseract OCR，并下载了中文语言包

### Q: 审查结果不稳定？
A: 使用 `/api/review/stable` 接口，该接口使用固定随机种子

## 技术栈总结

### Java 后端
- Spring Boot 3.2.0
- Spring WebFlux
- Maven
- H2 Database

### Python AI 服务
- FastAPI
- LangChain
- ChromaDB
- Sentence Transformers
- pytesseract
- pdfplumber
- python-docx

### 协议与标准
- MCP (Model Context Protocol)
- RESTful API
- CORS

## 团队分工建议

- **Java 开发**：后端架构、数据库设计、API 实现
- **Python 开发**：AI 模型、Agent 逻辑、OCR 处理
- **前端开发**：用户界面、交互设计
- **测试**：集成测试、稳定性测试
- **文档**：技术文档、API 文档、部署说明

## Git 提交规范

```bash
# 示例提交记录
git commit -m "feat: 添加 MCP 知识检索工具"
git commit -m "fix: 修复 OCR 识别置信度计算"
git commit -m "docs: 更新 API 文档"
git commit -m "test: 添加集成测试脚本"
git commit -m "refactor: 优化 ReviewService 重试机制"
git commit -m "feat(java): 添加稳定性审查接口"
git commit -m "feat(python): 实现合规审查 Agent"
git commit -m "chore: 更新依赖版本"
```

## 许可证

本项目仅供学习研究使用

## 联系方式

如有问题，请提交 Issue 或联系开发团队
