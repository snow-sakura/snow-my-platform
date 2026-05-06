from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.sse_handler import sse_handler
from fastapi.responses import StreamingResponse
from app.config import Config
from app.file_handler import FileHandler

app = FastAPI(
    title="AutoGen Chat API",
    description="FastAPI backend for AutoGen multi-agent chat with DeepSeek",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "autogen-chat-api"}


# 请求模型
class ChatRequest(BaseModel):
    session_id: str
    content: str
    attachment: Optional[str] = None  # 附件文本内容


@app.post("/api/session")
async def create_session():
    """创建新会话"""
    session_id = await sse_handler.create_session()
    return {"session_id": session_id}


@app.post("/api/chat")
async def send_message(request: ChatRequest):
    """接收用户消息"""
    try:
        await sse_handler.send_message(
            request.session_id, 
            request.content,
            request.attachment
        )
        return {"status": "message_sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传文件并提取文本"""
    try:
        content = await file.read()
        text = await FileHandler.extract_text_from_file(content, file.filename)
        return {"filename": file.filename, "content": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/stream/{session_id}")
async def stream_response(session_id: str):
    """SSE流式响应端点"""
    return StreamingResponse(
        sse_handler.stream_events(session_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )


if __name__ == "__main__":
    import uvicorn
    config = Config()
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,
        log_level="info"
    )
