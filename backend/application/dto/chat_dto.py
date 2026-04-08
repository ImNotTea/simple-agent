from dataclasses import dataclass

@dataclass
class ChatRequestDTO:
    message: str
    conversation_id: str | None = None
    role: str = "user"