# 使用Langchin:统一的接口
from langchain.chat_models import ChatOpenAI, ChatDeepSeek, ChatQwen,ChatAnthropic
from langchain_google_vertexai import ChatVertexAI

# 统一的调用方式
openai_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
deepseek_model = ChatDeepSeek(model_name="deepseek-ai/DeepSeek-V3.2", temperature=0.7)
anthropic_model = ChatAnthropic(model_name="anthropic-ai/Anthropic-Chat", temperature=0.7)
google_model = ChatVertexAI(model_name="vertex-ai/VertexAI-Language", temperature=0.7)
qwen_model = ChatQwen(model_name="qwen-3.5-plus", temperature=0.7)

# 只需要更换模型实例，代码逻辑完全一致
response = openai_model.invoke("Hello")
response = deepseek_model.invoke("Hello")
response = anthropic_model.invoke("Hello")
response = google_model.invoke("Hello")
response = qwen_model.invoke("Hello")
