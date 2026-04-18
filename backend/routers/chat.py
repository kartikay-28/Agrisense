from fastapi import APIRouter
from schemas import ChatRequest, ChatResponse
from services.llm_service import llm_service

router = APIRouter(prefix="/api/chat", tags=["AI Advisor"])

@router.post("", response_model=ChatResponse)
async def chat_with_advisor(request: ChatRequest):
    """
    Handle a conversational chat request using the Groq LLM service.
    Expects { "message": "hello", "history": [...] }
    """
    history_objs = getattr(request, 'history', [])
    message = request.message
    
    reply = await llm_service.chat(history=history_objs, message=message)
    return ChatResponse(reply=reply)
