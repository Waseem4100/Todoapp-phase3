from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlmodel import Session
from uuid import UUID

from src.database.database import get_session
from src.models.user import User
from src.api.deps import get_current_user
from src.services.ai_chatbot_service import AIChatbotService

router = APIRouter()


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    action: Optional[Dict[str, Any]] = None
    action_result: Optional[Dict[str, Any]] = None


@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_data: ChatMessage,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Chat with the AI assistant that can help manage your todos
    """
    chatbot_service = AIChatbotService()
    
    # Get AI response
    result = await chatbot_service.chat(chat_data.message, current_user.id, session)
    
    # Execute action if AI returned one
    action_result = None
    if result.get('action'):
        action_result = chatbot_service.execute_action(
            result['action'],
            current_user.id,
            session
        )
    
    return ChatResponse(
        response=result['response'],
        action=result.get('action'),
        action_result=action_result
    )


@router.get("/status")
async def get_chatbot_status():
    """
    Get the chatbot configuration status
    """
    api_key_configured = bool(__import__('os').getenv("GEMINI_API_KEY"))
    return {
        "configured": api_key_configured,
        "message": "Chatbot is ready" if api_key_configured else "Please set GEMINI_API_KEY environment variable"
    }
