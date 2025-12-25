from typing import List
from pydantic import BaseModel, ConfigDict

class QueryRequest(BaseModel):
    query: str
    n_results: int = 1
    
class QueryReturn(BaseModel):
    data: dict[str, list]

class APIResponse(BaseModel):
    Answer: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: bool = False