from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.chat_message import ChatMessage
from datetime import datetime, timezone

class ChatMessageRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["chat_messages"]

    async def create(self, message: ChatMessage) -> ChatMessage:
        message_dict = message.model_dump(by_alias=True, exclude_unset=True)
        message_dict["_id"] = ObjectId(message.id)
        message_dict["timestamp"] = datetime.now(timezone.utc)
        message_dict["plant_id"] = ObjectId(message.plant_id)
        result = await self.collection.insert_one(message_dict)
        message_dict["_id"] = str(result.inserted_id)
        message_dict["plant_id"] = str(message.plant_id)
        return ChatMessage(**message_dict)

    async def find_by_id(self, message_id: str) -> Optional[ChatMessage]:
        obj_id = ObjectId(message_id)
        data = await self.collection.find_one({"_id": obj_id})
        data["_id"] = str(data["_id"])
        data["plant_id"] = str(data["plant_id"])
        return ChatMessage(**data) if data else None

    async def list_by_plant(self, plant_id: str) -> List[ChatMessage]:
        obj_id = ObjectId(plant_id)
        cursor = self.collection.find({"plant_id": obj_id}).sort("timestamp", 1)
        messages = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["plant_id"] = str(doc["plant_id"])
            messages.append(ChatMessage(**doc))
        return messages

    async def delete_by_id(self, message_id: str) -> bool:
        obj_id = ObjectId(message_id)
        result = await self.collection.delete_one({"_id": obj_id})
        return result.deleted_count == 1

    async def delete_by_plant(self, plant_id: str) -> int:
        obj_id = ObjectId(plant_id)
        result = await self.collection.delete_many({"plant_id": obj_id})
        return result.deleted_count
