# ！/usr/bin/env python
# -*- coding:utf-8-*-
# @Time     :  2026/4/5 17:26
# @Author   :  snow-sakura
# @File     :  openai_model_client.py
# @Software :  PyCharm
import asyncio
from unittest import result

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage, SystemMessage, ModelFamily

openai_model_client = OpenAIChatCompletionClient(
    model="Qwen/Qwen2.5-7B-Instruct",
    base_url="https://api.siliconflow.cn/v1",
    api_key="sk-ruglbzcanhfmsmtxyjeuoxpfirurmdynhkepktnrwrtibzlo",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": True
    }
)



# 定义一个协程函数
# 异步，不能直接调用
async def main():
    result = await openai_model_client.create([UserMessage(content="帮我写一篇关于机器学习的文章！",source="user"),
                                               SystemMessage(content="你擅长编写文言文")])
    print(result)
    await openai_model_client.close()


asyncio.run(main())