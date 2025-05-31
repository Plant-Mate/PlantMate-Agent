from pydantic import BaseModel

class CareSuggestion(BaseModel):
    message: str
    need_watering: bool
    note: str
