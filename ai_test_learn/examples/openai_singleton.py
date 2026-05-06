# ！/usr/bin/env python
# -*- coding:utf-8-*-
# @Time     :  2026/4/6 14:18
# @Author   :  snow-sakura
# @File     :  openai_singleton.py
# @Software :  PyCharm
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
## 加载环境变量
load_dotenv()
## 单例模式调用openai
def get_model_client():
    """
    获取 OpenAI 聊天完成客户端的单例实例。

    该函数配置并返回一个连接到 SiliconFlow API 的 Qwen2.5-7B-Instruct 模型客户端。
    客户端启用了函数调用、JSON 输出和结构化输出功能，但不支持视觉处理。

    Returns:
        OpenAIChatCompletionClient: 配置好的 OpenAI 聊天完成客户端实例。
    """
    openai_model_client = OpenAIChatCompletionClient(
        model=os.getenv("OPENAI_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1"),
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.UNKNOWN,
            "structured_output": True,
            "multiple_system_messages": True
        }
    )
    return openai_model_client

# 全局单例实例：在模块加载时初始化一次，供整个应用复用
model_client = get_model_client()