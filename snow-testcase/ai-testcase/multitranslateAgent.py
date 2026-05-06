import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(encoding="utf-8")


class TranslationWorkflow:
    """多语言翻译工作流"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=os.getenv("QIANWEN_MODEL_NAME"),
            temperature=0.3,
            api_key=os.getenv("QIANWEN_API_KEY"),
            base_url=os.getenv("QIANWEN_BASE_URL")
        )

    def translate_with_context(self, text: str, target_lang: str):
        """带上下文的翻译"""
        prompt = f"""将以下文本翻译成{target_lang}：

原文：{text}

要求：
1. 保持原文的语气和风格
2. 考虑文化差异
3. 专业术语保持准确
4. 提供翻译说明

输出格式：
- 翻译结果
- 关键术语解释
- 文化适配说明
"""

        return self.llm.invoke(prompt)


if __name__ == "__main__":
    translator = TranslationWorkflow()

    # 示例文本
    sample_text = "Hello, welcome to our AI-powered customer service system. We are here to help you 24/7."

    print("原文：")
    print(sample_text)
    print("\n正在翻译成中文...")

    result = translator.translate_with_context(sample_text, "中文")

    print("\n翻译结果：")
    print(result.content)