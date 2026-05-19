"""
Agent服务 - 使用LangChain Agent实现合规性审查
"""

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any
import os
from src.tools.mcp_tools import MCPTools
from src.services.knowledge_service import KnowledgeService

class AgentService:
    """Agent服务类"""
    
    def __init__(self):
        self.llm = None
        self.agent = None
        self.tools = []
        self.knowledge_service = None
        
    async def initialize(self):
        """初始化Agent服务"""
        # 初始化LLM
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=os.getenv("OPENAI_API_KEY", "your-api-key"),
            temperature=0.1
        )
        
        # 初始化知识库服务
        self.knowledge_service = KnowledgeService()
        await self.knowledge_service.initialize()
        
        # 初始化MCP工具
        mcp_tools = MCPTools()
        self.tools = mcp_tools.get_tools()
        
        # 初始化Agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        
        print("Agent服务初始化完成")
    
    async def review_application(
        self,
        application_data: Dict[str, Any],
        documents: List[str],
        check_type: str = "full"
    ) -> Dict[str, Any]:
        """审查涉水申请材料"""
        try:
            issues = []
            recommendations = []
            
            # 1. 形式审查 - 完整性检查
            if check_type in ["full", "completeness"]:
                completeness_result = await self._check_completeness(application_data, documents)
                issues.extend(completeness_result.get("issues", []))
                recommendations.extend(completeness_result.get("recommendations", []))
            
            # 2. 内容规范性检查
            if check_type in ["full", "content"]:
                content_result = await self._check_content_norm(application_data)
                issues.extend(content_result.get("issues", []))
                recommendations.extend(content_result.get("recommendations", []))
            
            # 3. 实质合规性检查
            if check_type in ["full", "compliance"]:
                compliance_result = await self._check_compliance(application_data)
                issues.extend(compliance_result.get("issues", []))
                recommendations.extend(compliance_result.get("recommendations", []))
            
            # 确定审查状态
            status = "passed" if len(issues) == 0 else "failed"
            if len(issues) <= 2 and any(i["severity"] == "low" for i in issues):
                status = "warning"
            
            return {
                "status": status,
                "results": {
                    "check_type": check_type,
                    "total_issues": len(issues),
                    "critical_issues": len([i for i in issues if i["severity"] == "high"]),
                    "warning_issues": len([i for i in issues if i["severity"] == "medium"]),
                    "info_issues": len([i for i in issues if i["severity"] == "low"])
                },
                "issues": issues,
                "recommendations": recommendations
            }
        except Exception as e:
            raise Exception(f"审查失败: {str(e)}")
    
    async def _check_completeness(self, application_data: Dict[str, Any], documents: List[str]) -> Dict[str, Any]:
        """检查申请材料完整性"""
        issues = []
        recommendations = []
        
        # 检查必需字段
        required_fields = [
            "project_name", "applicant_name", "water_source",
            "water_purpose", "application_period", "water_volume"
        ]
        
        for field in required_fields:
            if field not in application_data or not application_data[field]:
                issues.append({
                    "type": "completeness",
                    "severity": "high",
                    "field": field,
                    "message": f"缺少必填字段: {field}"
                })
                recommendations.append(f"请补充{field}字段信息")
        
        # 检查必需文档
        required_docs = ["application_form", "business_license", "water_resource_report"]
        for doc in required_docs:
            if doc not in documents:
                issues.append({
                    "type": "completeness",
                    "severity": "high",
                    "document": doc,
                    "message": f"缺少必需文档: {doc}"
                })
                recommendations.append(f"请上传{doc}文档")
        
        return {"issues": issues, "recommendations": recommendations}
    
    async def _check_content_norm(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查内容规范性"""
        issues = []
        recommendations = []
        
        # 检查取水地点
        if "water_source" in application_data:
            water_source = application_data["water_source"]
            if not water_source or len(water_source.strip()) == 0:
                issues.append({
                    "type": "content",
                    "severity": "medium",
                    "field": "water_source",
                    "message": "取水地点信息为空或格式不正确"
                })
        
        # 检查取水量逻辑
        if "water_volume" in application_data and "project_volume" in application_data:
            app_volume = float(application_data["water_volume"])
            proj_volume = float(application_data["project_volume"])
            if app_volume > proj_volume * 1.2:  # 允许20%的误差
                issues.append({
                    "type": "content",
                    "severity": "high",
                    "field": "water_volume",
                    "message": "申请取水量超过项目可研报告测算用水量的20%"
                })
                recommendations.append("请核实申请取水量的合理性")
        
        return {"issues": issues, "recommendations": recommendations}
    
    async def _check_compliance(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查实质合规性"""
        issues = []
        recommendations = []
        
        # 使用知识库检索检查选址合规性
        if "water_source_location" in application_data:
            location = application_data["water_source_location"]
            
            # 查询知识库中的法规信息
            query = f"取水口位置限制 {location} 饮用水源保护区 自然保护区"
            search_results = await self._search_knowledge(query)
            
            # 检查是否存在违规情况
            for result in search_results:
                content = result.get("content", "").lower()
                if any(keyword in content for keyword in ["禁止取水", "限制取水", "保护区"]):
                    issues.append({
                        "type": "compliance",
                        "severity": "high",
                        "field": "water_source_location",
                        "message": f"取水口位置可能位于限制或禁止取水区域: {location}",
                        "reference": result.get("metadata", {}).get("source", "")
                    })
                    recommendations.append("请核实取水口位置是否符合相关法规要求")
                    break
        
        # 检查取水许可期限
        if "application_period" in application_data and "project_approval_period" in application_data:
            app_period = application_data["application_period"]
            proj_period = application_data["project_approval_period"]
            
            # 简单比较（实际应用中需要解析日期）
            if str(app_period) > str(proj_period):
                issues.append({
                    "type": "compliance",
                    "severity": "medium",
                    "field": "application_period",
                    "message": "申请取水许可期限可能超过项目批准期限"
                })
                recommendations.append("请核实取水许可期限是否合理")
        
        return {"issues": issues, "recommendations": recommendations}
    
    async def _search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """搜索知识库"""
        try:
            results = await self.knowledge_service.search(query, top_k=5)
            return results
        except Exception as e:
            print(f"知识库搜索失败: {str(e)}")
            return []
