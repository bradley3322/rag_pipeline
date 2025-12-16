from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    n_results: int = 1
    
class QueryReturn(BaseModel):
    data: dict[str, list]

class APIResponse(BaseModel):
    Answer: str