from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.assistant import ChatRequest, ChatResponse
from app.services.assistant_service import AssistantService

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])
assistant_service = AssistantService()

@router.post("/chat", response_model=ChatResponse, summary="Chat with AI Agriculture Assistant")
async def chat_assistant(payload: ChatRequest, db: Session = Depends(get_db)):
    try:
        return await assistant_service.chat(payload.message, payload.farm_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))