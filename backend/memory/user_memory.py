import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class UserMemory:
    def __init__(self, user_id: str = "default_user", memory_dir: str = "./data/memory"):
        self.user_id = user_id
        self.memory_dir = memory_dir
        self.short_term_memory: List[Dict] = []
        self.long_term_memory: Dict = {}
        
        os.makedirs(self.memory_dir, exist_ok=True)
        self._load_long_term_memory()
    
    def _load_long_term_memory(self):
        memory_file = os.path.join(self.memory_dir, f"{self.user_id}_profile.json")
        
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    self.long_term_memory = json.load(f)
            except Exception as e:
                print(f"加载长期记忆时出错：{e}")
                self.long_term_memory = {}
        else:
            self.long_term_memory = {
                "user_id": self.user_id,
                "major": "",
                "courses": [],
                "exam_schedule": {},
                "study_progress": {},
                "learning_goals": [],
                "preferences": {},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
    
    def _save_long_term_memory(self):
        memory_file = os.path.join(self.memory_dir, f"{self.user_id}_profile.json")
        
        self.long_term_memory["updated_at"] = datetime.now().isoformat()
        
        try:
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.long_term_memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存长期记忆时出错：{e}")
    
    def add_short_term_memory(self, user_query: str, agent_response: str):
        memory_item = {
            "timestamp": datetime.now().isoformat(),
            "user_query": user_query,
            "agent_response": agent_response
        }
        
        self.short_term_memory.append(memory_item)
        
        if len(self.short_term_memory) > 20:
            self.short_term_memory = self.short_term_memory[-20:]
    
    def get_short_term_memory_context(self, recent_n: int = 5) -> str:
        if not self.short_term_memory:
            return ""
        
        recent_memory = self.short_term_memory[-recent_n:]
        
        context = "【对话历史】\n"
        for item in recent_memory:
            timestamp = item['timestamp'][:19]
            context += f"[{timestamp}] 用户：{item['user_query']}\n"
            context += f"[{timestamp}] 助手：{item['agent_response']}\n\n"
        
        return context.strip()
    
    def update_user_profile(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.long_term_memory:
                self.long_term_memory[key] = value
        
        self._save_long_term_memory()
    
    def set_major(self, major: str):
        self.long_term_memory["major"] = major
        self._save_long_term_memory()
    
    def add_course(self, course_name: str):
        if course_name not in self.long_term_memory["courses"]:
            self.long_term_memory["courses"].append(course_name)
            self._save_long_term_memory()
    
    def set_exam_schedule(self, course_name: str, exam_date: str):
        self.long_term_memory["exam_schedule"][course_name] = exam_date
        self._save_long_term_memory()
    
    def update_study_progress(self, course_name: str, progress: str):
        self.long_term_memory["study_progress"][course_name] = progress
        self._save_long_term_memory()
    
    def add_learning_goal(self, goal: str):
        if goal not in self.long_term_memory["learning_goals"]:
            self.long_term_memory["learning_goals"].append(goal)
            self._save_long_term_memory()
    
    def set_preference(self, key: str, value):
        self.long_term_memory["preferences"][key] = value
        self._save_long_term_memory()
    
    def get_user_profile_context(self) -> str:
        if not self.long_term_memory:
            return ""
        
        profile = self.long_term_memory
        
        context = "【用户画像】\n"
        
        if profile.get("major"):
            context += f"- 专业：{profile['major']}\n"
        
        if profile.get("courses"):
            context += f"- 修读课程：{', '.join(profile['courses'])}\n"
        
        if profile.get("exam_schedule"):
            context += "- 考试安排：\n"
            for course, date in profile["exam_schedule"].items():
                context += f"  * {course}：{date}\n"
        
        if profile.get("study_progress"):
            context += "- 学习进度：\n"
            for course, progress in profile["study_progress"].items():
                context += f"  * {course}：{progress}\n"
        
        if profile.get("learning_goals"):
            context += f"- 学习目标：{'; '.join(profile['learning_goals'])}\n"
        
        return context.strip()
    
    def get_full_memory_context(self, recent_n: int = 5) -> str:
        profile_context = self.get_user_profile_context()
        history_context = self.get_short_term_memory_context(recent_n)
        
        if profile_context and history_context:
            return f"{profile_context}\n\n{history_context}"
        elif profile_context:
            return profile_context
        elif history_context:
            return history_context
        else:
            return ""
    
    def clear_short_term_memory(self):
        self.short_term_memory = []
    
    def reset_long_term_memory(self):
        self.long_term_memory = {
            "user_id": self.user_id,
            "major": "",
            "courses": [],
            "exam_schedule": {},
            "study_progress": {},
            "learning_goals": [],
            "preferences": {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self._save_long_term_memory()


if __name__ == "__main__":
    memory = UserMemory("test_user")
    
    print("=== 测试：初始状态 ===")
    print(memory.get_full_memory_context())
    
    print("\n=== 测试：设置用户画像 ===")
    memory.set_major("计算机技术")
    memory.add_course("软件体系结构")
    memory.add_course("高级机器学习")
    memory.set_exam_schedule("软件体系结构", "6月24日")
    memory.add_learning_goal("掌握微服务架构设计")
    print(memory.get_user_profile_context())
    
    print("\n=== 测试：添加短期记忆 ===")
    memory.add_short_term_memory("你好", "你好！我是你的研究生智能学习助手。")
    memory.add_short_term_memory("我是计算机技术专业", "好的，已记录你的专业信息。")
    memory.add_short_term_memory("我7天后考软件体系结构", "已记录你的考试安排，祝你考试顺利！")
    print(memory.get_short_term_memory_context())
    
    print("\n=== 测试：完整记忆上下文 ===")
    print(memory.get_full_memory_context())
    
    print("\n=== 测试：个性化问答 ===")
    context = memory.get_full_memory_context()
    print(f"记忆上下文：\n{context}")
    print("\n基于记忆的问题：'我该怎么复习？'")
    print("（此问题应结合用户画像和历史对话进行个性化回答）")
