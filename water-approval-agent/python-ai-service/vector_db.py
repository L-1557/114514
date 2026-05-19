"""
向量数据库模块 - 使用 ChromaDB 和 Sentence Transformers
"""

import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import hashlib
import json


class VectorDatabase:
    """向量数据库"""
    
    def __init__(self, persist_directory: str = "./chroma_db", embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """
        初始化向量数据库
        
        Args:
            persist_directory: 持久化目录
            embedding_model: 嵌入模型名称
        """
        self.persist_directory = persist_directory
        
        # 创建持久化客户端
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        
        # 加载嵌入模型（支持中文的多语言模型）
        print(f"加载嵌入模型：{embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        print("嵌入模型加载完成")
        
        # 知识库集合
        self.collection = None
        self._get_or_create_collection("knowledge_base")
    
    def _get_or_create_collection(self, name: str):
        """获取或创建集合"""
        try:
            self.collection = self.client.get_collection(name=name)
            print(f"使用现有集合：{name}")
        except Exception:
            self.collection = self.client.create_collection(name=name)
            print(f"创建新集合：{name}")
    
    def _generate_id(self, text: str, metadata: Dict) -> str:
        """生成唯一 ID"""
        content = text + json.dumps(metadata, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()
    
    def add_documents(self, documents: List[Dict]) -> Dict:
        """
        添加文档到向量数据库
        
        Args:
            documents: 文档列表
                [
                    {
                        'text': 文本内容，
                        'metadata': {
                            'source': 来源文件，
                            'chunk_id': 块 ID,
                            'page': 页码，
                            ...
                        }
                    }
                ]
        
        Returns:
            {
                'added': 添加数量，
                'ids': 添加的 ID 列表
            }
        """
        if not documents:
            return {'added': 0, 'ids': []}
        
        texts = [doc['text'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        ids = [self._generate_id(doc['text'], doc['metadata']) for doc in documents]
        
        # 生成嵌入向量
        print(f"正在为 {len(texts)} 个文档块生成嵌入向量...")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        
        # 添加到数据库
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"成功添加 {len(ids)} 个文档块")
        
        return {
            'added': len(ids),
            'ids': ids
        }
    
    def search(self, query: str, top_k: int = 5, min_similarity: float = 0.5) -> List[Dict]:
        """
        语义检索
        
        Args:
            query: 查询语句
            top_k: 返回结果数量
            min_similarity: 最小相似度阈值
            
        Returns:
            [
                {
                    'text': 文档内容，
                    'metadata': 元数据，
                    'similarity': 相似度分数，
                    'source': 来源文件，
                    'page': 页码
                }
            ]
        """
        # 生成查询向量
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
        
        # 检索
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k * 2  # 多获取一些，后面过滤
        )
        
        # 处理结果
        formatted_results = []
        
        if results and len(results['ids']) > 0:
            for i in range(len(results['ids'][0])):
                similarity = results['distances'][0][i] if 'distances' in results else 0.0
                # ChromaDB 返回的是距离，转换为相似度
                similarity = 1.0 / (1.0 + similarity)
                
                if similarity >= min_similarity:
                    formatted_results.append({
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'similarity': float(similarity),
                        'source': results['metadatas'][0][i].get('source', '未知'),
                        'page': results['metadatas'][0][i].get('page', None),
                        'chunk_id': results['metadatas'][0][i].get('chunk_id', None)
                    })
        
        # 按相似度排序
        formatted_results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return formatted_results[:top_k]
    
    def delete_by_source(self, source: str) -> int:
        """
        根据来源文件删除文档
        
        Args:
            source: 来源文件名
            
        Returns:
            删除的文档数量
        """
        # 获取所有文档
        all_docs = self.collection.get()
        
        # 找到匹配的 ID
        ids_to_delete = []
        for i, metadata in enumerate(all_docs['metadatas']):
            if metadata.get('source') == source:
                ids_to_delete.append(all_docs['ids'][i])
        
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
            print(f"删除了 {len(ids_to_delete)} 个文档块（来源：{source}）")
        
        return len(ids_to_delete)
    
    def get_stats(self) -> Dict:
        """获取数据库统计信息"""
        count = self.collection.count()
        return {
            'total_documents': count,
            'collection_name': self.collection.name
        }
    
    def list_sources(self) -> List[str]:
        """列出所有来源文件"""
        all_docs = self.collection.get()
        sources = set()
        for metadata in all_docs['metadatas']:
            if 'source' in metadata:
                sources.add(metadata['source'])
        return sorted(list(sources))


if __name__ == "__main__":
    # 测试代码
    db = VectorDatabase()
    
    # 测试添加
    test_docs = [
        {
            'text': '取水许可申请需要提交申请书、身份证明、水资源论证报告等材料。',
            'metadata': {'source': 'test.pdf', 'chunk_id': '0', 'page': 1}
        },
        {
            'text': '取水许可审批时限为 20 个工作日，特殊情况可延长 10 日。',
            'metadata': {'source': 'test.pdf', 'chunk_id': '1', 'page': 1}
        }
    ]
    
    result = db.add_documents(test_docs)
    print(f"添加结果：{result}")
    
    # 测试检索
    query = "申请取水许可需要什么材料？"
    results = db.search(query, top_k=3)
    
    print(f"\n查询：{query}")
    print(f"找到 {len(results)} 个相关结果\n")
    
    for i, r in enumerate(results, 1):
        print(f"{i}. 相似度：{r['similarity']:.3f}")
        print(f"   来源：{r['source']}")
        print(f"   内容：{r['text'][:100]}...")
        print()
