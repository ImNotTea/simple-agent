from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from dependency_injector.wiring import inject, Provide
from container import Container
from presentation.schemas.chat_schema import MessageSchema, ChatResponse
from application.use_case.chat_use_case import ChatUseCase
from logging import getLogger
logger = getLogger(__name__)


router = APIRouter()

@router.get("/health")
async def health_check(test: str = "ping"):
    """Independent API endpoint to check the health of the server"""
    return {"status": "ok", "message": "FastAPI backend is running smoothly!"}

@router.post("/chat", response_model=ChatResponse, description="Endpoint for chatting with the LLM. Streams responses as they are generated.")
@inject
async def chat(request: dict[str, str], chat_use_case: ChatUseCase = Depends(Provide[Container.chat_use_case])) -> ChatResponse:
    """An API endpoint for chatting"""
    # Validate request schema
    chat_request = MessageSchema(**request)
    chat_request_dto = chat_request.to_dto()
    
    async def event_generator():
        """Generator function to stream chat responses"""
        async for chunk in chat_use_case.process_message(chat_request_dto):
            yield chunk
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
