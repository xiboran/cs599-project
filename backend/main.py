import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_core import LearningAgent
from memory.user_memory import UserMemory
from rag.vector_store import search_knowledge
from tools.course_tools import get_course_schedule, get_exam_info, get_homework_status, get_study_tips


class GradStudentAssistant:
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.agent = LearningAgent()
        self.memory = UserMemory(user_id)
    
    def process_query(self, query: str) -> str:
        memory_context = self.memory.get_full_memory_context()
        
        result = self.agent.run(query, memory_context)
        
        if result.get("success"):
            self.memory.add_short_term_memory(query, result["answer"])
            
            self._update_profile_from_query(query)
        
        return result["answer"]
    
    def _update_profile_from_query(self, query: str):
        if "专业" in query or "方向" in query:
            if "计算机" in query:
                self.memory.set_major("计算机技术")
            elif "软件工程" in query:
                self.memory.set_major("软件工程")
        
        courses = ["软件体系结构", "高级机器学习", "高级软件工程", 
                   "自然语言处理", "企业级应用软件设计与开发"]
        for course in courses:
            if course in query:
                self.memory.add_course(course)
                
                if "考试" in query or "复习" in query:
                    exam_info = get_exam_info(course)
                    if "考试时间" in exam_info:
                        import re
                        date_match = re.search(r"(\d+月\d+日)", exam_info)
                        if date_match:
                            self.memory.set_exam_schedule(course, date_match.group(1))
    
    def search_knowledge_base(self, query: str) -> str:
        return search_knowledge(query)
    
    def get_user_profile(self) -> str:
        return self.memory.get_user_profile_context()
    
    def reset_conversation(self):
        self.memory.clear_short_term_memory()
        return "对话已重置，短期记忆已清空"
    
    def reset_profile(self):
        self.memory.reset_long_term_memory()
        return "用户画像已重置"


def main():
    print("=" * 60)
    print("🎓 研究生智能学习助手系统 v1.0")
    print("=" * 60)
    print("欢迎使用！我可以帮助你查询课程、考试信息、学习资料等。")
    print("输入 '退出' 或 'quit' 结束对话")
    print("输入 '重置对话' 清空当前对话历史")
    print("输入 '重置画像' 清空用户画像")
    print("输入 '查看画像' 查看当前用户画像")
    print("输入 '检索知识' 搜索知识库内容")
    print("=" * 60)
    
    assistant = GradStudentAssistant()
    
    while True:
        user_input = input("\n请输入你的问题：")
        
        if user_input in ["退出", "quit", "exit"]:
            print("感谢使用！祝你学习进步！")
            break
        
        if user_input == "重置对话":
            response = assistant.reset_conversation()
            print(response)
            continue
        
        if user_input == "重置画像":
            response = assistant.reset_profile()
            print(response)
            continue
        
        if user_input == "查看画像":
            profile = assistant.get_user_profile()
            print("\n当前用户画像：")
            print(profile)
            continue
        
        if user_input.startswith("检索知识"):
            query = user_input.replace("检索知识", "").strip()
            if not query:
                print("请输入检索内容，例如：检索知识 决策树原理")
                continue
            print(f"\n正在检索知识库：{query}")
            results = assistant.search_knowledge_base(query)
            print(results)
            continue
        
        print("\n正在思考...")
        response = assistant.process_query(user_input)
        print("\n助手回答：")
        print(response)


if __name__ == "__main__":
    main()
