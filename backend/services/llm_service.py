from dotenv import load_dotenv
import os
import asyncio
from fastapi import HTTPException
from groq import AsyncGroq
from services.data_service import DataService
from services.yield_service import yield_service
from services.climate_service import climate_service

load_dotenv()
load_dotenv(".env.local")

# FIXED: Default user mock profile for context injection
MOCK_USER_PROFILE = {
    "name": "Rajan",
    "crop": "Wheat",
    "season": "Rabi",
    "location": "Punjab",
    "acres": 12,
    "soil_type": "Alluvial",
    "rainfall": 120.0,
    "fertilizer": 80.0
}

data_service = DataService()

class LLMService:
    """
    Connects to the Groq API (using Llama3) to generate natural language advice at lightning speed.
    """
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = AsyncGroq(api_key=self.api_key) if self.api_key else None

    async def generate_insight(self, context_data: dict) -> str:
        """
        Asynchronously calls the Groq LLM with the provided context.
        """
        prompt = f"""
You are an experienced agricultural advisor in Himachal Pradesh, India. 
Speak in simple, friendly, Hindi-friendly English. 
Given this farmer data: 
- Crop: {context_data.get('crop')}
- Predicted Yield: {context_data.get('predicted_yield')} quintals/acre
- Current Market Price: ₹{context_data.get('current_price')}
- Climate Risk: {context_data.get('climate_risk_level')}

Write a helpful 2-paragraph insight and practical advice for the farmer.
"""
        
        if not self.client:
            # Fallback if no API key is configured
            return (
                f"Namaste! Looking at the data, the climate risk is {context_data.get('climate_risk_level')}. "
                f"Your expected {context_data.get('crop')} yield is around {context_data.get('predicted_yield')} quintals per acre. "
                f"With the current market price at ₹{context_data.get('current_price')}, it's a good time to plan your harvest strategy. \n\n"
                "Advice: Ensure you follow the recommended irrigation schedule. Please add your Groq API key to the .env file to enable live AI insights!"
            )
            
        try:
            # Live Groq API Call
            response = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile", # Advanced Groq model
                messages=[
                    {"role": "system", "content": "You are an expert, friendly agricultural advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=250
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

    async def chat(self, history: list, message: str, user_profile: dict = None) -> str:
        """
        Asynchronously handles conversational chat via the LLM API.
        Includes rich context injection dynamically mapped from the user's authentic profile.
        """
        # If no profile was provided from frontend, fallback to MOCK_USER_PROFILE safely
        profile = user_profile if user_profile else MOCK_USER_PROFILE
        
        try:
            market_data = data_service.get_market_data(profile.get("crop", "Wheat"))
            current_price = market_data.get("current_price", 0)
            price_change_7d = market_data.get("price_change_7d_percent", 0)
        except Exception:
            current_price = 0
            price_change_7d = 0
            
        try:
            yield_data = yield_service.predict_yield(
                crop=profile.get("crop", "Wheat"), 
                rainfall=profile.get("rainfall", 100.0), 
                fertilizer=profile.get("fertilizer", 50.0), 
                season=profile.get("season", "Rabi"), 
                soil_type=profile.get("soil_type", "Alluvial"), 
                acres=profile.get("acres", 10)
            )
            predicted_yield = yield_data.get("predicted_yield", 0)
        except Exception:
            predicted_yield = 0
            
        try:
            climate_data = climate_service.get_climate_risk(crop=profile.get("crop", "Wheat"))
            climate_risk = climate_data.get("risk_level", "Medium")
        except Exception:
            climate_risk = "Medium"

        system_prompt = f"""You are a helpful, expert AI agricultural advisor. Provide concise, friendly answers in simple, Hindi-friendly English.
You are talking to {profile.get("name", "Farmer")}.
Current farm profile:
- Primary Crop: {profile.get("crop", "Unknown")}
- Season: {profile.get("season", "Unknown")}
- Current Market Price: ₹{current_price} ({price_change_7d}% in last 7 days)
- Yield Prediction: {predicted_yield} quintals/acre
- Climate Risk Level: {climate_risk}

Always use this context to answer questions meaningfully. For example, if asked 'Should I sell my crops?', refer to the current price, recent price changes, and yield."""

        messages = [{"role": "system", "content": system_prompt}]
        for msg in history[-5:]: # Only keep last 5 for context limit and safety
            if msg.role in ["user", "assistant"]:
                messages.append({"role": msg.role, "content": msg.content})
        
        # In case the message isn't at the end of history yet
        if not history or history[-1].content != message:
            messages.append({"role": "user", "content": message})

        if not self.client:
            return "Namaste! I'm your AI assistant. You asked: '" + message + "'. Please add your GROQ API key to enable live chat!"

        try:
            response = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Chat Error: {str(e)}")

llm_service = LLMService()
