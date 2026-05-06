from dataclasses import dataclass

@dataclass
class ChatRequestDTO:
    request_id: str
    message: str
    conversation_id: str | None = None
    role: str = "user"