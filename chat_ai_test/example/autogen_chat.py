# ！/usr/bin/env python
# -*- coding:utf-8-*-
# @Time     :  2026/4/6 14:33
# @Author   :  snow-sakura
# @File     :  autogen_chat.py
# @Software :  PyCharm
import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console

from openai_singleton import model_client
agent = AssistantAgent(
    name="report_agent",
    model_client=model_client,
    system_message="你是一位善于编写测试报告的助手",
    model_client_stream=True,  # 使用流式输出
)

# await不能直接写在模块中
# 如果函数中调用了协程函数，那么当前函数必须声明为协程函数
async def main():
    result = await agent.run(task="请编写一份关于机器学习的测试报告！")
    print(result)

# 流式输出
async def main_stream():
    # 获取协程对象
    result = agent.run_stream(task="请编写一份关于机器学习的测试报告！")
    async for item in result:
        print(item)

# 前端流式输出
async def main_stream_console():
    await Console(agent.run_stream(task="请编写一份关于机器学习的测试报告！"))

asyncio.run(main_stream_console())