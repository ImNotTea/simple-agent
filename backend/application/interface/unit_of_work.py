from abc import ABC, abstractmethod
from backend.application.interface.conversation_repository import ConversationRepository
from backend.application.interface.message_repository import MessageRepository

class UnitOfWork(ABC):
    """Abstract base class for Unit of Work pattern to manage database transactions and repositories"""
    @property
    @abstractmethod
    def messages(self) -> MessageRepository:
        """Return the message repository for managing message data"""
        pass
    
    @property
    @abstractmethod
    def conversations(self) -> ConversationRepository:
        """Return the conversation repository for managing conversation data"""
        pass
    
    async def __aenter__(self):
        """Enter the runtime context related to this object, typically used for managing transactions"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context and handle transaction commit or rollback based on exceptions"""
        pass
    
    @abstractmethod
    async def commit(self):
        """Commit the current transaction"""
        pass
    
    @abstractmethod
    async def rollback(self):
        """Rollback the current transaction"""
        pass