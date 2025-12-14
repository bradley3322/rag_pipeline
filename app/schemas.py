from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    n_results: int = 1