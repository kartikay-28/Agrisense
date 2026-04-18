import pandas as pd
from pathlib import Path
from fastapi import HTTPException
from utils.crop_mapper import normalize_crop_name, find_canonical_crop, log_crop_search

class DataService:
    """
    DataService handles all Data Loading and Business Logic.
    
    Why separate this from routes?
    1. Separation of Concerns: Routers just handle HTTP requests. Services do the math.
    2. Performance (< 200ms): We load the CSV into memory ONCE during startup/first-request. 
       If we used pd.read_csv() inside the route, the API would be incredibly slow.
    """
    def __init__(self):
        self.df = None
        # Path resolution: Navigate up from services -> backend -> root -> data/processed
        self.data_path = Path(__file__).resolve().parent.parent.parent / "data" / "processed" / "agrisense_features.csv"

    def _load_data(self):
        """Loads and caches the dataframe in memory for lightning-fast queries."""
        if self.df is None:
            if not self.data_path.exists():
                raise FileNotFoundError(f"Dataset missing! Ensure notebook 08 was run at: {self.data_path}")
            
            # Load the single source of truth dataset
            self.df = pd.read_csv(self.data_path)
            self.df['date'] = pd.to_datetime(self.df['date'])

    def get_market_data(self, crop: str, state: str = None, start_date: str = None, end_date: str = None) -> dict:
        """
        Main business logic for fetching, filtering, and shaping market data.
        Now includes crop name normalization and graceful error handling.
        """
        self._load_data()
        
        # Normalize and find canonical crop name
        canonical_crop = find_canonical_crop(crop)
        
        filtered = self.df.copy()
        
        # 1. Filter by Crop with normalized matching
        filtered = filtered[filtered['commodity'].str.lower() == canonical_crop.lower()] if canonical_crop else pd.DataFrame()
        
        log_crop_search(requested=crop, canonical=canonical_crop, found=len(filtered) > 0, count=len(filtered))
        
        # If no data found, return graceful empty response instead of throwing error
        if filtered.empty:
            return {
                "crop_name": crop,
                "current_price": 0,
                "price_change_7d_percent": 0,
                "rolling_avg_7d": 0,
                "rolling_avg_30d": 0,
                "volatility_7d": 0,
                "recent_prices": [],
                "last_updated": None,
                "message": f"No records found for '{crop}' in the dataset."
            }
                
        # 2. Filter by State (Optional)
        if state:
            # Need to verify if 'state' column exists in our df, else ignore bounds
            if 'state' in filtered.columns:
                filtered = filtered[filtered['state'].str.lower() == state.lower()]
                if filtered.empty:
                    return {
                        "crop_name": crop,
                        "current_price": 0,
                        "price_change_7d_percent": 0,
                        "rolling_avg_7d": 0,
                        "rolling_avg_30d": 0,
                        "volatility_7d": 0,
                        "recent_prices": [],
                        "last_updated": None,
                        "message": f"No data for '{crop}' in state '{state}'."
                    }
                
        # 3. Filter by Date Range (Optional)
        if start_date:
            filtered = filtered[filtered['date'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered = filtered[filtered['date'] <= pd.to_datetime(end_date)]
            
        if filtered.empty:
            return {
                "crop_name": crop,
                "current_price": 0,
                "price_change_7d_percent": 0,
                "rolling_avg_7d": 0,
                "rolling_avg_30d": 0,
                "volatility_7d": 0,
                "recent_prices": [],
                "last_updated": None,
                "message": "No data found for the specified date filters."
            }
            
        # Sort chronologically to safely pull the "latest" records
        filtered = filtered.sort_values(by='date')
        
        # Extract the absolute newest row for our top-line metrics
        latest_record = filtered.iloc[-1]
        
        # Extract the last 30 days for the "recent_prices" sparkline array natively
        last_30_days = filtered.tail(30)
        recent_prices = [
            {
                "date": row['date'].strftime("%Y-%m-%d"), 
                "price": float(row['modal_price'])
            } 
            for _, row in last_30_days.iterrows()
        ]
        
        # Helper to convert NaN to 0.0 safely
        def safe_float(val):
            return float(val) if not pd.isna(val) else 0.0

        # Map pandas data into a dictionary that exactly matches our Pydantic Schema
        return {
            "crop_name": str(latest_record.get('commodity', crop)),
            "current_price": safe_float(latest_record.get('modal_price')),
            "price_change_7d_percent": safe_float(latest_record.get('price_pct_change')),
            "rolling_avg_7d": safe_float(latest_record.get('price_rolling_avg_7d')),
            "rolling_avg_30d": safe_float(latest_record.get('price_rolling_avg_30d')),
            "volatility_7d": safe_float(latest_record.get('price_volatility_7d')),
            "recent_prices": recent_prices,
            "last_updated": latest_record['date'].strftime("%Y-%m-%d")
        }

# Instantiate the service as a Singleton pattern so it caches the DF globally for the app
data_service = DataService()
