"""
Python AI 服务后端 - 涉水审批材料合规性审查系统
极简版本 - 仅使用 Python 标准库
运行方式：python main_simple.py
"""

import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from datetime import datetime

PORT = 8003

class ReviewHandler(http.server.SimpleHTTPRequestHandler):
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
                "status": "healthy",
                "service": "water-approval-ai",
                "timestamp": datetime.now().isoformat()
            })
        else:
            self.send_error(404)
    
    def do_POST(self):
        """处理 POST 请求"""
        parsed_path = urlparse(self.path)
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_json_response({"error": "Invalid JSON"}, status=400)
            return
        
        if parsed_path.path == '/api/review':
            result = self.review_application(data)
            self.send_json_response(result)
        elif parsed_path.path == '/api/knowledge/search':
            result = self.search_knowledge(data.get('query', ''), data.get('top_k', 5))
            self.send_json_response({"status": "success", "results": result})
        elif parsed_path.path == '/api/mcp/tools':
            result = self.mcp_tool_call(data.get('tool_name', ''), data.get('parameters', {}))
            self.send_json_response(result)
        else:
            self.send_error(404)
    
    def send_json_response(self, data, status=200):
        """发送 JSON 响应"""
        response_body = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', len(response_body))
        self.end_headers()
        self.wfile.write(response_body)
    
    def review_application(self, request_data):
        """审查涉水申请材料"""
        issues = []
        recommendations = []
        
        application_data = request_data.get('application_data', {})
        documents = request_data.get('documents', [])
        check_type = request_data.get('check_type', 'full')
        
        # 1. 形式审查 - 完整性检查
        if check_type in ['full', 'completeness']:
            required_fields = [
                'project_name', 'applicant_name', 'water_source',
                'water_purpose', 'application_period', 'water_volume'
            ]
            
            for field in required_fields:
                if field not in application_data or not application_data[field]:
                    issues.append({
                        'type': 'completeness',
                        'severity': 'high',
                        'field': field,
                        'message': f'缺少必填字段：{field}'
                    })
                    recommendations.append(f'请补充{field}字段信息')
            
            # 检查必需文档
            required_docs = ['application_form', 'business_license', 'water_resource_report']
            for doc in required_docs:
                if doc not in documents:
                    issues.append({
                        'type': 'completeness',
                        'severity': 'high',
                        'document': doc,
                        'message': f'缺少必需文档：{doc}'
                    })
                    recommendations.append(f'请上传{doc}文档')
        
        # 2. 内容规范性检查
        if check_type in ['full', 'content']:
            # 检查取水量逻辑
            if 'water_volume' in application_data and 'project_volume' in application_data:
                try:
                    app_volume = float(application_data['water_volume'])
                    proj_volume = float(application_data['project_volume'])
                    if app_volume > proj_volume * 1.2:
                        issues.append({
                            'type': 'content',
                            'severity': 'high',
                            'field': 'water_volume',
                            'message': '申请取水量超过项目可研报告测算用水量的 20%'
                        })
                        recommendations.append('请核实申请取水量的合理性')
                except (ValueError, TypeError):
                    pass
        
        # 3. 实质合规性检查
        if check_type in ['full', 'compliance']:
            # 检查取水许可期限
            if 'application_period' in application_data and 'project_approval_period' in application_data:
                app_period = str(application_data['application_period'])
                proj_period = str(application_data['project_approval_period'])
                if app_period > proj_period:
                    issues.append({
                        'type': 'compliance',
                        'severity': 'medium',
                        'field': 'application_period',
                        'message': '申请取水许可期限可能超过项目批准期限'
                    })
                    recommendations.append('请核实取水许可期限是否合理')
        
        # 确定审查状态
        status = 'passed' if len(issues) == 0 else 'failed'
        
        return {
            'status': status,
            'results': {
                'check_type': check_type,
                'total_issues': len(issues),
                'critical_issues': len([i for i in issues if i['severity'] == 'high']),
                'warning_issues': len([i for i in issues if i['severity'] == 'medium']),
                'info_issues': len([i for i in issues if i['severity'] == 'low'])
            },
            'issues': issues,
            'recommendations': recommendations
        }
    
    def search_knowledge(self, query, top_k):
        """搜索知识库 - 模拟实现"""
        results = [
            {
                'content': '《中华人民共和国水法》第三十三条规定：在饮用水水源保护区内，禁止设置排污口。',
                'source': '中华人民共和国水法',
                'article': '第三十三条',
                'relevance': 0.95
            },
            {
                'content': '《取水许可和水资源费征收管理条例》第十一条：取水许可申请应当附具建设项目水资源论证报告书。',
                'source': '取水许可和水资源费征收管理条例',
                'article': '第十一条',
                'relevance': 0.88
            },
            {
                'content': '《河道管理条例》第二十五条：在河道管理范围内进行下列活动，必须报经河道主管机关批准。',
                'source': '河道管理条例',
                'article': '第二十五条',
                'relevance': 0.82
            }
        ]
        return results[:top_k]
    
    def mcp_tool_call(self, tool_name, parameters):
        """MCP 工具调用"""
        if tool_name == 'knowledge_search':
            result = {
                'tool': 'knowledge_search',
                'result': self.search_knowledge(parameters.get('query', ''), 5)
            }
        elif tool_name == 'check_completeness':
            # 简化实现
            result = {
                'tool': 'check_completeness',
                'result': {'status': 'complete', 'message': '材料完整'}
            }
        else:
            result = {'error': f'未知工具：{tool_name}'}
        
        return {'status': 'success', 'result': result}
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), ReviewHandler) as httpd:
        print(f"========================================")
        print(f"Python AI 服务已启动")
        print(f"服务地址：http://localhost:{PORT}")
        print(f"API 接口:")
        print(f"  GET  /api/health          - 健康检查")
        print(f"  POST /api/review          - 审查申请")
        print(f"  POST /api/knowledge/search - 知识搜索")
        print(f"  POST /api/mcp/tools       - MCP 工具调用")
        print(f"========================================")
        print(f"按 Ctrl+C 停止服务")
        print(f"========================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务已停止")
