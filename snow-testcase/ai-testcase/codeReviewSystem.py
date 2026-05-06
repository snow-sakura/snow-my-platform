import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(encoding="utf-8")


class CodeReviewAssistant:
    """代码审查助手"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=os.getenv("QIANWEN_MODEL_NAME"),
            temperature=0.1,
            api_key=os.getenv("QIANWEN_API_KEY"),
            base_url=os.getenv("QIANWEN_BASE_URL")
        )

    def review_code(self, code: str, language: str = "python"):
        """审查代码"""
        review_prompt = f"""你是一位资深的{language}代码审查专家。请审查以下代码：

代码：
```{language}
{code}
```

请从以下维度进行审查：

1. 严重问题（必须修复）
2. 建议改进（推荐修复）
3. 最佳实践（可选优化）
4. 做得好的地方

对每个问题提供：
- 问题描述
- 位置（行号）
- 修复建议
- 代码示例
"""

        response = self.llm.invoke(review_prompt)
        return self._parse_review(response.content)

    def _parse_review(self, review_text):
        """解析审查结果"""
        return {
            "critical_issues": [],
            "suggestions": [],
            "best_practices": [],
            "positives": []
        }


if __name__ == "__main__":
    reviewer = CodeReviewAssistant()
    
    sample_code = """
def add(a, b):
    return a + b
"""
    
    print("正在审查代码...")
    result = reviewer.review_code(sample_code, "python")
    print("审查完成！")