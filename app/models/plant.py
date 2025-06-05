from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Plant(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    species: str
    description: str
    sensor_id: str = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }
