from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.core.database import engine, Base
from app.core.config import settings
from app.api import projects, test_points, test_cases, knowledge_bases, settings as settings_api, batches

# 配置日志
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/app.log", rotation="10 MB", level="DEBUG")

# 创建FastAPI应用
app = FastAPI(
    title="AI测试用例生成平台",
    description="AI驱动的测试用例生成平台，支持PRD文档解析、测试点提取、测试用例生成",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(projects.router, prefix="/api/v1")
app.include_router(test_points.router, prefix="/api/v1")
app.include_router(test_cases.router, prefix="/api/v1")
app.include_router(knowledge_bases.router, prefix="/api/v1")
app.include_router(settings_api.router, prefix="/api/v1")
app.include_router(batches.router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    """应用启动时执行"""
    logger.info("正在启动应用...")
    
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("应用启动完成")


@app.on_event("shutdown")
async def shutdown():
    """应用关闭时执行"""
    logger.info("正在关闭应用...")
    await engine.dispose()
    logger.info("应用已关闭")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI测试用例生成平台 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
