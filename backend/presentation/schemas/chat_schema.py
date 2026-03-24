from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Schema for chat request"""
    role: str = Field(..., description="Role of the message sender, e.g., 'user' or 'assistant'", min_length=1)
    message: str = Field(..., description="Content of the message", min_length=1)


class ChatResponse(BaseModel):
    """Schema for chat response"""
    result: str = Field(..., description="Response from the chat bot")
