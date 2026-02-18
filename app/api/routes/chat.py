from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.agent.agent_builder import SmartAgent

router = APIRouter()

# Request body schema
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"
    context: dict = None  # optional context: order items, order_number, etc.

# Response schema
class ChatResponse(BaseModel):
    type: str
    message: str
    data: dict = None

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    agent = SmartAgent(db, session_id=request.session_id)
    response = agent.handle_message(request.message, request.context)
    return response
