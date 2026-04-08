from dataclasses import dataclass
import uuid

@dataclass
class Message:
    role: str
    content: str
    status: str  # Status to track message state (e.g., 'pending', 'success', 'failed')
    id: str = ""  # Unique identifier for the message
    conversation_id: str = ""  # ID of the conversation this message belongs to
    
    @staticmethod
    def create(conversation_id: str, role: str, content: str, id: str = None, status: str = "pending") -> "Message":
        """Factory method to create a new Message instance with a unique ID"""
        return Message(
            id=id or str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            status=status
        )
        
    def mark_as_success(self) -> None:
        """Update the message status to 'success'"""
        self.status = "success"
        
    def mark_as_failed(self) -> None:
        """Update the message status to 'failed'"""
        self.status = "failed"
        
    
        
    