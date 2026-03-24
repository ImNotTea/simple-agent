from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from functools import lru_cache

class LLMSettings(BaseModel):
    """Settings related to LLM API keys and configurations"""
    temperature: float

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI + Chainlit Chatbot"
    API_V1_STR: str = "/api/v1"
    
    # LLM related settings
    LLM_TEMPERATURE: float = 0.7
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')
    
    # Define gettings for LLM configurations
    def get_llm_settings(self) -> LLMSettings:
        """Get LLM related settings as a structured object"""
        return LLMSettings(
            temperature=self.LLM_TEMPERATURE
        )

@lru_cache()
def get_settings():
    """Cache settings for better performance"""
    return Settings()