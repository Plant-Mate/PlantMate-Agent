from pydantic import BaseModel


class QueryRequest(BaseModel):
    key: str

class QueryResponse(BaseModel):
    answer: str

class daily_advice(BaseModel):
    timestamp: str   
    sentence: str 