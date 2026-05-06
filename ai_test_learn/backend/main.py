"""
测试用例智能生成系统 - FastAPI 后端服务
提供文件上传、SSE流式输出、Excel导出等功能
"""
import json
import os
import tempfile
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel, Field

from testcase_service import TestCaseService

# 全局服务实例
service: Optional[TestCaseService] = None


class TestCaseRequest(BaseModel):
    """测试用例生成请求"""
    context: str = Field(default="", description="上下文背景信息")
    requirements: str = Field(default="", description="用户具体要求")
    analysis_result: str = Field(default="", description="图片分析结果（用于直接生成测试用例）")


class TestCaseExportRequest(BaseModel):
    """测试用例导出请求"""
    testcases: list = Field(..., description="测试用例列表")
    filename: Optional[str] = Field(default=None, description="导出文件名")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期管理"""
    global service
    service = TestCaseService()
    print("✅ 测试用例生成服务已启动")
    yield
    if service:
        await service.close()
        print("👋 测试用例生成服务已关闭")


app = FastAPI(
    title="测试用例智能生成系统 API",
    description="基于 AutoGen 0.7.5 + 多模态大模型的测试用例自动生成服务",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health() -> dict:
    """健康检查接口"""
    return {
        "status": "ok",
        "service": "testcase-generator",
        "version": "1.0.0"
    }


@app.post("/api/analyze-image")
async def analyze_image(
    file: UploadFile = File(..., description="思维导图/流程图/界面截图"),
    context: str = Form(default="", description="上下文背景信息"),
    requirements: str = Form(default="", description="用户具体要求")
) -> StreamingResponse:
    """
    分析上传的图片，提取测试需求
    
    支持：思维导图、流程图、界面原型图、需求文档截图等
    """
    if not service:
        raise HTTPException(status_code=503, detail="服务未就绪")
    
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的文件类型: {file.content_type}，请上传图片文件"
        )
    
    try:
        # 读取图片数据
        image_data = await file.read()
        
        if len(image_data) > 10 * 1024 * 1024:  # 10MB 限制
            raise HTTPException(status_code=400, detail="图片大小超过10MB限制")
        
        async def event_stream() -> AsyncGenerator[str, None]:
            try:
                async for chunk in service.analyze_image_stream(
                    image_data=image_data,
                    context=context,
                    requirements=requirements
                ):
                    yield f"data: {chunk}\n\n"
                
                # 发送完成标记
                done = json.dumps({"type": "done"}, ensure_ascii=False)
                yield f"data: {done}\n\n"
                
            except Exception as exc:
                err = json.dumps({"type": "error", "error": str(exc)}, ensure_ascii=False)
                yield f"data: {err}\n\n"
        
        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片处理失败: {str(e)}")


@app.post("/api/generate-testcases")
async def generate_testcases(request: TestCaseRequest) -> StreamingResponse:
    """
    基于分析结果生成测试用例
    
    如果提供了 analysis_result，则直接生成测试用例
    否则需要先调用 /api/analyze-image 获取分析结果
    """
    if not service:
        raise HTTPException(status_code=503, detail="服务未就绪")
    
    if not request.analysis_result:
        raise HTTPException(status_code=400, detail="缺少分析结果，请先上传图片进行分析")
    
    async def event_stream() -> AsyncGenerator[str, None]:
        try:
            async for chunk in service.generate_testcases_stream(
                analysis_result=request.analysis_result,
                context=request.context,
                requirements=request.requirements
            ):
                yield f"data: {chunk}\n\n"
            
            # 发送完成标记
            done = json.dumps({"type": "done"}, ensure_ascii=False)
            yield f"data: {done}\n\n"
            
        except Exception as exc:
            err = json.dumps({"type": "error", "error": str(exc)}, ensure_ascii=False)
            yield f"data: {err}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/api/generate-all")
async def generate_all(
    file: UploadFile = File(..., description="思维导图/流程图/界面截图"),
    context: str = Form(default="", description="上下文背景信息"),
    requirements: str = Form(default="", description="用户具体要求")
) -> StreamingResponse:
    """
    一键生成：分析图片 + 生成测试用例（完整流程）
    """
    if not service:
        raise HTTPException(status_code=503, detail="服务未就绪")
    
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的文件类型: {file.content_type}"
        )
    
    try:
        image_data = await file.read()
        
        if len(image_data) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="图片大小超过10MB限制")
        
        async def event_stream() -> AsyncGenerator[str, None]:
            analysis_result = ""
            
            try:
                # 阶段1：图片分析
                yield f"data: {json.dumps({'type': 'stage', 'stage': 'analysis_start', 'message': '正在分析图片...'}, ensure_ascii=False)}\n\n"
                
                async for chunk in service.analyze_image_stream(
                    image_data=image_data,
                    context=context,
                    requirements=requirements
                ):
                    data = json.loads(chunk)
                    if data.get("type") == "analysis":
                        analysis_result += data.get("content", "")
                    yield f"data: {chunk}\n\n"
                
                yield f"data: {json.dumps({'type': 'stage', 'stage': 'analysis_complete', 'message': '图片分析完成'}, ensure_ascii=False)}\n\n"
                
                # 阶段2：生成测试用例
                yield f"data: {json.dumps({'type': 'stage', 'stage': 'generation_start', 'message': '正在生成测试用例...'}, ensure_ascii=False)}\n\n"
                
                async for chunk in service.generate_testcases_stream(
                    analysis_result=analysis_result,
                    context=context,
                    requirements=requirements
                ):
                    yield f"data: {chunk}\n\n"
                
                # 完成
                done = json.dumps({"type": "done"}, ensure_ascii=False)
                yield f"data: {done}\n\n"
                
            except Exception as exc:
                err = json.dumps({"type": "error", "error": str(exc)}, ensure_ascii=False)
                yield f"data: {err}\n\n"
        
        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@app.post("/api/export-excel")
async def export_excel(request: TestCaseExportRequest):
    """
    导出测试用例为 Excel 文件
    """
    if not service:
        raise HTTPException(status_code=503, detail="服务未就绪")
    
    if not request.testcases:
        raise HTTPException(status_code=400, detail="测试用例列表为空")
    
    try:
        # 生成 Excel 文件
        filename = request.filename or f"测试用例_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        excel_buffer = service.export_to_excel(request.testcases, filename)
        
        # 保存临时文件
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        
        with open(temp_path, 'wb') as f:
            f.write(excel_buffer.getvalue())
        
        return FileResponse(
            path=temp_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@app.get("/api/download-template")
async def download_template():
    """
    下载测试用例模板
    """
    try:
        # 创建示例测试用例
        sample_testcases = [
            {
                "id": "TC-001",
                "title": "示例测试用例-用户登录成功",
                "module": "用户管理",
                "precondition": "用户已注册，账号状态正常",
                "steps": ["打开登录页面", "输入正确的用户名", "输入正确的密码", "点击登录按钮"],
                "expected_result": "登录成功，跳转到首页",
                "priority": "P0",
                "test_type": "功能"
            },
            {
                "id": "TC-002",
                "title": "示例测试用例-用户登录失败-密码错误",
                "module": "用户管理",
                "precondition": "用户已注册",
                "steps": ["打开登录页面", "输入正确的用户名", "输入错误的密码", "点击登录按钮"],
                "expected_result": "提示密码错误，登录失败",
                "priority": "P1",
                "test_type": "功能"
            }
        ]
        
        if not service:
            raise HTTPException(status_code=503, detail="服务未就绪")
        
        excel_buffer = service.export_to_excel(sample_testcases, "测试用例模板.xlsx")
        
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "测试用例模板.xlsx")
        
        with open(temp_path, 'wb') as f:
            f.write(excel_buffer.getvalue())
        
        return FileResponse(
            path=temp_path,
            filename="测试用例模板.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模板生成失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
