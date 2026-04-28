import chainlit as cl
from config import settings
import httpx
from schema.chat_schema import MessageSchema

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
    msg = cl.Message(content="")
    await msg.send()

    request_message = MessageSchema(role="user", message=message.content)
    full_response: list[str] = []

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                "http://localhost:8000/api/v1/chat",
                json=request_message.model_dump(exclude_none=True),
            ) as response:
                response.raise_for_status()

                async for chunk in response.aiter_text():
                    if not chunk:
                        continue

                    full_response.append(chunk)
                    await msg.stream_token(chunk)

        msg.content = "".join(full_response)
    except httpx.HTTPError as exc:
        msg.content = f"Unable to reach chat service: {exc}"

    await msg.update()