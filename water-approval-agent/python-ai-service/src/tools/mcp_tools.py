"""
MCP 工具执行器
提供 MCP 工具调用的统一接口
"""

from typing import List, Dict, Any
from vector_db import VectorDatabase
from document_parser import DocumentParser, DocumentChunker


class MCPToolExecutor:
    """MCP 工具执行器"""
    
    def __init__(self, vector_db: VectorDatabase):
        """
        初始化工具执行器
        
        Args:
            vector_db: 向量数据库实例
        """
        self.vector_db = vector_db
        self.parser = DocumentParser()
        self.chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
        
        # 申请材料检查清单
        self.checklist = {
            'required': [
                '申请书',
                '身份证明（营业执照/组织机构代码证）',
                '水资源论证报告',
                '取水工程可行性研究报告',
                '水源地水质监测报告',
                '取水口位置图',
                '用水计划方案',
                '节水措施方案',
                '第三者利害关系说明'
            ],
            'optional': [
                '环境影响评价报告',
                '水土保持方案',
                '应急预案',
                '取水设施设计图纸'
            ]
        }
    
    async def execute(self, tool_name: str, parameters: Dict[str, Any]) -> Dict:
        """
        执行 MCP 工具
        
        Args:
            tool_name: 工具名称
            parameters: 工具参数
            
        Returns:
            工具执行结果
        """
        if tool_name == "knowledge_search":
            return await self.knowledge_search(
                query=parameters.get("query", ""),
                top_k=parameters.get("top_k", 5),
                min_similarity=parameters.get("min_similarity", 0.5)
            )
        
        elif tool_name == "check_completeness":
            return await self.check_completeness(
                submitted_documents=parameters.get("submitted_documents", []),
                check_type=parameters.get("check_type", "required")
            )
        
        elif tool_name == "upload_document":
            return await self.upload_document(
                file_path=parameters.get("file_path", ""),
                chunk_size=parameters.get("chunk_size", 500)
            )
        
        elif tool_name == "get_knowledge_stats":
            return await self.get_knowledge_stats()
        
        else:
            return {"error": f"未知工具：{tool_name}"}
    
    async def knowledge_search(self, query: str, top_k: int = 5, min_similarity: float = 0.5) -> Dict:
        """
        知识检索工具
        
        Args:
            query: 查询语句
            top_k: 返回结果数量
            min_similarity: 最小相似度
            
        Returns:
            检索结果
        """
        try:
            results = self.vector_db.search(query, top_k=top_k, min_similarity=min_similarity)
            
            return {
                "tool": "knowledge_search",
                "query": query,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            return {"error": f"知识检索失败：{str(e)}"}
    
    async def check_completeness(self, submitted_documents: List[str], check_type: str = "required") -> Dict:
        """
        材料完整性检查工具
        
        Args:
            submitted_documents: 已提交材料列表
            check_type: 检查类型 (required/all)
            
        Returns:
            检查结果
        """
        try:
            # 标准化材料名称
            submitted_set = set(doc.strip() for doc in submitted_documents)
            
            # 确定检查清单
            if check_type == "required":
                checklist = self.checklist['required']
            else:
                checklist = self.checklist['required'] + self.checklist['optional']
            
            # 检查
            missing = []
            provided = []
            
            for doc in checklist:
                found = False
                for submitted in submitted_set:
                    if doc in submitted or submitted in doc:
                        found = True
                        break
                
                if found:
                    provided.append(doc)
                else:
                    missing.append(doc)
            
            completeness = (len(provided) / len(checklist)) * 100 if checklist else 0
            
            return {
                "tool": "check_completeness",
                "check_type": check_type,
                "submitted_count": len(submitted_set),
                "required_count": len(checklist),
                "provided": provided,
                "missing": missing,
                "completeness": completeness,
                "is_complete": len(missing) == 0
            }
        
        except Exception as e:
            return {"error": f"材料检查失败：{str(e)}"}
    
    async def upload_document(self, file_path: str, chunk_size: int = 500) -> Dict:
        """
        文档上传工具
        
        Args:
            file_path: 文件路径
            chunk_size: 分块大小
            
        Returns:
            上传结果
        """
        try:
            # 解析文档
            parsed = self.parser.parse_file(file_path)
            
            # 分块
            metadata = {
                'source': parsed['filename'],
                'format': parsed['format']
            }
            
            chunks = self.chunker.chunk_text(parsed['content'], metadata)
            
            # 添加到向量数据库
            result = self.vector_db.add_documents(chunks)
            
            return {
                "tool": "upload_document",
                "filename": parsed['filename'],
                "format": parsed['format'],
                "pages": parsed['pages'],
                "chunks_created": len(chunks),
                "chunks_added": result['added']
            }
        
        except Exception as e:
            return {"error": f"文档上传失败：{str(e)}"}
    
    async def get_knowledge_stats(self) -> Dict:
        """
        获取知识库统计信息
        
        Returns:
            统计信息
        """
        try:
            stats = self.vector_db.get_stats()
            sources = self.vector_db.list_sources()
            
            return {
                "tool": "get_knowledge_stats",
                "total_documents": stats['total_documents'],
                "collection_name": stats['collection_name'],
                "sources": sources,
                "source_count": len(sources)
            }
        
        except Exception as e:
            return {"error": f"获取统计失败：{str(e)}"}
