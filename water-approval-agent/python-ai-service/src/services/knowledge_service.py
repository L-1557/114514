"""
知识库服务 - 使用ChromaDB实现文档向量化存储和检索
支持PDF、Word等非结构化文档的解析与处理
"""

import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_chroma import Chroma
import os
import uuid
from typing import List, Dict, Any
import tempfile

class KnowledgeService:
    """知识库服务类"""
    
    def __init__(self):
        self.chroma_client = None
        self.collection = None
        self.embeddings = None
        self.text_splitter = None
        self.knowledge_base_path = os.path.join(os.path.dirname(__file__), "..", "knowledge_base")
        
    async def initialize(self):
        """初始化知识库服务"""
        try:
            # 创建知识库目录
            os.makedirs(self.knowledge_base_path, exist_ok=True)
            
            # 初始化 Embedding 模型
            print("正在加载 Embedding 模型...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="shibing624/text2vec-base-chinese"
            )
            
            # 初始化文本分割器
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
            
            # 初始化 ChromaDB
            self.chroma_client = chromadb.PersistentClient(
                path=self.knowledge_base_path
            )
            
            # 获取或创建集合
            self.collection = self.chroma_client.get_or_create_collection(
                name="water_approval_knowledge",
                embedding_function=self.embeddings
            )
            
            print("知识库服务初始化完成")
        except Exception as e:
            print(f"知识库服务初始化失败：{e}")
            print("将使用简化模式运行")
    
    async def add_document(self, filename: str, content: bytes) -> Dict[str, Any]:
        """添加文档到知识库"""
        try:
            # 保存临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            # 根据文件类型加载文档
            documents = await self._load_document(tmp_path, filename)
            
            # 分割文本
            chunks = self.text_splitter.split_documents(documents)
            
            # 生成ID和内容
            ids = [str(uuid.uuid4()) for _ in chunks]
            texts = [doc.page_content for doc in chunks]
            metadatas = [{"source": filename, "chunk_index": i} for i, _ in enumerate(chunks)]
            
            # 添加到ChromaDB
            self.collection.add(
                documents=texts,
                ids=ids,
                metadatas=metadatas
            )
            
            # 清理临时文件
            os.unlink(tmp_path)
            
            return {
                "message": f"成功添加文档 {filename}",
                "chunks_count": len(chunks)
            }
        except Exception as e:
            raise Exception(f"添加文档失败: {str(e)}")
    
    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """搜索知识库"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            # 格式化结果
            formatted_results = []
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None
                })
            
            return formatted_results
        except Exception as e:
            raise Exception(f"搜索失败: {str(e)}")
    
    async def _load_document(self, file_path: str, filename: str):
        """根据文件类型加载文档"""
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext in [".docx", ".doc"]:
            loader = Docx2txtLoader(file_path)
        else:
            # 默认按文本处理
            with open(file_path, 'r', encoding='utf-8') as f:
                from langchain_core.documents import Document
                return [Document(page_content=f.read(), metadata={"source": filename})]
        
        return loader.load()
