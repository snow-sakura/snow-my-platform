# ！/usr/bin/env python
# -*- coding:utf-8-*-
# @Time     :  2026/4/5 17:08
# @Author   :  snow-sakura
# @File     :  openai_chat.py
# @Software :  PyCharm

from openai import OpenAI

client = OpenAI(api_key="sk-ruglbzcanhfmsmtxyjeuoxpfirurmdynhkepktnrwrtibzlo",base_url="https://api.siliconflow.cn/v1")

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[
        {"role": "system", "content": "你擅长编写文言文"},
        {"role": "user", "content": "帮我写一篇关于机器学习的文章！"},
    ],
    stream=False
)
print(response.choices[0].message.content)
