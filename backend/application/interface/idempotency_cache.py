from abc import ABC, abstractmethod

class IdempotencyCache(ABC):
    """Abstract base class for idempotency cache, defining the interface for storing and retrieving idempotency keys and their associated responses"""
    
    @abstractmethod
    def save_response(self, request_id: str, response: str) -> None:
        """Save a response to the cache with the given request ID as the key"""
        pass
    
    @abstractmethod
    def get_response(self, request_id: str) -> str | None:
        """Retrieve a cached response by its request ID, or return None if not found"""
        pass