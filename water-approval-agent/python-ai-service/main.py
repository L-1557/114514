"""
Python AI 服务后端 - 涉水审批材料合规性审查系统
简化版本 - 无需复杂依赖
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
import json

app = FastAPI(title="涉水审批 AI 服务", version="1.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewRequest(BaseModel):
    """审查请求模型"""
    application_data: Dict[str, Any]
    documents: Optional[List[str]] = []
    check_type: str = "full"  # full, completeness, compliance

class ReviewResponse(BaseModel):
    """审查响应模型"""
    status: str
    results: Dict[str, Any]
    issues: List[Dict[str, Any]]
    recommendations: List[str]

class KnowledgeQuery(BaseModel):
    """知识查询模型"""
    query: str
    top_k: int = 5

@app.post("/api/review", response_model=ReviewResponse)
async def review_application(request: ReviewRequest):
    """审查涉水申请材料"""
    issues = []
    recommendations = []
    
    # 1. 形式审查 - 完整性检查
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
    
    # 2. 内容规范性检查
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
    
    # 3. 实质合规性检查
    if request.check_type in ["full", "compliance"]:
        # 检查取水许可期限
        if "application_period" in request.application_data and "project_approval_period" in request.application_data:
            app_period = request.application_data["application_period"]
            proj_period = request.application_data["project_approval_period"]
            if str(app_period) > str(proj_period):
                issues.append({
                    "type": "compliance",
                    "severity": "medium",
                    "field": "application_period",
                    "message": "申请取水许可期限可能超过项目批准期限"
                })
                recommendations.append("请核实取水许可期限是否合理")
    
    # 确定审查状态
    status = "passed" if len(issues) == 0 else "failed"
    if len(issues) <= 2 and all(i.get("severity") == "low" for i in issues):
        status = "warning"
    
    return ReviewResponse(
        status=status,
        results={
            "check_type": request.check_type,
            "total_issues": len(issues),
            "critical_issues": len([i for i in issues if i["severity"] == "high"]),
            "warning_issues": len([i for i in issues if i["severity"] == "medium"]),
            "info_issues": len([i for i in issues if i["severity"] == "low"])
        },
        issues=issues,
        recommendations=recommendations
    )

@app.post("/api/knowledge/search")
async def search_knowledge(query: KnowledgeQuery):
    """搜索知识库 - 模拟实现"""
    results = [
        {
            "content": "《中华人民共和国水法》第三十三条规定：在饮用水水源保护区内，禁止设置排污口。",
            "source": "中华人民共和国水法",
            "article": "第三十三条",
            "relevance": 0.95
        },
        {
            "content": "《取水许可和水资源费征收管理条例》第十一条：取水许可申请应当附具建设项目水资源论证报告书。",
            "source": "取水许可和水资源费征收管理条例",
            "article": "第十一条",
            "relevance": 0.88
        }
    ]
    return {"status": "success", "results": results}

@app.post("/api/knowledge/upload")
async def upload_knowledge(file: UploadFile = File(...)):
    """上传知识文档 - 简化实现"""
    return {"status": "success", "message": f"文档 {file.filename} 已接收"}

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "water-approval-ai"}

@app.post("/api/mcp/tools")
async def mcp_tool_call(tool_name: str, parameters: Dict[str, Any]):
    """MCP 工具调用接口"""
    if tool_name == "knowledge_search":
        result = {
            "tool": "knowledge_search",
            "result": [
                {"content": "《水法》规定：在饮用水水源保护区内禁止设置排污口", "source": "水法"}
            ]
        }
    elif tool_name == "check_completeness":
        result = {
            "tool": "check_completeness",
            "result": {"status": "complete", "message": "材料完整"}
        }
    else:
        result = {"error": f"未知工具：{tool_name}"}
    
    return {"status": "success", "result": result}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
