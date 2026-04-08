from pydantic import BaseModel, Field
from application.dto.chat_dto import ChatRequestDTO


class MessageSchema(BaseModel):
    """Schema for chat request"""
    conversation_id: str | None = Field(None, description="ID of the conversation, if it's part of an existing conversation")
    role: str = Field(..., description="Role of the message sender, e.g., 'user' or 'assistant'", min_length=1)
    message: str = Field(..., description="Content of the message", min_length=1)
    
    def to_dto(self):
        """Convert the RequestMessage to a ChatRequestDTO"""
        
        return ChatRequestDTO(
            conversation_id=self.conversation_id,
            role=self.role,
            message=self.message or ""
        )


class ChatResponse(BaseModel):
    """Schema for chat response"""
    result: str = Field(..., description="Response from the chat bot")
