# PyCharm 快速启动指南

## ✅ 问题已解决

已修复的问题：
1. ✅ 导入错误：`from docx import Document`（不是 `python_docx`）
2. ✅ 依赖冲突：升级了 `huggingface_hub`, `transformers`, `sentence-transformers`
3. ✅ pip 损坏：使用 `python -m ensurepip` 修复
4. ✅ 版本兼容：使用稳定版本组合
   - huggingface_hub == 0.20.3
   - transformers == 4.36.0
   - sentence-transformers == 2.3.0

## 🚀 在 PyCharm 中运行

### 方法 1：直接运行（最简单）

1. 在 PyCharm 中打开项目
2. 找到文件：`run_all_demos.py`
3. 右键点击 → **Run 'run_all_demos'**
4. 查看输出结果

### 方法 2：配置虚拟环境解释器

1. **File** → **Settings** → **Project: python-ai-service** → **Python Interpreter**
2. 点击齿轮图标 ⚙️ → **Add...**
3. 选择 **Existing environment**
4. 浏览到：
   ```
   C:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\python-ai-service\.venv\Scripts\python.exe
   ```
5. 点击 **OK**

配置好后，直接右键运行任何 Python 脚本即可！

### 方法 3：使用 Terminal

在 PyCharm 底部的 Terminal 中运行：
```bash
.venv\Scripts\python.exe run_all_demos.py
```

## 📊 运行结果

所有 7 个功能演示成功：
```
功能演示 1: PDF/Word 文档解析        [OK] ✓
功能演示 2: 文档分块处理            [OK] ✓
功能演示 3: 向量化存储              [OK] ✓
功能演示 4: 语义检索                [OK] ✓
功能演示 5: MCP 服务启动            [OK] ✓
功能演示 6: knowledge_search 工具   [OK] ✓
功能演示 7: check_completeness 工具 [OK] ✓

演示总结
总演示数：7
成功：7
失败：0

[OK] 所有功能演示完成！
```

## 🔧 常用运行命令

### 运行所有演示
```bash
.venv\Scripts\python.exe run_all_demos.py
```

### 运行单个功能演示
```bash
.venv\Scripts\python.exe demo_feature_1_simple.py
```

### 运行完整功能演示
```bash
.venv\Scripts\python.exe demo_all_features.py
```

### 安装/更新依赖
```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 💡 PyCharm 技巧

### 1. 创建运行配置

1. 点击右上角的运行配置下拉框
2. 选择 **Edit Configurations...**
3. 点击 **+** 号 → 选择 **Python**
4. 配置：
   - **Name**: `所有功能演示`
   - **Script path**: 选择 `run_all_demos.py`
   - **Working directory**: 选择项目目录
   - **Python interpreter**: 选择 `.venv`
5. 点击 **OK**

### 2. 调试模式

1. 在代码行号旁点击设置断点（红色圆点）
2. 右键点击文件
3. 选择 **Debug '脚本名'**
4. 可以逐步执行，查看变量值

### 3. 查看运行结果

- 运行完成后在底部的 **Run** 窗口查看输出
- 使用 **Ctrl+F** 搜索关键词
- 右键 → **Export to Text File** 保存结果

## ⚠️ 常见问题

### 问题 1：ModuleNotFoundError

**解决**：
```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 问题 2：导入错误

**解决**：
检查导入语句是否正确：
- ✅ `from docx import Document`
- ❌ `from python_docx import Document`

### 问题 3：版本冲突

**解决**：
```bash
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install huggingface_hub==0.20.3 transformers==4.36.0 sentence-transformers==2.3.0
```

## 📋 答辩准备清单

演示前确认：
- [x] PyCharm 已安装
- [x] 虚拟环境已配置
- [x] 所有依赖已安装
- [x] 演示脚本可以运行
- [x] 已测试运行成功
- [x] 运行配置已创建（可选）

## 🎯 答辩演示流程

### 1. 打开 PyCharm（10 秒）
- 展示项目结构

### 2. 运行演示（2 分钟）
- 右键 `run_all_demos.py` → Run
- 边运行边讲解每个功能

### 3. 强调评分点（1 分钟）
- 指出每个功能对应的评分点
- 展示代码位置

### 4. 总结（30 秒）
- 所有 7 个功能演示成功
- 强调 7/7 全部通过

## 📚 相关文档

- `docs/功能演示指南.md` - 详细演示步骤
- `docs/评分点对应说明.md` - 评分点对照
- `docs/PyCharm 运行指南.md` - PyCharm 详细配置

---

**所有问题已解决，可以直接在 PyCharm 中运行！** 🎉
