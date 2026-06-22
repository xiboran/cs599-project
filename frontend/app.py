import streamlit as st
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from backend.agents.grad_student_assistant import GradStudentAssistant
from backend.memory.user_memory import UserMemory


st.set_page_config(
    page_title="研究生智能学习助手",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    if "assistant" not in st.session_state:
        st.session_state.assistant = GradStudentAssistant()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_id" not in st.session_state:
        st.session_state.user_id = "default_user"


def get_assistant_response(user_input: str) -> str:
    if user_input in ["退出", "quit", "exit"]:
        return None
    
    if user_input == "重置对话":
        st.session_state.assistant.reset_conversation()
        st.session_state.messages = []
        return "对话已重置"
    
    if user_input == "重置画像":
        st.session_state.assistant.reset_profile()
        return "用户画像已重置"
    
    if user_input == "查看画像":
        return st.session_state.assistant.get_user_profile()
    
    if user_input.startswith("检索知识"):
        query = user_input.replace("检索知识", "").strip()
        if query:
            return st.session_state.assistant.search_knowledge_base(query)
        return "请输入检索内容"
    
    return st.session_state.assistant.process_query(user_input)


def main():
    init_session_state()
    
    with st.sidebar:
        st.title("🎓 项目信息")
        st.subheader("项目介绍")
        st.markdown("研究生智能学习助手是一个基于大语言模型和多Agent协作的智能问答系统。")

        st.subheader("核心功能")
        st.markdown("- 📚 课程查询\n- 📝 考试信息\n- 📖 知识库检索\n- 📅 学习规划")

        st.subheader("用户设置")
        user_id = st.text_input("用户ID", value="default_user")
        if user_id != st.session_state.user_id:
            st.session_state.user_id = user_id
            st.session_state.assistant = GradStudentAssistant(user_id)
            st.session_state.messages = []
            st.rerun()

        st.subheader("快捷操作")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("查看画像", use_container_width=True):
                profile_info = st.session_state.assistant.get_user_profile()
                st.info(profile_info)
        with col2:
            if st.button("重置对话", use_container_width=True):
                st.session_state.assistant.reset_conversation()
                st.session_state.messages = []
                st.success("对话已重置")
                st.rerun()

        if st.button("重置用户画像", use_container_width=True):
            st.session_state.assistant.reset_profile()
            st.success("画像已重置")
            st.rerun()

        with st.expander("📘 操作说明"):
            st.markdown("""
            | 指令格式 | 功能 |
            |---|---|
            | `查看画像` | 查看当前用户画像 |
            | `重置对话` | 清空对话历史 |
            | `重置画像` | 清空用户长期画像 |
            | `检索知识 xxx` | 手动搜索知识库 |
            """)

        with st.expander("🔧 高级设置"):
            st.caption("预留扩展配置项")
    
    st.title("🎓 研究生智能学习助手")
    st.markdown("欢迎使用！请在下方输入您的问题，我来帮你解答。")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("请输入您的问题..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        if prompt in ["退出", "quit", "exit"]:
            st.success("感谢使用！祝你学习进步！")
            st.stop()
        
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                response = get_assistant_response(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
