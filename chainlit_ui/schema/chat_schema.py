from pydantic import BaseModel, Field

class MessageSchema(BaseModel):
    """Schema for chat request"""
    conversation_id: str | None = Field(None, description="ID of the conversation, if it's part of an existing conversation")
    role: str = Field(..., description="Role of the message sender, e.g., 'user' or 'assistant'", min_length=1)
    message: str = Field(..., description="Content of the message", min_length=1)