import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file into the environment
load_dotenv()

# Qwen_Model_Name = os.getenv("QIANWEN_MODEL_NAME")
# Qwen_API_Key = os.getenv("QIANWEN_API_KEY")
# Qwen_Base_URL = os.getenv("QIANWEN_BASE_URL")

# # Create a Qwen client
# client = OpenAI(api_key=Qwen_API_Key, base_url=Qwen_Base_URL)

# response = client.chat.completions.create(
#     model=Qwen_Model_Name,
#     messages=[
#         {"role": "system", "content": "你是个厉害的个人助理，擅长帮助用户解决各种问题。"},
#         {"role": "user", "content": "你是谁呀?"}
#         ]
# )

# print(response.choices[0].message.content)

# llm = ChatOpenAI(
#     model_name=os.getenv("QIANWEN_MODEL_NAME"),
#     openai_api_key=os.getenv("QIANWEN_API_KEY"),
#     base_url=os.getenv("QIANWEN_BASE_URL"),
#    tem perature=0.7#
#)
e# response = llm.invoke("请介绍下自己呗！")
# print(response.content)

# 直接设置环境变量，下面初始化模型时会自动读取
os.environ["QIANWEN_API_KEY"] = os.getenv("QIANWEN_API_KEY")

model = ChatOpenAI(model_name="qwen3.5-plus")

agent = create_agent(
    model=model,
    system_prompt="你是个厉害的个人助理，擅长帮助用户解决各种问题。",
)

result = agent.invoke(
    {"message"[{"role": "user", "content": "给我一道经典的软件测试面试题"}]})
print(result)
