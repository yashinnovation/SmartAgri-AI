from pydantic import BaseModel
from typing import Dict, Any

class ChatRequest(BaseModel):
    message: str
    farm_id: int = 1

class ChatResponse(BaseModel):
    reply: str
    context_used: Dict[str, Any]