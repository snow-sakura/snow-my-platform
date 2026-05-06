import asyncio
import json
import uuid
from datetime import datetime, date
from typing import AsyncGenerator, Dict, Any, Optional
from fastapi import HTTPException
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from .team_manager import team_manager


class SSEHandler:
    """SSE (Server-Sent Events) 处理器"""

    def __init__(self):
        # 会话管理: {session_id: {"queue": asyncio.Queue, "team": team, "active": bool}}
        self.sessions: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def _custom_json_serializer(obj):
        """自定义 JSON 序列化器，处理 datetime 等类型"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    async def create_session(self) -> str:
        """创建新会话，返回session_id"""
        session_id = str(uuid.uuid4())
        
        # 创建用户输入函数 (通过队列传递)
        input_queue = asyncio.Queue()
        
        async def user_input_func(prompt: str, cancellation_token=None) -> str:
            """从队列获取用户输入"""
            try:
                # 设置等待输入标志
                if session_id in self.sessions:
                    self.sessions[session_id]["waiting_for_input"] = True
                
                # 将提示放入队列（前端可以显示）
                await self._send_to_session(session_id, {
                    "type": "UserInputRequest",
                    "content": prompt,
                    "source": "system"
                })
                
                # 等待用户响应
                user_message = await input_queue.get()
                
                # 清除等待输入标志
                if session_id in self.sessions:
                    self.sessions[session_id]["waiting_for_input"] = False
                
                return user_message
            except Exception as e:
                print(f"Error getting user input: {e}")
                # 清除等待输入标志
                if session_id in self.sessions:
                    self.sessions[session_id]["waiting_for_input"] = False
                return "TERMINATE"
        
        # 创建团队
        team = await team_manager.create_team(user_input_func)
        
        # 存储会话信息
        self.sessions[session_id] = {
            "queue": input_queue,
            "team": team,
            "active": True,
            "waiting_for_input": False  # 标记是否在等待用户输入
        }
        
        print(f"Session created: {session_id}")
        return session_id

    async def send_message(self, session_id: str, content: str, attachment: Optional[str] = None):
        """接收用户消息并触发AI处理"""
        if session_id not in self.sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = self.sessions[session_id]
        
        if not session.get("active", False):
            raise HTTPException(status_code=400, detail="Session is not active")
        
        # 如果正在等待用户输入，将消息放入输入队列而不是触发新对话
        if session.get("waiting_for_input", False):
            print(f"[DEBUG] Received user input while waiting for session {session_id}")
            await session["queue"].put(content)
            return
        
        # 如果已经有正在运行的对话任务，拒绝新消息
        if session.get("task") and not session.get("task").done():
            raise HTTPException(status_code=400, detail="A conversation is already in progress")
        
        # 检查是否有活跃的SSE流（即event_queue存在）
        if "event_queue" not in session:
            raise HTTPException(status_code=400, detail="No active SSE stream. Please refresh the page.")
        
        print(f"[DEBUG] Sending message to session {session_id}: {content[:50]}...")
        if attachment:
            print(f"[DEBUG] Message has attachment ({len(attachment)} chars)")
        
        # 发送处理中状态
        await self._send_to_session(session_id, {
            "type": "processing",
            "status": "processing"
        })
        
        # 在后台启动对话处理
        task = asyncio.create_task(self._process_conversation(session_id, content, attachment))
        session["task"] = task
        
        # 添加任务完成回调，用于捕获异常
        def task_done_callback(t):
            try:
                t.result()  # 这会重新抛出异常（如果有）
                print(f"[DEBUG] Conversation task completed successfully for session {session_id}")
            except Exception as e:
                print(f"[ERROR] Conversation task failed for session {session_id}: {e}")
                import traceback
                traceback.print_exc()
        
        task.add_done_callback(task_done_callback)

    async def _process_conversation(self, session_id: str, user_content: str, attachment: Optional[str] = None):
        """处理对话并流式推送结果"""
        print(f"[DEBUG] Starting conversation processing for session {session_id}")
        
        if session_id not in self.sessions:
            print(f"[ERROR] Session {session_id} not found in _process_conversation")
            return
        
        session = self.sessions[session_id]
        team = session["team"]
        
        try:
            # 如果有附件，将附件内容附加到用户消息
            full_content = user_content
            if attachment:
                full_content = f"附件内容：\n{attachment}\n\n用户需求：\n{user_content}"
                print(f"[DEBUG] Attached content ({len(attachment)} chars) to message")
            
            # 创建用户消息
            user_message = TextMessage(
                content=full_content,
                source="user"
            )
            
            print(f"[DEBUG] Running team stream with message: {user_content[:50]}...")
            
            # 运行流式对话
            stream = team.run_stream(task=user_message)
            
            # 收集所有消息,按智能体分组
            collected_messages = {}
            message_count = 0
            
            async for message in stream:
                message_count += 1
                print(f"[DEBUG] Received message {message_count} from stream")
                
                # 跳过 TaskResult
                if isinstance(message, TaskResult):
                    print(f"[DEBUG] Received TaskResult, saving state...")
                    # 保存状态和历史
                    await team_manager.save_team_state(team)
                    await team_manager.save_history(message.messages)
                    
                    # 发送完成信号
                    await self._send_to_session(session_id, {
                        "type": "done",
                        "status": "completed"
                    })
                    print(f"[DEBUG] Sent done signal to session {session_id}")
                    continue
                
                # 只收集 assistant 的消息,过滤掉 user_proxy 的中间对话
                message_data = message.model_dump()
                source = message_data.get("source", "unknown")
                
                print(f"[DEBUG] Message from source: {source}, content: {message_data.get('content', '')[:50]}...")
                
                # 只过滤 user_proxy 的消息，保留 user 和 assistant 的消息
                if source == "user_proxy":
                    print(f"[DEBUG] Skipping user_proxy message")
                    continue
                
                # 按智能体分组收集
                if source not in collected_messages:
                    collected_messages[source] = []
                collected_messages[source].append(message_data.get("content", ""))
            
            print(f"[DEBUG] Stream completed with {message_count} messages, {len(collected_messages)} agents")
            print(f"[DEBUG] Collected messages from agents: {list(collected_messages.keys())}")
            
            # 流式对话结束后,发送分组后的消息
            if not collected_messages:
                print(f"[WARN] No messages collected from assistant, sending default response")
                response_data = {
                    "type": "AgentResponse",
                    "source": "assistant",
                    "content": "对话完成，但没有收到助手的回复。",
                    "timestamp": datetime.now().isoformat()
                }
                await self._send_to_session(session_id, response_data)
            else:
                for source, contents in collected_messages.items():
                    # 合并同一智能体的所有消息
                    merged_content = "\n\n".join(contents)
                    response_data = {
                        "type": "AgentResponse",
                        "source": source,
                        "content": merged_content,
                        "timestamp": datetime.now().isoformat()
                    }
                    print(f"[DEBUG] Sending AgentResponse from {source}: {merged_content[:50]}...")
                    await self._send_to_session(session_id, response_data)
                    print(f"[DEBUG] Sent AgentResponse to session {session_id}")
            
            print(f"[DEBUG] Conversation processing completed for session {session_id}")
                
        except Exception as e:
            error_msg = {
                "type": "error",
                "content": f"Error during conversation: {str(e)}",
                "source": "system"
            }
            print(f"[ERROR] Conversation error for session {session_id}: {e}")
            import traceback
            traceback.print_exc()
            
            try:
                await self._send_to_session(session_id, error_msg)
                print(f"[DEBUG] Sent error message to session {session_id}")
            except Exception as send_error:
                print(f"[ERROR] Failed to send error message: {send_error}")

    async def _send_to_session(self, session_id: str, data: dict):
        """向指定会话发送数据（如果该会话有活跃的SSE连接）"""
        # 这个方法会在stream_events中被实际使用
        # 这里我们先将数据存入一个临时队列
        if session_id in self.sessions:
            session = self.sessions[session_id]
            if "event_queue" in session:
                await session["event_queue"].put(data)

    async def stream_events(self, session_id: str) -> AsyncGenerator[str, None]:
        """SSE事件流生成器"""
        if session_id not in self.sessions:
            # 在流式响应开始前检查 Session，如果不存在则直接返回
            # 避免在 yield 之后抛出 HTTPException 导致 RuntimeError
            print(f"[WARN] Stream requested for non-existent session: {session_id}")
            return
        
        session = self.sessions[session_id]
        
        # 创建事件队列
        event_queue = asyncio.Queue()
        session["event_queue"] = event_queue
        
        print(f"[DEBUG] SSE stream started for session {session_id}")
        
        try:
            # 发送连接成功事件
            yield self._format_sse_event("connected", {
                "session_id": session_id,
                "status": "connected"
            })
            print(f"[DEBUG] Sent connected event to session {session_id}")
            
            # 持续监听事件队列 - 不设置超时，不主动退出
            # FastAPI/Starlette会在客户端断开时取消这个generator
            while True:
                try:
                    # 等待事件，设置合理的超时用于检测连接状态
                    data = await asyncio.wait_for(event_queue.get(), timeout=60.0)
                    
                    print(f"[DEBUG] Sending event from queue: {data.get('type', 'unknown')}")
                    
                    # 格式化并发送SSE事件
                    event_type = data.get("type", "message")
                    yield self._format_sse_event(event_type, data)
                    print(f"[DEBUG] Yielded {event_type} event")
                    
                    # done/error事件只通知前端，不终止流
                    # 前端需要继续保持连接以接收后续对话
                    
                except asyncio.TimeoutError:
                    # 超时，发送keep-alive注释保持连接
                    print(f"[DEBUG] Timeout, sending keep-alive")
                    yield ": keep-alive\n\n"
                    
        except asyncio.CancelledError:
            # 客户端断开连接时会触发
            print(f"[DEBUG] SSE stream cancelled for session {session_id} (client disconnected)")
        except Exception as e:
            print(f"[ERROR] SSE stream error for session {session_id}: {e}")
            import traceback
            traceback.print_exc()
            try:
                yield self._format_sse_event("error", {
                    "type": "error",
                    "content": f"Stream error: {str(e)}"
                })
            except:
                pass
        finally:
            # 只清理event_queue，不删除session
            if "event_queue" in session:
                del session["event_queue"]
            print(f"[DEBUG] SSE stream cleanup completed for session {session_id}")

    @staticmethod
    def _format_sse_event(event_type: str, data: dict) -> str:
        """格式化SSE事件"""
        json_data = json.dumps(data, default=SSEHandler._custom_json_serializer)
        return f"event: {event_type}\ndata: {json_data}\nretry: 3000\n\n"


# 全局SSE处理器实例
sse_handler = SSEHandler()
