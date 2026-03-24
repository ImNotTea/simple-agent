from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chainlit UI"
    API_V1_STR: str = "/api/v1"
    GROQ_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    """Cache settings for better performance"""
    return Settings()