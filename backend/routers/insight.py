import asyncio
from fastapi import APIRouter
from schemas import InsightRequest, InsightResponse
from services.llm_service import llm_service

router = APIRouter(prefix="/api/llm-insight", tags=["AI Advisor"])

@router.post("", response_model=InsightResponse)
async def get_ai_insight(request: InsightRequest):
    """
    Passes comprehensive Dashboard metrics into an LLM (like GPT-4o-mini)
    to generate personalized, plain-language agricultural advice.
    """
    
    # Create the context dictionary
    context = {
        "crop": request.crop,
        "predicted_yield": request.predicted_yield,
        "current_price": request.current_price,
        "climate_risk_level": request.climate_risk_level,
        "location": request.location
    }
    
    # Await the async LLM call
    advice_text = await llm_service.generate_insight(context)
    
    return InsightResponse(insight_text=advice_text)
