"""
Prediction routes — CORE ML endpoints.

GET /api/predict/crop/{farm_id}
  1. Fetch farm details (lat, lon, soil) from DB
  2. Call OpenWeather API for 7-day avg Temp & Rainfall
  3. Pass features into crop_model.pkl  → top 3 crops
  4. Pass crops into price_model.pkl   → expected price per crop
  5. Return ranked recommendations
"""

import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import get_db
from app.models import Farm, User
from app.services.weather_api import get_weather_for_location
from app.ml_models.predictor import predict_crops, predict_price

router = APIRouter(prefix="/api/predict", tags=["predict"])
bearer = HTTPBearer()

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
ALGORITHM = "HS256"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/crop/{farm_id}")
def predict_crop_for_farm(
    farm_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Fetch farm
    farm = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.user_id == current_user.id,
    ).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    # 2. Get weather data for farm location
    weather = get_weather_for_location(farm.lat, farm.lon)

    # 3. Build feature dict for ML model
    features = {
        "state": farm.state or "Unknown",
        "soil_type": farm.soil_type or "Loamy",
        "temperature": weather["avg_temp"],
        "humidity": weather["avg_humidity"],
        "rainfall": weather["avg_rainfall"],
    }

    # 4. Predict top 3 crops (Classification)
    top_crops = predict_crops(features)  # returns list of {crop, match_score}

    # 5. Predict price for each crop (Regression)
    recommendations = []
    for item in top_crops:
        price = predict_price(item["crop"], farm.state, features["temperature"])
        recommendations.append({
            "crop": item["crop"],
            "match_score": f"{item['match_score']:.0f}%",
            "expected_price": f"₹{price:.0f}/q",
            "reason": item["reason"],
        })

    return {"farm_id": farm_id, "recommendations": recommendations}
