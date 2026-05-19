"""
审查结果稳定性测试脚本
测试多次调用 Agent 对同一文档审查结果的一致性
"""

import requests
import json
import hashlib
from typing import Dict, Any


class StabilityTester:
    """稳定性测试器"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_data = {
            "project_name": "某取水项目",
            "applicant_name": "某某公司",
            "water_source": "地表水",
            "water_purpose": "工业用水",
            "application_period": "2024-01-01 至 2034-12-31",
            "water_volume": 1000,
            "project_volume": 800,  # 故意设置矛盾值
            "water_source_location": "饮用水水源保护区",  # 故意设置违规位置
            "third_party_statement": None  # 故意缺失
        }
    
    def run_test(self, iterations: int = 5) -> Dict[str, Any]:
        """
        运行稳定性测试
        
        Args:
            iterations: 测试次数
            
        Returns:
            测试结果统计
        """
        print(f"\n开始稳定性测试，迭代 {iterations} 次...")
        print("=" * 60)
        
        results = []
        statuses = []
        issue_counts = []
        
        for i in range(iterations):
            print(f"\n第 {i+1}/{iterations} 次测试...")
            
            try:
                # 调用审查接口
                response = requests.post(
                    f"{self.base_url}/api/review",
                    json={
                        "application_data": self.test_data,
                        "documents": ["application_form", "business_license"],
                        "check_type": "full"
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    results.append(result)
                    statuses.append(result["status"])
                    issue_counts.append(result["results"]["total_issues"])
                    
                    print(f"  状态：{result['status']}")
                    print(f"  问题数：{result['results']['total_issues']}")
                    print(f"  耗时：{response.elapsed.total_seconds():.3f}s")
                else:
                    print(f"  请求失败：{response.status_code}")
                    results.append(None)
            
            except Exception as e:
                print(f"  异常：{str(e)}")
                results.append(None)
        
        # 统计分析
        print("\n" + "=" * 60)
        print("测试结果统计:")
        
        # 状态一致性
        unique_statuses = set(statuses)
        status_consistency = len(unique_statuses) == 1
        
        print(f"\n1. 审查状态一致性:")
        print(f"   唯一状态数：{len(unique_statuses)}")
        print(f"   状态列表：{list(unique_statuses)}")
        print(f"   一致性：{'✓ 通过' if status_consistency else '✗ 不通过'}")
        
        # 问题数一致性
        unique_issue_counts = set(issue_counts)
        issue_count_consistency = len(unique_issue_counts) == 1
        
        print(f"\n2. 问题数量一致性:")
        print(f"   唯一问题数：{list(unique_issue_counts)}")
        print(f"   一致性：{'✓ 通过' if issue_count_consistency else '✗ 不通过'}")
        
        # 问题类型一致性
        if results[0]:
            issue_types = []
            for result in results:
                if result:
                    types = [issue["type"] for issue in result["issues"]]
                    issue_types.append(tuple(sorted(types)))
            
            unique_issue_types = set(issue_types)
            issue_type_consistency = len(unique_issue_types) == 1
            
            print(f"\n3. 问题类型一致性:")
            print(f"   唯一类型组合数：{len(unique_issue_types)}")
            print(f"   一致性：{'✓ 通过' if issue_type_consistency else '✗ 不通过'}")
        
        # 建议一致性
        if results[0]:
            recommendation_hashes = []
            for result in results:
                if result:
                    recs = sorted(result.get("recommendations", []))
                    hash_val = hashlib.md5(str(recs).encode()).hexdigest()
                    recommendation_hashes.append(hash_val)
            
            unique_recs = set(recommendation_hashes)
            rec_consistency = len(unique_recs) == 1
            
            print(f"\n4. 修改建议一致性:")
            print(f"   唯一建议组合数：{len(unique_recs)}")
            print(f"   一致性：{'✓ 通过' if rec_consistency else '✗ 不通过'}")
        
        # 总体评估
        all_consistent = (
            status_consistency and 
            issue_count_consistency and 
            issue_type_consistency and 
            rec_consistency
        )
        
        print("\n" + "=" * 60)
        print(f"总体评估：{'✓ 通过 - 审查结果稳定' if all_consistent else '✗ 不通过 - 审查结果不稳定'}")
        print("=" * 60)
        
        return {
            "total_iterations": iterations,
            "successful_calls": len([r for r in results if r]),
            "status_consistency": status_consistency,
            "issue_count_consistency": issue_count_consistency,
            "issue_type_consistency": issue_type_consistency,
            "recommendation_consistency": rec_consistency,
            "overall_pass": all_consistent
        }
    
    def test_stable_endpoint(self, iterations: int = 3) -> Dict[str, Any]:
        """
        测试稳定性专用接口（使用固定随机种子）
        
        Args:
            iterations: 测试次数
            
        Returns:
            测试结果
        """
        print(f"\n测试稳定性专用接口 (/api/review/stable)...")
        print("=" * 60)
        
        results = []
        
        for i in range(iterations):
            print(f"\n第 {i+1}/{iterations} 次测试...")
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/review/stable",
                    json={
                        "application_data": self.test_data,
                        "documents": [],
                        "check_type": "compliance"
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    results.append(result)
                    
                    print(f"  状态：{result['status']}")
                    print(f"  问题数：{result['results']['total_issues']}")
                else:
                    print(f"  请求失败：{response.status_code}")
            
            except Exception as e:
                print(f"  异常：{str(e)}")
        
        # 检查结果一致性
        if len(results) >= 2:
            consistent = all(
                results[i]["status"] == results[0]["status"] and
                results[i]["results"]["total_issues"] == results[0]["results"]["total_issues"]
                for i in range(1, len(results))
            )
            
            print(f"\n稳定性专用接口一致性：{'✓ 通过' if consistent else '✗ 不通过'}")
            
            return {"consistent": consistent, "results": results}
        
        return {"consistent": False, "results": results}


if __name__ == "__main__":
    tester = StabilityTester()
    
    # 测试普通接口
    result = tester.run_test(iterations=5)
    
    # 测试稳定性接口
    stable_result = tester.test_stable_endpoint(iterations=3)
    
    # 输出结果
    print("\n\n最终测试结果:")
    print(f"普通接口稳定性：{'✓ 通过' if result['overall_pass'] else '✗ 不通过'}")
    print(f"稳定性接口一致性：{'✓ 通过' if stable_result.get('consistent') else '✗ 不通过'}")
