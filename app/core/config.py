import os
from pydantic_settings import BaseSettings
from typing import Optional

# 获取当前环境，默认为 development
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "用户管理系统 API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str
    
    # JWT 配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 邮件配置
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.qq.com"
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # 基础 URL
    BASE_URL: str = "http://127.0.0.1:8000"
    
    class Config:
        # 根据环境加载对应的 .env 文件
        env_file = f".env.{ENVIRONMENT}"
        case_sensitive = True

settings = Settings()