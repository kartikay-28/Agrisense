from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.market import router as market_router

# ==================================================================
# AGRISENSE API - FASTAPI ENTRY POINT
# ==================================================================

app = FastAPI(
    title="AgriSense API",
    description="The unified backend driving the AgriSense Agricultural Machine Learning Platform.",
    version="1.0.0"
)

# ------------------------------------------------------------------
# 1. CORS Middleware (Cross-Origin Resource Sharing)
# ------------------------------------------------------------------
# Our React/Next.js frontend runs on localhost:3000
# Our FastAPI backend runs on localhost:8000
# Without CORS, browsers block the frontend from talking to the backend!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

# ------------------------------------------------------------------
# 2. Register Routers
# ------------------------------------------------------------------
# We inject all the routes from our 'routers' folder.
# This keeps main.py clean and highly organized.
app.include_router(market_router)

# ------------------------------------------------------------------
# 3. Root Health Check Endpoint
# ------------------------------------------------------------------
@app.get("/", tags=["System"])
def health_check():
    """Simple status endpoint to verify the API is running."""
    return {
        "status": "online",
        "service": "AgriSense Backend API",
        "docs_url": "/docs"
    }

# NOTE: The ML models (yield_predictor.pkl, price_forecaster.pkl) 
# will be loaded in their specific prediction routers later!
