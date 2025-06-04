from typing import List, Optional
from app.models.plant import Plant
from app.repositories.plant_repository import PlantRepository


class PlantService:
    def __init__(self, plant_repo: PlantRepository):
        self.plant_repo = plant_repo

    async def create_plant(self, plant: Plant) -> Plant:
        return await self.plant_repo.create(plant)

    async def get_plant(self, plant_id: str) -> Optional[Plant]:
        return await self.plant_repo.find_by_id(plant_id)

    async def list_plants(self) -> List[Plant]:
        return await self.plant_repo.list()

    async def update_plant(self, plant_id: str, update_data: dict) -> Optional[Plant]:
        return await self.plant_repo.update(plant_id, update_data)

    async def delete_plant(self, plant_id: str) -> bool:
        return await self.plant_repo.delete(plant_id)
