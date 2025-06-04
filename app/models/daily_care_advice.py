from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.models.mongo import PyObjectId

class Advice(BaseModel):
    message: str
    need_watering: bool
    note: str

class SensorDataSummary(BaseModel):
    avg_temperature: float
    avg_humidity: float
    avg_soil_moisture: float

class DailyCareAdvice(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    plant_id: PyObjectId
    advice: Advice
    generated_date: datetime
    sensor_data_summary: SensorDataSummary

    class Config:
        populate_by_name=True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }
