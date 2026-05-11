import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = (
        "mysql+aiomysql://snow:your_password@localhost:3306/test_platform"
    )
    
    # LLM配置
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4"
    LLM_BASE_URL: Optional[str] = None
    
    # 飞书配置
    FEISHU_WEBHOOK_URL: Optional[str] = None
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    KNOWLEDGE_BASE_DIR: str = "knowledge_base"
    
    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# 确保目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.KNOWLEDGE_BASE_DIR, exist_ok=True)
