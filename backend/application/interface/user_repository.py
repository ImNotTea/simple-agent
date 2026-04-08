from abc import ABC, abstractmethod

class UserRepository(ABC):
    """Abstract base class for user repository, defining the interface for user data storage and retrieval"""
    
    @abstractmethod
    def save_user(self, user_id: str, user_data: dict) -> None:
        """Save a user to the repository"""
        pass
    
    @abstractmethod
    def get_user(self, user_id: str) -> dict:
        """Retrieve a user from the repository by their ID"""
        pass