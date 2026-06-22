from dotenv import load_dotenv
import os
import sys
from typing import TypedDict, Literal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

from backend.tools.course_tools import get_course_schedule, get_exam_info, get_homework_status, get_study_tips
from backend.rag.vector_store import search_knowledge


env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env.example")
load_dotenv(env_path)

llm = ChatOpenAI(
    model="qwen-turbo",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("BASE_URL"),
    temperature=0.1
)


class AgentState(TypedDict):
    user_query: str
    memory_context: str
    route: Literal["course", "paper", "planning", "unknown"]
    course_agent_response: str
    paper_agent_response: str
    planning_agent_response: str
    final_answer: str


class CourseAgent:
    """课程助手Agent：负责课程答疑、考试查询"""
    
    def __init__(self):
        self.tools = self._initialize_tools()
        self.graph = self._create_graph()
    
    def _initialize_tools(self):
        @tool("get_course_schedule")
        def course_schedule_tool() -> str:
            """查询本周研究生课程表"""
            return get_course_schedule()
        
        @tool("get_exam_info")
        def exam_info_tool(course_name: str) -> str:
            """查询考试时间和重点范围"""
            return get_exam_info(course_name)
        
        @tool("get_homework_status")
        def homework_status_tool(course_name: str = None) -> str:
            """查询作业提交状态"""
            return get_homework_status(course_name)
        
        @tool("get_study_tips")
        def study_tips_tool(course_name: str) -> str:
            """获取学习建议和资源推荐"""
            return get_study_tips(course_name)
        
        @tool("search_knowledge")
        def search_knowledge_tool(query: str) -> str:
            """检索知识库内容"""
            return search_knowledge(query)
        
        return [course_schedule_tool, exam_info_tool, homework_status_tool, study_tips_tool, search_knowledge_tool]
    
    def _create_graph(self):
        system_prompt = """你是一名专业的课程助手Agent，专注于课程答疑和考试查询。

可用工具：
1. get_course_schedule: 查询本周课程表
2. get_exam_info: 查询考试信息
3. get_homework_status: 查询作业状态
4. get_study_tips: 获取学习建议
5. search_knowledge: 检索知识库

回答要简洁明了，结构清晰。"""
        return create_agent(model=llm, tools=self.tools, system_prompt=system_prompt)
    
    def run(self, query: str, memory_context: str = "") -> str:
        full_input = f"{memory_context}\n\n用户问题：{query}" if memory_context else query
        config = {"configurable": {"thread_id": "course_agent_thread"}}
        response = self.graph.invoke({"messages": [HumanMessage(content=full_input)]}, config=config)
        last_message = response["messages"][-1]
        return last_message.content if hasattr(last_message, 'content') else str(last_message)


class PaperAgent:
    """论文助手Agent：负责论文总结、概念解释"""
    
    def __init__(self):
        self.tools = self._initialize_tools()
        self.graph = self._create_graph()
    
    def _initialize_tools(self):
        @tool("search_knowledge")
        def search_knowledge_tool(query: str) -> str:
            """检索知识库中的学术概念和论文内容"""
            return search_knowledge(query)
        return [search_knowledge_tool]
    
    def _create_graph(self):
        system_prompt = """你是一名专业的论文助手Agent，专注于学术概念解释和论文内容总结。

可用工具：
1. search_knowledge: 检索知识库中的学术概念和论文内容

回答要学术严谨，条理清晰，必要时提供示例。"""
        return create_agent(model=llm, tools=self.tools, system_prompt=system_prompt)
    
    def run(self, query: str, memory_context: str = "") -> str:
        full_input = f"{memory_context}\n\n用户问题：{query}" if memory_context else query
        config = {"configurable": {"thread_id": "paper_agent_thread"}}
        response = self.graph.invoke({"messages": [HumanMessage(content=full_input)]}, config=config)
        last_message = response["messages"][-1]
        return last_message.content if hasattr(last_message, 'content') else str(last_message)


class PlanningAgent:
    """学习规划Agent：负责生成复习计划"""
    
    def __init__(self):
        self.tools = self._initialize_tools()
        self.graph = self._create_graph()
    
    def _initialize_tools(self):
        @tool("get_course_schedule")
        def course_schedule_tool() -> str:
            """查询本周课程表"""
            return get_course_schedule()
        
        @tool("get_exam_info")
        def exam_info_tool(course_name: str) -> str:
            """查询考试时间"""
            return get_exam_info(course_name)
        
        @tool("get_homework_status")
        def homework_status_tool(course_name: str = None) -> str:
            """查询作业状态"""
            return get_homework_status(course_name)
        
        @tool("get_study_tips")
        def study_tips_tool(course_name: str) -> str:
            """获取学习建议"""
            return get_study_tips(course_name)
        
        return [course_schedule_tool, exam_info_tool, homework_status_tool, study_tips_tool]
    
    def _create_graph(self):
        system_prompt = """你是一名专业的学习规划Agent，专注于生成复习计划和学习安排。

可用工具：
1. get_course_schedule: 查询本周课程表
2. get_exam_info: 查询考试时间
3. get_homework_status: 查询作业状态
4. get_study_tips: 获取学习建议

计划要具体可行，包含每日学习内容和时间分配。"""
        return create_agent(model=llm, tools=self.tools, system_prompt=system_prompt)
    
    def run(self, query: str, memory_context: str = "") -> str:
        full_input = f"{memory_context}\n\n用户问题：{query}" if memory_context else query
        config = {"configurable": {"thread_id": "planning_agent_thread"}}
        response = self.graph.invoke({"messages": [HumanMessage(content=full_input)]}, config=config)
        last_message = response["messages"][-1]
        return last_message.content if hasattr(last_message, 'content') else str(last_message)


class RouterAgent:
    """路由Agent：识别问题类型并分发到对应子Agent"""
    
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""你是一个智能路由Agent，负责将用户问题分发到正确的子Agent。

子Agent类型：
1. course（课程助手）：处理课程表、考试、作业、学习建议
2. paper（论文助手）：处理学术概念、论文内容、技术原理
3. planning（学习规划）：处理复习计划、时间安排、备考策略

请根据用户问题的内容，返回一个单词：course、paper 或 planning。
如果无法确定，返回 unknown。"""),
            HumanMessage(content="{user_query}")
        ])
        self.chain = self.prompt | llm | StrOutputParser()
    
    def route(self, user_query: str) -> Literal["course", "paper", "planning", "unknown"]:
        result = self.chain.invoke({"user_query": user_query})
        result = result.strip().lower()
        if result in ["course", "paper", "planning"]:
            return result
        return "unknown"


# 全局实例
course_agent = CourseAgent()
paper_agent = PaperAgent()
planning_agent = PlanningAgent()
router_agent = RouterAgent()


def initialize_state(state: AgentState) -> AgentState:
    return state


def route_query(state: AgentState) -> AgentState:
    route = router_agent.route(state["user_query"])
    return {"route": route}


def process_course(state: AgentState) -> AgentState:
    response = course_agent.run(state["user_query"], state["memory_context"])
    return {"course_agent_response": response}


def process_paper(state: AgentState) -> AgentState:
    response = paper_agent.run(state["user_query"], state["memory_context"])
    return {"paper_agent_response": response}


def process_planning(state: AgentState) -> AgentState:
    response = planning_agent.run(state["user_query"], state["memory_context"])
    return {"planning_agent_response": response}


def process_unknown(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="你是一名研究生智能学习助手。请礼貌说明你的定位，引导用户提出学习相关问题。"),
        HumanMessage(content="{user_query}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"user_query": state["user_query"]})
    return {"final_answer": response}


def generate_final_answer(state: AgentState) -> AgentState:
    route = state["route"]
    if route == "course":
        answer = state["course_agent_response"]
    elif route == "paper":
        answer = state["paper_agent_response"]
    elif route == "planning":
        answer = state["planning_agent_response"]
    else:
        answer = state.get("final_answer", "抱歉，无法处理该问题")
    return {"final_answer": answer}


def build_study_graph() -> StateGraph:
    workflow = StateGraph(AgentState)
    
    workflow.add_node("initialize", initialize_state)
    workflow.add_node("route", route_query)
    workflow.add_node("course", process_course)
    workflow.add_node("paper", process_paper)
    workflow.add_node("planning", process_planning)
    workflow.add_node("unknown", process_unknown)
    workflow.add_node("finalize", generate_final_answer)
    
    workflow.set_entry_point("initialize")
    workflow.add_edge("initialize", "route")
    
    workflow.add_conditional_edges(
        "route",
        lambda state: state["route"],
        {"course": "course", "paper": "paper", "planning": "planning", "unknown": "unknown"}
    )
    
    workflow.add_edge("course", "finalize")
    workflow.add_edge("paper", "finalize")
    workflow.add_edge("planning", "finalize")
    workflow.add_edge("unknown", "finalize")
    workflow.add_edge("finalize", END)
    
    return workflow.compile()


study_graph = build_study_graph()


def run_study_graph(user_query: str, memory_context: str = "") -> str:
    result = study_graph.invoke({
        "user_query": user_query,
        "memory_context": memory_context,
        "route": "unknown",
        "course_agent_response": "",
        "paper_agent_response": "",
        "planning_agent_response": "",
        "final_answer": ""
    })
    return result["final_answer"]


if __name__ == "__main__":
    print("=" * 60)
    print("多Agent协作系统测试")
    print("=" * 60)
    
    print("\n--- 测试1：课程助手 ---")
    result = run_study_graph("本周有什么课？")
    print(f"回答: {result[:150]}...")
    print("-" * 50)
    
    print("\n--- 测试2：论文助手 ---")
    result = run_study_graph("什么是微服务架构？")
    print(f"回答: {result[:150]}...")
    print("-" * 50)
    
    print("\n--- 测试3：学习规划 ---")
    result = run_study_graph("帮我制定期末复习计划")
    print(f"回答: {result[:150]}...")