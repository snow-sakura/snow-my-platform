import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

# 创建模型实例
model = ChatOpenAI(
    model_name="deepseek-ai/DeepSeek-V3.2",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0.7
)

# 创建 Agent
agent = create_agent(
    model=model,
    tools=[],  # 空工具列表
    system_prompt="你是个厉害的个人助理，擅长帮助用户解决各种问题。"
)

# 调用 Agent - 使用正确的输入格式
result = agent.invoke({"messages": [{"role": "user", "content": "给我一道经典的软件测试面试题"}]})

# 打印最后一条消息的内容
print(result["messages"][-1].content)

