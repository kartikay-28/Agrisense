import os
import asyncio
from fastapi import HTTPException

# For a production app, install openai via: pip install openai
# import openai

class LLMService:
    """
    Connects to AI APIs (like OpenAI GPT-4o-mini) to generate natural language advice.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    async def generate_insight(self, context_data: dict) -> str:
        """
        Asynchronously calls the LLM with the provided context.
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
        
        if not self.api_key:
            # Fallback if no API key is configured
            return (
                f"Namaste! Looking at the data, the climate risk is {context_data.get('climate_risk_level')}. "
                f"Your expected {context_data.get('crop')} yield is around {context_data.get('predicted_yield')} quintals per acre. "
                f"With the current market price at ₹{context_data.get('current_price')}, it's a good time to plan your harvest strategy. \n\n"
                "Advice: Ensure you follow the recommended irrigation schedule. Keep an eye on the market prices over the next two weeks to maximize your profits!"
            )
            
        try:
            # Real API call example (Requires openai package)
            # client = openai.AsyncOpenAI(api_key=self.api_key)
            # response = await client.chat.completions.create(
            #     model="gpt-4o-mini",
            #     messages=[
            #         {"role": "system", "content": "You are an expert, friendly agricultural advisor."},
            #         {"role": "user", "content": prompt}
            #     ],
            #     temperature=0.7,
            #     max_tokens=250
            # )
            # return response.choices[0].message.content.strip()
            
            # Simulated await to mirror async behavior
            await asyncio.sleep(0.5) 
            return "Namaste! (OpenAI API key detected, but actual openai package call is mocked for safety in this template). " + prompt
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

llm_service = LLMService()
