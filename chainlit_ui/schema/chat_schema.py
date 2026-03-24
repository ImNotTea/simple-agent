from pydantic import BaseModel, Field

class RequestMessage(BaseModel):
    """Schema for individual messages in the chat"""
    role: str = Field(..., description="Role of the message sender, e.g., 'user' or 'assistant'")
    message: str = Field(..., description="Content of the message")