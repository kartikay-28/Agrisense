"""
Background jobs — run by APScheduler.

Job 1: update_market_data()   — daily at midnight
Job 2: send_weekly_insights() — every Sunday 8 AM
"""

import pandas as pd
from datetime import date, datetime
from app.database import SessionLocal
from app.models import User, Farm, MarketData, Crop
from app.services.weather_api import get_weather_for_location
from app.services.email_service import send_weekly_insight
from app.ml_models.predictor import predict_crops, predict_price


# ── Job 1 ─────────────────────────────────────────────────────────────────────

def update_market_data():
    """
    Fetch latest mandi prices CSV and upsert into market_data table.
    In production: pull from AGMARKNET API or govt data portal.
    For MVP: reads from data/raw/mandi_prices.csv
    """
    print(f"[scheduler] update_market_data started at {datetime.utcnow()}")
    try:
        df = pd.read_csv("../data/raw/mandi_prices.csv")
        db = SessionLocal()

        for _, row in df.iterrows():
            # Find crop by name
            crop = db.query(Crop).filter(Crop.name == row["commodity"]).first()
            if not crop:
                continue

            # Avoid duplicate entries for same crop+state+date
            existing = db.query(MarketData).filter(
                MarketData.crop_id == crop.id,
                MarketData.state == row["state"],
                MarketData.date == row["date"],
            ).first()

            if not existing:
                entry = MarketData(
                    crop_id=crop.id,
                    state=row["state"],
                    date=row["date"],
                    price_per_quintal=float(row["modal_price"]),
                    demand_index=None,  # calculated separately
                )
                db.add(entry)

        db.commit()
        db.close()
        print("[scheduler] Market data updated successfully")
    except Exception as e:
        print(f"[scheduler] update_market_data failed: {e}")


# ── Job 2 ─────────────────────────────────────────────────────────────────────

def send_weekly_insights():
    """
    For every user, run crop prediction on their farms and send an email.
    """
    print(f"[scheduler] send_weekly_insights started at {datetime.utcnow()}")
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            farms = db.query(Farm).filter(Farm.user_id == user.id).all()
            if not farms:
                continue

            for farm in farms:
                weather = get_weather_for_location(farm.lat, farm.lon)
                features = {
                    "state": farm.state or "Unknown",
                    "soil_type": farm.soil_type or "Loamy",
                    "temperature": weather["avg_temp"],
                    "humidity": weather["avg_humidity"],
                    "rainfall": weather["avg_rainfall"],
                }

                top_crops = predict_crops(features)
                recommendations = []
                for item in top_crops:
                    price = predict_price(item["crop"], farm.state, datetime.utcnow().month)
                    recommendations.append({
                        "crop": item["crop"],
                        "match_score": f"{item['match_score']:.0f}%",
                        "expected_price": f"₹{price:.0f}/q",
                        "reason": item["reason"],
                    })

                rain = weather["avg_rainfall"]
                if rain > 80:
                    weather_summary = "Heavy rains are expected next week"
                elif rain < 20:
                    weather_summary = "Dry conditions are forecast next week"
                else:
                    weather_summary = "Moderate weather conditions are expected"

                send_weekly_insight(
                    to_email=user.email,
                    farmer_name=user.name,
                    farm_name=farm.farm_name,
                    recommendations=recommendations,
                    weather_summary=weather_summary,
                )
    finally:
        db.close()
    print("[scheduler] Weekly insights sent")
