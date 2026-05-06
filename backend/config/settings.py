from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field, SecretStr
from functools import lru_cache

class LLMSettings(BaseModel):
    """Settings related to LLM API keys and configurations"""
    temperature: float
    
class DBSettings(BaseModel):
    """Settings related to database connections"""
    host: str
    port: int
    user: str
    password: SecretStr
    database: str
    db_schema: str
    pool_size: int
    max_overflow: int
    pool_recycle: int  # Recycle connections after 1 hour of inactivity
    
class RedisSettings(BaseModel):
    """Settings related to Redis connections"""
    host: str
    port: int
    password: SecretStr | None = None
    db: int = 0
    idem_cache_ttl: int = Field(default=3600, description="Time-to-live for idempotency cache entries in seconds")
    idem_prefix: str = Field(default="chat:idem", description="Prefix for idempotency cache keys in Redis")
    
class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI + Chainlit Chatbot"
    API_V1_STR: str = "/api/v1"
    
    # DB related settings
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5433)
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: SecretStr = Field(default=SecretStr("password"))
    DB_NAME: str = Field(default="chatbot_db")
    DB_SCHEMA: str = Field(default="public")
    DB_POOL_SIZE: int = Field(default=1)
    DB_MAX_OVERFLOW: int = Field(default=10)
    DB_POOL_RECYCLE: int = Field(default=3600)
    
    # Redis related settings
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: SecretStr | None = Field(default=None)
    REDIS_DB: int = Field(default=0)
    IDEM_CACHE_TTL: int = Field(default=3600, description="Time-to-live for idempotency cache entries in seconds")
    IDEM_PREFIX: str = Field(default="chat:idem", description="Prefix for idempotency cache keys in Redis")

    # LLM related settings
    LLM_TEMPERATURE: float = Field(default=0.7)
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')
    
    # Define gettings for LLM configurations
    def get_llm_settings(self) -> LLMSettings:
        """Get LLM related settings as a structured object"""
        return LLMSettings(
            temperature=self.LLM_TEMPERATURE
        )
    
    # Define settings for database connections
    def get_db_settings(self) -> DBSettings:
        """Get database related settings as a structured object"""
        return DBSettings(
            host=self.DB_HOST,
            port=self.DB_PORT,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            database=self.DB_NAME,
            db_schema=self.DB_SCHEMA,
            pool_size=self.DB_POOL_SIZE,
            max_overflow=self.DB_MAX_OVERFLOW,
            pool_recycle=self.DB_POOL_RECYCLE
        )
        
    # Define settings for Redis connections
    def get_redis_settings(self) -> RedisSettings:
        """Get Redis related settings as a structured object"""
        return RedisSettings(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            password=self.REDIS_PASSWORD,
            db=self.REDIS_DB,
            idem_cache_ttl=self.IDEM_CACHE_TTL,
            idem_prefix=self.IDEM_PREFIX
        )

@lru_cache()
def get_settings():
    """Cache settings for better performance"""
    return Settings()