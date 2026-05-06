import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import asyncio

# 加载环境变量
load_dotenv(encoding='utf-8')

# 定义不同角色的Agent
class DevelopmentTeam:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=os.getenv("QIANWEN_MODEL_NAME"),
            temperature=0.3,
            api_key=os.getenv("QIANWEN_API_KEY"),
            base_url=os.getenv("QIANWEN_BASE_URL")
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
    def create_product_manager(self):
        """产品经理Agent"""
        pm_prompt = """
        你是产品经理，负责：
        1. 分析用户需求
        2. 编写产品需求文档
        3. 制定产品路线图
        
        基于对话历史和当前请求，输出产品需求。
        """
        return self._create_agent(pm_prompt)
    
    def create_architect(self):
        """架构师Agent"""
        arch_prompt = """
        你是技术架构师，负责：
        1. 设计系统架构
        2. 技术选型
        3. 制定开发规范
        
        基于产品需求，输出技术方案。
        """
        return self._create_agent(arch_prompt)
    
    def create_developer(self):
        """开发工程师Agent"""
        dev_prompt = """
        你是高级软件工程师，负责：
        1. 编写高质量代码
        2. 代码审查
        3. 性能优化
        
        基于技术方案，输出实现代码。
        """
        return self._create_agent(dev_prompt)
    
    def create_tester(self):
        """测试工程师Agent"""
        test_prompt = """
        你是测试工程师，负责：
        1. 编写测试用例
        2. 执行测试
        3. 发现并报告bug
        
        基于功能和代码，输出测试方案。
        """
        return self._create_agent(test_prompt)
    
    def _create_agent(self, system_prompt):
        """创建Agent - 使用新版 LCEL 链式调用"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        # 新版 LangChain 使用管道操作符创建链
        chain = prompt | self.llm
        return chain
    
    async def execute_project(self, project_idea):
        """执行项目的完整流程"""
        print(f"🚀 开始项目：{project_idea}\n")
        
        # 1. 产品经理分析需求
        print("=" * 50)
        print("👔 产品经理分析需求...")
        pm = self.create_product_manager()
        prd = pm.invoke({
            "input": f"项目想法：{project_idea}",
            "chat_history": []
        })
        print(f"📋 产品需求文档：\n{prd.content}\n")
        
        # 2. 架构师设计方案
        print("=" * 50)
        print("🏗️ 架构师设计方案...")
        architect = self.create_architect()
        design = architect.invoke({
            "input": f"需求文档：\n{prd.content}",
            "chat_history": []
        })
        print(f"🔧 技术方案：\n{design.content}\n")
        
        # 3. 开发工程师实现
        print("=" * 50)
        print("💻 开发工程师实现...")
        developer = self.create_developer()
        code = developer.invoke({
            "input": f"技术方案：\n{design.content}",
            "chat_history": []
        })
        print(f"⌨️ 代码实现：\n{code.content}\n")
        
        # 4. 测试工程师测试
        print("=" * 50)
        print("🧪 测试工程师测试...")
        tester = self.create_tester()
        test_report = tester.invoke({
            "input": f"功能和代码：\n{code.content}",
            "chat_history": []
        })
        print(f"📊 测试报告：\n{test_report.content}\n")
        
        print("=" * 50)
        print("✅ 项目完成！")

# 使用示例
team = DevelopmentTeam()
asyncio.run(team.execute_project("开发一个智能待办事项应用"))
