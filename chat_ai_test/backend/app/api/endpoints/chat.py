from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.autogen_service import AutoGenService
from app.core.config import settings

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"

# 创建全局单例
autogen_service = AutoGenService()

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream chat responses using SSE
    """
    async def generate():
        try:
            async for chunk in autogen_service.get_response(request.message):
                yield chunk
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield 'data: {"error": "' + str(e) + '"}\n\n'
            yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )

@router.post("/message")
async def send_message(request: ChatRequest):
    """
    Send a message and get response (non-streaming)
    """
    try:
        service = AutoGenService()
        response = await service.get_full_response(request.message)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
