"""
系统集成测试脚本
测试 Java-Python 双栈集成、MCP 工具调用、文档处理等功能
"""

import requests
import json
import os
from typing import Dict, Any


class IntegrationTester:
    """集成测试器"""
    
    def __init__(self, python_url: str = "http://localhost:8000", java_url: str = "http://localhost:8080"):
        self.python_url = python_url
        self.java_url = java_url
        self.test_results = []
    
    def test_python_health(self) -> bool:
        """测试 Python 服务健康检查"""
        print("\n[测试 1/8] Python AI 服务健康检查...")
        try:
            response = requests.get(f"{self.python_url}/api/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✓ Python 服务正常：{data.get('service')} v{data.get('version')}")
                return True
            else:
                print(f"  ✗ 响应状态码：{response.status_code}")
                return False
        except Exception as e:
            print(f"  ✗ 连接失败：{str(e)}")
            return False
    
    def test_java_health(self) -> bool:
        """测试 Java 服务健康检查"""
        print("\n[测试 2/8] Java 后端健康检查...")
        try:
            response = requests.get(f"{self.java_url}/api/health", timeout=5)
            if response.status_code == 200:
                print(f"  ✓ Java 后端正常")
                return True
            else:
                print(f"  ✗ 响应状态码：{response.status_code}")
                return False
        except Exception as e:
            print(f"  ✗ 连接失败：{str(e)}")
            return False
    
    def test_mcp_knowledge_search(self) -> bool:
        """测试 MCP 知识检索工具"""
        print("\n[测试 3/8] MCP 知识检索工具...")
        try:
            response = requests.post(
                f"{self.python_url}/api/mcp/tools",
                json={
                    "tool_name": "knowledge_search",
                    "parameters": {
                        "query": "取水许可申请需要什么材料？",
                        "top_k": 3
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    print(f"  ✓ MCP 知识检索工具正常")
                    return True
            
            print(f"  ✗ 工具调用失败")
            return False
        
        except Exception as e:
            print(f"  ✗ 异常：{str(e)}")
            return False
    
    def test_mcp_check_completeness(self) -> bool:
        """测试 MCP 材料完整性检查工具"""
        print("\n[测试 4/8] MCP 材料完整性检查...")
        try:
            response = requests.post(
                f"{self.python_url}/api/mcp/tools",
                json={
                    "tool_name": "check_completeness",
                    "parameters": {
                        "submitted_documents": ["申请书", "身份证明", "水资源论证报告"],
                        "check_type": "required"
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success" or "tool" in data:
                    result = data.get("result", data)
                    missing_count = len(result.get("missing", []))
                    print(f"  ✓ MCP 材料检查工具正常 (缺失 {missing_count} 项)")
                    return True
            
            print(f"  ✗ 工具调用失败")
            return False
        
        except Exception as e:
            print(f"  ✗ 异常：{str(e)}")
            return False
    
    def test_review_endpoint(self) -> bool:
        """测试审查接口"""
        print("\n[测试 5/8] Python AI 审查接口...")
        try:
            test_data = {
                "application_data": {
                    "project_name": "测试项目",
                    "applicant_name": "测试单位",
                    "water_source": "地表水",
                    "water_purpose": "工业用水",
                    "application_period": "2024-01-01 至 2034-12-31",
                    "water_volume": 1000
                },
                "documents": ["application_form"],
                "check_type": "full"
            }
            
            response = requests.post(
                f"{self.python_url}/api/review",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✓ 审查接口正常 (状态：{result.get('status')}, 问题数：{result.get('results', {}).get('total_issues')})")
                return True
            else:
                print(f"  ✗ 响应状态码：{response.status_code}")
                return False
        
        except Exception as e:
            print(f"  ✗ 异常：{str(e)}")
            return False
    
    def test_java_python_integration(self) -> bool:
        """测试 Java-Python 集成"""
        print("\n[测试 6/8] Java-Python 集成测试...")
        try:
            test_data = {
                "applicationData": {
                    "project_name": "Java 集成测试项目",
                    "applicant_name": "测试单位",
                    "water_source": "地表水",
                    "water_purpose": "工业用水",
                    "application_period": "2024-01-01 至 2034-12-31",
                    "water_volume": 1000
                },
                "documents": [],
                "checkType": "full"
            }
            
            response = requests.post(
                f"{self.java_url}/api/review",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✓ Java-Python 集成正常 (状态：{result.get('status')})")
                return True
            elif response.status_code == 500:
                print(f"  ⚠ Java 后端可用，但 AI 审查失败（可能 Python 服务未启动）")
                return False
            else:
                print(f"  ✗ 响应状态码：{response.status_code}")
                return False
        
        except Exception as e:
            print(f"  ✗ 异常：{str(e)}")
            return False
    
    def test_knowledge_upload(self) -> bool:
        """测试知识库上传"""
        print("\n[测试 7/8] 知识库上传功能...")
        try:
            # 创建测试文件
            test_content = """
            《中华人民共和国水法》
            第三十三条 在饮用水水源保护区内，禁止设置排污口。
            第四十八条 直接从江河、湖泊或者地下取用水资源的单位和个人，
            应当按照国家取水许可制度和水资源有偿使用制度的规定，
            向水行政主管部门或者流域管理机构申请领取取水许可证，并缴纳水资源费。
            """
            
            test_file = "test_knowledge.txt"
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_content)
            
            with open(test_file, "rb") as f:
                response = requests.post(
                    f"{self.python_url}/api/knowledge/upload",
                    files={"file": f},
                    timeout=10
                )
            
            os.remove(test_file)
            
            if response.status_code == 200:
                print(f"  ✓ 知识库上传功能正常")
                return True
            else:
                print(f"  ✗ 响应状态码：{response.status_code}")
                return False
        
        except Exception as e:
            print(f"  ✗ 异常：{str(e)}")
            return False
    
    def test_rules_management(self) -> bool:
        """测试规则管理"""
        print("\n[测试 8/8] 合规规则管理...")
        try:
            # 获取规则列表
            response = requests.get(f"{self.python_url}/api/rules/list", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                rules_count = len(data.get("rules", []))
                print(f"  ✓ 规则管理功能正常 (当前规则数：{rules_count})")
                return True
            else:
                print(f"  ✗ 响应状态码：{response.status_code}")
                return False
        
        except Exception as e:
            print(f"  ✗ 异常：{str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("=" * 60)
        print("系统集成测试")
        print("=" * 60)
        
        tests = [
            ("Python 服务健康", self.test_python_health),
            ("Java 服务健康", self.test_java_health),
            ("MCP 知识检索", self.test_mcp_knowledge_search),
            ("MCP 材料检查", self.test_mcp_check_completeness),
            ("AI 审查接口", self.test_review_endpoint),
            ("Java-Python 集成", self.test_java_python_integration),
            ("知识库上传", self.test_knowledge_upload),
            ("规则管理", self.test_rules_management)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                passed = test_func()
                results.append({"name": test_name, "passed": passed})
            except Exception as e:
                print(f"  ✗ 测试异常：{str(e)}")
                results.append({"name": test_name, "passed": False})
        
        # 统计结果
        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        
        print("\n" + "=" * 60)
        print(f"测试结果：{passed}/{total} 通过")
        print("=" * 60)
        
        for result in results:
            status = "✓" if result["passed"] else "✗"
            print(f"{status} {result['name']}")
        
        return {
            "total": total,
            "passed": passed,
            "success_rate": passed / total if total > 0 else 0,
            "results": results
        }


if __name__ == "__main__":
    tester = IntegrationTester()
    result = tester.run_all_tests()
    
    print("\n\n测试总结:")
    if result["success_rate"] >= 0.8:
        print("✓ 系统集成测试通过，系统可以正常运行")
    elif result["success_rate"] >= 0.5:
        print("⚠ 部分功能正常，需要检查未通过的项目")
    else:
        print("✗ 系统集成测试失败，请检查服务状态")
    
    # 退出码
    exit(0 if result["success_rate"] >= 0.8 else 1)
