# 研究生智能学习助手

基于大语言模型与多Agent协作技术的一站式智能学习助手，面向研究生群体提供课程信息查询、知识答疑、学习规划等核心功能。

## 🎯 核心功能

- **课程信息查询**：课程表、考试安排、作业状态、学习建议
- **知识库智能问答**：基于RAG检索增强生成，提供精准知识解答
- **个性化学习规划**：根据课程安排自动生成定制化复习计划
- **用户画像与记忆**：短期对话记忆 + 长期用户画像持久化
- **多Agent智能分发**：路由Agent自动识别问题类型，分发至对应专属Agent

## 🛠️ 技术栈

| 技术 | 版本 | 作用 |
|------|------|------|
| 大模型 | 通义千问 qwen-turbo | 核心推理与工具调用 |
| Agent框架 | LangChain + LangGraph | 工具调用编排、多Agent状态流转 |
| 向量数据库 | ChromaDB | 知识库向量存储与相似度检索 |
| 前端框架 | Streamlit | Web交互界面 |
| 文档处理 | PyPDF + langchain-text-splitters | PDF加载与文本分割 |

## 📁 项目结构

```
cs599-project/
├── .env.example                    # API配置
├── backend/                        # 后端代码
│   ├── agents/                     # Agent模块
│   │   ├── agent_core.py           # 单Agent核心
│   │   ├── grad_student_assistant.py  # 完整主程序
│   │   └── study_graph.py          # 多Agent协作系统
│   ├── tools/                      # 工具层
│   │   └── course_tools.py         # 课程工具函数
│   ├── rag/                        # RAG检索层
│   │   └── vector_store.py         # 向量库与检索
│   ├── memory/                     # 记忆管理层
│   │   └── user_memory.py          # 用户记忆类
│   └── test_*.py                   # 测试文件
├── frontend/                       # 前端代码
│   └── app.py                      # Streamlit应用
├── docs/                           # 规格文档
│   ├── product_spec.md             # 产品规格文档
│   ├── architecture_spec.md        # 架构设计文档
│   └── api_spec.md                 # API接口规格文档
├── data/                           # 数据目录
│   └── chroma_db/                  # 向量库数据
├── Dockerfile                      # Docker配置
├── docker-compose.yml              # Docker Compose配置
├── requirements.txt                # 依赖清单
└── README.md                       # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.11+
- 阿里云百炼API密钥（配置在 `.env.example`）

### 本地运行

```powershell
# 安装依赖
pip install -r requirements.txt

# 运行前端界面
streamlit run frontend/app.py

# 浏览器访问
# http://localhost:8501
```

### Docker运行

```powershell
# 构建并启动容器
docker-compose up -d --build

# 查看运行状态
docker-compose ps

# 浏览器访问
# http://localhost:8501
```

## 📝 功能演示

### 特殊指令

| 指令 | 功能 |
|------|------|
| `退出` / `quit` | 结束程序 |
| `重置对话` | 清空短期记忆 |
| `重置画像` | 清空用户画像 |
| `查看画像` | 显示当前用户画像 |
| `检索知识 xxx` | 直接搜索知识库 |

### 示例对话

```
用户：本周有什么课？
助手：周一：软件体系结构（9:00-10:35）...

用户：软件体系结构什么时候考试？
助手：考试时间：第16周周三（6月24日）...

用户：解释一下微服务架构
助手：知识库检索结果：微服务架构是一种将应用程序构建为一组小型服务的方法...
```

## 📄 规格文档

- [产品规格文档](docs/product_spec.md)
- [架构设计文档](docs/architecture_spec.md)
- [API接口规格文档](docs/api_spec.md)

## 👨‍💻 开发者

研究生智能学习助手项目组