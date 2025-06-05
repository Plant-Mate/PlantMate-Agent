from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.plant import Plant
from app.services.plant_service import PlantService
from app.dependencies import get_plant_service

router = APIRouter(prefix="/api/plants", tags=["plants"])


@router.post("/", response_model=Plant)
async def create_plant(plant: Plant, service: PlantService = Depends(get_plant_service)):
    return await service.create_plant(plant)


@router.get("/", response_model=List[Plant])
async def list_plants(service: PlantService = Depends(get_plant_service)):
    return await service.list_plants()


@router.get("/{plant_id}", response_model=Plant)
async def get_plant(plant_id: str, service: PlantService = Depends(get_plant_service)):
    plant = await service.get_plant(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


@router.put("/{plant_id}", response_model=Plant)
async def update_plant(plant_id: str, update_data: dict, service: PlantService = Depends(get_plant_service)):
    updated = await service.update_plant(plant_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Plant not found")
    return updated


@router.delete("/{plant_id}")
async def delete_plant(plant_id: str, service: PlantService = Depends(get_plant_service)):
    success = await service.delete_plant(plant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plant not found")
    return {"success": True}
