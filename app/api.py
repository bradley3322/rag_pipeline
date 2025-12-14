from typing import Union, Optional
from fastapi import APIRouter, FastAPI

from app.schemas import QueryRequest

app = FastAPI()

class QueryAPI:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/query/", self.query_endpoint, methods=["POST"])
        self.router.add_api_route("/health/", self.health_endpoint, methods=["GET"])
        
    async def health_endpoint(self):
        return {"status": "healthy"}    
    
    async def query_endpoint(self, request: QueryRequest):
        return {"query": request.query,
                "n_results": request.n_results}

query_api = QueryAPI()
app.include_router(query_api.router, prefix="/api")
        