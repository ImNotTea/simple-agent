from abc import ABC, abstractmethod
from email.message import Message

class MessageRepository(ABC):
    """Abstract base class for message repository, defining the interface for message data storage and retrieval"""
    
    @abstractmethod
    async def save_message(self, message: Message) -> None:
        """Save a message to the repository under the specified conversation ID"""
        pass
    
    @abstractmethod
    async def update_message_status(self, message_id: str, status: str) -> bool:
        """Update the status of a message in the repository"""
        pass
    
    @abstractmethod
    async def get_messages(self, message_id: str) -> list[Message | None]:
        """Retrieve all messages for a given conversation ID from the repository"""
        pass