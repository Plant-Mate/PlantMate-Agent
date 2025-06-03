from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.daily_care_advice import DailyCareAdvice
from datetime import datetime, timezone


class DailyCareAdviceRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["daily_care_advices"]

    async def create(self, advice: DailyCareAdvice) -> DailyCareAdvice:
        advice_dict = advice.model_dump(by_alias=True)
        advice_dict["generated_date"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(advice_dict)
        advice_dict["_id"] = str(result.inserted_id)
        return DailyCareAdvice(**advice_dict)

    async def find_by_id(self, advice_id: ObjectId) -> Optional[DailyCareAdvice]:
        data = await self.collection.find_one({"_id": advice_id})
        return DailyCareAdvice(**data) if data else None

    async def list_by_plant(self, plant_id: ObjectId) -> List[DailyCareAdvice]:
        cursor = self.collection.find({"plant_id": plant_id}).sort("generated_date", -1)
        return [DailyCareAdvice(**doc) async for doc in cursor]

    async def delete_by_id(self, advice_id: ObjectId) -> bool:
        result = await self.collection.delete_one({"_id": advice_id})
        return result.deleted_count == 1

    async def delete_by_plant(self, plant_id: ObjectId) -> int:
        result = await self.collection.delete_many({"plant_id": plant_id})
        return result.deleted_count
