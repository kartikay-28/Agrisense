import os
import random

class ClimateService:
    """
    Handles fetching weather data and running the logic for the Climate Risk Scorer.
    """
    # Default location: Shimla, Himachal Pradesh (center of AgriSense operations)
    DEFAULT_LAT = 31.1048
    DEFAULT_LON = 77.1734
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

    def _fetch_weather(self, lat: float = None, lon: float = None):
        # Use defaults if not provided
        if lat is None:
            lat = self.DEFAULT_LAT
        if lon is None:
            lon = self.DEFAULT_LON
            
        # If no API key is provided, gracefully fallback to simulated weather anomalies
        if not self.api_key:
            return {
                "rain_deviation": random.randint(-40, 60),  # % deviation
                "temp_deviation": random.randint(-5, 15),   # % deviation
                "soil_moisture": random.randint(30, 80)     # % capacity
            }
        
        # Real integration would use requests.get() to OpenWeatherMap here
        # import requests
        # url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}"
        # data = requests.get(url).json()
        
        # For this template, return simulated anomalies
        return {
            "rain_deviation": random.randint(-40, 60),
            "temp_deviation": random.randint(-5, 15),
            "soil_moisture": random.randint(30, 80)
        }

    def get_climate_risk(self, lat: float = None, lon: float = None, crop: str = None) -> dict:
        # Use defaults if not provided
        if lat is None:
            lat = self.DEFAULT_LAT
        if lon is None:
            lon = self.DEFAULT_LON
            
        weather = self._fetch_weather(lat, lon)
        
        rain_dev = weather["rain_deviation"]
        temp_dev = weather["temp_deviation"]
        soil_mst = weather["soil_moisture"]
        
        # 1. Apply the Rule-Based Formula
        soil_dryness = 100 - soil_mst
        risk_score = (abs(rain_dev) * 0.5) + (abs(temp_dev) * 0.3) + (soil_dryness * 0.2)
        risk_score = min(100, max(0, int(risk_score)))
        
        # 2. Categorize Overall Risk
        if risk_score < 30:
            level = "Low"
            advice = "Conditions are optimal. Normal irrigation schedule applies."
        elif risk_score < 65:
            level = "Medium"
            advice = "Irrigate twice this week. Keep an eye on soil dryness."
        else:
            level = "High"
            advice = "Immediate action required. High risk of moisture stress."

        # 3. Calculate Sub-risks
        drought_risk = int((soil_dryness * 0.6) + (temp_dev if temp_dev > 0 else 0 * 0.4))
        flood_risk = int(rain_dev) if rain_dev > 0 else 0
        frost_risk = int(abs(temp_dev)) if temp_dev < -20 else 5  # Example heuristic

        return {
            "risk_level": level,
            "risk_score": risk_score,
            "drought_risk": min(100, max(0, drought_risk)),
            "flood_risk": min(100, max(0, flood_risk)),
            "frost_risk": min(100, max(0, frost_risk)),
            "irrigation_advice": advice
        }

climate_service = ClimateService()
