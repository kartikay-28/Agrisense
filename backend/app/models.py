"""
SQLAlchemy ORM Models — matches the LLD database schema exactly.
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Float, Integer, Date, DateTime,
    ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    farms = relationship("Farm", back_populates="user", cascade="all, delete-orphan")


class Farm(Base):
    __tablename__ = "farms"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    farm_name = Column(String(120), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    state = Column(String(100))
    soil_type = Column(String(100))

    user = relationship("User", back_populates="farms")


class Crop(Base):
    """Static master data — seeded once."""
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100))
    N_req = Column(Float)   # Nitrogen requirement
    P_req = Column(Float)   # Phosphorus requirement
    K_req = Column(Float)   # Potassium requirement
    pH_min = Column(Float)
    pH_max = Column(Float)

    market_data = relationship("MarketData", back_populates="crop")


class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    state = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    price_per_quintal = Column(Float, nullable=False)
    demand_index = Column(Float)  # Calculated profitability score

    crop = relationship("Crop", back_populates="market_data")
