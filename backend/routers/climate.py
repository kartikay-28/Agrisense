from fastapi import APIRouter, Query
from schemas import ClimateRiskResponse
from services.climate_service import climate_service

router = APIRouter(prefix="/api/climate-risk", tags=["Analytics & ML"])

@router.get("", response_model=ClimateRiskResponse)
def get_climate_risk(
    lat: float = Query(None, description="Latitude of the farm (optional, defaults to Shimla)"),
    lon: float = Query(None, description="Longitude of the farm (optional, defaults to Shimla)"),
    crop: str = Query(None, description="Optional target crop to refine risk")
):
    """
    Fetches real-time weather data and calculates a transparent, rule-based 
    climate risk score for the farmer.
    
    If lat/lon are not provided, defaults to Shimla, Himachal Pradesh.
    """
    result = climate_service.get_climate_risk(lat=lat, lon=lon, crop=crop)
    return result
