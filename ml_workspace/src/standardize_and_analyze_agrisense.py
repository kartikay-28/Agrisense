"""
=============================================================================
Script: STANDARDIZE & ANALYZE - Naming Conventions and Grouping Data
=============================================================================

Educational Purpose:
This script teaches you how to STANDARDIZE column names and compute
SUMMARY STATISTICS using pandas groupby().

Why standardize column names?
In the real world, data comes from different sources (different markets, 
different weather stations). One Excel file might call it "Crop_Name", 
another might say "commodity", and a third might say "  Crop Name  ".
If you don't standardize names, your code will crash because it won't 
find the columns it expects!

Key Concepts Learned:
- df.columns.str methods (lowercase, strip, replace)
- df.rename() for specific column mapping
- df.groupby() for aggregating data by categories
- df.agg() for multiple statistics at once (mean, min, max)
- Sorting results with sort_values()

Author: AgriSense Educational Series
Sections: 4.36 - 4.38
Date: April 2026

=============================================================================
"""

import pandas as pd
from pathlib import Path

# ============================================================================
# SECTION 1: STANDARDIZE COLUMN NAMES
# ============================================================================

def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes all column names in a DataFrame.
    
    Steps taken:
    1. Convert to lowercase
    2. Remove leading/trailing spaces
    3. Remove special characters like (), #, etc.
    4. Replace spaces with underscores
    5. Rename common variations to standard AgriSense names
    """
    # Work on a copy to avoid SettingWithCopyWarning
    df_clean = df.copy()
    
    # Save original columns for comparison later
    original_cols = list(df_clean.columns)
    
    # Step 1-4: String manipulation on column names directly
    df_clean.columns = (
        df_clean.columns
        .str.lower()                                    # 1. Lowercase
        .str.strip()                                    # 2. Remove edge spaces
        .str.replace(r'[^a-z0-9_\s]', '', regex=True)   # 3. Remove special chars
        .str.replace(r'\s+', '_', regex=True)           # 4. Spaces to underscores
    )
    
    # Step 5: Rename specific variations to our AgriSense standards
    # We want: crop_name, modal_price, arrival_date, state
    mapping = {
        'commodity': 'crop_name',
        'cropname': 'crop_name',
        'cropnm': 'crop_name',
        
        'price': 'modal_price',
        'modalprice': 'modal_price',
        'modal_price_rs': 'modal_price',
        
        'date': 'arrival_date',
        'arrivaldate': 'arrival_date',
        
        'statename': 'state'
    }
    
    # Apply the renaming
    df_clean = df_clean.rename(columns=mapping)
    
    # Print the Before and After
    print("\n" + "=" * 60)
    print("🧹 STANDARD STATUS: COLUMN NAMES")
    print("=" * 60)
    print(f"Original Columns:     {original_cols}")
    print(f"Standardized Columns: {list(df_clean.columns)}")
    
    return df_clean


def inject_messy_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Utility function to scramble our nice columns so we can
    demonstrate the cleaning process.
    """
    df_messy = df.copy()
    # Intentionally messy names with spaces, caps, and special characters
    messy_names = {
        'date': 'Arrival Date ',
        'commodity': 'Crop_Name',
        'modal_price': 'Modal Price (Rs)',
        'state': ' State_Name '
    }
    return df_messy.rename(columns=messy_names)


# ============================================================================
# SECTION 2: SUMMARY STATISTICS & COMPARISON
# ============================================================================

def analyze_crop_prices(df: pd.DataFrame):
    """
    Uses pandas groupby() to compute summary statistics and compare crops.
    """
    print("\n" + "=" * 60)
    print("📈 AGRISENSE - DATA ANALYSIS & SUMMARY")
    print("=" * 60)
    
    # 1. Group by crop and calculate mean, min, max, and count
    # The agg() function lets us compute multiple stats at the same time!
    crop_stats = df.groupby('crop_name')['modal_price'].agg(['mean', 'min', 'max', 'count'])
    
    # Round the mean for cleaner output
    crop_stats['mean'] = crop_stats['mean'].round(2)
    
    print("\n🟢 Average Price by Crop:")
    for crop in crop_stats.index:
        avg_price = crop_stats.loc[crop, 'mean']
        print(f"  {crop.ljust(10)} → ₹{avg_price:,.2f}")
    
    # 2. Top Most Expensive and Cheapest Crops
    # Sort values based on the 'mean' column
    sorted_by_price = crop_stats.sort_values(by='mean', ascending=False)
    
    print("\n🔝 Top Most Expensive Crops (on average):")
    # Using head(3) instead of 5 because our standard dataset has 5 crops total
    top_3 = sorted_by_price.head(3)
    for i, (crop, row) in enumerate(top_3.iterrows(), 1):
        print(f"  {i}. {crop.ljust(10)} (₹{row['mean']:.2f})")
        
    print("\n📉 Top Cheapest Crops (on average):")
    bottom_3 = sorted_by_price.tail(3).sort_values(by='mean') # Re-sort ascending to show lowest first
    for i, (crop, row) in enumerate(bottom_3.iterrows(), 1):
        print(f"  {i}. {crop.ljust(10)} (₹{row['mean']:.2f})")
        

def compare_specific_crops(df: pd.DataFrame, crops_to_compare: list):
    """
    Compare specific crops side-by-side using describe()
    """
    print("\n" + "=" * 60)
    print(f"⚖️ CROP COMPARISON: {' vs '.join(crops_to_compare)}")
    print("=" * 60)
    
    # Filter the dataframe to only include the crops we want to compare
    comparison_df = df[df['crop_name'].isin(crops_to_compare)]
    
    # Group by crop name and use describe() to get full distribution stats
    stats = comparison_df.groupby('crop_name')['modal_price'].describe().round(2)
    
    for crop in crops_to_compare:
        if crop in stats.index:
            row = stats.loc[crop]
            print(f"\n🌾 {crop.upper()}:")
            print(f"   Data Points: {int(row['count'])} records")
            print(f"   Mean Price:  ₹{row['mean']:,.2f}")
            print(f"   Price Range: ₹{row['min']:,.2f} to ₹{row['max']:,.2f}")
            print(f"   Volatility (Std Dev): ₹{row['std']:,.2f}")
            print(f"   Median (50%): ₹{row['50%']:,.2f}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    
    # Define file paths safely using pathlib
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_path = project_root / "data" / "raw" / "mandi_prices.csv"
    
    if not data_path.exists():
        print(f"❌ Error: Cannot find {data_path}")
        print("Please ensure your raw data is placed in the data/raw folder.")
    else:
        # Load the raw dataset
        raw_df = pd.read_csv(data_path)
        
        # 1. Scramble columns for educational demonstration
        messy_df = inject_messy_columns(raw_df)
        
        # 2. Section 4.36: Standardize names
        clean_df = standardize_column_names(messy_df)
        
        # 3. Section 4.37: Summary Stats
        analyze_crop_prices(clean_df)
        
        # 4. Section 4.38: Crop Comparisons
        compare_specific_crops(clean_df, ['Wheat', 'Rice'])

# ============================================================================
# STUDENT INSTRUCTIONS & AGRISENSE CONTEXT
# ============================================================================
"""
📚 HOW THIS SCRIPT CONNECTS TO YOUR PROJECT

1. HOW TO RUN:
   Open your terminal and run:
   > python src/standardize_and_analyze_agrisense.py

2. WHY STANDARDIZING NAMES MATTERS:
   In your FastAPI backend (`backend/routes/predict.py` or `farms.py`), 
   you will write functions that expect column names like `crop_name` 
   and `state`.
   
   If a user uploads a new Excel file to the AgriSense dashboard and the 
   column is named "Crop Name " (with a space at the end), pandas will 
   throw a KeyError because "crop_name" != "Crop Name ". 
   
   Calling `standardize_column_names()` guarantees your columns behave, 
   no matter how messy the uploaded file is.

3. WHY GROUPBY MATTERS:
   The `groupby()` function is the engine behind Dashboard charts. 
   When your React frontend asks the backend "Give me the average price 
   of all crops to draw a Bar Chart", the backend will run:
   `df.groupby('crop_name')['modal_price'].mean()`
   and send the resulting JSON to the web app.

Next Step: In Section 4.39, you will learn how to join and merge different 
datasets (like linking pricing data with weather data)!
"""
