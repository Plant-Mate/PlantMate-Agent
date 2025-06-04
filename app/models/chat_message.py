from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal
from bson import ObjectId
from app.models.mongo import PyObjectId

class ChatMessage(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    plant_id: PyObjectId
    message_type: Literal['user', 'assistant']
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }
