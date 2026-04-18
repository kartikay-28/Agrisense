from fastapi import APIRouter
from schemas import YieldPredictRequest, YieldPredictResponse
from services.yield_service import yield_service

router = APIRouter(prefix="/api/yield-predict", tags=["Analytics & ML"])

@router.post("", response_model=YieldPredictResponse)
def predict_yield(request: YieldPredictRequest):
    """
    Predicts the expected crop yield per acre using our trained Random Forest model.
    """
    result = yield_service.predict_yield(
        crop=request.crop,
        rainfall=request.rainfall_mm,
        fertilizer=request.fertilizer_pct,
        season=request.season,
        soil_type=request.soil_type,
        acres=request.field_acres
    )
    return result
