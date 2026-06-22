import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from backend.rag.vector_store import search_knowledge

def test_rag_search():
    result = search_knowledge("微服务架构")
    assert isinstance(result, str), "返回值类型错误"
    assert len(result) > 0, "检索结果为空"
    assert "微服务" in result or "架构" in result, "检索结果与查询不相关"
    print("[OK] test_rag_search 测试通过")

if __name__ == "__main__":
    print("=== RAG检索功能测试 ===")
    try:
        test_rag_search()
        print("\n[SUCCESS] RAG检索测试通过")
    except AssertionError as e:
        print(f"\n[FAIL] 测试失败：{e}")
        sys.exit(1)