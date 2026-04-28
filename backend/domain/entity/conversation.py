from dataclasses import dataclass, field
from domain.entity.message import Message
import uuid

@dataclass
class Conversation:
    id: str
    messages: list[Message] = field(default_factory=list)
    
    @staticmethod
    def create(messages: list[Message | None] = None) -> "Conversation":
        """Factory method to create a new Conversation instance with a unique ID"""
        return Conversation(
            id=str(uuid.uuid4()),
            messages=messages or []
        )
        
    def add_message(self, message: Message) -> None:
        """Add a message to the conversation's message list"""
        self.messages.append(message)