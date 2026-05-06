from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # AutoGen configuration
    AUTOGEN_MODEL: str = "Qwen/Qwen2-VL-72B-Instruct"
    API_BASE_URL: str = "https://api.siliconflow.cn/v1"
    AUTOGEN_API_KEY: str = "sk-ruglbzcanhfmsmtxyjeuoxpfirurmdynhkepktnrwrtibzlo"
    AUTOGEN_TEMPERATURE: float = 0.7
    AUTOGEN_MAX_TOKENS: int = 2000
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()
