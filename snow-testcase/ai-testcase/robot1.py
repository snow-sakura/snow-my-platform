# 最简单的实例
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


# 初始化模型
llm = ChatOpenAI(model_name="qwen-3.5-plus")

# 发送消息
response = llm([SystemMessage(content="你是一个 helpful assistant。"), HumanMessage(content="What is the weather like in San Francisco?")])
print(response.content)
