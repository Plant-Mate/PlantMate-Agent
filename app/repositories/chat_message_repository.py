from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.chat_message import ChatMessage
from datetime import datetime, timezone

class ChatMessageRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["chat_messages"]

    async def create(self, message: ChatMessage) -> ChatMessage:
        message_dict = message.model_dump(by_alias=True)
        message_dict["timestamp"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(message_dict)
        message_dict["_id"] = str(result.inserted_id)
        return ChatMessage(**message_dict)

    async def find_by_id(self, message_id: ObjectId) -> Optional[ChatMessage]:
        data = await self.collection.find_one({"_id": message_id})
        return ChatMessage(**data) if data else None

    async def list_by_plant(self, plant_id: ObjectId) -> List[ChatMessage]:
        cursor = self.collection.find({"plant_id": plant_id}).sort("timestamp", 1)
        return [ChatMessage(**doc) async for doc in cursor]

    async def delete_by_id(self, message_id: ObjectId) -> bool:
        result = await self.collection.delete_one({"_id": message_id})
        return result.deleted_count == 1

    async def delete_by_plant(self, plant_id: ObjectId) -> int:
        result = await self.collection.delete_many({"plant_id": plant_id})
        return result.deleted_count
