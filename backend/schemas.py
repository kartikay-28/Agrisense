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
