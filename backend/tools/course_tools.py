from typing import Optional


def get_course_schedule() -> str:
    """查询本周研究生课程表，返回课程安排信息"""
    return """
周一：软件体系结构（上午8:00-10:00，地点：主楼A301）
周二：高级机器学习（上午10:00-12:00，地点：科技楼B105）
周三：高级软件工程（下午14:00-16:00，地点：主楼A301）
周四：自然语言处理（上午8:00-10:00，地点：科技楼B203）
周五：企业级应用软件设计与开发（上午10:00-12:00，地点：主楼A402）
"""


def get_exam_info(course_name: str) -> str:
    """查询指定课程的考试时间和重点范围
    
    Args:
        course_name: 课程名称，如机器学习、软件体系结构
    """
    exam_data = {
        "软件体系结构": "考试时间：第16周周三（6月24日）；考试形式：闭卷；重点范围：微服务架构、设计模式、质量属性、架构评估方法",
        "高级机器学习": "考试时间：第17周周一（6月29日）；考试形式：开卷；重点范围：决策树、SVM、EM算法、神经网络、深度学习框架",
        "高级软件工程": "考试时间：第16周周五（6月26日）；考试形式：闭卷；重点范围：敏捷开发、DevOps、软件测试、需求工程",
        "自然语言处理": "考试时间：第17周周三（7月1日）；考试形式：半开卷；重点范围：词向量、Transformer、注意力机制、文本生成",
        "企业级应用软件设计与开发": "考试时间：第18周周一（7月6日）；考试形式：项目答辩；重点范围：系统设计、架构模式、技术选型、项目管理"
    }
    return exam_data.get(course_name, f"暂未找到「{course_name}」的考试信息，请确认课程名称是否正确")


def get_homework_status(course_name: Optional[str] = None) -> str:
    """查询作业提交状态
    
    Args:
        course_name: 课程名称（可选），不传则查询所有课程的作业状态
    """
    homework_data = {
        "软件体系结构": "第3次作业：架构设计文档（截止日期：6月20日，未提交）",
        "高级机器学习": "第2次作业：实验报告（截止日期：6月18日，已提交）",
        "高级软件工程": "第4次作业：测试用例设计（截止日期：6月22日，未提交）",
        "自然语言处理": "第1次作业：文本分类实验（截止日期：6月25日，未提交）",
        "企业级应用软件设计与开发": "第1次作业：需求分析文档（截止日期：6月30日，进行中）"
    }
    
    if course_name:
        return homework_data.get(course_name, f"暂未找到「{course_name}」的作业信息")
    
    result = "当前所有课程作业状态：\n"
    for course, status in homework_data.items():
        result += f"- {course}：{status}\n"
    return result


def get_study_tips(course_name: str) -> str:
    """获取指定课程的学习建议和资源推荐
    
    Args:
        course_name: 课程名称
    """
    tips_data = {
        "软件体系结构": """学习建议：
1. 重点理解微服务架构的设计原则和边界划分
2. 掌握常见设计模式的应用场景（工厂模式、观察者模式、策略模式）
3. 深入学习质量属性（性能、可用性、安全性、可维护性）

推荐资源：
- 《软件体系结构：面向服务的方法》
- Martin Fowler 关于微服务的系列文章
- 架构师之路博客系列
""",
        "高级机器学习": """学习建议：
1. 理解各类算法的数学原理，不要死记硬背
2. 动手实现经典算法（决策树、SVM、神经网络）
3. 使用Scikit-learn和PyTorch进行实践

推荐资源：
- 《机器学习》- 周志华
- 《Pattern Recognition and Machine Learning》- Bishop
- Kaggle竞赛平台实践
""",
        "高级软件工程": """学习建议：
1. 掌握敏捷开发方法论和Scrum框架
2. 理解DevOps的核心概念和工具链
3. 实践TDD（测试驱动开发）

推荐资源：
- 《敏捷宣言》官方文档
- 《DevOps实践指南》
- Jenkins、GitLab CI/CD官方文档
"""
    }
    return tips_data.get(course_name, f"暂未找到「{course_name}」的学习建议，请尝试其他课程")
