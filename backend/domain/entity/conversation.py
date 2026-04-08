from dataclasses import dataclass
from domain.entity.message import Message
import uuid

@dataclass
class Conversation:
    id: str # Unique identifier for the conversation
    messages: list[Message | None]
    
    @staticmethod
    def create(messages: list[Message | None] = []) -> "Conversation":
        """Factory method to create a new Conversation instance with a unique ID"""
        return Conversation(
            id=str(uuid.uuid4()),
            messages=messages
        )
        
    def add_message(self, message: Message) -> None:
        """Add a message to the conversation's message list"""
        self.messages.append(message)