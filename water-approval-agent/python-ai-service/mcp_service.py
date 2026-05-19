"""
MCP 服务 - 知识库工具
提供 knowledge_search 和 check_completeness 工具
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio

from vector_db import VectorDatabase
from document_parser import DocumentParser, DocumentChunker


# 初始化服务
server = Server("water-approval-knowledge")

# 初始化组件
db = VectorDatabase()
parser = DocumentParser()
chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)

# 申请材料检查清单
CHECKLIST = {
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


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出可用的 MCP 工具"""
    return [
        Tool(
            name="knowledge_search",
            description="搜索知识库中的法规、政策、办事指南等信息。接收查询语句，返回相关文档片段，包含内容、来源、相似度分数。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "查询语句，例如：'取水许可申请需要什么材料？'"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "返回结果数量，默认 5",
                        "default": 5
                    },
                    "min_similarity": {
                        "type": "number",
                        "description": "最小相似度阈值，默认 0.5",
                        "default": 0.5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="check_completeness",
            description="检查申请材料是否完整。接收申请材料列表，对照检查清单返回缺失项和已具备项。",
            inputSchema={
                "type": "object",
                "properties": {
                    "submitted_documents": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "已提交的申请材料列表，例如：['申请书', '身份证明', '水资源论证报告']"
                    },
                    "check_type": {
                        "type": "string",
                        "description": "检查类型：required(仅必需), all(全部)",
                        "enum": ["required", "all"],
                        "default": "required"
                    }
                },
                "required": ["submitted_documents"]
            }
        ),
        Tool(
            name="upload_document",
            description="上传文档到知识库。接收文件路径，解析并存入向量数据库。",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文档文件路径，支持 PDF 和 Word 格式"
                    },
                    "chunk_size": {
                        "type": "integer",
                        "description": "分块大小，默认 500",
                        "default": 500
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="get_knowledge_stats",
            description="获取知识库统计信息，包括文档数量、来源列表等。",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """调用 MCP 工具"""
    
    try:
        if name == "knowledge_search":
            return await knowledge_search(
                query=arguments.get("query"),
                top_k=arguments.get("top_k", 5),
                min_similarity=arguments.get("min_similarity", 0.5)
            )
        
        elif name == "check_completeness":
            return await check_completeness(
                submitted_documents=arguments.get("submitted_documents", []),
                check_type=arguments.get("check_type", "required")
            )
        
        elif name == "upload_document":
            return await upload_document(
                file_path=arguments.get("file_path"),
                chunk_size=arguments.get("chunk_size", 500)
            )
        
        elif name == "get_knowledge_stats":
            return await get_knowledge_stats()
        
        else:
            return [TextContent(type="text", text=f"未知工具：{name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"工具调用失败：{str(e)}")]


async def knowledge_search(query: str, top_k: int = 5, min_similarity: float = 0.5) -> List[TextContent]:
    """
    知识检索工具
    
    Args:
        query: 查询语句
        top_k: 返回结果数量
        min_similarity: 最小相似度
        
    Returns:
        检索结果列表
    """
    print(f"\n[知识检索] 查询：{query}")
    
    # 检索
    results = db.search(query, top_k=top_k, min_similarity=min_similarity)
    
    if not results:
        return [TextContent(
            type="text",
            text=f"未找到相关文档。查询：{query}"
        )]
    
    # 格式化结果
    output = f"找到 {len(results)} 个相关文档片段：\n\n"
    
    for i, result in enumerate(results, 1):
        output += f"[{i}] 相似度：{result['similarity']:.3f}\n"
        output += f"    来源：{result['source']}"
        if result.get('page'):
            output += f" (第{result['page']}页)"
        output += f"\n    内容：{result['text']}\n\n"
    
    return [TextContent(type="text", text=output)]


async def check_completeness(submitted_documents: List[str], check_type: str = "required") -> List[TextContent]:
    """
    材料完整性检查工具
    
    Args:
        submitted_documents: 已提交的材料列表
        check_type: 检查类型
        
    Returns:
        检查结果
    """
    print(f"\n[材料检查] 已提交：{len(submitted_documents)} 个材料")
    
    # 标准化材料名称（去除空格、统一大小写）
    submitted_set = set(doc.strip() for doc in submitted_documents)
    
    # 确定检查清单
    if check_type == "required":
        checklist = CHECKLIST['required']
    else:
        checklist = CHECKLIST['required'] + CHECKLIST['optional']
    
    # 检查
    missing = []
    provided = []
    
    for doc in checklist:
        # 模糊匹配
        found = False
        for submitted in submitted_set:
            if doc in submitted or submitted in doc:
                found = True
                break
        
        if found:
            provided.append(doc)
        else:
            missing.append(doc)
    
    # 生成报告
    output = f"材料完整性检查报告\n"
    output += f"{'='*50}\n\n"
    output += f"检查类型：{'必需材料' if check_type == 'required' else '全部材料'}\n"
    output += f"已提交：{len(submitted_set)} 个\n"
    output += f"应提交：{len(checklist)} 个\n\n"
    
    output += f"✅ 已具备材料 ({len(provided)}/{len(checklist)}):\n"
    for doc in provided:
        output += f"   - {doc}\n"
    
    if missing:
        output += f"\n❌ 缺失材料 ({len(missing)}):\n"
        for doc in missing:
            output += f"   - {doc}\n"
        
        completeness = (len(provided) / len(checklist)) * 100
        output += f"\n完整度：{completeness:.1f}%\n"
        output += f"\n建议：请补充缺失的材料后再提交申请。"
    else:
        output += f"\n✅ 材料齐全，可以提交申请！\n"
    
    return [TextContent(type="text", text=output)]


async def upload_document(file_path: str, chunk_size: int = 500) -> List[TextContent]:
    """
    文档上传工具
    
    Args:
        file_path: 文件路径
        chunk_size: 分块大小
        
    Returns:
        上传结果
    """
    print(f"\n[文档上传] 文件：{file_path}")
    
    try:
        # 解析文档
        parsed = parser.parse_file(file_path)
        print(f"解析成功：{parsed['filename']} ({parsed['pages']} 页)")
        
        # 分块
        metadata = {
            'source': parsed['filename'],
            'format': parsed['format'],
            'upload_time': str(asyncio.get_event_loop().time())
        }
        
        chunks = chunker.chunk_text(parsed['content'], metadata)
        print(f"分块完成：{len(chunks)} 个块")
        
        # 添加到向量数据库
        result = db.add_documents(chunks)
        
        output = f"文档上传成功\n"
        output += f"{'='*50}\n"
        output += f"文件名：{parsed['filename']}\n"
        output += f"格式：{parsed['format']}\n"
        output += f"页数/段落：{parsed['pages']}\n"
        output += f"分块数：{len(chunks)}\n"
        output += f"添加到数据库：{result['added']} 个\n"
        
        return [TextContent(type="text", text=output)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"文档上传失败：{str(e)}")]


async def get_knowledge_stats() -> List[TextContent]:
    """获取知识库统计信息"""
    stats = db.get_stats()
    sources = db.list_sources()
    
    output = f"知识库统计信息\n"
    output += f"{'='*50}\n"
    output += f"文档块总数：{stats['total_documents']}\n"
    output += f"集合名称：{stats['collection_name']}\n\n"
    output += f"来源文件列表 ({len(sources)}):\n"
    
    for source in sources:
        output += f"   - {source}\n"
    
    if not sources:
        output += f"   (暂无文档)\n"
    
    return [TextContent(type="text", text=output)]


async def main():
    """启动 MCP 服务"""
    print("启动 MCP 知识库服务...")
    print("可用工具:")
    print("  - knowledge_search: 知识检索")
    print("  - check_completeness: 材料检查")
    print("  - upload_document: 文档上传")
    print("  - get_knowledge_stats: 统计信息")
    print()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
