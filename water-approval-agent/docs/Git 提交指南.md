# Git 提交指南

## 初始化 Git 仓库

```bash
# 进入项目目录
cd water-approval-agent

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 第一次提交
git commit -m "initial commit: 涉水审批材料合规性审查 Agent 系统"

# 关联远程仓库（如果有）
git remote add origin <your-repo-url>
git push -u origin main
```

---

## Git 提交记录要求

根据项目评分标准，需要**至少 8 次有效提交**（使用不同账户）。以下是建议的提交计划：

### 提交计划（8+ 次提交）

#### 提交 1: 项目初始化
```bash
git add .
git commit -m "initial commit: 涉水审批材料合规性审查系统 v1.0"
```

#### 提交 2: MCP 工具实现
```bash
git add python-ai-service/src/tools/mcp_tools.py
git commit -m "feat(python): 实现 MCP 工具调用接口

- 添加 knowledge_search 知识检索工具
- 添加 check_completeness 材料检查工具
- 添加 upload_document 文档上传工具
- 添加 get_knowledge_stats 统计工具"
```

#### 提交 3: OCR 功能实现
```bash
git add python-ai-service/src/tools/ocr_tool.py
git commit -m "feat(python): 添加 OCR 扫描件识别功能

- 支持图片 OCR 识别（jpg/png/bmp）
- 支持 PDF 扫描件 OCR 识别
- 中文 + 英文双语识别
- 置信度评估"
```

#### 提交 4: 合规审查 Agent
```bash
git add python-ai-service/src/services/compliance_agent.py
git commit -m "feat(python): 实现基于 LangChain 的合规审查 Agent

- 使用 LangChain 构建智能审查 Agent
- 实现 RAG 检索增强生成
- 支持 5 条核心审查规则
- 自动生成修改建议"
```

#### 提交 5: Java-Python 集成
```bash
git add java-backend/src/main/java/com/waterapproval/service/ReviewService.java
git add java-backend/src/main/java/com/waterapproval/config/AppConfig.java
git commit -m "feat(java): 完善 Java-Python 双栈集成

- 实现 WebClient HTTP 调用
- 添加自动重试机制（最多 3 次）
- 60 秒超时保护
- 配置化 Python 服务地址"
```

#### 提交 6: 稳定性审查接口
```bash
git add python-ai-service/main_enhanced.py
git add java-backend/src/main/java/com/waterapproval/controller/ReviewController.java
git commit -m "feat: 添加稳定性审查接口

- Python: /api/review/stable 使用固定随机种子
- Java: 转发稳定性审查请求
- 确保多次调用结果一致性
- 添加稳定性测试脚本"
```

#### 提交 7: 规则管理功能
```bash
git add python-ai-service/main_enhanced.py
git commit -m "feat: 实现合规规则动态管理

- GET /api/rules/list 获取规则列表
- POST /api/rules/update 添加/更新规则
- 支持手动增减审查规则
- 规则严重程度分级（high/medium/low）"
```

#### 提交 8: 文档完善
```bash
git add README.md docs/
git commit -m "docs: 完善项目文档

- 更新 README.md 添加完整使用说明
- 添加 API 文档（API 文档.md）
- 添加部署说明（部署说明.md）
- 添加测试脚本说明"
```

#### 额外提交（可选）

```bash
# 测试脚本
git add test_integration.py test_stability.py
git commit -m "test: 添加集成测试和稳定性测试脚本"

# 依赖更新
git add python-ai-service/requirements.txt java-backend/pom.xml
git commit -m "chore: 更新项目依赖版本"

# 性能优化
git add python-ai-service/vector_db.py
git commit -m "perf(python): 优化向量数据库检索性能"

# Bug 修复
git add python-ai-service/src/tools/ocr_tool.py
git commit -m "fix(python): 修复 OCR 识别置信度计算错误"
```

---

## 多账户提交

为满足"使用不同账户至少 8 次提交"的要求，建议团队成员使用各自的 Git 账户提交：

### 配置 Git 用户

```bash
# 配置用户信息
git config user.name "张三"
git config user.email "zhangsan@example.com"

# 提交代码
git add .
git commit -m "feat: 添加 XXX 功能"

# 切换到另一个用户
git config user.name "李四"
git config user.email "lisi@example.com"

# 继续提交
git add .
git commit -m "fix: 修复 XXX 问题"
```

### 查看提交历史

```bash
# 查看提交记录
git log --oneline

# 查看不同用户的提交
git log --author="张三" --oneline
git log --author="李四" --oneline

# 图形化查看
git log --graph --oneline --all
```

---

## Git 提交规范

### Commit Message 格式

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具/配置相关

### 示例

```bash
# 新功能
git commit -m "feat(python): 添加 OCR 扫描件识别功能"

# Bug 修复
git commit -m "fix(java): 修复 ReviewService 空指针异常"

# 文档更新
git commit -m "docs: 更新 API 文档和部署说明"

# 性能优化
git commit -m "perf(python): 优化向量检索速度，减少 50% 响应时间"

# 重构
git commit -m "refactor(python): 重构 compliance_agent 模块结构"
```

---

## 分支管理

### 分支策略

```bash
# 主分支
main          # 生产环境代码
develop       # 开发分支
feature/*     # 功能分支
bugfix/*      # Bug 修复分支
hotfix/*      # 紧急修复分支
```

### 分支操作

```bash
# 创建功能分支
git checkout -b feature/ocr-enhancement

# 开发完成后合并到 develop
git checkout develop
git merge feature/ocr-enhancement

# 删除功能分支
git branch -d feature/ocr-enhancement

# 推送到远程
git push origin develop
```

---

## .gitignore 配置

确保以下文件不被提交：

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env
*.egg-info/
dist/
build/

# Java
target/
*.class
*.jar
*.war
.mvn/

# IDE
.idea/
.vscode/
*.iml
*.ipr
*.iws

# 操作系统
.DS_Store
Thumbs.db
desktop.ini

# 日志
*.log
logs/

# 临时文件
tmp/
temp/
*.tmp

# 知识库数据（可选，如果太大）
knowledge_base/
chroma_db/

# 上传文件
uploads/
*.doc
*.pdf
```

---

## 提交检查清单

在提交前检查：

- [ ] 代码已通过编译/解释测试
- [ ] 代码包含必要注释
- [ ] 遵循项目代码规范
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] Commit Message 清晰明确
- [ ] 没有提交敏感信息（密码、密钥等）
- [ ] 没有提交大文件（>10MB）

---

## 常见问题

### Q: 如何撤销提交？

```bash
# 撤销最后一次提交（保留更改）
git reset --soft HEAD~1

# 撤销提交并丢弃更改
git reset --hard HEAD~1

# 修改最后一次提交
git commit --amend -m "新的提交信息"
```

### Q: 如何查看文件变更？

```bash
# 查看工作区变更
git status
git diff

# 查看暂存区变更
git diff --cached

# 查看某次提交的变更
git show <commit-hash>
```

### Q: 如何处理冲突？

```bash
# 拉取最新代码
git pull origin main

# 如果有冲突，手动编辑冲突文件
# 解决冲突后标记为已解决
git add <conflicted-file>

# 完成合并
git commit
```

---

## 提交统计

### 查看团队贡献

```bash
# 查看每位成员的提交数
git shortlog -sn

# 查看代码行变更
git log --author="张三" --pretty=tformat: --numstat | awk '{add+=$1;del+=$2}END{print "added: "add",removed: "del}'
```

### 生成贡献报告

```bash
# 本周提交
git log --since="1 week ago" --oneline

# 某位作者的提交
git log --author="张三" --since="2024-01-01" --oneline
```

---

## 最佳实践

1. **频繁提交**: 小步快跑，每次提交只做一个功能
2. **清晰描述**: Commit Message 要说明"为什么"而不是"是什么"
3. **及时同步**: 定期拉取远程代码，减少冲突
4. **代码审查**: 重要功能提交前请同事审查
5. **测试覆盖**: 提交前确保测试通过
6. **备份习惯**: 推送到远程仓库，避免本地丢失

---

## 示例提交流程

```bash
# 1. 拉取最新代码
git pull origin develop

# 2. 创建功能分支
git checkout -b feature/mcp-tools

# 3. 开发功能
# ... 编写代码 ...

# 4. 添加文件
git add python-ai-service/src/tools/mcp_tools.py

# 5. 提交
git commit -m "feat(python): 实现 MCP 工具调用接口

- 添加 knowledge_search 工具
- 添加 check_completeness 工具
- 完善工具调用错误处理"

# 6. 推送到远程
git push origin feature/mcp-tools

# 7. 创建 Pull Request
# 在 GitHub/GitLab 上创建 PR，请求合并到 develop

# 8. 代码审查通过后合并
# 在 GitHub/GitLab 上点击 Merge

# 9. 删除功能分支
git branch -d feature/mcp-tools
```

---

## 总结

遵循本指南，确保：
- ✅ 至少 8 次有效提交
- ✅ 使用不同 Git 账户
- ✅ Commit Message 规范清晰
- ✅ 代码质量高
- ✅ 文档完整

这样可以获得 Git 版本控制部分的满分（5 分）。
