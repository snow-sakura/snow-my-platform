import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv(encoding='utf-8')

# 定义学习助手的提示词模板
study_prompt = PromptTemplate(
    input_variables=["topic", "learning_style", "prior_knowledge"],
    template="""
你是一个专业的学习辅导老师。请根据以下信息为学生制定学习计划：

主题：{topic}
学习风格：{learning_style}
已有知识：{prior_knowledge}

请按以下格式输出：

1. 📋 学习目标
    - 列出3-5个具体学习目标

2. 📚 学习内容大纲
    - 分阶段的学习内容

3. 🎯 推荐学习资源
    - 书籍、视频、网站等

4. ⏰ 时间规划
    - 建议的学习时间表

5. ✅ 自测题目
    - 3-5个检验学习效果的题目

请开始制定学习计划：
"""
)

# 创建LLM
llm = ChatOpenAI(
    model_name=os.getenv("QIANWEN_MODEL_NAME"),
    temperature=0.7,
    api_key=os.getenv("QIANWEN_API_KEY"),
    base_url=os.getenv("QIANWEN_BASE_URL")
)

# 创建链（新版使用管道操作符 |）
study_chain = study_prompt | llm

# 使用
plan = study_chain.invoke({
    "topic": "Python机器学习",
    "learning_style": "实践导向，喜欢做项目",
    "prior_knowledge": "有Python基础,解基本语法"
})

print(plan.content)