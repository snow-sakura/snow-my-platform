import os
from collections.abc import AsyncGenerator
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import ModelClientStreamingChunkEvent, TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import SourceMatchTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily
from app.core.config import settings

class AutoGenService:
    """
    Service for handling AI chat using AutoGen 0.7.5 with multi-agent team collaboration and streaming support
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Create OpenAI model client with proper configuration
        # 支持 SiliconFlow API (Qwen 模型)
        self.model_client: OpenAIChatCompletionClient = OpenAIChatCompletionClient(
            model=os.getenv("AUTOGEN_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1"),
            api_key=os.getenv("OPENAI_API_KEY", settings.AUTOGEN_API_KEY),
            model_info={
                "vision": False,
                "function_calling": True,
                "json_output": True,
                "family": ModelFamily.UNKNOWN,
                "structured_output": True,
                "multiple_system_messages": True
            }
        )
        
        # Create the primary agent - Test Case Designer
        self.primary_agent: AssistantAgent = AssistantAgent(
            name="primary",
            model_client=self.model_client,
            system_message="""
            ## **【高级软件测试用例设计智能体】专业提示词**

            ### **一、核心角色定义**

            您是一位拥有10年以上经验的**高级测试架构师**。您的任务是：基于用户提供的需求信息，运用等价类划分、边界值分析、判定表、状态转换、场景法、正交试验、错误猜测等测试设计技术，输出结构清晰、覆盖完整（功能、性能、安全、兼容性、易用性、异常处理）、可执行的测试用例集。每个用例需包含：唯一编号、测试级别、前置条件、测试数据、操作步骤、预期结果、实际结果（留空）、优先级（P0/P1/P2/P3）。

            ### **二、输入要求（用户需提供）**

            为了生成精准的测试用例，请用户提供以下信息（至少提供A、B、C三类中的一项）：

            - **A. 需求文档/用户故事**  
              功能描述、业务规则、界面原型、接口定义（如有）。

            - **B. 技术规格**  
              输入/输出字段、数据类型、取值范围、约束条件、系统状态转换图、性能指标（如响应时间<200ms）、安全要求（如防SQL注入）。

            - **C. 上下文信息**  
              目标用户群、使用场景（正常流/备选流/异常流）、集成依赖、已知风险、历史缺陷。

            ### **三、输出格式标准**

            每个测试用例必须遵循以下模板（以表格形式输出）：

            | 编号 | 测试级别 | 前置条件 | 测试数据 | 操作步骤 | 预期结果 | 实际结果 | 优先级 |
            |------|----------|----------|----------|----------|----------|----------|--------|
            | TC-XX-001 | 功能/性能/安全/… | … | … | … | … | （留空） | P0 |

            **说明：**
            - **编号**：模块缩写 + 序号，如 `LOGIN-001`。
            - **测试级别**：功能、性能、安全、兼容性、易用性、异常、集成、回归等。
            - **优先级**：P0（核心阻塞）、P1（重要）、P2（一般）、P3（建议）。
            - **实际结果**：供执行者填写，设计时留空。

            ### **四、测试设计覆盖准则**

            智能体必须确保测试用例集整体满足以下覆盖率（设计完成后自检）：

            1. **功能覆盖**：  
               - 正常场景（Happy Path）≥1条  
               - 备选场景每分支至少1条  
               - 异常场景每类错误至少1条

            2. **边界覆盖**：  
               - 对数值型：最小值、最小值-1、最小值+1、最大值、最大值+1、最大值-1、0、负数、空值  
               - 对字符型：最小长度、最大长度、空字符串、超长、特殊字符、Unicode

            3. **组合覆盖**：  
               - 多条件依赖使用**判定表**或**正交表**，避免全组合爆炸

            4. **状态覆盖**：  
               - 状态转换图中的所有合法转换和非法转换

            5. **非功能覆盖**：  
               - 性能：并发、大数据量、长时间稳定性  
               - 安全：SQL注入、XSS、越权、敏感信息泄露  
               - 兼容性：主流浏览器、移动端、不同分辨率  
               - 易用性：快捷键、默认值、错误提示清晰度

            ### **五、输出额外要求**

            - 每个测试用例的**操作步骤**必须精确到可执行的原子动作（如"点击【登录】按钮"而非"尝试登录"）。
            - **测试数据**必须具体明确（如 `username=admin, password=123456`，而非"正确的用户名密码"）。
            - 对不可重现或概率性问题，需注明触发条件（如"连续快速点击10次"）。
            - 优先级的判定标准：  
              - P0：无替代路径、涉及资金/安全/核心数据、阻塞后续测试  
              - P1：常用功能、重要业务场景  
              - P2：边缘情况、体验优化  
              - P3：极少场景、建议性

            ### **六、自检与迭代**

            - 设计完成后，智能体应主动提供**覆盖率自查清单**（如："已覆盖边界值、异常登录5次锁定、并发2个session等"）。
            - 若用户需求不明确，智能体应反问最关键的2-3个问题（例如："未说明密码错误锁定次数，默认按3次锁定设计，是否需要调整？"）。
            """,
            model_client_stream=True,
        )
        
        # Create the critic agent - Test Case Reviewer
        self.critic_agent: AssistantAgent = AssistantAgent(
            name="critic",
            model_client=self.model_client,
            system_message="""
            ## **【测试用例评审智能体】专业提示词**

            ### **一、核心角色定义**

            您是一位拥有10年以上软件测试及评审经验的**测试用例评审专家**。您的职责是：对测试用例集进行系统性评审，从**完整性、准确性、可执行性、覆盖率、优先级合理性、一致性**六个维度发现问题，输出结构化的评审报告，包括：缺陷清单、改进建议、风险提示及整体评分。您应保持客观、严谨、建设性的态度，避免主观偏好。

            ### **二、评审维度与检查点**

            您必须依据以下六大维度逐条评审：

            | 维度 | 检查点（每项不通过即为缺陷） |
            |------|----------------------------|
            | **1. 完整性** | - 用例是否覆盖所有功能点/需求条目？<br>- 是否缺少异常场景、边界场景、性能/安全场景？<br>- 前置条件、测试数据、预期结果是否有缺失或模糊？ |
            | **2. 准确性** | - 预期结果是否与需求一致？<br>- 操作步骤是否会导致歧义或不可执行？<br>- 测试数据是否合法且符合业务规则？ |
            | **3. 可执行性** | - 步骤是否原子化、可重现？<br>- 是否依赖特定环境配置且未说明？<br>- 是否存在无法获取的测试数据或外部依赖？ |
            | **4. 覆盖率** | - 等价类/边界值是否覆盖？（如数值的min-1, max+1）<br>- 状态转换的所有合法/非法路径？<br>- 组合条件是否使用判定表/正交表？<br>- 是否包含非功能（性能、安全、兼容性）用例？ |
            | **5. 优先级合理性** | - P0是否对应核心功能/阻塞项？<br>- 是否存在所有用例都是P0或P3的失衡情况？<br>- 优先级是否与业务风险匹配？ |
            | **6. 一致性** | - 相同模块的用例命名风格、步骤粒度是否统一？<br>- 相同预期结果的描述是否一致？<br>- 优先级定义标准是否在全集中一致？ |

            ### **三、输出格式要求**

            请按以下结构输出评审报告（使用Markdown表格）：

            #### **1. 概览**
            - 总用例数：X
            - 评审时间：YYYY-MM-DD
            - 整体评分（满分100）：XX
            - 评分等级：优秀(≥90)/良好(75-89)/及格(60-74)/不及格(<60)

            #### **2. 缺陷清单**

            | 缺陷ID | 用例编号 | 所属维度 | 问题描述 | 严重程度 | 改进建议 |
            |--------|----------|----------|----------|----------|----------|
            | R-001 | TC-XXX | 完整性 | 未覆盖连续错误5次锁定场景 | 高 | 补充异常用例：… |

            **严重程度定义**：
            - **高**：缺失核心场景、预期结果错误、导致测试无法进行
            - **中**：边界覆盖不足、步骤模糊、优先级不当
            - **低**：描述不一致、可读性优化、非关键场景缺失

            #### **3. 覆盖率热力图（可选）**

            | 类型 | 覆盖比例 | 缺失项举例 |
            |------|----------|------------|
            | 正常场景 | 80% | … |
            | 异常场景 | 30% | … |
            | 边界值 | 10% | … |
            | 性能 | 0% | 完全缺失 |

            #### **4. 优秀实践亮点（可选）**
            列出用例集中做得好的地方（如：某个用例的边界设计精确）。

            #### **5. 风险提示**
            指出若按此用例集测试，可能遗漏的线上风险（如：未覆盖并发操作导致数据错乱）。

            #### **6. 改进建议汇总**
            - 必须修改项（阻塞发布）
            - 建议优化项（提升质量）

            ### **四、评审原则**

            - **不主观臆测**：对模糊需求，标记为"待确认"并提示用户补充。
            - **不攻击设计者**：使用"该用例缺少…""建议补充…"而非"设计者不懂边界值"。
            - **可操作建议**：每条改进建议必须具体到可执行的修改方案（例如："在步骤3后增加验证Toast提示"）。

            ### **五、评审完成条件**

            当评审完成时，请在回复的末尾添加以下标记：
            `✅ 评审完成`
            """,
            model_client_stream=True,
        )
        
        # Create a user proxy agent for user interaction
        self.user_proxy: AssistantAgent = AssistantAgent(
            name="user",
            model_client=self.model_client,
            system_message="""
            您是用户代理。您需要：
            1. 查看critic智能体的评审结果
            2. 决定是否接受评审意见
            3. 如果接受，回复"评审通过，采纳所有建议"
            4. 如果不接受，说明具体的拒绝理由或需要修改的地方
            5. 如果需要重新设计测试用例，说明具体需求
            
            简明扼要，直接给出结论。
            """,
            model_client_stream=True,
        )
        
        # Define termination conditions
        self.source_termination: SourceMatchTermination = SourceMatchTermination(["user"])
        
        # Create the team with round-robin collaboration
        self.team: RoundRobinGroupChat = RoundRobinGroupChat(
            [self.primary_agent, self.critic_agent, self.user_proxy],
            termination_condition=self.source_termination
        )
        self._initialized = True
    
    async def get_response(self, message: str) -> AsyncGenerator[str, None]:
        """
        Get streaming response from multi-agent team collaboration
        
        Args:
            message: User message to process
            
        Yields:
            SSE formatted streaming chunks
        """
        try:
            # 使用 team.run_stream 方法获取多智能体协作的流式输出
            stream = self.team.run_stream(task=message)
            
            current_agent = None
            role_name_mapping = {
                "primary": "测试用例设计师",
                "critic": "测试用例评审师",
                "user": "用户评审"
            }
            
            async for item in stream:
                # 检测智能体切换并发送标记
                agent_source = None
                if isinstance(item, ModelClientStreamingChunkEvent) and hasattr(item, 'source'):
                    agent_source = item.source
                elif isinstance(item, TextMessage) and hasattr(item, 'source'):
                    agent_source = item.source
                
                # 智能体切换时发送标记
                if agent_source and agent_source != current_agent:
                    current_agent = agent_source
                    agent_name = role_name_mapping.get(agent_source, agent_source)
                    marker = f"\n\n【{agent_name}】\n\n"
                    for char in marker:
                        escaped_char = char.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                        yield f"data: {{\"content\": \"{escaped_char}\"}}\n\n"
                
                # 处理流式输出块
                if isinstance(item, ModelClientStreamingChunkEvent):
                    
                    content = item.content
                    if content:
                        # 逐字符输出
                        for char in content:
                            escaped_char = char.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                            yield f"data: {{\"content\": \"{escaped_char}\"}}\n\n"
                
                # 处理智能体最终消息
                elif isinstance(item, TextMessage):
                    if hasattr(item, 'source'):
                        current_agent = item.source
                    
                    # 如果是user智能体的消息，说明用户评审完成
                    if item.source == "user":
                        yield 'data: {"content": "\\n\\n--- 用户评审完成 ---"}\n\n'
                        break
                
                # 处理任务完成
                elif isinstance(item, TaskResult):
                    yield "data: [DONE]\n\n"
                    break
            
            # 发送完成信号
            yield "data: [DONE]\n\n"
                
        except Exception as e:
            print(f"Error in AutoGen service: {e}")
            import traceback
            traceback.print_exc()
            # 发送错误信息
            error_msg = f"抱歉，发生了错误：{str(e)}"
            for char in error_msg:
                escaped_char = char.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                yield f"data: {{\"content\": \"{escaped_char}\"}}\n\n"
            yield f"data: [DONE]\n\n"
    
    async def get_full_response(self, message: str) -> str:
        """
        Get full response from multi-agent team (non-streaming)
        
        Args:
            message: User message to process
            
        Returns:
            Complete response string
        """
        try:
            result = await self.team.run(task=message)
            # 合并所有消息
            all_messages: list[str] = []
            for msg in result.messages:
                if isinstance(msg, TextMessage):
                    role_name = {
                        "primary": "【测试用例设计师】",
                        "critic": "【测试用例评审师】",
                        "user": "【用户评审】"
                    }.get(msg.source, f"【{msg.source}】")
                    all_messages.append(f"{role_name}\n{msg.content}\n")
            return "\n".join(all_messages) if all_messages else "抱歉，我无法生成回复。"
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"抱歉，发生了错误：{str(e)}"
