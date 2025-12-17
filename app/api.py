import re
from typing import Union, Optional
from fastapi import APIRouter, FastAPI

from app.ollama import generate_rag_prompt, generate_response_ollama
from app.schemas import QueryRequest
from app.vectorstore import query_texts_from_db

app = FastAPI()

class QueryAPI:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/query", self.query_endpoint, methods=["POST"])
        self.router.add_api_route("/health", self.health_endpoint, methods=["GET"])
        
    @staticmethod
    def clean_text_for_response(text: str) -> str:
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @staticmethod
    def build_response_for_query(query_results: dict) -> dict[str, list]:
        cleaned_documents = []
        for doc in query_results.get("documents", [])[0]:
            cleaned_documents.append(QueryAPI.clean_text_for_response(doc))
        cleaned_results = {
            "ids": query_results.get("ids", []),
            "distances": query_results.get("distances", []),
            "metadatas": query_results.get("metadatas", []),
            "documents": cleaned_documents
        }
        return cleaned_results
        
    async def health_endpoint(self):
        return {"status": "healthy"}    
    
    async def query_endpoint(self, request: QueryRequest):
        query_results = query_texts_from_db(request.query, request.n_results)
        
        final_rag_prompt = generate_rag_prompt(request.query, query_results.get("documents", [])[0])
        llm_answer = generate_response_ollama(final_rag_prompt)

        print(f"User Query: {request.query}")
        print("---")
        print(f"LLM Answer:\n{llm_answer}")
        return self.build_response_for_query(query_results)

query_api = QueryAPI()
app.include_router(query_api.router, prefix="/api")
        