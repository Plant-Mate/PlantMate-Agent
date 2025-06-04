from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.daily_care_advice import DailyCareAdvice
from datetime import datetime, timezone


class DailyCareAdviceRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["daily_care_advices"]

    async def create(self, advice: DailyCareAdvice) -> DailyCareAdvice:
        advice_dict = advice.model_dump(by_alias=True, exclude_unset=True)
        advice_dict["_id"] = ObjectId(advice.id)
        advice_dict["generated_date"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(advice_dict)
        advice_dict["_id"] = str(result.inserted_id)
        advice_dict["plant_id"] = str(advice.plant_id)
        return DailyCareAdvice(**advice_dict)

    async def find_by_id(self, advice_id: str) -> Optional[DailyCareAdvice]:
        obj_id = ObjectId(advice_id)
        data = await self.collection.find_one({"_id": obj_id})
        data["_id"] = str(data["_id"])
        return DailyCareAdvice(**data) if data else None

    async def list_by_plant(self, plant_id: str) -> List[DailyCareAdvice]:
        obj_id = ObjectId(plant_id)
        cursor = self.collection.find({"plant_id": obj_id}).sort("generated_date", -1)
        advices = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["plant_id"] = str(doc["plant_id"])
            advices.append(DailyCareAdvice(**doc))
        return advices

    async def delete_by_id(self, advice_id: str) -> bool:
        obj_id = ObjectId(advice_id)
        result = await self.collection.delete_one({"_id": obj_id})
        return result.deleted_count == 1

    async def delete_by_plant(self, plant_id: str) -> int:
        obj_id = ObjectId(plant_id)
        result = await self.collection.delete_many({"plant_id": obj_id})
        return result.deleted_count
