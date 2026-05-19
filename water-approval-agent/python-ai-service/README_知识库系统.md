# 📚 知识库系统使用指南

## 目录

1. [系统概述](#系统概述)
2. [快速开始](#快速开始)
3. [功能说明](#功能说明)
4. [API 接口文档](#api 接口文档)
5. [MCP 服务](#mcp 服务)
6. [使用示例](#使用示例)
7. [常见问题](#常见问题)

---

## 系统概述

### 功能特性

✅ **文档解析**
- 支持 PDF 格式文档解析
- 支持 Word (.doc/.docx) 格式文档解析
- 自动提取文本内容和页码信息

✅ **智能分块**
- 自动将长文档分块处理
- 支持自定义分块大小和重叠度
- 保留文档元数据（来源、页码等）

✅ **向量化存储**
- 使用 Sentence Transformers 生成嵌入向量
- 支持中文的多语言模型 (paraphrase-multilingual-MiniLM-L12-v2)
- ChromaDB 向量数据库持久化存储

✅ **语义检索**
- 基于语义相似度的智能检索
- 返回相关文档片段
- 提供相似度分数、来源、页码等信息

✅ **MCP 服务**
- `knowledge_search`: 知识检索工具
- `check_completeness`: 材料完整性检查工具
- `upload_document`: 文档上传工具
- `get_knowledge_stats`: 知识库统计工具

---

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- 操作系统：Windows / macOS / Linux
- 内存：至少 4GB（推荐 8GB）
- 磁盘空间：至少 2GB

### 安装依赖

```bash
cd python-ai-service
pip install -r requirements.txt
```

### 启动服务

**Windows:**
```bash
双击运行：一键启动知识库服务.bat
```

**macOS/Linux:**
```bash
python main_knowledge.py
```

### 验证服务

浏览器访问：http://localhost:8003/api/health

看到以下响应表示服务正常：
```json
{
  "status": "healthy",
  "service": "water-approval-ai-knowledge",
  "timestamp": "2026-05-13T...",
  "port": 8003
}
```

---

## 功能说明

### 1. 文档上传

**支持格式：**
- PDF (.pdf)
- Word (.doc, .docx)

**上传方式：**

#### 方式一：通过 Web 界面
1. 访问：http://localhost:8003/knowledge_manager.html
2. 点击上传区域或拖拽文件
3. 等待解析和向量化完成

#### 方式二：通过 API
```bash
curl -X POST http://localhost:8003/api/knowledge/upload \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "C:/documents/取水许可管理办法.pdf",
    "chunk_size": 500
  }'
```

**响应示例：**
```json
{
  "success": true,
  "filename": "取水许可管理办法.pdf",
  "format": "pdf",
  "pages": 15,
  "chunks": 45,
  "added": 45
}
```

### 2. 知识检索

#### 方式一：通过 Web 界面
1. 访问：http://localhost:8003/knowledge_manager.html
2. 在搜索框输入查询内容
3. 点击"搜索"按钮
4. 查看检索结果（包含相似度、来源、内容）

#### 方式二：通过 API
```bash
curl -X POST http://localhost:8003/api/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "取水许可申请需要什么材料？",
    "top_k": 5,
    "min_similarity": 0.5
  }'
```

**响应示例：**
```json
{
  "query": "取水许可申请需要什么材料？",
  "results": [
    {
      "text": "取水许可申请需要提交申请书、身份证明、水资源论证报告等材料。",
      "metadata": {
        "source": "取水许可管理办法.pdf",
        "chunk_id": "chunk_0",
        "page": 1
      },
      "similarity": 0.892,
      "source": "取水许可管理办法.pdf",
      "page": 1
    }
  ],
  "count": 1
}
```

### 3. 材料完整性检查

#### 通过 Web 界面
1. 访问：http://localhost:8003/knowledge_manager.html
2. 在"材料完整性检查"区域输入已提交的材料
3. 点击"检查材料完整性"
4. 查看检查结果（已具备/缺失材料）

#### 通过 API
```bash
curl -X POST http://localhost:8003/api/knowledge/check \
  -H "Content-Type: application/json" \
  -d '{
    "submitted_documents": ["申请书", "身份证明", "水资源论证报告"]
  }'
```

**响应示例：**
```json
{
  "provided": [
    "申请书",
    "身份证明",
    "水资源论证报告"
  ],
  "missing": [
    "取水工程可行性研究报告",
    "水源地水质监测报告",
    "取水口位置图",
    "用水计划方案",
    "节水措施方案",
    "第三者利害关系说明"
  ],
  "completeness": 33.3
}
```

### 4. 知识库统计

```bash
curl http://localhost:8003/api/knowledge/stats
```

**响应示例：**
```json
{
  "stats": {
    "total_documents": 150,
    "collection_name": "knowledge_base"
  },
  "sources": [
    "取水许可管理办法.pdf",
    "水资源论证报告编制指南.docx",
    "取水许可审批工作规程.pdf"
  ]
}
```

### 5. 删除文档

```bash
curl -X POST http://localhost:8003/api/knowledge/delete \
  -H "Content-Type: application/json" \
  -d '{
    "source": "取水许可管理办法.pdf"
  }'
```

**响应示例：**
```json
{
  "deleted": 45,
  "source": "取水许可管理办法.pdf"
}
```

---

## API 接口文档

### 基础信息

- **基础 URL:** `http://localhost:8003/api`
- **Content-Type:** `application/json`
- **CORS:** 允许所有来源访问

### 接口列表

#### 1. 健康检查
```
GET /api/health
```

#### 2. 知识库统计
```
GET /api/knowledge/stats
```

#### 3. 知识检索（GET）
```
GET /api/knowledge/search?query=查询内容&top_k=5&min_similarity=0.5
```

#### 4. 知识检索（POST）
```
POST /api/knowledge/search
Content-Type: application/json

{
  "query": "查询内容",
  "top_k": 5,
  "min_similarity": 0.5
}
```

#### 5. 文档上传
```
POST /api/knowledge/upload
Content-Type: application/json

{
  "file_path": "文件路径",
  "chunk_size": 500
}
```

#### 6. 删除文档
```
POST /api/knowledge/delete
Content-Type: application/json

{
  "source": "来源文件名"
}
```

---

## MCP 服务

### 启动 MCP 服务

```bash
python mcp_service.py
```

### 可用工具

#### 1. knowledge_search - 知识检索

**功能：** 搜索知识库中的法规、政策、办事指南等信息

**参数：**
- `query` (必需): 查询语句
- `top_k` (可选): 返回结果数量，默认 5
- `min_similarity` (可选): 最小相似度阈值，默认 0.5

**示例：**
```json
{
  "name": "knowledge_search",
  "arguments": {
    "query": "取水许可申请需要什么材料？",
    "top_k": 5
  }
}
```

**返回：**
```
找到 3 个相关文档片段：

[1] 相似度：0.892
    来源：取水许可管理办法.pdf (第 1 页)
    内容：取水许可申请需要提交申请书、身份证明、水资源论证报告等材料。

[2] 相似度：0.756
    来源：水资源论证报告编制指南.docx (第 3 页)
    内容：水资源论证报告应当包括建设项目取水情况、用水合理性分析等内容。
```

#### 2. check_completeness - 材料检查

**功能：** 检查申请材料是否完整

**参数：**
- `submitted_documents` (必需): 已提交的材料列表
- `check_type` (可选): 检查类型（required/all），默认 required

**示例：**
```json
{
  "name": "check_completeness",
  "arguments": {
    "submitted_documents": ["申请书", "身份证明", "水资源论证报告"],
    "check_type": "required"
  }
}
```

**返回：**
```
材料完整性检查报告
==================================================

检查类型：必需材料
已提交：3 个
应提交：9 个

✅ 已具备材料 (3/9):
   - 申请书
   - 身份证明
   - 水资源论证报告

❌ 缺失材料 (6):
   - 取水工程可行性研究报告
   - 水源地水质监测报告
   - 取水口位置图
   - 用水计划方案
   - 节水措施方案
   - 第三者利害关系说明

完整度：33.3%

建议：请补充缺失的材料后再提交申请。
```

#### 3. upload_document - 文档上传

**功能：** 上传文档到知识库

**参数：**
- `file_path` (必需): 文档文件路径
- `chunk_size` (可选): 分块大小，默认 500

**示例：**
```json
{
  "name": "upload_document",
  "arguments": {
    "file_path": "C:/documents/取水许可管理办法.pdf",
    "chunk_size": 500
  }
}
```

#### 4. get_knowledge_stats - 统计信息

**功能：** 获取知识库统计信息

**示例：**
```json
{
  "name": "get_knowledge_stats",
  "arguments": {}
}
```

**返回：**
```
知识库统计信息
==================================================
文档块总数：150
集合名称：knowledge_base

来源文件列表 (3):
   - 取水许可管理办法.pdf
   - 水资源论证报告编制指南.docx
   - 取水许可审批工作规程.pdf
```

---

## 使用示例

### 示例 1：上传法规文档

```python
import requests

# 上传 PDF 文档
response = requests.post('http://localhost:8003/api/knowledge/upload', json={
    'file_path': 'C:/documents/取水许可管理办法.pdf',
    'chunk_size': 500
})

print(response.json())
# 输出：{'success': True, 'filename': '取水许可管理办法.pdf', 'chunks': 45, ...}
```

### 示例 2：检索相关知识

```python
import requests

# 检索问题答案
response = requests.post('http://localhost:8003/api/knowledge/search', json={
    'query': '取水许可的审批时限是多久？',
    'top_k': 3
})

results = response.json()['results']
for r in results:
    print(f"相似度：{r['similarity']:.3f}")
    print(f"来源：{r['source']}")
    print(f"内容：{r['text']}")
    print()
```

### 示例 3：检查材料完整性

```python
import requests

# 检查材料
response = requests.post('http://localhost:8003/api/knowledge/check', json={
    'submitted_documents': ['申请书', '身份证明', '水资源论证报告']
})

result = response.json()
print(f"已具备：{len(result['provided'])} 个")
print(f"缺失：{len(result['missing'])} 个")
print(f"完整度：{result['completeness']:.1f}%")
```

---

## 常见问题

### Q1: 服务启动失败，提示端口被占用

**解决方案：**
```bash
# Windows: 杀死占用 8003 端口的进程
netstat -ano | findstr :8003
taskkill /F /PID <进程 ID>

# 或直接使用一键启动脚本（会自动处理）
一键启动知识库服务.bat
```

### Q2: 依赖包安装失败

**解决方案：**
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或手动安装核心依赖
pip install flask flask-cors chromadb sentence-transformers PyPDF2 python-docx
```

### Q3: 首次加载模型很慢

**说明：** 首次运行时会下载 Sentence Transformers 模型（约 400MB），请耐心等待。后续运行会自动加载本地模型。

**解决方案：**
- 使用稳定的网络连接
- 可以预先下载模型到本地

### Q4: 检索结果不准确

**优化建议：**
1. 调整 `min_similarity` 参数（默认 0.5，可调高到 0.6-0.7）
2. 增加文档数量，丰富知识库
3. 优化查询语句，使用更明确的关键词
4. 调整分块大小（chunk_size）

### Q5: PDF 解析乱码

**原因：** 部分 PDF 使用了特殊字体或加密

**解决方案：**
1. 使用文字版 PDF（非扫描版）
2. 转换为 Word 格式后上传
3. 使用 OCR 工具预处理扫描版 PDF

### Q6: 内存不足

**解决方案：**
1. 减少并发请求数量
2. 减小分块大小（chunk_size）
3. 增加系统内存或使用服务器部署

---

## 技术架构

```
┌─────────────────┐
│   Web 界面      │  http://localhost:8003/knowledge_manager.html
│  (HTML/JS)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask 服务     │  http://localhost:8003
│  (main_knowledge.py) │
└────────┬────────┘
         │
         ├─────► ┌─────────────────┐
         │       │  文档解析器     │  PyPDF2, python-docx
         │       │  (PDF/Word)     │
         │       └─────────────────┘
         │
         ├─────► ┌─────────────────┐
         │       │  分块器         │  DocumentChunker
         │       │  (智能分块)     │
         │       └─────────────────┘
         │
         ├─────► ┌─────────────────┐
         │       │  嵌入模型       │  Sentence Transformers
         │       │  (向量化)       │
         │       └─────────────────┘
         │
         └─────► ┌─────────────────┐
                 │  ChromaDB       │  向量数据库
                 │  (持久化存储)   │
                 └─────────────────┘
```

---

## 项目结构

```
python-ai-service/
├── main_knowledge.py          # 主服务程序
├── mcp_service.py             # MCP 服务
├── document_parser.py         # 文档解析模块
├── vector_db.py               # 向量数据库模块
├── knowledge_manager.html     # 知识库管理界面
├── requirements.txt           # Python 依赖
├── 一键启动知识库服务.bat     # 启动脚本
├── chroma_db/                 # ChromaDB 数据目录（自动生成）
└── README_知识库系统.md       # 本文档
```

---

## 下一步

### 已实现 ✅
- [x] PDF/Word 文档解析
- [x] 智能文档分块
- [x] 向量化存储（ChromaDB）
- [x] 语义检索
- [x] MCP 服务（knowledge_search, check_completeness）
- [x] Web 管理界面

### 计划实现 📋
- [ ] 支持更多文档格式（Excel, PPT）
- [ ] 批量上传文档
- [ ] 文档版本管理
- [ ] 检索历史记录
- [ ] 用户权限管理
- [ ] 检索结果导出

---

## 技术支持

如有问题，请检查：
1. Python 版本是否符合要求
2. 依赖包是否正确安装
3. 端口 8003 是否被占用
4. 查看控制台错误日志

---

祝使用愉快！🚀
