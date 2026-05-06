import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

load_dotenv(encoding="utf-8")


class DataAnalysisAgent:
    """数据分析Agent"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.agent = create_pandas_dataframe_agent(
            ChatOpenAI(
                model_name=os.getenv("QIANWEN_MODEL_NAME"),
                temperature=0,
                api_key=os.getenv("QIANWEN_API_KEY"),
                base_url=os.getenv("QIANWEN_BASE_URL")
            ),
            df,
            verbose=True,
            allow_dangerous_code=True
        )

    def analyze(self, question: str):
        """分析数据"""
        return self.agent.run(question)


if __name__ == "__main__":
    # 检查数据文件是否存在
    csv_file = "sales_data.csv"
    if not os.path.exists(csv_file):
        print(f"数据文件 {csv_file} 不存在，创建示例数据...")
        # 创建示例数据
        sample_data = {
            "产品": ["产品A", "产品B", "产品C", "产品A", "产品B"],
            "销售额": [10000, 15000, 8000, 12000, 18000],
            "季度": ["Q1", "Q1", "Q1", "Q2", "Q2"]
        }
        df = pd.DataFrame(sample_data)
        df.to_csv(csv_file, index=False)
        print(f"已创建示例数据文件：{csv_file}")
    else:
        df = pd.read_csv(csv_file)

    agent = DataAnalysisAgent(df)

    print("\n数据分析Agent（输入 quit 退出）\n")
    print(f"数据列：{list(df.columns)}")
    print(f"数据行数：{len(df)}\n")

    while True:
        question = input("请输入分析问题：").strip()
        if question.lower() == "quit":
            break
        if not question:
            continue

        try:
            result = agent.analyze(question)
            print(f"\n结果：{result}\n")
        except Exception as e:
            print(f"\n错误：{e}\n")