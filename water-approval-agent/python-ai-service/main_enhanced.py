"""
Python AI 服务 - 增强版
整合 MCP、OCR、合规审查 Agent、知识库等功能
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
import json
import hashlib

# 导入服务模块
from src.services.compliance_agent import ComplianceReviewAgent
from src.tools.ocr_tool import OCRProcessor
from src.tools.mcp_tools import MCPToolExecutor
from vector_db import VectorDatabase
from document_parser import DocumentParser, DocumentChunker

app = FastAPI(title="涉水审批 AI 服务", version="2.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
compliance_agent = None
ocr_processor = OCRProcessor(lang='chi_sim+eng')
vector_db = VectorDatabase()
doc_parser = DocumentParser()
doc_chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
mcp_executor = MCPToolExecutor(vector_db)

# 上传目录
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ReviewRequest(BaseModel):
    """审查请求模型"""
    application_data: Dict[str, Any]
    documents: Optional[List[str]] = []
    check_type: str = "full"  # full, completeness, compliance
    is_scan: bool = False  # 是否为扫描件


class ReviewResponse(BaseModel):
    """审查响应模型"""
    status: str
    results: Dict[str, Any]
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    knowledge_references: Optional[List[Dict]] = []


class KnowledgeQuery(BaseModel):
    """知识查询模型"""
    query: str
    top_k: int = 5


class RuleUpdate(BaseModel):
    """规则更新模型"""
    rules: List[Dict[str, Any]]


@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    global compliance_agent
    print("初始化合规审查 Agent...")
    compliance_agent = ComplianceReviewAgent(vector_db)
    print("✓ 服务初始化完成")


@app.post("/api/review", response_model=ReviewResponse)
async def review_application(request: ReviewRequest):
    """
    审查涉水申请材料
    
    支持：
    1. 形式审查（完整性检查）
    2. 内容规范性检查
    3. 实质合规性检查（基于 Agent 和 RAG）
    4. OCR 扫描件处理
    """
    issues = []
    recommendations = []
    knowledge_refs = []
    
    # 1. 处理扫描件（OCR）
    if request.is_scan:
        print("处理扫描件...")
        # OCR 处理逻辑将在文件上传接口中处理
    
    # 2. 形式审查 - 完整性检查
    if request.check_type in ["full", "completeness"]:
        required_fields = [
            "project_name", "applicant_name", "water_source",
            "water_purpose", "application_period", "water_volume"
        ]
        
        for field in required_fields:
            if field not in request.application_data or not request.application_data[field]:
                issues.append({
                    "type": "completeness",
                    "severity": "high",
                    "field": field,
                    "message": f"缺少必填字段：{field}"
                })
                recommendations.append(f"请补充{field}字段信息")
        
        # 检查必需文档
        required_docs = ["application_form", "business_license", "water_resource_report"]
        for doc in required_docs:
            if doc not in request.documents:
                issues.append({
                    "type": "completeness",
                    "severity": "high",
                    "document": doc,
                    "message": f"缺少必需文档：{doc}"
                })
                recommendations.append(f"请上传{doc}文档")
    
    # 3. 内容规范性检查
    if request.check_type in ["full", "content"]:
        # 检查取水量逻辑
        if "water_volume" in request.application_data and "project_volume" in request.application_data:
            app_volume = float(request.application_data["water_volume"])
            proj_volume = float(request.application_data["project_volume"])
            if app_volume > proj_volume * 1.2:
                issues.append({
                    "type": "content",
                    "severity": "high",
                    "field": "water_volume",
                    "message": "申请取水量超过项目可研报告测算用水量的 20%"
                })
                recommendations.append("请核实申请取水量的合理性")
    
    # 4. 实质合规性检查（使用 Agent）
    if request.check_type in ["full", "compliance"] and compliance_agent:
        print("执行 Agent 合规审查...")
        agent_result = compliance_agent.review(
            application_data=request.application_data,
            documents=request.documents
        )
        
        # 合并 Agent 审查结果
        for issue in agent_result.get('issues', []):
            issues.append({
                "type": "compliance",
                "severity": issue.get('severity', 'medium'),
                "rule": issue.get('rule'),
                "message": issue.get('description')
            })
        
        recommendations.extend(agent_result.get('recommendations', []))
        knowledge_refs = agent_result.get('knowledge_references', [])
    
    # 5. 确定审查状态
    status = "passed" if len(issues) == 0 else "failed"
    if len(issues) <= 2 and all(i.get("severity") == "low" for i in issues):
        status = "warning"
    
    return ReviewResponse(
        status=status,
        results={
            "check_type": request.check_type,
            "total_issues": len(issues),
            "critical_issues": len([i for i in issues if i.get("severity") == "high"]),
            "warning_issues": len([i for i in issues if i.get("severity") == "medium"]),
            "info_issues": len([i for i in issues if i.get("severity") == "low"])
        },
        issues=issues,
        recommendations=recommendations,
        knowledge_references=knowledge_refs
    )


@app.post("/api/review/stable", response_model=ReviewResponse)
async def review_application_stable(request: ReviewRequest):
    """
    稳定性审查接口
    使用固定随机种子，确保多次调用结果一致
    """
    # 设置随机种子确保稳定性
    import random
    random.seed(42)
    
    # 调用审查接口
    return await review_application(request)


@app.post("/api/upload", response_model=Dict[str, Any])
async def upload_file(
    file: UploadFile = File(...),
    is_scan: bool = False,
    process_type: str = "parse"  # parse, ocr, both
):
    """
    上传并处理文件
    
    支持：
    - PDF/Word 文档解析
    - 扫描件 OCR 识别
    - 自动存入知识库
    """
    try:
        # 保存文件
        file_content = await file.read()
        file_hash = hashlib.md5(file_content).hexdigest()
        file_path = os.path.join(UPLOAD_DIR, f"{file_hash}_{file.filename}")
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        result = {
            "filename": file.filename,
            "file_path": file_path,
            "file_hash": file_hash
        }
        
        # 处理文件
        if process_type in ["parse", "both"]:
            # 文档解析
            parsed = doc_parser.parse_file(file_path)
            result["parsed"] = {
                "content_length": len(parsed["content"]),
                "pages": parsed["pages"],
                "format": parsed["format"]
            }
            
            # 分块并存储
            metadata = {"source": file.filename, "format": parsed["format"]}
            chunks = doc_chunker.chunk_text(parsed["content"], metadata)
            
            if chunks:
                db_result = vector_db.add_documents(chunks)
                result["stored"] = db_result
        
        if process_type in ["ocr", "both"] or is_scan:
            # OCR 处理
            file_ext = os.path.splitext(file.filename)[1].lower()
            if file_ext in ['.pdf', '.jpg', '.jpeg', '.png']:
                try:
                    if file_ext == '.pdf':
                        ocr_result = ocr_processor.extract_text_from_pdf(file_path)
                    else:
                        ocr_result = ocr_processor.extract_text_from_image(file_path)
                    
                    result["ocr"] = {
                        "text_length": len(ocr_result["text"]),
                        "confidence": ocr_result.get("confidence", 0)
                    }
                except Exception as e:
                    result["ocr_error"] = str(e)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败：{str(e)}")


@app.post("/api/knowledge/search")
async def search_knowledge(query: KnowledgeQuery):
    """搜索知识库"""
    try:
        results = vector_db.search(query.query, top_k=query.top_k)
        return {
            "status": "success",
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败：{str(e)}")


@app.post("/api/knowledge/upload")
async def upload_knowledge(file: UploadFile = File(...)):
    """上传知识文档到向量库"""
    try:
        # 保存文件
        file_content = await file.read()
        file_hash = hashlib.md5(file_content).hexdigest()
        file_path = os.path.join(UPLOAD_DIR, f"knowledge_{file_hash}_{file.filename}")
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # 解析文档
        parsed = doc_parser.parse_file(file_path)
        
        # 分块
        metadata = {"source": file.filename, "format": parsed["format"]}
        chunks = doc_chunker.chunk_text(parsed["content"], metadata)
        
        # 存储到向量库
        if chunks:
            result = vector_db.add_documents(chunks)
            return {
                "status": "success",
                "message": f"文档上传成功",
                "chunks_added": result["added"]
            }
        
        return {"status": "success", "message": "文档解析成功，但无内容可存储"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败：{str(e)}")


@app.post("/api/knowledge/stats")
async def get_knowledge_stats():
    """获取知识库统计信息"""
    try:
        stats = vector_db.get_stats()
        sources = vector_db.list_sources()
        return {
            "status": "success",
            "data": {
                "total_documents": stats["total_documents"],
                "collection_name": stats["collection_name"],
                "sources": sources,
                "source_count": len(sources)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计失败：{str(e)}")


@app.post("/api/mcp/tools")
async def mcp_tool_call(tool_name: str, parameters: Dict[str, Any]):
    """MCP 工具调用接口"""
    try:
        result = await mcp_executor.execute(tool_name, parameters)
        return {
            "status": "success",
            "tool": tool_name,
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "tool": tool_name,
            "error": str(e)
        }


@app.post("/api/rules/update")
async def update_rules(request: RuleUpdate):
    """更新合规审查规则"""
    if not compliance_agent:
        raise HTTPException(status_code=500, detail="Agent 未初始化")
    
    try:
        success = compliance_agent.update_rules(request.rules)
        if success:
            return {
                "status": "success",
                "message": f"规则更新成功",
                "rules_count": len(compliance_agent.review_rules)
            }
        else:
            raise HTTPException(status_code=500, detail="规则更新失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新失败：{str(e)}")


@app.get("/api/rules/list")
async def list_rules():
    """获取合规审查规则列表"""
    if not compliance_agent:
        return {"rules": []}
    
    return {
        "status": "success",
        "rules": compliance_agent.review_rules,
        "count": len(compliance_agent.review_rules)
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "water-approval-ai",
        "version": "2.0.0",
        "components": {
            "compliance_agent": compliance_agent is not None,
            "ocr_processor": True,
            "vector_db": True,
            "mcp_executor": True
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main_enhanced:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
