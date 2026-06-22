import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from backend.tools.course_tools import get_course_schedule, get_exam_info, get_homework_status, get_study_tips

def test_course_schedule():
    result = get_course_schedule()
    assert isinstance(result, str), "返回值类型错误"
    assert len(result) > 0, "课程表返回为空"
    print("[OK] test_course_schedule 测试通过")

def test_exam_info():
    result = get_exam_info("软件体系结构")
    assert isinstance(result, str), "返回值类型错误"
    assert "考试" in result or "重点" in result, "考试信息内容缺失"
    print("[OK] test_exam_info 测试通过")

def test_homework_status():
    result = get_homework_status()
    assert isinstance(result, str), "返回值类型错误"
    print("[OK] test_homework_status 测试通过")

def test_study_tips():
    result = get_study_tips("高级机器学习")
    assert isinstance(result, str), "返回值类型错误"
    assert len(result) > 0, "学习建议返回为空"
    print("[OK] test_study_tips 测试通过")

if __name__ == "__main__":
    print("=== 工具层功能测试 ===")
    try:
        test_course_schedule()
        test_exam_info()
        test_homework_status()
        test_study_tips()
        print("\n[SUCCESS] 工具层所有测试用例全部通过")
    except AssertionError as e:
        print(f"\n[FAIL] 测试失败：{e}")
        sys.exit(1)