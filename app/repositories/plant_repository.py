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
        plant_dict["_id"] = ObjectId(plant.id)
        plant_dict["created_at"] = datetime.now(timezone.utc)
        plant_dict["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(plant_dict)
        plant_dict["_id"] = str(result.inserted_id)
        return Plant(**plant_dict)

    async def find_by_id(self, plant_id: str) -> Optional[Plant]:
        obj_id = ObjectId(plant_id)
        data = await self.collection.find_one({"_id": obj_id})
        data["_id"] = str(data["_id"])
        return Plant(**data) if data else None

    async def list(self) -> List[Plant]:
        cursor = self.collection.find()
        plants = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            plants.append(Plant(**doc))
        return plants

    async def update(self, plant_id: str, update_data: dict) -> Optional[Plant]:
        obj_id = ObjectId(plant_id)
        update_data["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.find_one_and_update(
            {"_id": obj_id},
            {"$set": update_data},
            return_document=True
        )
        result["_id"] = str(result["_id"])
        return Plant(**result) if result else None

    async def delete(self, plant_id: str) -> bool:
        obj_id = ObjectId(plant_id)
        result = await self.collection.delete_one({"_id": obj_id})
        return result.deleted_count == 1
