from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from typing import List, Dict, Any

from backend.tools.course_tools import get_course_schedule, get_exam_info, get_homework_status, get_study_tips
from backend.rag.vector_store import search_knowledge


class LearningAgent:
    def __init__(self):
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env.example")
        load_dotenv(env_path)
        
        self.llm = ChatOpenAI(
            model="qwen-turbo",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url=os.getenv("BASE_URL"),
            temperature=0.1
        )
        
        self.tools = self._initialize_tools()
        self.graph = self._create_graph()
    
    def _initialize_tools(self) -> List:
        tool_list = []
        
        @tool("get_course_schedule")
        def course_schedule_tool() -> str:
            """查询本周研究生课程表，返回课程安排信息"""
            return get_course_schedule()
        
        @tool("get_exam_info")
        def exam_info_tool(course_name: str) -> str:
            """查询指定课程的考试时间和重点范围
            
            Args:
                course_name: 课程名称，如机器学习、软件体系结构
            """
            return get_exam_info(course_name)
        
        @tool("get_homework_status")
        def homework_status_tool(course_name: str = None) -> str:
            """查询作业提交状态
            
            Args:
                course_name: 课程名称（可选），不传则查询所有课程的作业状态
            """
            return get_homework_status(course_name)
        
        @tool("get_study_tips")
        def study_tips_tool(course_name: str) -> str:
            """获取指定课程的学习建议和资源推荐
            
            Args:
                course_name: 课程名称
            """
            return get_study_tips(course_name)
        
        @tool("search_knowledge")
        def search_knowledge_tool(query: str) -> str:
            """在知识库中检索相关内容，用于回答课程相关问题
            
            Args:
                query: 检索查询词
            """
            return search_knowledge(query)
        
        tool_list.append(course_schedule_tool)
        tool_list.append(exam_info_tool)
        tool_list.append(homework_status_tool)
        tool_list.append(study_tips_tool)
        tool_list.append(search_knowledge_tool)
        
        return tool_list
    
    def _create_graph(self):
        system_prompt = """
你是一名专业的研究生智能学习助手，你的任务是帮助研究生管理学习、查询课程信息、获取考试资料和学习建议。

你拥有以下工具可用：
1. get_course_schedule: 查询本周课程表
2. get_exam_info: 查询指定课程的考试信息
3. get_homework_status: 查询作业提交状态
4. get_study_tips: 获取学习建议和资源推荐
5. search_knowledge: 在知识库中检索相关内容，用于回答课程相关问题（如决策树原理、微服务架构等）

工作原则：
1. 当用户询问课程安排、考试时间、作业状态等具体信息时，优先调用工具获取准确数据
2. 当用户询问课程知识问题（如算法原理、架构概念等）时，优先调用search_knowledge工具检索知识库
3. 只有在工具返回结果后，才能基于工具结果进行回答，不要编造信息
4. 如果工具返回的信息不足以回答问题，可以结合你的知识进行补充说明
5. 回答要简洁明了，结构清晰，方便用户快速获取关键信息
6. 如果用户的问题与学习无关，礼貌地说明你的定位并引导到学习相关话题

请根据用户的问题，判断是否需要调用工具。如果需要，选择合适的工具进行调用。
"""
        
        graph = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt
        )
        
        return graph
    
    def run(self, query: str, memory_context: str = "") -> Dict[str, Any]:
        full_input = f"{memory_context}\n\n用户问题：{query}" if memory_context else query
        
        try:
            config = {"configurable": {"thread_id": "test_thread"}}
            
            response = self.graph.invoke(
                {"messages": [HumanMessage(content=full_input)]},
                config=config
            )
            
            last_message = response["messages"][-1]
            
            return {
                "success": True,
                "answer": last_message.content if hasattr(last_message, 'content') else str(last_message),
                "query": query
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "answer": f"处理请求时出现错误：{str(e)}",
                "query": query
            }


if __name__ == "__main__":
    agent = LearningAgent()
    
    print("测试1：查询本周课程表")
    result = agent.run("本周有什么课？")
    print(result["answer"])
    print("-" * 50)
    
    print("测试2：查询软件体系结构考试信息")
    result = agent.run("软件体系结构什么时候考试？")
    print(result["answer"])
    print("-" * 50)
    
    print("测试3：查询所有作业状态")
    result = agent.run("我的作业都提交了吗？")
    print(result["answer"])
    print("-" * 50)
    
    print("测试4：获取机器学习学习建议")
    result = agent.run("高级机器学习怎么学比较好？")
    print(result["answer"])