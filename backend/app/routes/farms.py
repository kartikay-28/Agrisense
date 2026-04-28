"""
Farm management routes.
POST /api/farms  — create farm (auto-detects state + soil from lat/lon)
GET  /api/farms  — list all farms for logged-in user
"""

import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import get_db
from app.models import Farm, User
from app.services.weather_api import reverse_geocode_state
from app.services.soil_lookup import get_soil_type

router = APIRouter(prefix="/api/farms", tags=["farms"])
bearer = HTTPBearer()

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
ALGORITHM = "HS256"


# ── Auth dependency ───────────────────────────────────────────────────────────

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


# ── Schemas ───────────────────────────────────────────────────────────────────

class CreateFarmRequest(BaseModel):
    farm_name: str
    lat: float
    lon: float


class FarmResponse(BaseModel):
    id: str
    farm_name: str
    lat: float
    lon: float
    state: str | None
    soil_type: str | None

    class Config:
        from_attributes = True


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("", status_code=201, response_model=FarmResponse)
def create_farm(
    body: CreateFarmRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Auto-detect state and soil type from coordinates
    state = reverse_geocode_state(body.lat, body.lon)
    soil_type = get_soil_type(body.lat, body.lon)

    farm = Farm(
        user_id=current_user.id,
        farm_name=body.farm_name,
        lat=body.lat,
        lon=body.lon,
        state=state,
        soil_type=soil_type,
    )
    db.add(farm)
    db.commit()
    db.refresh(farm)
    return farm


@router.get("", response_model=list[FarmResponse])
def list_farms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Farm).filter(Farm.user_id == current_user.id).all()
