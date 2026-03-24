import json
from typing import AsyncGenerator

from application.interfaces.llm_client import LLMClient

class ChatUseCase:
    """Chat use case class to handle chat interactions and business logic"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        # Initialize any necessary attributes, e.g., message history, user context, etc.
        self.message_history = []
        
    async def process_message(self, message: dict[str, str]) -> AsyncGenerator[str, None]:
        """Process a user message and return a response from the LLM"""        
        # Get response from LLM client
        async for chunk in self.llm_client.stream_response(message.get("content", "")):
            yield chunk 