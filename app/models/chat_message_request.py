from pydantic import BaseModel
from typing import Literal
from app.models.chat_message import ChatMessage

class ChatMessageRequest(BaseModel):
    message_type: Literal['user', 'assistant']
    content: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    def to_chat_message(self, plant_id: str) -> "ChatMessage":
        return ChatMessage(
            plant_id=plant_id,
            message_type=self.message_type,
            content=self.content
        )
