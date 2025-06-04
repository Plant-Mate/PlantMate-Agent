from typing import List, Optional
from bson import ObjectId
from app.models.chat_message import ChatMessage
from app.repositories.chat_message_repository import ChatMessageRepository


class ChatMessageService:
    def __init__(self, chat_repo: ChatMessageRepository):
        self.chat_repo = chat_repo

    async def create_message(self, message: ChatMessage) -> ChatMessage:
        return await self.chat_repo.create(message)

    async def get_message(self, message_id: str) -> Optional[ChatMessage]:
        return await self.chat_repo.find_by_id(message_id)

    async def list_messages_by_plant(self, plant_id: str) -> List[ChatMessage]:
        return await self.chat_repo.list_by_plant(plant_id)

    async def delete_message(self, message_id: str) -> bool:
        return await self.chat_repo.delete_by_id(message_id)

    async def delete_messages_by_plant(self, plant_id: str) -> int:
        return await self.chat_repo.delete_by_plant(plant_id)
