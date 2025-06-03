from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from app.models.plant import Plant
from app.services.plant_service import PlantService
from app.dependencies import get_plant_service

router = APIRouter(prefix="/plants", tags=["plants"])


@router.post("/", response_model=Plant)
async def create_plant(plant: Plant, service: PlantService = Depends(get_plant_service)):
    return await service.create_plant(plant)


@router.get("/", response_model=List[Plant])
async def list_plants(service: PlantService = Depends(get_plant_service)):
    return await service.list_plants()


@router.get("/{plant_id}", response_model=Plant)
async def get_plant(plant_id: str, service: PlantService = Depends(get_plant_service)):
    obj_id = ObjectId(plant_id)
    plant = await service.get_plant(obj_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


@router.put("/{plant_id}", response_model=Plant)
async def update_plant(plant_id: str, update_data: dict, service: PlantService = Depends(get_plant_service)):
    obj_id = ObjectId(plant_id)
    updated = await service.update_plant(obj_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Plant not found")
    return updated


@router.delete("/{plant_id}")
async def delete_plant(plant_id: str, service: PlantService = Depends(get_plant_service)):
    obj_id = ObjectId(plant_id)
    success = await service.delete_plant(obj_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plant not found")
    return {"success": True}
