import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_classic.memory import ConversationBufferWindowMemory

load_dotenv(encoding="utf-8")


class IntelligentCustomerService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=os.getenv("QIANWEN_MODEL_NAME"),
            temperature=0.3,
            api_key=os.getenv("QIANWEN_API_KEY"),
            base_url=os.getenv("QIANWEN_BASE_URL")
        )
        self.memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = self._create_tools()
        self.agent = self._create_agent()

    def _create_tools(self):
        @tool
        def check_order_status(order_id: str) -> str:
            return f"订单{order_id}状态：已发货"

        @tool
        def process_refund(order_id: str, amount: float) -> str:
            return f"退款{amount}元已申请，订单{order_id}"

        @tool
        def get_product_info(product_id: str) -> str:
            return f"产品{product_id}详情..."

        @tool
        def escalate_to_human(issue: str) -> str:
            return "已转接人工客服，请稍候..."

        return [check_order_status, process_refund, get_product_info, escalate_to_human]

    def _create_agent(self):
        system_prompt = """你是专业的客服助手，负责：
1. 回答客户咨询
2. 处理订单问题
3. 提供产品信息
4. 必要时转接人工客服

保持友好、专业、耐心。"""

        agent = create_tool_calling_agent(
            self.llm,
            self.tools,
            ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ])
        )

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )

    def handle_query(self, query: str, customer_id: str):
        result = self.agent.invoke({
            "input": f"[客户ID: {customer_id}] {query}"
        })
        return result["output"]


if __name__ == "__main__":
    cs = IntelligentCustomerService()
    print("智能客服系统（输入 quit 退出）")
    while True:
        query = input("客户: ").strip()
        if query.lower() == "quit":
            break
        if not query:
            continue
        response = cs.handle_query(query, "cust_001")
        print(f"客服: {response}")