import os
from typing import List, Dict, Any
from chromadb import Client
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader


class VectorStore:
    def __init__(self, persist_directory: str = "./data/chroma_db"):
        self.persist_directory = persist_directory
        self.client = Client()
        self.collection = self.client.get_or_create_collection(name="course_knowledge")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )
    
    def load_documents(self, directory: str) -> List[Dict]:
        documents = []
        
        pdf_loader = DirectoryLoader(
            directory,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        text_loader = DirectoryLoader(
            directory,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        
        try:
            pdf_docs = pdf_loader.load()
            documents.extend(pdf_docs)
        except Exception as e:
            print(f"加载PDF文件时出错：{e}")
        
        try:
            text_docs = text_loader.load()
            documents.extend(text_docs)
        except Exception as e:
            print(f"加载文本文件时出错：{e}")
        
        return documents
    
    def split_documents(self, documents: List[Any]) -> List[Dict[str, str]]:
        split_docs = self.text_splitter.split_documents(documents)
        
        chunks = []
        for i, doc in enumerate(split_docs):
            chunks.append({
                "id": f"chunk_{i}",
                "content": doc.page_content,
                "metadata": doc.metadata if hasattr(doc, 'metadata') else {}
            })
        
        return chunks
    
    def add_documents(self, chunks: List[Dict[str, str]]):
        if not chunks:
            return
        
        ids = [chunk["id"] for chunk in chunks]
        contents = [chunk["content"] for chunk in chunks]
        metadatas = [chunk.get("metadata", {}) for chunk in chunks]
        
        self.collection.add(
            ids=ids,
            documents=contents,
            metadatas=metadatas
        )
    
    def build_knowledge_base(self, directory: str):
        print(f"开始构建知识库，目录：{directory}")
        
        documents = self.load_documents(directory)
        print(f"加载到 {len(documents)} 个文档")
        
        if not documents:
            print("未找到任何文档，使用默认知识库")
            self._load_default_knowledge()
            return
        
        chunks = self.split_documents(documents)
        print(f"分割成 {len(chunks)} 个文本块")
        
        self.add_documents(chunks)
        print(f"知识库构建完成，共 {len(chunks)} 条记录")
    
    def _load_default_knowledge(self):
        default_knowledge = [
            {
                "id": "default_1",
                "content": "决策树是一种监督学习算法，用于分类和回归任务。它通过递归地将数据集划分为子集来构建树结构。每个内部节点表示一个特征测试，每个分支表示测试结果，每个叶节点表示一个类别或数值。决策树的核心原理是信息增益和基尼不纯度，用于选择最优分割特征。",
                "metadata": {"source": "机器学习基础", "topic": "决策树"}
            },
            {
                "id": "default_2",
                "content": "微服务架构是一种将应用程序构建为一组小型、独立服务的方法。每个服务运行在自己的进程中，通过轻量级机制（如HTTP API）进行通信。微服务架构的核心特点包括：服务独立部署、独立扩展、技术多样性、容错性和可维护性。",
                "metadata": {"source": "软件体系结构", "topic": "微服务"}
            },
            {
                "id": "default_3",
                "content": "SVM（支持向量机）是一种强大的分类算法。它的核心思想是在特征空间中找到一个最优超平面，将不同类别的样本分开，并且使margin最大化。SVM可以通过核函数处理非线性问题，常用的核函数包括线性核、多项式核和RBF核。",
                "metadata": {"source": "机器学习基础", "topic": "SVM"}
            },
            {
                "id": "default_4",
                "content": "Transformer是一种基于自注意力机制的深度学习模型，由Google在2017年提出。它彻底改变了自然语言处理领域。Transformer的核心组件包括多头注意力机制、位置编码、前馈神经网络和残差连接。BERT、GPT等知名模型都基于Transformer架构。",
                "metadata": {"source": "自然语言处理", "topic": "Transformer"}
            },
            {
                "id": "default_5",
                "content": "设计模式是在软件开发中针对特定问题的通用、可复用的解决方案。常见的设计模式分为三类：创建型模式（如工厂模式、单例模式）、结构型模式（如适配器模式、装饰器模式）和行为型模式（如观察者模式、策略模式）。",
                "metadata": {"source": "软件体系结构", "topic": "设计模式"}
            },
            {
                "id": "default_6",
                "content": "敏捷开发是一种以人为核心、迭代、循序渐进的开发方法。敏捷宣言强调个体和互动高于流程和工具，工作的软件高于详尽的文档，客户合作高于合同谈判，响应变化高于遵循计划。Scrum是最流行的敏捷框架之一。",
                "metadata": {"source": "高级软件工程", "topic": "敏捷开发"}
            },
            {
                "id": "default_7",
                "content": "神经网络是一种模仿人脑神经元结构的机器学习模型。它由输入层、隐藏层和输出层组成。每个神经元接收输入，应用权重和激活函数，产生输出。反向传播算法用于训练神经网络，通过梯度下降更新权重。",
                "metadata": {"source": "机器学习基础", "topic": "神经网络"}
            },
            {
                "id": "default_8",
                "content": "DevOps是一种软件开发方法论，强调开发和运维团队之间的协作和沟通。DevOps的目标是缩短系统开发周期，提高部署频率，同时保持高质量。核心实践包括持续集成、持续交付、自动化测试和基础设施即代码。",
                "metadata": {"source": "高级软件工程", "topic": "DevOps"}
            }
        ]
        
        self.add_documents(default_knowledge)
        print(f"加载默认知识库，共 {len(default_knowledge)} 条记录")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        if not results or not results.get('documents'):
            return []
        
        search_results = []
        for i in range(len(results['documents'][0])):
            search_results.append({
                "content": results['documents'][0][i],
                "distance": results['distances'][0][i] if results.get('distances') else None,
                "metadata": results['metadatas'][0][i] if results.get('metadatas') else {}
            })
        
        return search_results
    
    def get_collection_stats(self) -> Dict:
        return self.collection.count()


def search_knowledge(query: str, top_k: int = 3) -> str:
    """在知识库中检索相关内容，用于回答课程相关问题
    
    Args:
        query: 检索查询词
        top_k: 返回的结果数量，默认3条
    """
    vector_store = VectorStore()
    
    if vector_store.get_collection_stats() == 0:
        vector_store.build_knowledge_base("./data")
    
    results = vector_store.search(query, top_k)
    
    if not results:
        return "未在知识库中找到相关内容"
    
    formatted_results = f"知识库检索结果（共找到 {len(results)} 条相关内容）：\n\n"
    for i, result in enumerate(results, 1):
        source = result['metadata'].get('source', '未知来源')
        topic = result['metadata'].get('topic', '')
        topic_str = f"【{topic}】" if topic else ""
        
        formatted_results += f"📚 结果{i} {topic_str}\n"
        formatted_results += f"来源：{source}\n"
        formatted_results += f"内容：{result['content']}\n\n"
    
    return formatted_results


if __name__ == "__main__":
    vector_store = VectorStore()
    
    print("=== 构建知识库 ===")
    vector_store.build_knowledge_base("./data")
    
    print("\n=== 测试检索 ===")
    query = "决策树的核心原理是什么？"
    print(f"查询：{query}")
    results = search_knowledge(query)
    print(results)
    
    print("\n=== 测试检索2 ===")
    query = "微服务架构的特点"
    print(f"查询：{query}")
    results = search_knowledge(query)
    print(results)
