from abc import ABC, abstractmethod
from domain.entity.conversation import Conversation

class ConversationRepository(ABC):
    """Abstract base class for conversation repository, defining the interface for conversation data storage and retrieval"""
    
    @abstractmethod
    async def save_conversation(self, conversation: Conversation) -> str | None:
        """
        Save a conversation to the repository
        Returns the ID of the saved conversation or None if saving failed
        """
        pass
    
    @abstractmethod
    async def update_conversation(self, conversation: Conversation) -> bool:
        """
        Update an existing conversation in the repository
        Returns True if the update was successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def get_conversation(self, conversation_id: str) -> Conversation | None:
        """
        Retrieve a conversation from the repository by its ID
        Returns a Conversation object or None if the conversation is not found
        """
        pass