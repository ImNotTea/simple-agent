# Adapter for LLMClient to interact with Groq LLM API
from application.interface.llm_client import LLMClient
from config.settings import LLMSettings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from typing import AsyncGenerator

# Use GroqClient to implement the LLMClient interface for interacting with Groq LLM API
class GroqLLMClient(LLMClient):
    """Adapter for LLMClient to interact with Groq LLM API"""
    
    def __init__(self, llm_settings: LLMSettings, model_name: str = "openai/gpt-oss-20b"):
        # Initialize ChatGroq with API key and settings
        self.client = ChatGroq(
            model=model_name, 
            temperature=llm_settings.temperature
        )
    
    def send_message(self, message: str) -> str:
        """Send a message to the Groq LLM and receive a response"""
        # Use invoke() method with HumanMessage
        response = self.client.invoke([HumanMessage(content=message)])
        return response.content
    
    async def stream_response(self, message: str) -> AsyncGenerator:
        """Send a message to the Groq LLM and receive a streaming response"""
        # Use astream() method with HumanMessage
        async for chunk in self.client.astream([HumanMessage(content=message)]):
            if chunk.content:
                yield chunk.content