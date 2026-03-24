from abc import ABC, abstractmethod

class LLMClient(ABC):
    """Abstract base class for LLM Client to define the interface for interacting with language models"""
    
    @abstractmethod
    def send_message(self, message: str) -> str:
        """Send a message to the language model and receive a response"""
        pass
    
    @abstractmethod
    def stream_response(self, message: str):
        """Send a message to the language model and receive a streaming response"""
        pass