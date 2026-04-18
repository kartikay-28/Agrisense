from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Backend server starting...")
    yield
    # Shutdown
    print("🛑 Backend server shutting down...")

app = FastAPI(
    title="AgriSense API",
    description="Agricultural data analysis and forecasting API",
    lifespan=lifespan
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AgriSense API is running", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import and include routes
try:
    from agrisense_functions import get_crop_recommendation
    
    @app.get("/api/recommendations/{crop}")
    async def get_recommendations(crop: str):
        """Get crop recommendations"""
        return {"crop": crop, "status": "fetching"}
except ImportError:
    print("Warning: Could not import agrisense_functions")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
