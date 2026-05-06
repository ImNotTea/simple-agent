from application.interface.idempotency_cache import IdempotencyCache
import redis
from config.settings import RedisSettings

class RedisIdempotencyCache(IdempotencyCache):
    """Redis-based implementation of the IdempotencyCache interface, using Redis to store and retrieve cached responses based on request IDs"""
    
    def __init__(self, redis_settings: RedisSettings):
        self.redis_settings = redis_settings
        if redis_settings.password:
            redis_url = f"redis://:{redis_settings.password.get_secret_value()}@{redis_settings.host}:{redis_settings.port}/{redis_settings.db}"
        else:
            redis_url = f"redis://{redis_settings.host}:{redis_settings.port}/{redis_settings.db}"
            
        self.redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
        self.prefix = redis_settings.idem_prefix
        
    def save_response(self, request_id: str, response: str) -> None:
        """Save a response to Redis with the request ID as the key and a TTL of 1 hour"""
        self.redis_client.set(f"{self.prefix}:{request_id}", response, ex=self.redis_settings.idem_cache_ttl)
        
    def get_response(self, request_id: str) -> str | None:
        """Retrieve a cached response from Redis by its request ID, or return None if not found"""
        return self.redis_client.get(f"{self.prefix}:{request_id}")