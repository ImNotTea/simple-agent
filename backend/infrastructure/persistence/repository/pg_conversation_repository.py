from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, selectinload
from application.interface.conversation_repository import ConversationRepository
from infrastructure.persistence.repository.pg_message_repository import MessageORM
import uuid
from domain.entity.conversation import Conversation
from infrastructure.persistence.database.base import Base
from datetime import datetime
from sqlalchemy.future import select
from domain.entity.message import Message
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger

logger = getLogger(__name__)

class ConversationORM(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True)
    messages = relationship("MessageORM", back_populates="conversation", cascade="all, delete-orphan", lazy="selectin")
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=True)

class PGConversationRepository(ConversationRepository):
    """PostgreSQL implementation of the ConversationRepository interface for storing and retrieving conversations"""
    def __init__(self, session: AsyncSession):
        self._session = session
        
    async def save_conversation(self, conversation: Conversation) -> str | None:
        """
        Save a conversation to the PostgreSQL database
        Returns the ID of the saved conversation or None if saving failed
        """
        try:
            logger.info("Saving conversation with ID %s to PostgreSQL database", conversation.id)
            orm = ConversationORM(
                id=conversation.id,
                messages=[
                    MessageORM(
                        id=message.id,
                        role=message.role,
                        content=message.content,
                        status=message.status,
                        conversation_id=conversation.id,
                        created_at=datetime.now().isoformat(),
                        updated_at=datetime.now().isoformat()
                    )
                    for message in conversation.messages
                ],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            self._session.add(orm)
            await self._session.flush()  # Ensure the conversation is saved and ID is generated
            logger.info("Saving conversation with ID %s to PostgreSQL database", orm.id)
            return orm.id
        except Exception as exc:
            logger.error("Error saving conversation to PostgreSQL database: %s", exc)
            await self._session.rollback()
            return None
        
    async def update_conversation(self, conversation: Conversation) -> bool:
        """
        Update an existing conversation in the PostgreSQL database
        Returns True if the update was successful, False otherwise
        """
        try:
            logger.info("Updating conversation with ID %s in PostgreSQL database", conversation.id)
            result = await self._session.execute(select(ConversationORM).where(ConversationORM.id == conversation.id))
            orm = result.scalars().first()
            if orm is None:
                logger.warning("Conversation with ID %s not found for update", conversation.id)
                return False
            
            # Update all messages
            orm.messages = [
                MessageORM(
                    id=message.id,
                    role=message.role,
                    content=message.content,
                    status=message.status,
                    conversation_id=conversation.id,
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat()
                )
                for message in conversation.messages
            ]
            orm.updated_at = datetime.now().isoformat()
            await self._session.flush()
            logger.info("Updated conversation with ID %s in PostgreSQL database", conversation.id)
            return True
        except Exception as exc:
            logger.error("Error updating conversation in PostgreSQL database: %s", exc)
            await self._session.rollback()
            return False
    
    async def get_conversation(self, conversation_id: str) -> Conversation | None:
        """
        Retrieve a conversation from the PostgreSQL database by its ID
        Returns a Conversation object or None if the conversation is not found
        """
        
        try:
            logger.info("Retrieving conversation with ID %s from PostgreSQL database", conversation_id)
            
            result = await self._session.execute(
                select(ConversationORM).options(selectinload(ConversationORM.messages)).where(ConversationORM.id == conversation_id)
            )
            orm = result.scalars().first()
            
            if orm is None:
                return None
            
            return Conversation(
                id=orm.id,
                messages=[
                    Message.create(conversation_id=orm.id, role=m.role, content=m.content, id=m.id, status=m.status)
                    for m in orm.messages
                ]
            )
        except Exception as exc:
            logger.error("Error retrieving conversation from PostgreSQL database: %s", exc)
            return None