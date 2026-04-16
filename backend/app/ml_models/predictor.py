"""
ML Model loader and inference.

Loads crop_model.pkl and price_model.pkl from this directory.
If .pkl files don't exist yet (pre-training), falls back to
rule-based mock predictions so the API still works during dev.

Train the real models using:
  notebooks/crop_training.ipynb
  notebooks/price_training.ipynb
"""

import os
import joblib
import numpy as np
from pathlib import Path

MODEL_DIR = Path(__file__).parent

# State encoding — must match what was used during training
STATE_ENCODING = {
    "Punjab": 0, "Haryana": 1, "Uttar Pradesh": 2, "Maharashtra": 3,
    "Rajasthan": 4, "Madhya Pradesh": 5, "Unknown": 6,
}

SOIL_ENCODING = {
    "Alluvial": 0, "Black": 1, "Red Laterite": 2, "Arid/Desert": 3, "Loamy": 4,
}

CROP_NAMES = [
    "Rice", "Wheat", "Maize", "Chickpea", "Kidney Beans", "Pigeon Peas",
    "Moth Beans", "Mung Bean", "Black Gram", "Lentil", "Pomegranate",
    "Banana", "Mango", "Grapes", "Watermelon", "Muskmelon", "Apple",
    "Orange", "Papaya", "Coconut", "Cotton", "Jute", "Coffee",
]


def _load_model(filename: str):
    path = MODEL_DIR / filename
    if path.exists():
        return joblib.load(path)
    return None


_crop_model = _load_model("crop_model.pkl")
_price_model = _load_model("price_model.pkl")


def predict_crops(features: dict) -> list[dict]:
    """
    Predict top 3 recommended crops for given farm features.

    Parameters:
    -----------
    features : dict with keys:
        state, soil_type, temperature, humidity, rainfall

    Returns:
    --------
    list of 3 dicts: {crop, match_score, reason}
    """
    state_enc = STATE_ENCODING.get(features.get("state", "Unknown"), 6)
    soil_enc = SOIL_ENCODING.get(features.get("soil_type", "Loamy"), 4)
    temp = features.get("temperature", 28.0)
    humidity = features.get("humidity", 65.0)
    rainfall = features.get("rainfall", 50.0)

    X = np.array([[state_enc, soil_enc, temp, humidity, rainfall]])

    if _crop_model is not None:
        # Real model: get probability for each class
        proba = _crop_model.predict_proba(X)[0]
        top3_idx = np.argsort(proba)[::-1][:3]
        results = []
        for idx in top3_idx:
            crop = _crop_model.classes_[idx]
            score = proba[idx] * 100
            results.append({
                "crop": crop,
                "match_score": round(score, 1),
                "reason": _get_reason(crop, features),
            })
        return results

    # ── Fallback mock (pre-training) ──────────────────────────────────────────
    mock = [
        {"crop": "Wheat",  "match_score": 92.0, "reason": "Optimal soil and temperature match"},
        {"crop": "Maize",  "match_score": 85.0, "reason": "High rainfall compatibility"},
        {"crop": "Lentil", "match_score": 78.0, "reason": "Good nitrogen fixation for soil type"},
    ]
    return mock


def predict_price(crop: str, state: str, month: int) -> float:
    """
    Predict price (₹/quintal) for a crop in a given state and month.

    Parameters:
    -----------
    crop : str
    state : str
    month : int  (1-12)

    Returns:
    --------
    float — predicted price per quintal
    """
    state_enc = STATE_ENCODING.get(state, 6)

    # Encode crop as integer index
    crop_id = CROP_NAMES.index(crop) if crop in CROP_NAMES else 0

    X = np.array([[crop_id, state_enc, month]])

    if _price_model is not None:
        return float(_price_model.predict(X)[0])

    # ── Fallback mock prices ──────────────────────────────────────────────────
    base_prices = {
        "Wheat": 2400, "Rice": 3200, "Maize": 2050,
        "Lentil": 5500, "Chickpea": 4800,
    }
    return float(base_prices.get(crop, 2500))


def _get_reason(crop: str, features: dict) -> str:
    """Generate a human-readable reason for the recommendation."""
    rainfall = features.get("rainfall", 50)
    soil = features.get("soil_type", "Loamy")

    if rainfall > 80:
        return f"High rainfall match for {crop}"
    elif rainfall < 30:
        return f"Drought-tolerant — suitable for current dry conditions"
    elif soil == "Black":
        return f"Black soil highly suitable for {crop}"
    else:
        return f"Optimal soil and climate conditions for {crop}"
