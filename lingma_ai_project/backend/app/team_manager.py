import json
import os
from typing import Callable, Optional
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from .config import Config


class TeamManager:
    """AutoGen 团队管理器"""

    def __init__(self):
        self.team: Optional[RoundRobinGroupChat] = None
        self.state_file = "team_state.json"
        self.history_file = "team_history.json"

    async def create_team(self, user_input_func: Callable) -> RoundRobinGroupChat:
        """创建 AutoGen 团队"""

        # 验证配置
        Config.validate()
        model_config = Config.get_model_config()
        model_info = Config.get_model_info()

        # 创建模型客户端 (DeepSeek)
        model_client = OpenAIChatCompletionClient(
            model=model_config["model"],
            api_key=model_config["api_key"],
            base_url=model_config["base_url"],
            model_info=model_info,  # 添加模型能力信息
        )

        # 创建测试用例编写员
        test_writer = AssistantAgent(
            name="test_writer",
            model_client=model_client,
            system_message="""你是资深测试用例编写专家。
职责：
1. 根据需求描述编写详细的测试用例
2. 测试用例应包含：用例编号、用例标题、前置条件、测试步骤、预期结果、优先级
3. 使用Markdown表格格式输出
4. 覆盖正常场景、异常场景和边界场景
5. 完成编写后等待评审员的反馈""",
        )

        # 创建测试用例评审员
        test_reviewer = AssistantAgent(
            name="test_reviewer",
            model_client=model_client,
            system_message="""你是资深测试评审专家。
职责：
1. 评审测试用例的完整性、准确性和可执行性
2. 指出遗漏的测试场景
3. 提出改进建议
4. 如果发现严重问题，标记为REVIEW_REJECT并要求重新编写
5. 如果用例质量合格，标记为REVIEW_PASS并TERMINATE""",
        )

        # 创建协调员
        coordinator = AssistantAgent(
            name="coordinator",
            model_client=model_client,
            system_message="""你是测试流程协调员。
职责：
1. 管理测试用例编写和评审流程
2. 如果评审员REJECT，协调编写员重新编写
3. 如果评审员PASS，总结最终结果并TERMINATE
4. 确保流程高效进行
5. 在开始时接收用户需求并分配任务""",
        )

        # 创建终止条件
        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(30)

        # 创建团队
        team = RoundRobinGroupChat(
            participants=[coordinator, test_writer, test_reviewer],
            termination_condition=termination,
        )

        # 尝试加载之前的状态
        await self._load_team_state(team)

        self.team = team
        return team

    async def _load_team_state(self, team: RoundRobinGroupChat):
        """加载团队状态"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                await team.load_state(state)
                print(f"Loaded team state from {self.state_file}")
            except Exception as e:
                print(f"Failed to load team state: {e}")

    async def save_team_state(self, team: RoundRobinGroupChat):
        """保存团队状态"""
        try:
            state = await team.save_state()
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            print(f"Saved team state to {self.state_file}")
        except Exception as e:
            print(f"Failed to save team state: {e}")

    async def save_history(self, messages: list):
        """保存聊天历史"""
        try:
            history = [msg.model_dump() if hasattr(msg, "model_dump") else msg for msg in messages]
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            print(f"Saved history to {self.history_file}")
        except Exception as e:
            print(f"Failed to save history: {e}")

    async def load_history(self) -> list:
        """加载聊天历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load history: {e}")
        return []


# 全局团队管理器实例
team_manager = TeamManager()
