import os
import asyncio
from fastapi import HTTPException
from groq import AsyncGroq

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
                model="llama3-8b-8192", # Extremely fast Groq model suitable for advice
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

llm_service = LLMService()
