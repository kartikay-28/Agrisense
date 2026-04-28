"""
================================================================================
                    AGRISENSE: PANDAS DATAFRAMES & SERIES
          Learn to Load, Explore, and Analyze Agricultural Data from CSV
================================================================================

This script teaches you how to:
    1. Load CSV files into Pandas DataFrames
    2. Explore and understand your data
    3. Work with Series (single columns)
    4. Filter and group data
    5. Calculate statistics for agronomic analysis

Key Learning Goals:
    1. Read CSV files using pd.read_csv()
    2. Understand DataFrame structure (rows × columns)
    3. Extract and work with Series
    4. Use groupby() for crop-based analysis
    5. Handle missing data gracefully
    6. Create reusable data loading functions

Real-World Context:
    This script will power:
    - Market Price API (get prices for any crop/date)
    - Climate Risk Advisor (analyze weather patterns)
    - Yield Prediction (historical data aggregation)
    - Dashboard visualizations (data exploration)

Author: AgriSense Education Team
Version: 1.0
================================================================================
"""


import pandas as pd
import numpy as np
# Path is used for file system operations (e.g., locating data files)
from pathlib import Path
from typing import Optional, Tuple


# ============================================================================
# SECTION 1: FILE PATHS & SETUP
# ============================================================================

# Use pathlib for cross-platform file paths (works on Windows, Mac, Linux)
PROJECT_ROOT = Path(__file__).parent.parent  # Go up from src/ to project root
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

print(f"\n{'='*80}")
print(f"Project root: {PROJECT_ROOT}")
print(f"Data directory: {RAW_DATA_DIR}")
print(f"{'='*80}")


# ============================================================================
# SECTION 2: HELPER FUNCTION TO CHECK FILE EXISTS
# ============================================================================

def file_exists(filepath: Path) -> bool:
    """
    Check if a file exists and print a helpful message if it doesn't.
    
    Args:
        filepath: Path object to the file to check
        
    Returns:
        True if file exists, False otherwise
    """
    if filepath.exists():
        print(f"✓ Found: {filepath}")
        return True
    else:
        print(f"✗ NOT FOUND: {filepath}")
        print(f"  Please ensure the CSV file exists at this location.")
        return False


# ============================================================================
# SECTION 3: LOAD CROP PRICES DATA
# ============================================================================

def load_crop_prices(filepath: Optional[Path] = None) -> Optional[pd.DataFrame]:
    """
    Load crop prices CSV file into a Pandas DataFrame.
    
    This function demonstrates:
    - Reading CSV files with pd.read_csv()
    - Handling file paths with pathlib
    - Error handling for missing files
    - Initial data exploration
    
    Args:
        filepath: Path to the CSV file. If None, uses default location.
        
    Returns:
        Pandas DataFrame with price data, or None if file not found
    """
    
    # Use default path if not specified
    if filepath is None:
        filepath = RAW_DATA_DIR / "mandi_prices.csv"
    
    print(f"\n{'='*80}")
    print("STEP 1: LOADING CROP PRICES DATA")
    print(f"{'='*80}")
    
    # Always check if file exists first!
    if not file_exists(filepath):
        print("\n💡 TIP: You need to create a CSV file at the path above.")
        print("   The CSV should have columns like: date, commodity, modal_price, etc.")
        return None
    
    try:
        # Read the CSV file into a DataFrame
        # This is the most common way to load data for analysis
        df = pd.read_csv(filepath)
        
        print(f"\n✓ Successfully loaded data from {filepath.name}")
        print(f"  Total rows: {len(df):,}")
        print(f"  Total columns: {len(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"\n✗ Error loading CSV file: {e}")
        return None


# ============================================================================
# SECTION 4: LOAD WEATHER DATA
# ============================================================================

def load_weather_data(filepath: Optional[Path] = None) -> Optional[pd.DataFrame]:
    """
    Load weather data CSV file into a Pandas DataFrame.
    
    Note: If weather_data.csv doesn't exist, we'll create sample data
    to demonstrate the concepts.
    
    Args:
        filepath: Path to the CSV file. If None, uses default location.
        
    Returns:
        Pandas DataFrame with weather data, or None if loading fails
    """
    
    if filepath is None:
        filepath = RAW_DATA_DIR / "weather_data.csv"
    
    print(f"\n{'='*80}")
    print("STEP 2: LOADING WEATHER DATA")
    print(f"{'='*80}")
    
    if file_exists(filepath):
        try:
            df = pd.read_csv(filepath)
            print(f"\n✓ Successfully loaded weather data")
            print(f"  Total rows: {len(df):,}")
            print(f"  Total columns: {len(df.columns)}")
            return df
        except Exception as e:
            print(f"\n✗ Error loading weather CSV: {e}")
            return None
    else:
        print("\n💡 Weather data CSV not found. Creating sample data instead...")
        return create_sample_weather_data()


# ============================================================================
# SECTION 5: CREATE SAMPLE DATA (FALLBACK)
# ============================================================================

def create_sample_weather_data() -> pd.DataFrame:
    """
    Create sample weather data if the CSV file doesn't exist.
    This allows us to demonstrate DataFrame operations even without
    real data files.
    
    Returns:
        DataFrame with sample weather data
    """
    sample_data = {
        'date': pd.date_range('2024-01-01', periods=30, freq='D'),
        'state': ['Himachal Pradesh'] * 10 + ['Punjab'] * 10 + ['Haryana'] * 10,
        'rainfall_mm': np.random.uniform(5, 25, 30),
        'temperature_c': np.random.uniform(15, 35, 30),
        'humidity_pct': np.random.uniform(40, 90, 30),
        'wind_speed_kmh': np.random.uniform(5, 20, 30)
    }
    
    df = pd.DataFrame(sample_data)
    print(f"✓ Created sample weather data: {len(df)} rows")
    return df


# ============================================================================
# SECTION 6: EXPLORE DATAFRAME STRUCTURE
# ============================================================================

def explore_dataframe(df: pd.DataFrame, name: str = "Data"):
    """
    Demonstrate essential DataFrame exploration methods.
    
    This function shows:
    - df.head() - first few rows
    - df.shape - dimensions
    - df.columns - column names
    - df.dtypes - data types
    - df.info() - summary information
    - df.describe() - statistical summary
    
    Args:
        df: The DataFrame to explore
        name: Name to print (e.g., "Crop Prices")
    """
    
    print(f"\n{'='*80}")
    print(f"EXPLORING {name.upper()}")
    print(f"{'='*80}")
    
    # 1. DataFrame SHAPE (dimensions)
    print(f"\n1. SHAPE: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"   Meaning: {df.shape[0]:,} records with {df.shape[1]} variables each")
    
    # 2. COLUMN NAMES
    print(f"\n2. COLUMN NAMES:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    
    # 3. DATA TYPES
    print(f"\n3. DATA TYPES:")
    print(df.dtypes)
    
    # 4. FIRST FEW ROWS
    print(f"\n4. FIRST 5 ROWS (using .head()):")
    print(df.head())
    
    # 5. STATISTICAL SUMMARY
    print(f"\n5. STATISTICAL SUMMARY (using .describe()):")
    print(df.describe())
    
    # 6. MISSING VALUES
    print(f"\n6. MISSING VALUES (using .isnull().sum()):")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   ✓ No missing values! Data is clean.")
    else:
        print(missing[missing > 0])


# ============================================================================
# SECTION 7: WORK WITH SERIES
# ============================================================================

def explore_series(df: pd.DataFrame, column_name: str):
    """
    Demonstrate Series operations.
    
    A Series is a single column from a DataFrame — essentially a 1D array
    with labeled indices. This function shows:
    - How to extract a Series
    - Basic statistics (mean, min, max, std)
    - Value counts (how many of each value)
    - Filtering
    
    Args:
        df: DataFrame containing the column
        column_name: Name of the column to extract as Series
    """
    
    print(f"\n{'='*80}")
    print(f"WORKING WITH SERIES: {column_name.upper()}")
    print(f"{'='*80}")
    
    # Check if column exists
    if column_name not in df.columns:
        print(f"\n✗ Column '{column_name}' not found in DataFrame")
        print(f"  Available columns: {list(df.columns)}")
        return
    
    # Extract column as Series
    series = df[column_name]
    
    print(f"\n1. SERIES BASICS:")
    print(f"   Type: {type(series).__name__}")
    print(f"   Length: {len(series)} values")
    print(f"   Data type: {series.dtype}")
    
    # For numeric columns, show statistics
    if pd.api.types.is_numeric_dtype(series):
        print(f"\n2. STATISTICS:")
        print(f"   Mean:        {series.mean():.2f}")
        print(f"   Median:      {series.median():.2f}")
        print(f"   Std Dev:     {series.std():.2f}")
        print(f"   Min:         {series.min():.2f}")
        print(f"   Max:         {series.max():.2f}")
        print(f"   25th %ile:   {series.quantile(0.25):.2f}")
        print(f"   75th %ile:   {series.quantile(0.75):.2f}")
    
    # For categorical columns, show value counts
    else:
        print(f"\n2. UNIQUE VALUES (using .value_counts()):")
        value_counts = series.value_counts()
        if len(value_counts) <= 10:
            print(value_counts)
        else:
            print(value_counts.head(10))


# ============================================================================
# SECTION 8: FILTER DATA
# ============================================================================

def filter_data_examples(df: pd.DataFrame):
    """
    Demonstrate different ways to filter (subset) a DataFrame.
    
    Filtering is essential for:
    - Finding prices for a specific crop
    - Getting data for a specific region
    - Selecting recent data only
    - Finding high-yield fields
    
    Args:
        df: DataFrame to filter
    """
    
    print(f"\n{'='*80}")
    print("FILTERING DATA EXAMPLES")
    print(f"{'='*80}")
    
    print("\n1. FILTER BY SINGLE CONDITION:")
    print("   Code: df[df['price'] > 2000]")
    
    # Try different filters based on available columns
    if 'modal_price' in df.columns:
        high_price = df[df['modal_price'] > df['modal_price'].quantile(0.75)]
        print(f"   Crops with price > 75th percentile: {len(high_price)} rows")
        if len(high_price) > 0:
            print(f"   Sample:\n{high_price.head(3)}\n")
    
    print("\n2. FILTER BY MULTIPLE CONDITIONS:")
    print("   Code: df[(df['price'] > 2000) & (df['quantity'] > 100)]")
    if 'modal_price' in df.columns:
        filtered = df[df['modal_price'] > df['modal_price'].mean()]
        print(f"   Result: {len(filtered)} rows with above-average price\n")
    
    print("3. SELECT SPECIFIC COLUMNS:")
    print("   Code: df[['commodity', 'modal_price']]")
    if 'modal_price' in df.columns and 'commodity' in df.columns:
        subset = df[['commodity', 'modal_price']].head(5)
        print(f"   Result:\n{subset}\n")


# ============================================================================
# SECTION 9: GROUP AND AGGREGATE
# ============================================================================

def groupby_examples(df: pd.DataFrame):
    """
    Demonstrate GROUP BY operations.
    
    GroupBy is incredibly useful for agricultural analysis:
    - Average price per crop
    - Total yield per state
    - Weather patterns by season
    - Price trends per commodity
    
    Args:
        df: DataFrame to group
    """
    
    print(f"\n{'='*80}")
    print("GROUP BY & AGGREGATION")
    print(f"{'='*80}")
    
    print("\n1. GROUP BY SINGLE COLUMN:")
    if 'commodity' in df.columns and 'modal_price' in df.columns:
        print("   Code: df.groupby('commodity')['modal_price'].mean()")
        grouped = df.groupby('commodity')['modal_price'].agg(['mean', 'min', 'max', 'count'])
        grouped.columns = ['Average Price', 'Min Price', 'Max Price', 'Count']
        print(f"\n   Result:\n{grouped}\n")
    
    print("\n2. MULTIPLE AGGREGATIONS:")
    if 'commodity' in df.columns and 'modal_price' in df.columns:
        print("   Code: df.groupby('commodity').agg({'modal_price': 'mean', ...})")
        agg_df = df.groupby('commodity')['modal_price'].agg([
            ('average_price', 'mean'),
            ('volatile_low', 'min'),
            ('volatile_high', 'max'),
            ('days_recorded', 'count')
        ])
        print(f"\n   Result:\n{agg_df.head()}\n")
    
    print("\n3. WHAT'S AVAILABLE IN YOUR DATA?")
    if 'commodity' in df.columns:
        unique_commodities = df['commodity'].unique()
        print(f"   Unique commodities: {len(unique_commodities)}")
        print(f"   Sample crops: {', '.join(unique_commodities[:5])}")


# ============================================================================
# SECTION 10: HANDLE MISSING DATA
# ============================================================================

def check_data_quality(df: pd.DataFrame, name: str = "Data"):
    """
    Check and report on data quality issues.
    
    Real-world data is messy! This function helps identify:
    - Missing values (NaN, None)
    - Duplicate rows
    - Unusual data types
    - Potential outliers
    
    Args:
        df: DataFrame to check
        name: Name for reporting
    """
    
    print(f"\n{'='*80}")
    print(f"DATA QUALITY CHECK: {name}")
    print(f"{'='*80}")
    
    # 1. Missing values
    print(f"\n1. MISSING VALUES:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   ✓ No missing values!")
    else:
        print("   Missing values per column:")
        for col, count in missing[missing > 0].items():
            pct = (count / len(df)) * 100
            print(f"   - {col}: {count} ({pct:.1f}%)")
    
    # 2. Duplicates
    print(f"\n2. DUPLICATE ROWS:")
    duplicates = df.duplicated().sum()
    if duplicates == 0:
        print("   ✓ No duplicate rows!")
    else:
        print(f"   ⚠ Found {duplicates} duplicate rows")
        print("   Code to remove: df.drop_duplicates(inplace=True)")
    
    # 3. Data types
    print(f"\n3. DATA TYPES:")
    print(df.dtypes)
    
    # 4. Basic stats
    print(f"\n4. QUICK STATS:")
    print(f"   Total records: {len(df):,}")
    print(f"   Total features: {len(df.columns)}")
    print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")


# ============================================================================
# SECTION 11: CREATE REUSABLE DATA LOADER
# ============================================================================

class AgriSenseDataLoader:
    """
    A reusable class to load and manage agricultural data.
    
    This class encapsulates all data loading operations, making it
    easy to use in other parts of the AgriSense application.
    
    Usage:
        loader = AgriSenseDataLoader()
        prices_df = loader.load_prices()
        weather_df = loader.load_weather()
    
    This pattern is called a "data access layer" and it's great for:
    - Keeping data loading logic in one place
    - Making the code reusable
    - Easy to test
    - Easy to swap data sources (CSV → database)
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the data loader.
        
        Args:
            data_dir: Path to data directory. Uses default if None.
        """
        if data_dir is None:
            data_dir = RAW_DATA_DIR
        
        self.data_dir = data_dir
        self.prices_df = None
        self.weather_df = None
    
    def load_prices(self) -> Optional[pd.DataFrame]:
        """Load and cache crop prices data."""
        if self.prices_df is None:
            self.prices_df = load_crop_prices(self.data_dir / "mandi_prices.csv")
        return self.prices_df
    
    def load_weather(self) -> Optional[pd.DataFrame]:
        """Load and cache weather data."""
        if self.weather_df is None:
            self.weather_df = load_weather_data(self.data_dir / "weather_data.csv")
        return self.weather_df
    
    def get_prices_for_crop(self, crop_name: str) -> Optional[pd.DataFrame]:
        """
        Get all price records for a specific crop.
        
        Args:
            crop_name: Name of the crop to filter
            
        Returns:
            Filtered DataFrame or None if crop not found
        """
        prices = self.load_prices()
        
        if prices is None or 'commodity' not in prices.columns:
            return None
        
        return prices[prices['commodity'].str.lower() == crop_name.lower()]
    
    def get_average_price(self, crop_name: str) -> Optional[float]:
        """
        Get average price for a crop.
        
        Args:
            crop_name: Name of the crop
            
        Returns:
            Average price or None if not available
        """
        crop_prices = self.get_prices_for_crop(crop_name)
        
        if crop_prices is None or len(crop_prices) == 0:
            return None
        
        if 'modal_price' in crop_prices.columns:
            return crop_prices['modal_price'].mean()
        
        return None


# ============================================================================
# SECTION 12: MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*18 + "AGRISENSE: PANDAS DATAFRAMES & SERIES TUTORIAL" + " "*15 + "║")
    print("║" + " "*16 + "Learn to Load and Analyze Agricultural Data" + " "*20 + "║")
    print("╚" + "="*78 + "╝")
    
    # ---- LOAD DATA ----
    print("\n📂 STEP 1: LOAD DATA FROM CSV FILES")
    print("="*80)
    
    prices_df = load_crop_prices()
    weather_df = load_weather_data()
    
    # ---- EXPLORE PRICES DATA ----
    if prices_df is not None:
        explore_dataframe(prices_df, "Crop Prices")
        
        # Work with specific columns as Series
        if 'modal_price' in prices_df.columns:
            explore_series(prices_df, 'modal_price')
        
        if 'commodity' in prices_df.columns:
            explore_series(prices_df, 'commodity')
        
        # Filter examples
        filter_data_examples(prices_df)
        
        # Group by examples
        groupby_examples(prices_df)
        
        # Data quality
        check_data_quality(prices_df, "Crop Prices")
    
    # ---- EXPLORE WEATHER DATA ----
    if weather_df is not None:
        explore_dataframe(weather_df, "Weather")
        check_data_quality(weather_df, "Weather")
    
    # ---- DEMONSTRATE REUSABLE CLASS ----
    print("\n" + "="*80)
    print("BONUS: USING THE REUSABLE DATA LOADER CLASS")
    print("="*80)
    
    loader = AgriSenseDataLoader()
    
    print("\nLoading data using the AgriSenseDataLoader class:")
    loader_prices = loader.load_prices()
    loader_weather = loader.load_weather()
    
    if loader_prices is not None and 'commodity' in loader_prices.columns:
        print("\nFinding price statistics for specific crops:")
        sample_crops = loader_prices['commodity'].unique()[:3]
        
        for crop in sample_crops:
            avg_price = loader.get_average_price(crop)
            if avg_price is not None:
                print(f"  {crop}: ₹{avg_price:.2f} (average)")
    
    # ---- INSTRUCTIONS ----
    print("\n" + "="*80)
    print("HOW TO USE THIS SCRIPT")
    print("="*80)
    
    instructions = """
1. PREPARE YOUR DATA:
   
   You need CSV files in: data/raw/
   
   • mandi_prices.csv should have columns like:
     - date
     - commodity (crop name: Wheat, Rice, etc.)
     - modal_price (₹ per quintal)
     - market (optional)
     - state (optional)
   
   • weather_data.csv should have columns like:
     - date
     - state
     - rainfall_mm
     - temperature_c
     - humidity_pct

2. CREATE SAMPLE CSV FILES:
   
   If you don't have real data, create sample CSVs:
   
   Example: data/raw/mandi_prices.csv
   ──────────────────────────────────
   date,commodity,modal_price,market
   2024-01-01,Wheat,2400,Shimla
   2024-01-01,Rice,3200,Chandgarh
   2024-01-02,Wheat,2410,Shimla
   ...

3. RUN THE SCRIPT:
   
   python src/load_dataframes_agrisense.py

4. UNDERSTAND THE OUTPUT:
   
   ✓ Learns how to download and explore data
   ✓ Shows DataFrame structure and operations
   ✓ Demonstrates Series (column) operations
   ✓ Shows filtering and grouping techniques

5. USE IN YOUR APPLICATION:
   
   From other Python files, you can now:
   
   from load_dataframes_agrisense import AgriSenseDataLoader
   
   loader = AgriSenseDataLoader()
   prices = loader.load_prices()
   avg = loader.get_average_price('Wheat')

FEATURES THAT WILL USE THIS:
───────────────────────────

✓ Market Page:
  - Display prices using groupby() results
  - Filter by crop using the filtering examples

✓ Climate Risk Advisor:
  - Load weather data
  - Calculate averages by state and season
  - Show historical patterns

✓ Yield Prediction:
  - Aggregate yield data by crop
  - Compare across regions
  - Calculate percentiles

✓ Dashboard:
  - Show recent prices (filter by date)
  - Display trends (groupby + aggregation)
  - Compare crops (Series statistics)

✓ Price API:
  - Use AgriSenseDataLoader class
  - Return prices as JSON
  - Filter by crop/date/state

NEXT STEPS:
──────────

1. Create your CSV files in data/raw/
2. Run this script to verify loading works
3. Modify groupby_examples() to explore YOUR data
4. Create new functions for specific needs
5. Import AgriSenseDataLoader in your feature code

"""
    print(instructions)
    
    print("="*80)
    print("Made with ❤️ for AgriSense - Understanding Pandas DataFrames")
    print("="*80 + "\n")
