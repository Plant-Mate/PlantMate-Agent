from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class ChatMessage(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    plant_id: str
    message_type: Literal['user', 'assistant']
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }
