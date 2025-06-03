from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.plant import Plant
from datetime import datetime, timezone

class PlantRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["plants"]

    async def create(self, plant: Plant) -> Plant:
        plant_dict = plant.model_dump(by_alias=True, exclude_unset=True)
        plant_dict["created_at"] = datetime.now(timezone.utc)
        plant_dict["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(plant_dict)
        plant_dict["_id"] = str(result.inserted_id)
        return Plant(**plant_dict)

    async def find_by_id(self, plant_id: ObjectId) -> Optional[Plant]:
        data = await self.collection.find_one({"_id": plant_id})
        return Plant(**data) if data else None

    async def list(self) -> List[Plant]:
        cursor = self.collection.find()
        return [Plant(**doc) async for doc in cursor]

    async def update(self, plant_id: ObjectId, update_data: dict) -> Optional[Plant]:
        update_data["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.find_one_and_update(
            {"_id": plant_id},
            {"$set": update_data},
            return_document=True
        )
        return Plant(**result) if result else None

    async def delete(self, plant_id: ObjectId) -> bool:
        result = await self.collection.delete_one({"_id": plant_id})
        return result.deleted_count == 1
