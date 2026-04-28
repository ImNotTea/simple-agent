from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chainlit UI"
    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

@lru_cache()
def get_settings():
    """Cache settings for better performance"""
    return Settings()