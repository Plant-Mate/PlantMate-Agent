from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CareAdvice(BaseModel):
    plant_status: str
    watering_and_care_advice: str
    note: str

class SensorDataSummary(BaseModel):
    temperature: float
    humidity: float
    soil_moisture: float

class DailyCareAdvice(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    plant_id: str
    advice: CareAdvice
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