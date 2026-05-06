import json
from typing import AsyncGenerator
import uuid

from application.dto.chat_dto import ChatRequestDTO
from application.interface.llm_client import LLMClient
from application.interface.unit_of_work import UnitOfWork
from application.interface.idempotency_cache import IdempotencyCache
from domain.entity.conversation import Conversation
from domain.entity.message import Message

class ChatUseCase:
    """Chat use case class to handle chat interactions and business logic"""
    
    def __init__(self, llm_client: LLMClient, unit_of_work: UnitOfWork, idempotency_cache: IdempotencyCache):
        self.llm_client = llm_client
        self.unit_of_work = unit_of_work
        self.idempotency_cache = idempotency_cache
        
    async def process_message(self, chat_request: ChatRequestDTO) -> AsyncGenerator[str, None]:
        """Process a user message and return a response from the LLM"""
        # Check idempotency cache first
        cached_response = self.idempotency_cache.get_response(chat_request.request_id)
        if cached_response:
            yield cached_response
            return
        
        # PHASE 1: Handle conversation and message persistence
        if not chat_request.conversation_id:
            # Create a new conversation and save the initial message
            conversation = Conversation.create()
            request_message = Message.create(
                conversation_id=conversation.id,
                role=chat_request.role,
                content=chat_request.message,
                status="pending"
            )
            conversation.add_message(request_message)
            
            async with self.unit_of_work as uow:
                conversation_id = await uow.conversations.save_conversation(conversation)
                chat_request.conversation_id = conversation_id
                
        else:
            # Retrieve the existing conversation and add the new message
            async with self.unit_of_work as uow:
                conversation: Conversation = await uow.conversations.get_conversation(chat_request.conversation_id)
                if not conversation:
                    raise ValueError(f"Conversation with ID {chat_request.conversation_id} not found")
                request_message = Message.create(
                    conversation_id=conversation.id,
                    role=chat_request.role,
                    content=chat_request.message,
                    status="pending"
                )
                conversation.add_message(request_message)
                await uow.conversations.update_conversation(conversation)
        
        # Get response from LLM client
        reponse_message_content = ""
        async for chunk in self.llm_client.stream_response(chat_request.message):
            reponse_message_content += chunk
            yield chunk
        
        # Save the complete response to idempotency cache
        self.idempotency_cache.save_response(chat_request.request_id, reponse_message_content)
        
        # PHASE 2: Update the conversation with the response message
        reponse_message = Message.create(
            conversation_id=chat_request.conversation_id,
            role="assistant",
            content=reponse_message_content,
            status="success"
        )
        request_message.mark_as_success()  # Mark the request message as successful after processing
        async with self.unit_of_work as uow:
            if conversation:
                conversation.add_message(reponse_message)
                await uow.conversations.update_conversation(conversation)