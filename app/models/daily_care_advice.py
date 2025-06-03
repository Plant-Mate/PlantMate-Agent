from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SensorDataSummary(BaseModel):
    avg_temperature: float
    avg_humidity: float
    avg_soil_moisture: float

class DailyCareAdvice(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    plant_id: str
    advice: str
    generated_date: datetime
    sensor_data_summary: SensorDataSummary

    class Config:
        populate_by_name=True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }
