import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.grad_student_assistant import GradStudentAssistant

def run_agent_test():
    assistant = GradStudentAssistant("integration_test_user")
    
    test_cases = [
        {"id": 1, "question": "本周有哪些课程？分别在周几？", "expected_route": "course", 
         "expected_tools": ["get_course_schedule"], "validation_keywords": ["周一", "软件体系结构"]},
        {"id": 2, "question": "软件体系结构什么时候考试？复习重点有哪些？", "expected_route": "course",
         "expected_tools": ["get_exam_info"], "validation_keywords": ["考试", "6月24日"]},
        {"id": 3, "question": "我所有课程的作业都提交了吗？", "expected_route": "course",
         "expected_tools": ["get_homework_status"], "validation_keywords": ["作业"]},
        {"id": 4, "question": "高级机器学习这门课怎么学比较好？", "expected_route": "course",
         "expected_tools": ["get_study_tips"], "validation_keywords": ["学习建议", "资源"]},
        {"id": 5, "question": "解释一下微服务架构的核心特点", "expected_route": "paper",
         "expected_tools": ["search_knowledge"], "validation_keywords": ["微服务"]},
        {"id": 6, "question": "什么是决策树算法？它的优缺点是什么？", "expected_route": "paper",
         "expected_tools": ["search_knowledge"], "validation_keywords": ["决策树"]},
        {"id": 7, "question": "我是计算机技术专业的，帮我记一下", "expected_route": "-",
         "expected_tools": ["-"], "validation_keywords": ["记住", "好的"]},
        {"id": 8, "question": "查看我的用户画像", "expected_route": "-",
         "expected_tools": ["-"], "validation_keywords": ["计算机技术"]},
        {"id": 9, "question": "帮我制定软件体系结构的7天期末复习计划", "expected_route": "planning",
         "expected_tools": ["get_exam_info", "get_study_tips"], "validation_keywords": ["复习计划", "7天"]},
        {"id": 10, "question": "帮我总结一下SVM算法的核心思想", "expected_route": "paper",
         "expected_tools": ["search_knowledge"], "validation_keywords": ["SVM"]},
    ]
    
    results = []
    start_time = datetime.now()
    
    for tc in test_cases:
        print(f"\n--- 测试问题 {tc['id']} ---")
        print(f"问题：{tc['question']}")
        print(f"预期路由：{tc['expected_route']}")
        
        try:
            response = assistant.process_query(tc['question'])
            print(f"回答：{response[:100]}..." if len(response) > 100 else f"回答：{response}")
            
            passed = any(kw in response for kw in tc['validation_keywords'])
            results.append({
                "编号": tc['id'],
                "问题": tc['question'],
                "预期路由": tc['expected_route'],
                "预期工具": tc['expected_tools'],
                "验证结果": "通过" if passed else "失败",
                "验证关键词": tc['validation_keywords']
            })
        except Exception as e:
            print(f"错误：{e}")
            results.append({
                "编号": tc['id'],
                "问题": tc['question'],
                "预期路由": tc['expected_route'],
                "预期工具": tc['expected_tools'],
                "验证结果": "失败",
                "错误信息": str(e)
            })
    
    end_time = datetime.now()
    pass_count = sum(1 for r in results if r["验证结果"] == "通过")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(base_dir, "../docs/report/integration_test_report.md")
    
    with open(report_path, "w", encoding='utf-8') as f:
        f.write("# Agent集成测试报告\n\n")
        f.write(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"测试总数：{len(results)} | 通过：{pass_count} | 失败：{len(results)-pass_count}\n\n")
        f.write("## 测试详情\n\n")
        f.write("| 编号 | 测试问题 | 预期路由 | 预期调用工具 | 验证结果 |\n")
        f.write("|------|----------|----------|--------------|----------|\n")
        for r in results:
            tools_str = ", ".join(r["预期工具"])
            f.write(f"| {r['编号']} | {r['问题']} | {r['预期路由']} | {tools_str} | {r['验证结果']} |\n")
        f.write(f"\n测试总耗时：{(end_time-start_time).total_seconds():.2f} 秒\n")
    
    print(f"\n{'='*50}")
    print(f"测试完成，通过率：{pass_count}/{len(results)}")
    print(f"测试报告已生成：docs/report/integration_test_report.md")
    print('='*50)
    
    return pass_count == len(results)

if __name__ == "__main__":
    print("=== Agent集成测试（10个标准测试问题）===")
    try:
        all_passed = run_agent_test()
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\n[FAIL] 测试执行异常：{e}")
        sys.exit(1)