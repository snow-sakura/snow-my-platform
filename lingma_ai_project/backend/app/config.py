import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置管理"""

    # DeepSeek API 配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError(
                "DEEPSEEK_API_KEY is not set. Please copy .env.example to .env and configure your API key."
            )
        return True

    @classmethod
    def get_model_config(cls) -> dict:
        """获取模型配置字典"""
        return {
            "model": cls.DEEPSEEK_MODEL,
            "api_key": cls.DEEPSEEK_API_KEY,
            "base_url": cls.DEEPSEEK_BASE_URL,
        }

    @classmethod
    def get_model_info(cls) -> dict:
        """获取模型能力信息（用于非 OpenAI 官方模型）"""
        return {
            "vision": False,  # DeepSeek 不支持视觉
            "function_calling": True,  # 支持函数调用
            "json_output": True,  # 支持 JSON 输出
            "family": "unknown",  # 模型家族
            "structured_output": False,  # 是否支持结构化输出
        }
