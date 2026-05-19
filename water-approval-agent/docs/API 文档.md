# API 文档

## Python AI 服务 API

### 基础信息
- **基础 URL**: `http://localhost:8000`
- **数据格式**: JSON
- **字符编码**: UTF-8

---

## 审查接口

### 1. 提交审查请求

**接口**: `POST /api/review`

**描述**: 提交涉水申请材料进行合规性审查

**请求参数**:
```json
{
  "application_data": {
    "project_name": "string",
    "applicant_name": "string",
    "water_source": "string",
    "water_purpose": "string",
    "application_period": "string",
    "water_volume": "number",
    "project_volume": "number",
    "water_source_location": "string",
    "third_party_statement": "string"
  },
  "documents": ["string"],
  "check_type": "string",
  "is_scan": "boolean"
}
```

**参数说明**:
- `application_data` (object): 申请材料数据
  - `project_name` (string): 项目名称
  - `applicant_name` (string): 申请人/单位名称
  - `water_source` (string): 水源类型（地表水/地下水）
  - `water_purpose` (string): 取水用途
  - `application_period` (string): 申请期限
  - `water_volume` (number): 申请取水量
  - `project_volume` (number): 可研报告测算用水量
  - `water_source_location` (string): 取水口位置
  - `third_party_statement` (string): 第三者利害关系说明
- `documents` (array): 已提交的文档列表
- `check_type` (string): 检查类型
  - `full`: 完整审查
  - `completeness`: 仅完整性检查
  - `compliance`: 仅合规性检查
- `is_scan` (boolean): 是否为扫描件（默认 false）

**响应示例**:
```json
{
  "status": "failed",
  "results": {
    "check_type": "full",
    "total_issues": 3,
    "critical_issues": 2,
    "warning_issues": 1,
    "info_issues": 0
  },
  "issues": [
    {
      "type": "completeness",
      "severity": "high",
      "field": "water_source_location",
      "message": "取水口位置位于饮用水水源保护区"
    },
    {
      "type": "compliance",
      "severity": "high",
      "rule": "取水量合理性",
      "message": "申请取水量超过可研报告测算值"
    }
  ],
  "recommendations": [
    "重新选择取水口位置，避开饮用水水源保护区",
    "核实申请取水量的合理性，提供详细的用水测算依据"
  ],
  "knowledge_references": [
    {
      "issue": "取水口位置位于饮用水水源保护区",
      "regulation": "《中华人民共和国水法》第三十三条：在饮用水水源保护区内，禁止设置排污口。",
      "source": "中华人民共和国水法"
    }
  ]
}
```

**状态码说明**:
- `passed`: 审查通过
- `failed`: 审查不通过（存在严重问题）
- `warning`: 审查通过但存在警告
- `error`: 审查过程出错

---

### 2. 稳定性审查接口

**接口**: `POST /api/review/stable`

**描述**: 使用固定随机种子进行审查，确保多次调用结果一致

**请求参数**: 与 `/api/review` 相同

**响应示例**: 与 `/api/review` 相同

**特点**:
- 使用固定随机种子（42）
- 确保相同输入产生相同输出
- 适用于需要结果稳定性的场景

---

## 知识库接口

### 3. 搜索知识库

**接口**: `POST /api/knowledge/search`

**描述**: 在知识库中检索相关法规政策

**请求参数**:
```json
{
  "query": "string",
  "top_k": 5
}
```

**参数说明**:
- `query` (string): 查询语句
- `top_k` (number): 返回结果数量（默认 5）

**响应示例**:
```json
{
  "status": "success",
  "results": [
    {
      "text": "《中华人民共和国水法》第三十三条：在饮用水水源保护区内，禁止设置排污口。",
      "metadata": {
        "source": "中华人民共和国水法.pdf",
        "chunk_id": "chunk_0",
        "page": 5
      },
      "similarity": 0.95,
      "source": "中华人民共和国水法.pdf",
      "page": 5
    }
  ],
  "count": 1
}
```

---

### 4. 上传知识文档

**接口**: `POST /api/knowledge/upload`

**描述**: 上传法规文档到知识库

**请求参数**:
- `file` (file): 文件（支持 PDF、Word 格式）

**响应示例**:
```json
{
  "status": "success",
  "message": "文档上传成功",
  "chunks_added": 15
}
```

---

### 5. 获取知识库统计

**接口**: `POST /api/knowledge/stats`

**描述**: 获取知识库的统计信息

**响应示例**:
```json
{
  "status": "success",
  "data": {
    "total_documents": 150,
    "collection_name": "knowledge_base",
    "sources": [
      "中华人民共和国水法.pdf",
      "取水许可和水资源费征收管理条例.docx"
    ],
    "source_count": 2
  }
}
```

---

## MCP 工具接口

### 6. MCP 工具调用

**接口**: `POST /api/mcp/tools`

**描述**: 调用 MCP 协议定义的工具

**请求参数**:
```json
{
  "tool_name": "string",
  "parameters": {}
}
```

**可用工具**:

#### 6.1 knowledge_search - 知识检索

**参数**:
```json
{
  "tool_name": "knowledge_search",
  "parameters": {
    "query": "取水许可申请需要什么材料？",
    "top_k": 5,
    "min_similarity": 0.5
  }
}
```

**响应**:
```json
{
  "status": "success",
  "tool": "knowledge_search",
  "result": {
    "query": "取水许可申请需要什么材料？",
    "results": [...],
    "count": 5
  }
}
```

#### 6.2 check_completeness - 材料完整性检查

**参数**:
```json
{
  "tool_name": "check_completeness",
  "parameters": {
    "submitted_documents": ["申请书", "身份证明", "水资源论证报告"],
    "check_type": "required"
  }
}
```

**响应**:
```json
{
  "status": "success",
  "tool": "check_completeness",
  "result": {
    "check_type": "required",
    "submitted_count": 3,
    "required_count": 9,
    "provided": ["申请书", "身份证明", "水资源论证报告"],
    "missing": [
      "取水工程可行性研究报告",
      "水源地水质监测报告",
      "取水口位置图",
      "用水计划方案",
      "节水措施方案",
      "第三者利害关系说明"
    ],
    "completeness": 33.33,
    "is_complete": false
  }
}
```

#### 6.3 upload_document - 文档上传

**参数**:
```json
{
  "tool_name": "upload_document",
  "parameters": {
    "file_path": "/path/to/document.pdf",
    "chunk_size": 500
  }
}
```

**响应**:
```json
{
  "status": "success",
  "tool": "upload_document",
  "result": {
    "filename": "document.pdf",
    "format": "pdf",
    "pages": 10,
    "chunks_created": 20,
    "chunks_added": 20
  }
}
```

#### 6.4 get_knowledge_stats - 知识库统计

**参数**:
```json
{
  "tool_name": "get_knowledge_stats",
  "parameters": {}
}
```

**响应**:
```json
{
  "status": "success",
  "tool": "get_knowledge_stats",
  "result": {
    "total_documents": 150,
    "collection_name": "knowledge_base",
    "sources": [...],
    "source_count": 2
  }
}
```

---

## 规则管理接口

### 7. 获取规则列表

**接口**: `GET /api/rules/list`

**描述**: 获取所有合规审查规则

**响应示例**:
```json
{
  "status": "success",
  "rules": [
    {
      "id": "rule_001",
      "name": "水源地保护",
      "description": "取水水源地必须符合饮用水水源保护区规定",
      "check_points": [
        "取水口位置是否在饮用水水源保护区内",
        "是否设置排污口",
        "是否有防护措施"
      ],
      "severity": "high"
    },
    {
      "id": "rule_002",
      "name": "取水量合理性",
      "description": "申请取水量不得超过水资源论证报告测算的用水量",
      "check_points": [
        "申请取水量是否超过可研报告测算值",
        "是否有合理的用水依据",
        "是否符合行业用水定额标准"
      ],
      "severity": "high"
    }
  ],
  "count": 5
}
```

---

### 8. 更新审查规则

**接口**: `POST /api/rules/update`

**描述**: 添加或更新审查规则

**请求参数**:
```json
{
  "rules": [
    {
      "id": "rule_006",
      "name": "环境保护",
      "description": "取水项目必须符合环境保护要求",
      "check_points": [
        "是否进行环评",
        "是否有环保措施"
      ],
      "severity": "high"
    }
  ]
}
```

**参数说明**:
- `rules` (array): 规则列表
  - `id` (string): 规则 ID（可选，自动生成）
  - `name` (string): 规则名称
  - `description` (string): 规则描述
  - `check_points` (array): 检查点列表
  - `severity` (string): 严重程度（high/medium/low）

**响应示例**:
```json
{
  "status": "success",
  "message": "规则更新成功",
  "rules_count": 6
}
```

---

## 文件处理接口

### 9. 上传并处理文件

**接口**: `POST /api/upload`

**描述**: 上传文件并进行解析或 OCR 处理

**请求参数**:
- `file` (file): 文件
- `is_scan` (boolean): 是否为扫描件（默认 false）
- `process_type` (string): 处理类型
  - `parse`: 仅解析
  - `ocr`: 仅 OCR
  - `both`: 解析 + OCR

**响应示例**:
```json
{
  "filename": "document.pdf",
  "file_path": "/path/to/uploads/xxx_document.pdf",
  "file_hash": "abc123...",
  "parsed": {
    "content_length": 5000,
    "pages": 10,
    "format": "pdf"
  },
  "ocr": {
    "text_length": 4800,
    "confidence": 0.95
  }
}
```

---

## 健康检查接口

### 10. 健康检查

**接口**: `GET /api/health`

**描述**: 检查服务运行状态

**响应示例**:
```json
{
  "status": "healthy",
  "service": "water-approval-ai",
  "version": "2.0.0",
  "components": {
    "compliance_agent": true,
    "ocr_processor": true,
    "vector_db": true,
    "mcp_executor": true
  }
}
```

---

## Java 后端 API

### 11. 提交审查（Java）

**接口**: `POST /api/review`

**描述**: 通过 Java 后端提交审查（会转发到 Python 服务）

**请求参数**: 与 Python 服务相同

**响应示例**: 与 Python 服务相同

---

### 12. 稳定性审查（Java）

**接口**: `POST /api/review/stable`

**描述**: 通过 Java 后端提交稳定性审查

**请求参数**: 与 Python 服务相同

**响应示例**: 与 Python 服务相同

---

## 错误处理

### 错误响应格式

```json
{
  "status": "error",
  "message": "错误描述信息"
}
```

### 常见错误码

| HTTP 状态码 | 说明 |
|------------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

### 错误处理示例

```python
import requests

try:
    response = requests.post("http://localhost:8000/api/review", json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("status") == "error":
            print(f"审查失败：{result.get('message')}")
    else:
        print(f"请求失败：{response.status_code}")
except Exception as e:
    print(f"异常：{str(e)}")
```

---

## 使用建议

### 1. 审查流程

```
1. 上传知识文档 → /api/knowledge/upload
2. 检查材料完整性 → /api/mcp/tools (check_completeness)
3. 提交审查请求 → /api/review 或 /api/review/stable
4. 获取审查结果和修改建议
5. 根据建议修改后重新提交
```

### 2. 稳定性保证

- 使用 `/api/review/stable` 接口确保结果一致性
- Java 端实现了自动重试机制（最多 3 次）
- 设置 60 秒超时保护

### 3. 性能优化

- 批量上传知识文档
- 使用合适的 `chunk_size`（推荐 500）
- 对于大文件，使用 OCR 时设置合适的 DPI

### 4. 规则管理

- 定期更新审查规则
- 根据实际业务调整规则严重程度
- 保留规则 ID 以便追踪

---

## 版本历史

### v2.0.0 (当前版本)
- ✅ 新增 MCP 协议支持
- ✅ 新增 OCR 扫描件处理
- ✅ 新增合规审查 Agent
- ✅ 新增稳定性审查接口
- ✅ 新增规则管理功能
- ✅ 增强 Java-Python 集成

### v1.0.0
- 基础审查功能
- 知识库检索
- 材料完整性检查
