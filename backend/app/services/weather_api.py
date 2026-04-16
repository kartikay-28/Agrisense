"""
Weather API service — wraps OpenWeatherMap.
Also handles reverse geocoding (lat/lon → state name).

Set WEATHER_API_KEY in .env to use live data.
Falls back to mock data if key is missing (dev mode).
"""

import os
import requests

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
OWM_BASE = "https://api.openweathermap.org/data/2.5"


def get_weather_for_location(lat: float, lon: float) -> dict:
    """
    Fetch 7-day forecast and return averaged temp, humidity, rainfall.
    Falls back to mock values if no API key is set.
    """
    if not WEATHER_API_KEY:
        # Dev fallback — realistic mock values
        return {
            "avg_temp": 28.5,
            "avg_humidity": 65.0,
            "avg_rainfall": 45.0,
        }

    url = f"{OWM_BASE}/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&cnt=56"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    temps, humidities, rains = [], [], []
    for entry in data.get("list", []):
        temps.append(entry["main"]["temp"])
        humidities.append(entry["main"]["humidity"])
        rains.append(entry.get("rain", {}).get("3h", 0))

    return {
        "avg_temp": sum(temps) / len(temps) if temps else 28.0,
        "avg_humidity": sum(humidities) / len(humidities) if humidities else 60.0,
        "avg_rainfall": sum(rains) if rains else 40.0,
    }


def reverse_geocode_state(lat: float, lon: float) -> str:
    """
    Convert lat/lon to Indian state name using OpenWeatherMap Geocoding API.
    Falls back to 'Unknown' if API key is missing.
    """
    if not WEATHER_API_KEY:
        return "Punjab"  # dev fallback

    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={WEATHER_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data:
            return data[0].get("state", "Unknown")
    except Exception:
        pass
    return "Unknown"
