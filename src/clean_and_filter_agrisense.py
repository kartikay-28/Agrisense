"""
=============================================================================
Script: DATA CLEANING & FILTERING - Getting Data Ready for AgriSense
=============================================================================

Educational Purpose:
This script teaches you how to CLEAN and FILTER data using pandas.
In real-world agriculture data (like Mandi prices or weather reports),
data is NEVER perfect. It will have gaps, mistakes, and duplicate entries.

Why is cleaning "non-negotiable"?
If you train a Machine Learning model on bad data, it will make bad
predictions (Garbage In = Garbage Out). If your API serves missing prices,
the AgriSense Market Dashboard will crash. 

Key Concepts Learned:
- Indexing & Slicing: Extracting specific rows/columns (.loc[], boolean indexing)
- Filtering: df[df['column'] == 'value'] and .between() for dates
- Duplicates: df.duplicated().sum() and df.drop_duplicates()
- Missing Values: df.isnull().sum(), df.dropna(), and df.fillna()

Author: AgriSense Educational Series
Sections: 4.32 - 4.35
Date: April 2026

=============================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================================
# SECTION 1: FILTERING (INDEXING & SLICING)
# ============================================================================
# These functions are reusable! You can import them directly into your
# FastAPI backend routes to serve filtered data to the React frontend.

def filter_by_crop(df: pd.DataFrame, crop_name: str) -> pd.DataFrame:
    """
    Filter the dataframe to show only records for a specific crop.
    
    Demonstrates: Boolean Indexing
    Formula: dataframe[condition]
    """
    # Make it case-insensitive to avoid missing 'wheat' if user types 'Wheat'
    condition = df['commodity'].str.lower() == crop_name.lower()
    
    # Return the filtered dataframe
    return df[condition]

def filter_by_state(df: pd.DataFrame, state_name: str) -> pd.DataFrame:
    """
    Filter the dataframe for a specific state using .loc[]
    
    Demonstrates: .loc[] filtering
    Formula: dataframe.loc[row_indexer, column_indexer]
    """
    # Using .loc is another popular way to filter data in pandas
    # .loc[rows_we_want, :] means get specific rows, and all columns
    condition = df['state'].str.lower() == state_name.lower()
    return df.loc[condition, :]

def filter_by_date_range(df: pd.DataFrame, start_date: str, end_date: str, date_col: str = 'date') -> pd.DataFrame:
    """
    Filter the dataframe for records that fall between two dates.
    
    Demonstrates: .between() and type conversion
    """
    # Always ensure the date column is actually a datetime object!
    # If it's stored as plain text (string), filtering between dates won't work correctly.
    df = df.copy()  # Create a copy to avoid SettingWithCopyWarning
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Convert input strings to datetime
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # Use pandas .between() method for extremely clean date filtering
    condition = df[date_col].between(start, end)
    return df[condition]


# ============================================================================
# SECTION 2: HANDLING MISSING VALUES & DUPLICATES
# ============================================================================

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    A comprehensive function to clean raw agricultural data.
    Finds and handles duplicates and missing values.
    
    Returns a clean, analytics-ready DataFrame.
    """
    print("\n" + "=" * 60)
    print("🧹 AGRISENSE DATA CLEANING PROCESS")
    print("=" * 60)
    
    # Work on a copy of the dataframe to keep the original safe
    cleaned_df = df.copy()
    
    # ---------------------------------------------------------
    # STEP 1: Record Original State
    # ---------------------------------------------------------
    original_shape = cleaned_df.shape
    print(f"Original Shape: {original_shape[0]} rows, {original_shape[1]} columns")
    
    # ---------------------------------------------------------
    # STEP 2: Handle Duplicates
    # ---------------------------------------------------------
    # Check how many exact duplicate rows exist
    duplicate_count = cleaned_df.duplicated().sum()
    
    if duplicate_count > 0:
        print(f"Found {duplicate_count} duplicate rows. Removing them...")
        # Drop duplicates and modify the dataframe in place
        cleaned_df.drop_duplicates(inplace=True)
    else:
        print("No duplicate rows found.")
        
    print(f"Shape after removing duplicates: {cleaned_df.shape}")
    
    # ---------------------------------------------------------
    # STEP 3: Handle Missing Values (NaN)
    # ---------------------------------------------------------
    print("\nChecking for Missing Values:")
    missing_totals = cleaned_df.isnull().sum()
    
    if missing_totals.sum() == 0:
        print("✓ No missing values detected! Data is fully populated.")
    else:
        # Show columns that have missing data
        for col, count in missing_totals.items():
            if count > 0:
                print(f" - {col}: {count} missing values")
                
                # Handling strategy depends on the column:
                if col == 'modal_price':
                    # Strategy A: Imputation (filling missing values)
                    # For prices, substituting the median is safer than the mean 
                    # because it ignores extreme outliers.
                    median_price = cleaned_df['modal_price'].median()
                    cleaned_df[col] = cleaned_df[col].fillna(median_price)
                    print(f"   → Filled missing {col} with median value: ₹{median_price:.2f}")
                
                elif cleaned_df[col].dtype == 'object':
                    # Strategy B: Fill with "Unknown" for text columns
                    cleaned_df[col] = cleaned_df[col].fillna("Unknown")
                    print(f"   → Filled missing text in {col} with 'Unknown'")
                    
                else:
                    # Strategy C: Drop rows with missing values
                    # If we don't know how to fill it safely, just remove the row entirely.
                    initial_rows = len(cleaned_df)
                    cleaned_df.dropna(subset=[col], inplace=True)
                    rows_dropped = initial_rows - len(cleaned_df)
                    print(f"   → Dropped {rows_dropped} rows due to missing {col}")

    print("\n" + "=" * 60)
    print("✓ Cleaning Complete! Data is ready for ML and Dashboards.")
    print("=" * 60 + "\n")
    
    return cleaned_df


# ============================================================================
# UTILITY: Create Messy Data for Demonstration
# ============================================================================
def inject_messy_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Since our sample mandi_prices.csv is surprisingly clean, 
    this helper function injects some artificial messiness 
    (duplicates and missing values) so we can see the cleaning in action!
    """
    messy = df.copy()
    
    # 1. Add some exact duplicate rows (take first 3 rows and append them)
    duplicates_to_add = messy.head(3)
    messy = pd.concat([messy, duplicates_to_add], ignore_index=True)
    
    # 2. Inject some NaN (missing) values into random places
    messy.loc[5, 'modal_price'] = np.nan
    messy.loc[12, 'modal_price'] = np.nan
    messy.loc[18, 'state'] = np.nan
    messy.loc[25, 'market'] = np.nan
    
    return messy


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    
    # Setup paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_path = project_root / "data" / "raw" / "mandi_prices.csv"
    
    print("\n" + "=" * 80)
    print("🌾 AGRISENSE: DATA CLEANING AND FILTERING DEMO")
    print("=" * 80)
    
    if not data_path.exists():
        print(f"❌ Error: Cannot find {data_path}")
        print("Please ensure your raw data is placed in the data/raw folder.")
    else:
        # Load the raw data
        raw_df = pd.read_csv(data_path)
        print(f"\n1️⃣ Successfully loaded raw dataset (Shape: {raw_df.shape})")
        
        # Make the data "messy" just to demonstrate our cleaning function
        # (In reality, you wouldn't do this, you'd just clean the raw data directly)
        messy_df = inject_messy_data(raw_df)
        print(f"   Injected artificial duplicates and missing values for demonstration.")
        print(f"   Messy Shape: {messy_df.shape}")
        
        # --- CLEANING DEMO ---
        # Run our master cleaning function
        clean_df = clean_dataset(messy_df)
        
        # --- FILTERING DEMO ---
        print("\n" + "=" * 60)
        print("🔍 FILTERING (INDEXING & SLICING) EXAMPLES")
        print("=" * 60)
        
        # Example 1: Filter by Crop
        target_crop = "Wheat"
        wheat_df = filter_by_crop(clean_df, target_crop)
        print(f"\n🌾 Filtered by Crop: '{target_crop}'")
        print(f"   Found {len(wheat_df)} records.")
        if not wheat_df.empty:
            print("   Average price: ₹{:.2f}".format(wheat_df['modal_price'].mean()))
        
        # Example 2: Filter by State
        target_state = "Himachal Pradesh"
        state_df = filter_by_state(clean_df, target_state)
        print(f"\n🗺️ Filtered by State: '{target_state}'")
        print(f"   Found {len(state_df)} records.")
        if not state_df.empty:
             print("   Sample unique crops grown here: {}".format(
                 ", ".join(state_df['commodity'].unique())
             ))
        
        # Example 3: Filter by Date Range AND Crop
        try:
            date_df = filter_by_date_range(clean_df, "2024-01-01", "2024-01-04")
            # We can chain filters!
            date_and_crop = filter_by_crop(date_df, "Tomato")
            
            print(f"\n📅 Filtered Tomatoes strictly between Jan 1 and Jan 4, 2024:")
            print(f"   Found {len(date_and_crop)} records.")
            if not date_and_crop.empty:
                print(f"   Highest price in this window: ₹{date_and_crop['modal_price'].max()}")
        except Exception as e:
            print(f"\n   Notice: Date range filter failed. Date column might not be formatted right.")
            print(f"   Error: {e}")


# ============================================================================
# STUDENT INSTRUCTIONS & AGRISENSE CONTEXT
# ============================================================================
"""
📚 HOW THIS SCRIPT CONNECTS TO YOUR PROJECT

1. WHERE TO PLACE DATA:
   Ensure your raw CSV file is located at:
   S84-0426-AKM-Python-Pandas-NumPy-AgriSense/data/raw/mandi_prices.csv

2. HOW TO RUN:
   Open your terminal and run:
   > python src/clean_and_filter_agrisense.py

3. WHY IT MATTERS FOR YOUR PAGES:

   📊 Market Page (app/market/page.tsx):
   When a user selects "Wheat" and "Punjab" from the frontend dropdowns, 
   your FastAPI backend will use code EXACTLY like `filter_by_crop()` and
   `filter_by_state()` to slice the data and return only the requested rows
   as JSON.

   📈 Yield & Climate Pages:
   Those pages depend on date ranges (e.g., comparing yields between 2020 
   and 2024). The `filter_by_date_range()` using pandas `.between()` is the
   most efficient way to query huge time-series datasets.

   🤖 Machine Learning Model:
   The `clean_dataset()` function is identical to a "data preprocessing pipeline".
   If you feed NaN (null) values into a Scikit-Learn Random Forest, the 
   training code will crash instantly. Handling duplicates prevents the model
   from artificially over-weighting repeated data.

Next Step: In Section 4.36, we will start building new columns using 
Feature Engineering!
"""
