import chainlit as cl
from config import settings
import httpx
from schema.chat_schema import RequestMessage

# Load settings
cfg_settings = settings.get_settings()

# Define chat flow
@cl.on_chat_start
async def on_chat_start():
    """Initialize session when user opens Chat interface"""
    await cl.Message(content="Hi sweetie! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    """Process messages from user"""
    # Initiate empty response message
    msg = cl.Message(content="")
    request_message = RequestMessage(role="user", message=message.content)
    async with httpx.AsyncClient(timeout=None) as client:

        async with client.stream(
            "POST",
            "http://localhost:8000/api/v1/chat",
            json=request_message.model_dump(),
        ) as response:

            async for chunk in response.aiter_text():
                await msg.stream_token(chunk)

    await msg.update()