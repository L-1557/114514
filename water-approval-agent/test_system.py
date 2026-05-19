"""
测试脚本 - 验证系统功能
"""

import requests
import json

# 测试Python AI服务
def test_python_service():
    print("=== 测试Python AI服务 ===")
    
    # 健康检查
    response = requests.get("http://localhost:8000/api/health")
    print(f"健康检查: {response.json()}")
    
    # 测试审查接口
    test_data = {
        "application_data": {
            "project_name": "测试取水项目",
            "applicant_name": "测试申请人",
            "water_source": "某河流",
            "water_purpose": "工业用水",
            "application_period": "2024-01-01至2025-12-31",
            "water_volume": 10000,
            "water_source_location": "某市某区"
        },
        "documents": ["application_form", "business_license"],
        "check_type": "full"
    }
    
    response = requests.post(
        "http://localhost:8000/api/review",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"审查结果: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

# 测试Java后端
def test_java_backend():
    print("\n=== 测试Java后端 ===")
    
    # 健康检查
    response = requests.get("http://localhost:8080/api/health")
    print(f"健康检查: {response.text}")

if __name__ == "__main__":
    try:
        test_python_service()
    except Exception as e:
        print(f"Python服务测试失败: {e}")
    
    try:
        test_java_backend()
    except Exception as e:
        print(f"Java后端测试失败: {e}")
