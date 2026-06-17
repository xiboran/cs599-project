import sys, os
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test(module_name, test_file):
    print(f"\n{'='*50}")
    print(f"运行测试：{module_name}")
    print('='*50)
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"stderr: {result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("[FAIL] 测试超时")
        return False
    except Exception as e:
        print(f"[FAIL] 执行异常：{e}")
        return False

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_cases = [
        ("工具层", os.path.join(base_dir, "test_tools.py")),
        ("RAG检索层", os.path.join(base_dir, "test_rag.py")),
        ("记忆模块", os.path.join(base_dir, "test_memory.py")),
    ]
    
    results = []
    start_time = datetime.now()
    
    for name, path in test_cases:
        passed = run_test(name, path)
        results.append({"模块": name, "结果": "通过" if passed else "失败"})
    
    end_time = datetime.now()
    pass_count = sum(1 for r in results if r["结果"] == "通过")
    
    report_path = os.path.join(base_dir, "../docs/test_report.md")
    with open(report_path, "w", encoding='utf-8') as f:
        f.write("# 功能测试报告\n\n")
        f.write(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"测试总数：{len(results)} | 通过：{pass_count} | 失败：{len(results)-pass_count}\n\n")
        f.write("## 测试详情\n\n")
        f.write("| 模块 | 测试结果 |\n|------|----------|\n")
        for r in results:
            f.write(f"| {r['模块']} | {r['结果']} |\n")
        f.write(f"\n测试总耗时：{(end_time-start_time).total_seconds():.2f} 秒\n")
    
    print(f"\n{'='*50}")
    print(f"测试完成，通过率：{pass_count}/{len(results)}")
    print(f"测试报告已生成：docs/test_report.md")
    print('='*50)