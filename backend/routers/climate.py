from fastapi import APIRouter, Query
from schemas import ClimateRiskResponse
from services.climate_service import climate_service

router = APIRouter(prefix="/api/climate-risk", tags=["Analytics & ML"])

@router.get("", response_model=ClimateRiskResponse)
def get_climate_risk(
    lat: float = Query(..., description="Latitude of the farm"),
    lon: float = Query(..., description="Longitude of the farm"),
    crop: str = Query(None, description="Optional target crop to refine risk")
):
    """
    Fetches real-time weather data and calculates a transparent, rule-based 
    climate risk score for the farmer.
    """
    result = climate_service.get_climate_risk(lat=lat, lon=lon, crop=crop)
    return result
