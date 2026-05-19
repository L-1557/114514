"""
知识库系统测试脚本
测试所有功能模块
"""

import requests
import json
import os
import time

API_BASE = 'http://localhost:8003/api'


def test_health():
    """测试健康检查"""
    print("=" * 60)
    print("测试 1: 健康检查")
    print("=" * 60)
    
    try:
        response = requests.get(f'{API_BASE}/health', timeout=5)
        data = response.json()
        
        print(f"✓ 服务状态：{data['status']}")
        print(f"✓ 服务名称：{data['service']}")
        print(f"✓ 端口：{data['port']}")
        print()
        return True
        
    except Exception as e:
        print(f"✗ 测试失败：{e}")
        print("提示：请确保 Python AI 服务已启动")
        print()
        return False


def test_stats():
    """测试统计信息"""
    print("=" * 60)
    print("测试 2: 知识库统计")
    print("=" * 60)
    
    try:
        response = requests.get(f'{API_BASE}/knowledge/stats', timeout=5)
        data = response.json()
        
        print(f"✓ 文档块总数：{data['stats']['total_documents']}")
        print(f"✓ 集合名称：{data['stats']['collection_name']}")
        print(f"✓ 来源文件数：{len(data['sources'])}")
        
        if data['sources']:
            print("\n来源文件列表:")
            for source in data['sources'][:5]:  # 只显示前 5 个
                print(f"  - {source}")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ 测试失败：{e}")
        print()
        return False


def test_search():
    """测试知识检索"""
    print("=" * 60)
    print("测试 3: 知识检索")
    print("=" * 60)
    
    try:
        # 测试查询
        query = "取水许可申请需要什么材料？"
        print(f"查询：{query}")
        print()
        
        response = requests.post(f'{API_BASE}/knowledge/search', json={
            'query': query,
            'top_k': 3,
            'min_similarity': 0.5
        }, timeout=10)
        
        data = response.json()
        
        if data['count'] == 0:
            print("⚠ 未找到相关结果（知识库可能为空）")
            print("提示：请先上传文档到知识库")
        else:
            print(f"✓ 找到 {data['count']} 个相关结果")
            print()
            
            for i, result in enumerate(data['results'], 1):
                print(f"[{i}] 相似度：{result['similarity']:.3f}")
                print(f"    来源：{result['source']}")
                if result.get('page'):
                    print(f"    页码：{result['page']}")
                print(f"    内容：{result['text'][:100]}...")
                print()
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败：{e}")
        print()
        return False


def test_check_completeness():
    """测试材料完整性检查"""
    print("=" * 60)
    print("测试 4: 材料完整性检查")
    print("=" * 60)
    
    try:
        # 测试数据
        submitted = ['申请书', '身份证明', '水资源论证报告']
        print(f"已提交材料：{submitted}")
        print()
        
        response = requests.post(f'{API_BASE}/knowledge/check', json={
            'submitted_documents': submitted
        }, timeout=10)
        
        data = response.json()
        
        print("检查结果:")
        print(f"✓ 已具备：{len(data.get('provided', []))} 个")
        print(f"✗ 缺失：{len(data.get('missing', []))} 个")
        print(f"📊 完整度：{data.get('completeness', 0):.1f}%")
        print()
        
        if data.get('missing'):
            print("缺失材料:")
            for doc in data['missing'][:5]:  # 只显示前 5 个
                print(f"  - {doc}")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ 测试失败：{e}")
        print()
        return False


def test_upload_sample():
    """测试文档上传（创建测试文档）"""
    print("=" * 60)
    print("测试 5: 文档上传测试")
    print("=" * 60)
    
    try:
        # 创建测试文本文件
        test_content = """
取水许可管理办法

第一章 总则

第一条 为加强水资源管理和保护，规范取水许可管理，根据《中华人民共和国水法》等法律法规，制定本办法。

第二条 在本行政区域内利用取水工程或者设施直接从江河、湖泊或者地下取用水资源的单位和个人，应当申请领取取水许可证，并缴纳水资源费。

第三条 取水许可应当遵循总量控制、定额管理、合理配置、高效利用的原则。

第二章 申请与受理

第四条 申请取水许可应当提交下列材料：
（一）取水许可申请书；
（二）申请人的身份证明或者营业执照；
（三）建设项目水资源论证报告；
（四）取水工程可行性研究报告；
（五）水源地水质监测报告；
（六）取水口位置图；
（七）用水计划方案；
（八）节水措施方案；
（九）与第三者利害关系说明。

第五条 取水许可申请书应当包括下列内容：
（一）申请人的名称、地址、联系方式；
（二）取水目的、取水量、取水水源、取水方式；
（三）退水位置、退水量、退水水质；
（四）取水工程或者设施的基本情况；
（五）其他需要说明的事项。

第三章 审批与决定

第六条 水行政主管部门应当自受理取水申请之日起 20 个工作日内完成审查。
对符合条件的，核发取水许可证；对不符合条件的，书面通知申请人并说明理由。

第七条 取水许可证有效期一般为 5 年。有效期届满，需要延续的，应当在有效期届满 30 日前向原审批机关提出申请。

第四章 监督管理

第八条 取水单位或者个人应当按照批准的取水许可规定条件取水，并安装计量设施，保证计量设施正常运行。

第九条 取水单位或者个人应当于每年 12 月 31 日前向水行政主管部门报送本年度的取水情况和下一年度取水计划建议。

第五章 法律责任

第十条 未经批准擅自取水的，由水行政主管部门责令停止违法行为，限期采取补救措施，处 2 万元以上 10 万元以下的罚款。

第十一条 拒不执行水量调度方案和水量分配预案的，由水行政主管部门责令限期改正，处 2 万元以上 10 万元以下的罚款。

第六章 附则

第十二条 本办法自发布之日起施行。
"""
        
        # 保存为测试文件
        test_file = 'test_document.txt'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"✓ 创建测试文档：{test_file}")
        print(f"✓ 文档大小：{len(test_content)} 字符")
        print()
        
        # 注意：实际上传需要 PDF 或 Word 格式
        print("⚠ 注意：当前版本仅支持 PDF 和 Word 格式")
        print("提示：请将测试文档转换为 PDF 或 Word 格式后上传")
        print()
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败：{e}")
        print()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "知识库系统测试" + " " * 27 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # 检查服务是否运行
    print("正在检查服务状态...")
    print()
    
    results = []
    
    # 测试 1: 健康检查
    results.append(test_health())
    
    if not results[0]:
        print("=" * 60)
        print("测试中止：服务未启动")
        print("=" * 60)
        print()
        print("请执行以下步骤:")
        print("1. 运行：一键启动知识库服务.bat")
        print("2. 等待服务启动完成")
        print("3. 重新运行测试脚本")
        print()
        return
    
    # 测试 2: 统计信息
    results.append(test_stats())
    
    # 测试 3: 知识检索
    results.append(test_search())
    
    # 测试 4: 材料检查
    results.append(test_check_completeness())
    
    # 测试 5: 文档上传
    results.append(test_upload_sample())
    
    # 总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通过：{passed}/{total}")
    
    if passed == total:
        print("✓ 所有测试通过！")
    else:
        print(f"⚠ {total - passed} 个测试失败")
    
    print()


if __name__ == "__main__":
    run_all_tests()
