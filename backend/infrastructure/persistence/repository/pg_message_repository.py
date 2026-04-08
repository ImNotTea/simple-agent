from datetime import datetime
from pyexpat.errors import messages

from application.interface.message_repository import MessageRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.persistence.database.base import Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
import uuid
from domain.entity.message import Message
from logging import getLogger

logger = getLogger(__name__)


class MessageORM(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    status = Column(String, nullable=True) # Status field to track message state (e.g., 'pending', 'success', 'failed')
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=True)
    conversation = relationship("ConversationORM", back_populates="messages")


class PGMessageRepository(MessageRepository):
    """PostgreSQL implementation of the MessageRepository interface for storing and retrieving messages"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save_message(self, message: Message) -> None:
        """Save a message to the PostgreSQL database under the specified conversation ID"""
        # Implement logic to save message to PostgreSQL using self.session
        try:
            logger.info("Saving message with ID %s to PostgreSQL database", message.id)
            orm = MessageORM(
                id=message.id,
                conversation_id=message.conversation_id,
                role=message.role,
                content=message.content,
                status=message.status,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            self.session.add(orm)
            await self.session.flush()
        except Exception as exc:
            logger.error("Error saving message to PostgreSQL database: %s", exc)
            await self.session.rollback()
            
    async def update_message_status(self, message_id: str, status: str) -> bool:
        """Update the status of a message in the PostgreSQL database"""
        try:
            logger.info("Updating status of message with ID %s to '%s' in PostgreSQL database", message_id, status)
            result = await self.session.execute(select(MessageORM).where(MessageORM.id == message_id))
            orm = result.scalars().first()
            if orm is None:
                logger.warning("Message with ID %s not found in PostgreSQL database for status update", message_id)
                return False
            orm.status = status
            orm.updated_at = datetime.now().isoformat()
            await self.session.flush()
            logger.info("Updated status of message with ID %s to '%s' in PostgreSQL database", message_id, status)
            return True
        except Exception as exc:
            logger.error("Error updating message status in PostgreSQL database: %s", exc)
            await self.session.rollback()
            return False
    
    async def get_messages(self, message_id: str) -> list[dict]:
        """Retrieve all messages for a given message ID from the PostgreSQL database"""
        # Implement logic to retrieve messages from PostgreSQL using self.session
        try:
            logger.info("Retrieving messages for message ID %s from PostgreSQL database", message_id)
            result = await self.session.execute(select(MessageORM).where(MessageORM.id == message_id))
            message = result.scalars().first()
            if message is None:
                return []
            return [
                Message(
                    id=message.id,
                    conversation_id=message.conversation_id,
                    role=message.role,
                    content=message.content,
                    status=message.status
                )
                for message in messages
            ]
        except Exception as exc:
            logger.error("Error retrieving messages from PostgreSQL database: %s", exc)
            return []