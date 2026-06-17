import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.memory.user_memory import UserMemory

def test_memory():
    mem = UserMemory("test_report_user")
    
    mem.add_short_term_memory("我叫张三", "好的，记住了")
    context = mem.get_short_term_memory_context()
    assert "张三" in context, "短期记忆写入失败"
    print("[OK] 短期记忆测试通过")
    
    mem.set_major("计算机技术")
    mem.add_course("软件体系结构")
    profile = mem.get_user_profile_context()
    assert "计算机技术" in profile, "专业信息写入失败"
    assert "软件体系结构" in profile, "课程信息写入失败"
    print("[OK] 长期画像测试通过")
    
    mem.clear_short_term_memory()
    assert len(mem.short_term_memory) == 0, "短期记忆清空失败"
    print("[OK] 记忆清空功能测试通过")
    
    mem.reset_long_term_memory()

if __name__ == "__main__":
    print("=== 记忆模块功能测试 ===")
    try:
        test_memory()
        print("\n[SUCCESS] 记忆模块所有测试通过")
    except AssertionError as e:
        print(f"\n[FAIL] 测试失败：{e}")
        sys.exit(1)