# PyCharm 运行指南

本文档说明如何在 PyCharm 中运行所有功能演示脚本。

---

## 📁 项目结构

```
water-approval-agent/
├── python-ai-service/              # Python AI 服务
│   ├── demo_feature_1_simple.py    # 功能 1 演示（简化版）
│   ├── demo_feature_1_parsing.py   # 功能 1 演示（完整版）
│   ├── demo_feature_2_chunking.py  # 功能 2 演示
│   ├── demo_feature_3_vector.py    # 功能 3 演示
│   ├── demo_feature_4_search.py    # 功能 4 演示
│   ├── demo_all_features.py        # 全部功能演示
│   ├── document_parser.py          # 文档解析器
│   ├── vector_db.py                # 向量数据库
│   ├── mcp_service.py              # MCP 服务
│   └── ...
├── java-backend/                   # Java 后端
└── docs/                           # 文档
```

---

## 🔧 PyCharm 配置步骤

### 步骤 1：打开项目

1. 启动 PyCharm
2. 点击 `File` → `Open`
3. 选择项目目录：`c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\python-ai-service`
4. 点击 `OK`

### 步骤 2：配置 Python 解释器

1. 点击 `File` → `Settings` (Windows) 或 `PyCharm` → `Preferences` (Mac)
2. 导航到 `Project: python-ai-service` → `Python Interpreter`
3. 点击右上角的齿轮图标 ⚙️
4. 选择 `Add...` 或 `Add Local...`
5. 选择已有的虚拟环境或创建新的虚拟环境
6. 点击 `OK`

### 步骤 3：安装依赖

打开 PyCharm 的 Terminal（终端），运行：

```bash
pip install -r requirements.txt
```

如果没有 requirements.txt，运行：

```bash
pip install PyPDF2 pdfplumber python-docx sentence-transformers chromadb langchain openai mcp
```

### 步骤 4：配置运行脚本

#### 方法 1：直接运行（推荐）

1. 在项目视图中找到演示脚本（如 `demo_feature_1_simple.py`）
2. 右键点击文件
3. 选择 `Run 'demo_feature_1_simple'`
4. 或使用快捷键：`Shift + F10`

#### 方法 2：创建运行配置

1. 点击右上角的运行配置下拉框（通常显示 `Add Configuration...`）
2. 选择 `Edit Configurations...`
3. 点击左上角的 `+` 号
4. 选择 `Python`
5. 配置以下参数：
   - **Name**: `功能 1 - 文档解析`
   - **Script path**: 选择 `demo_feature_1_simple.py`
   - **Working directory**: 选择 `python-ai-service` 目录
   - **Python interpreter**: 选择已配置的解释器
6. 点击 `Apply` 和 `OK`

---

## 🎯 演示脚本运行顺序

### 方案 A：逐个功能演示（推荐用于答辩）

1. **功能 1：PDF/Word 文档解析**
   - 运行：`demo_feature_1_simple.py`
   - 说明：展示文档解析器的结构和使用

2. **功能 2：文档分块处理**
   - 运行：`demo_feature_2_chunking.py`（待创建）
   - 说明：展示智能分块和重叠处理

3. **功能 3：向量化存储**
   - 运行：`demo_feature_3_vector.py`（待创建）
   - 说明：展示 HuggingFace 模型向量化

4. **功能 4：语义检索**
   - 运行：`demo_feature_4_search.py`（待创建）
   - 说明：展示相似度搜索

5. **功能 5：MCP 服务启动**
   - 运行：`mcp_service.py`
   - 说明：展示 MCP 协议和工具列表

6. **功能 6-7：工具调用演示**
   - 运行：`demo_mcp_tools.py`（待创建）
   - 说明：展示 knowledge_search 和 check_completeness

### 方案 B：一键演示全部功能

- 运行：`demo_all_features.py`
- 说明：自动演示所有功能点

---

## 💻 PyCharm 运行技巧

### 1. 使用运行工具窗口

- 运行脚本后，可以在底部的 `Run` 工具窗口查看输出
- 使用 `Ctrl+F` 在输出中搜索关键信息
- 使用 `Export to Text File` 保存运行结果

### 2. 使用调试模式

1. 在代码行号旁边点击，设置断点（红色圆点）
2. 右键点击文件
3. 选择 `Debug '脚本名'`
4. 可以逐步执行代码，查看变量值

### 3. 多脚本同时运行

1. 为每个脚本创建独立的运行配置
2. 可以依次运行多个配置
3. 每个配置会在单独的终端中运行

### 4. 使用 Terminal 运行

在 PyCharm 底部的 Terminal 中，可以直接运行：

```bash
# 切换到 python-ai-service 目录
cd python-ai-service

# 运行演示脚本
python demo_feature_1_simple.py
python demo_all_features.py
```

---

## 🔍 常见问题解决

### 问题 1：找不到模块

**错误**：`ModuleNotFoundError: No module named 'xxx'`

**解决**：
```bash
pip install <模块名>
```

或在 PyCharm 中：
1. 将鼠标悬停在报错的导入语句上
2. 点击 `Install package <模块名>`

### 问题 2：编码错误

**错误**：`UnicodeEncodeError: 'gbk' codec can't encode character`

**解决**：
1. 点击 `File` → `Settings`
2. 导航到 `Editor` → `File Encodings`
3. 设置：
   - `Global Encoding`: UTF-8
   - `Project Encoding`: UTF-8
   - `Default encoding for properties files`: UTF-8

### 问题 3：工作目录错误

**错误**：`FileNotFoundError: [Errno 2] No such file or directory`

**解决**：
1. 右键点击运行配置
2. 选择 `Edit Configurations...`
3. 确保 `Working directory` 设置为 `python-ai-service` 目录

### 问题 4：依赖冲突

**解决**：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 重新安装依赖
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📋 答辩时的 PyCharm 准备

### 1. 预先打开所有演示脚本

- 在 PyCharm 中打开所有要演示的脚本
- 使用标签页切换，方便快速访问

### 2. 创建运行配置集合

为每个演示创建运行配置：
- `Demo 1 - 文档解析`
- `Demo 2 - 文档分块`
- `Demo 3 - 向量化`
- `Demo 4 - 语义检索`
- `Demo 5 - MCP 服务`
- `Demo 6 - 工具调用`

### 3. 设置运行顺序

按照答辩流程依次运行配置

### 4. 准备备用方案

- 导出运行结果为文本文件
- 准备截图或录屏

---

## 🎬 答辩演示流程（PyCharm 版）

### 开场（1 分钟）

1. 展示 PyCharm 项目结构
2. 说明技术栈：Python + Java 双栈架构

### 功能演示（8 分钟）

#### 第 1 分钟：文档解析
- 打开 `demo_feature_1_simple.py`
- 右键 → Run
- 讲解输出内容

#### 第 2 分钟：文档分块
- 打开 `demo_feature_2_chunking.py`
- 右键 → Run
- 说明分块策略

#### 第 3 分钟：向量化
- 打开 `demo_feature_3_vector.py`
- 右键 → Run
- 展示 HuggingFace 模型

#### 第 4 分钟：语义检索
- 打开 `demo_feature_4_search.py`
- 右键 → Run
- 展示相似度结果

#### 第 5 分钟：MCP 服务
- 打开 `mcp_service.py`
- 右键 → Run
- 展示工具列表

#### 第 6-8 分钟：工具调用
- 打开 `demo_mcp_tools.py`
- 右键 → Run
- 演示 knowledge_search 和 check_completeness

### 总结（1 分钟）

- 打开 `README.md`
- 总结所有实现的功能
- 强调创新点

---

## ✅ 检查清单

演示前确认：
- [ ] PyCharm 已安装并配置好
- [ ] Python 解释器已配置
- [ ] 所有依赖已安装
- [ ] 所有演示脚本可以运行
- [ ] 运行配置已创建
- [ ] 项目编码设置为 UTF-8
- [ ] 工作目录设置正确
- [ ] 已测试所有脚本可以正常运行

---

## 📚 相关文档

- `docs/功能演示指南.md` - 详细演示步骤
- `docs/评分点对应说明.md` - 评分点对照
- `docs/部署说明.md` - 部署指南

---

**祝演示顺利！** 🎉
