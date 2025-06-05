from pydantic import BaseModel


class QueryRequest(BaseModel):
    key: str

class QueryResponse(BaseModel):
    answer: str

