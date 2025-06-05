from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Advice(BaseModel):
    message: str
    need_watering: bool
    note: str

class SensorDataSummary(BaseModel):
    avg_temperature: float
    avg_humidity: float
    avg_soil_moisture: float

class DailyCareAdvice(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    plant_id: str
    advice: Advice
    generated_date: datetime = Field(default_factory=datetime.now)
    sensor_data_summary: SensorDataSummary

    class Config:
        populate_by_name=True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }

class FakeDailyAdvice(BaseModel):
    advice: str
    generated_date: datetime = Field(default_factory=datetime.now)