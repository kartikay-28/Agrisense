from pydantic import BaseModel, Field
from typing import List

class PricePoint(BaseModel):
    """Schema for individual data points in sparklines/charts"""
    date: str = Field(..., description="Date of the record (YYYY-MM-DD)")
    price: float = Field(..., description="Modal price on that date")

class MarketDataResponse(BaseModel):
    """
    Standardized response schema for the Market Data dashboard.
    Using Pydantic ensures the API always returns the exact structure React expects!
    """
    crop_name: str = Field(..., description="Name of the agricultural commodity")
    current_price: float = Field(..., description="Latest available modal price")
    price_change_7d_percent: float = Field(..., description="Percentage change day-over-day (our engineered feature)")
    rolling_avg_7d: float = Field(..., description="7-Day Smoothed Rolling Average")
    rolling_avg_30d: float = Field(..., description="30-Day Smoothed Rolling Average")
    volatility_7d: float = Field(..., description="Price volatility (standard deviation) over the last 7 days")
    recent_prices: List[PricePoint] = Field(..., description="Array of up to 30 recent prices for UI sparklines")
    last_updated: str = Field(..., description="The date of the most recent price record")

from typing import Optional

# --- Yield Prediction Schemas (3.3) ---
class YieldPredictRequest(BaseModel):
    crop: str = Field(..., description="Crop type (e.g., Wheat, Rice)")
    rainfall_mm: float = Field(..., description="Expected rainfall in mm")
    fertilizer_pct: float = Field(..., description="Amount of fertilizer applied (pct or kg/acre)")
    season: str = Field(..., description="Agricultural season (e.g., Rabi, Kharif, Zaid)")
    field_acres: float = Field(..., description="Size of the field in acres")
    soil_type: Optional[str] = Field("Alluvial", description="Soil type")

class YieldPredictResponse(BaseModel):
    predicted_yield: float
    unit: str
    confidence_pct: int
    historical_avg: float
    message: str

# --- Climate Risk Schemas (3.4) ---
class ClimateRiskResponse(BaseModel):
    risk_level: str
    risk_score: int
    drought_risk: int
    flood_risk: int
    frost_risk: int
    irrigation_advice: str

# --- LLM Insight Schemas (3.5) ---
class InsightRequest(BaseModel):
    crop: str
    predicted_yield: float
    current_price: float
    climate_risk_level: str
    location: Optional[str] = "Himachal Pradesh"

class InsightResponse(BaseModel):
    insight_text: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    reply: str

