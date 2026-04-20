import asyncio
from typing import Union
from fastapi import APIRouter
from schemas import InsightRequest, InsightResponse, ChatRequest, ChatResponse
from services.llm_service import llm_service

router = APIRouter(prefix="/api/llm-insight", tags=["AI Advisor"])

@router.post("", response_model=Union[InsightResponse, ChatResponse])
async def process_llm_request(request: Union[ChatRequest, InsightRequest]):
    if isinstance(request, ChatRequest):
        history_objs = getattr(request, 'history', [])
        user_profile = getattr(request, 'user_profile', None)
        reply = await llm_service.chat(history=history_objs, message=request.message, user_profile=user_profile)
        return ChatResponse(reply=reply)
    else:
        context = {
            "crop": request.crop,
            "predicted_yield": request.predicted_yield,
            "current_price": request.current_price,
            "climate_risk_level": request.climate_risk_level,
            "location": request.location
        }
        advice_text = await llm_service.generate_insight(context)
        return InsightResponse(insight_text=advice_text)
