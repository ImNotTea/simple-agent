from application.interface.conversation_repository import ConversationRepository
from application.interface.unit_of_work import UnitOfWork
from application.interface.message_repository import MessageRepository
from infrastructure.persistence.database.db import Database
from infrastructure.persistence.repository.pg_conversation_repository import PGConversationRepository
from infrastructure.persistence.repository.pg_message_repository import PGMessageRepository
from logging import getLogger

logger = getLogger(__name__)

class UOW(UnitOfWork):
    """Unit of Work pattern implementation for managing database transactions and repositories"""
    
    def __init__(self, db: Database):
        self.db = db
        self._session = None  # Initialize session to None, will be set in __aenter__
        self._conversation_repository = None
        self._message_repository = None
        
    @property
    def messages(self):
        if self._message_repository is None:
            self._message_repository = PGMessageRepository(self._session)
        return self._message_repository
        
    @property
    def conversations(self):
        if self._conversation_repository is None:
            self._conversation_repository = PGConversationRepository(self._session)
        return self._conversation_repository
    
    async def _init_session(self):
        self._session = await self.db.get_session()
    
    async def __aenter__(self):
        await self._init_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            await self.rollback()
        else:
            await self.commit()
            
        await self._session.close()
        self._session = None
        self._conversation_repository = None
        self._message_repository = None
        
    async def commit(self):
        try:
            await self._session.commit()
            logger.info("Transaction committed successfully")
        except Exception as exc:
            logger.error("Error committing transaction: %s", exc)
            await self._session.rollback()
            raise
            
    async def rollback(self):
        try:
            await self._session.rollback()
            logger.info("Transaction rolled back successfully")
        except Exception as exc:
            logger.error("Error rolling back transaction: %s", exc)
            raise