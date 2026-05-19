"""
Python AI 服务 - 知识库版本
支持 PDF/Word 解析、向量化存储、语义检索、MCP 服务

运行方式：python main_knowledge.py
"""

import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import os
import sys

from document_parser import DocumentParser, DocumentChunker
from vector_db import VectorDatabase

PORT = 8003

# 初始化组件
parser = DocumentParser()
chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
db = VectorDatabase()


class KnowledgeHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP 请求处理器"""
    
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/health':
            self.send_json_response({
                'status': 'healthy',
                'service': 'water-approval-ai-knowledge',
                'timestamp': datetime.now().isoformat(),
                'port': PORT
            })
        
        elif parsed_path.path == '/api/knowledge/stats':
            stats = db.get_stats()
            sources = db.list_sources()
            self.send_json_response({
                'stats': stats,
                'sources': sources
            })
        
        elif parsed_path.path.startswith('/api/knowledge/search'):
            query_params = parse_qs(parsed_path.query)
            query = query_params.get('query', [''])[0]
            top_k = int(query_params.get('top_k', [5])[0])
            min_similarity = float(query_params.get('min_similarity', [0.5])[0])
            
            if not query:
                self.send_error_response(400, "缺少查询参数：query")
                return
            
            results = db.search(query, top_k=top_k, min_similarity=min_similarity)
            self.send_json_response({
                'query': query,
                'results': results,
                'count': len(results)
            })
        
        else:
            self.send_error_response(404, "接口不存在")
    
    def do_POST(self):
        """处理 POST 请求"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error_response(400, "无效的 JSON 数据")
            return
        
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/knowledge/upload':
            self.handle_upload(data)
        
        elif parsed_path.path == '/api/knowledge/search':
            query = data.get('query', '')
            top_k = data.get('top_k', 5)
            min_similarity = data.get('min_similarity', 0.5)
            
            if not query:
                self.send_error_response(400, "缺少查询参数：query")
                return
            
            results = db.search(query, top_k=top_k, min_similarity=min_similarity)
            self.send_json_response({
                'query': query,
                'results': results,
                'count': len(results)
            })
        
        elif parsed_path.path == '/api/knowledge/delete':
            source = data.get('source', '')
            if not source:
                self.send_error_response(400, "缺少参数：source")
                return
            
            count = db.delete_by_source(source)
            self.send_json_response({
                'deleted': count,
                'source': source
            })
        
        else:
            self.send_error_response(404, "接口不存在")
    
    def handle_upload(self, data: dict):
        """处理文档上传"""
        file_path = data.get('file_path')
        chunk_size = data.get('chunk_size', 500)
        
        if not file_path:
            self.send_error_response(400, "缺少参数：file_path")
            return
        
        try:
            # 解析文档
            parsed = parser.parse_file(file_path)
            
            # 分块
            metadata = {
                'source': parsed['filename'],
                'format': parsed['format'],
                'upload_time': datetime.now().isoformat()
            }
            
            chunks = chunker.chunk_text(parsed['content'], metadata)
            
            # 添加到向量数据库
            result = db.add_documents(chunks)
            
            self.send_json_response({
                'success': True,
                'filename': parsed['filename'],
                'format': parsed['format'],
                'pages': parsed['pages'],
                'chunks': len(chunks),
                'added': result['added']
            })
        
        except Exception as e:
            self.send_error_response(500, f"上传失败：{str(e)}")
    
    def send_json_response(self, data: dict, status: int = 200):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def send_error_response(self, status: int, message: str):
        """发送错误响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = json.dumps({
            'error': message,
            'status': status
        }, ensure_ascii=False, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def main():
    """主函数"""
    print("=" * 60)
    print("Python AI 服务 - 知识库版本")
    print("=" * 60)
    print()
    print(f"服务启动在端口：{PORT}")
    print()
    print("可用接口:")
    print(f"  GET  /api/health              - 健康检查")
    print(f"  GET  /api/knowledge/stats     - 知识库统计")
    print(f"  GET  /api/knowledge/search    - 知识检索 (query, top_k, min_similarity)")
    print(f"  POST /api/knowledge/search    - 知识检索 (JSON: query, top_k, min_similarity)")
    print(f"  POST /api/knowledge/upload    - 文档上传 (JSON: file_path, chunk_size)")
    print(f"  POST /api/knowledge/delete    - 删除文档 (JSON: source)")
    print()
    print("MCP 服务:")
    print("  python mcp_service.py")
    print()
    print("=" * 60)
    print()
    
    # 启动服务器
    with socketserver.TCPServer(("", PORT), KnowledgeHandler) as httpd:
        try:
            print(f"Serving at port {PORT}")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务已停止")


if __name__ == "__main__":
    main()
