import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(encoding="utf-8")


class DocumentGenerator:
    """文档生成器"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=os.getenv("QIANWEN_MODEL_NAME"),
            temperature=0.7,
            api_key=os.getenv("QIANWEN_API_KEY"),
            base_url=os.getenv("QIANWEN_BASE_URL")
        )

    def generate_report(self, data: dict, template: str):
        """生成报告"""
        prompt = f"""基于以下数据生成一份专业的{template}报告：

数据：
{json.dumps(data, indent=2, ensure_ascii=False)}

要求：
1. 使用Markdown格式
2. 包含执行摘要
3. 数据可视化建议
4. 关键发现和建议
5. 专业但易读的语言
"""

        return self.llm.invoke(prompt)


if __name__ == "__main__":
    # 示例数据
    sample_data = {
        "季度": "2024 Q1",
        "销售额": 1500000,
        "增长率": 23.5,
        "客户数": 1200,
        "满意度": 4.5
    }

    generator = DocumentGenerator()
    print("正在生成报告...")
    result = generator.generate_report(sample_data, "季度销售")
    print("\n生成的报告：")
    print(result.content)