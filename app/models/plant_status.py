from pydantic import BaseModel

class PlantStatus(BaseModel):
    name: str
    species: str
    last_watered_days: int
    temperature: float
    humidity: float
