"""
=============================================================================
Script: INSPECT DATA - Learn to Explore DataFrames Before Analysis
=============================================================================

Educational Purpose:
This script teaches you how to INSPECT data before:
- Building machine learning models
- Creating visualizations
- Making business decisions
- Writing data cleaning code

Why is data inspection important?
1. Understand data structure (rows, columns, data types)
2. Find missing values and outliers
3. Check date ranges and distributions
4. Identify unique values in categorical columns
5. Spot potential data quality issues early

This helps you avoid garbage-in-garbage-out (GIGO) problems!

Key Functions Learned:
- df.head()          → First few rows
- df.info()          → Data types and non-null counts
- df.describe()      → Summary statistics
- df.isnull().sum()  → Missing values
- df.unique()        → Unique values in a column
- df.shape           → Number of rows and columns
- df.columns         → Column names
- df.dtypes          → Data type of each column

Author: AgriSense Educational Series
Sections: 4.30 - 4.31
Date: April 2026

=============================================================================
"""

# Standard library imports
from pathlib import Path

# Third-party imports
import pandas as pd
import sys

# ============================================================================
# FUNCTION 1: Inspect a Single DataFrame
# ============================================================================

def inspect_dataframe(df, dataset_name: str) -> None:
    """
    Thoroughly inspect a pandas DataFrame and print detailed information.
    
    This function demonstrates how to use pandas inspection methods:
    - head(): See the first few rows
    - info(): Get column types and null counts
    - describe(): Get summary statistics
    - isnull().sum(): Count missing values
    - unique(): See unique values in categorical columns
    
    Why this matters:
    When you receive NEW data, this is your FIRST STEP!
    Before writing any analysis code, you must understand what you're working with.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame to inspect
    dataset_name : str
        Human-readable name for the dataset (e.g., "Crop Prices Data")
    
    Returns:
    --------
    None
        Prints formatted output to console
    
    Example:
    --------
    >>> prices_df = pd.read_csv('data/raw/mandi_prices.csv')
    >>> inspect_dataframe(prices_df, "Mandi Prices")
    """
    
    # Print header banner
    print("\n" + "=" * 80)
    print(f"📊 INSPECTING: {dataset_name}")
    print("=" * 80)
    
    
    # STEP 1: Basic Information
    # ========================================================================
    print(f"\n📈 DATASET SHAPE (rows, columns):")
    print(f"   Total Rows: {df.shape[0]:,}")
    print(f"   Total Columns: {df.shape[1]}")
    
    print(f"\n📋 COLUMN NAMES:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    
    
    # STEP 2: Data Types
    # ========================================================================
    print(f"\n🔤 DATA TYPES (important for analysis):")
    print(df.dtypes)
    
    
    # STEP 3: First Few Rows
    # ========================================================================
    print(f"\n👀 FIRST 5 ROWS (to understand structure):")
    print(df.head().to_string())
    
    
    # STEP 4: Summary Statistics
    # ========================================================================
    print(f"\n📊 SUMMARY STATISTICS (numeric columns only):")
    summary = df.describe()
    print(summary.to_string())
    
    
    # STEP 5: Missing Values Check
    # ========================================================================
    print(f"\n⚠️ MISSING VALUES (important for data cleaning!):")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   ✓ Great news! No missing values found.")
    else:
        print(f"   Total missing values: {missing.sum()}")
        print("\n   Break-down by column:")
        for col, count in missing.items():
            if count > 0:
                percentage = (count / len(df)) * 100
                print(f"   - {col}: {count} ({percentage:.2f}%)")
    
    
    # STEP 6: Unique Values in Categorical Columns
    # ========================================================================
    print(f"\n🏷️ UNIQUE VALUES (in categorical/text columns):")
    
    # Identify categorical columns (object or string types)
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    if len(categorical_cols) == 0:
        print("   No categorical columns found.")
    else:
        for col in categorical_cols:
            unique_count = df[col].nunique()
            print(f"\n   {col}: {unique_count} unique value(s)")
            
            # Show unique values if not too many
            if unique_count <= 10:
                print(f"   Values: {sorted(df[col].unique().tolist())}")
            else:
                # Show first 10 if there are many
                print(f"   Sample values: {sorted(df[col].unique()[:10].tolist())}...")
    
    
    # STEP 7: AgriSense-Specific Checks
    # ========================================================================
    # Check if this is crop/mandi price data
    if 'modal_price' in df.columns or 'price' in df.columns:
        print(f"\n💰 PRICE DATA SUMMARY (AgriSense-specific):")
        price_col = 'modal_price' if 'modal_price' in df.columns else 'price'
        
        if df[price_col].dtype in ['float64', 'int64']:
            avg_price = df[price_col].mean()
            max_price = df[price_col].max()
            min_price = df[price_col].min()
            
            print(f"   Average Price: ₹{avg_price:,.2f}")
            print(f"   Highest Price: ₹{max_price:,.2f}")
            print(f"   Lowest Price: ₹{min_price:,.2f}")
    
    
    # Check if this is weather data or has date column
    if 'date' in df.columns:
        print(f"\n📅 DATE RANGE (important for time-series analysis):")
        try:
            df_sorted = df.sort_values('date')
            print(f"   From: {df_sorted['date'].iloc[0]}")
            print(f"   To: {df_sorted['date'].iloc[-1]}")
            
            # Calculate time span
            if pd.api.types.is_datetime64_any_dtype(df['date']):
                days_span = (df['date'].max() - df['date'].min()).days
                print(f"   Duration: {days_span} days (~{days_span/30:.1f} months)")
        except Exception as e:
            print(f"   Could not parse dates: {e}")
    
    
    # Show crops if commodity column exists
    if 'commodity' in df.columns:
        print(f"\n🌾 COMMODITIES FOUND:")
        commodities = df['commodity'].unique()
        print(f"   Total: {len(commodities)} commodities")
        print(f"   List: {', '.join(commodities)}")
    
    
    # Show states if state column exists
    if 'state' in df.columns:
        print(f"\n🗺️ STATES COVERED:")
        states = df['state'].unique()
        print(f"   Total: {len(states)} states/regions")
        print(f"   List: {', '.join(sorted(states))}")
    
    
    # STEP 8: Recommendations
    # ========================================================================
    print(f"\n💡 NEXT STEPS & RECOMMENDATIONS:")
    
    # Check for missing values
    if missing.sum() > 0:
        print(f"   ⚠️ Found missing values - consider data cleaning/imputation")
    else:
        print(f"   ✓ No missing values detected")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"   ⚠️ Found {duplicates} duplicate rows - consider removing them")
    else:
        print(f"   ✓ No duplicate rows found")
    
    # General recommendations
    print(f"   → Consider filtering data by date range if too large")
    print(f"   → Check for outliers in numeric columns")
    print(f"   → Verify data consistency with business logic")
    print(f"   → Document any data quality issues found")
    
    print("\n" + "=" * 80 + "\n")


# ============================================================================
# FUNCTION 2: Load Data with Error Handling
# ============================================================================

def load_csv_safely(file_path: Path) -> pd.DataFrame:
    """
    Load a CSV file with helpful error messages.
    
    This function demonstrates:
    - Using pathlib for cross-platform file paths
    - Error handling with try-except
    - User-friendly error messages
    
    Parameters:
    -----------
    file_path : Path
        pathlib.Path object pointing to CSV file
    
    Returns:
    --------
    pd.DataFrame or None
        The loaded DataFrame, or None if file doesn't exist
    
    Example:
    --------
    >>> from pathlib import Path
    >>> df = load_csv_safely(Path('data/raw/mandi_prices.csv'))
    """
    
    if not file_path.exists():
        print(f"\n❌ File not found: {file_path}")
        print(f"   Please ensure the file is at the correct location.")
        return None
    
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Successfully loaded: {file_path} ({len(df)} rows)")
        return df
    
    except pd.errors.EmptyDataError:
        print(f"❌ Error: File is empty: {file_path}")
        return None
    
    except Exception as e:
        print(f"❌ Error loading file: {file_path}")
        print(f"   Details: {e}")
        return None


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Main execution block - runs when script is called directly.
    
    This section:
    1. Sets up file paths using pathlib (works on Windows, Mac, Linux)
    2. Loads CSV files
    3. Inspects each DataFrame
    4. Demonstrates the inspection workflow
    """
    
    print("\n" + "=" * 80)
    print("🚀 AGRISENSE DATA INSPECTION SCRIPT")
    print("Sections 4.30 - 4.31: Learning Data Exploration")
    print("=" * 80)
    
    
    # Step 1: Set up file paths using pathlib
    # ========================================================================
    # pathlib is MUCH better than string paths - works on all operating systems!
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # Go up one level from 'src/' to project root
    project_root = script_dir.parent
    
    # Construct paths to our data files
    mandi_prices_path = project_root / "data" / "raw" / "mandi_prices.csv"
    weather_data_path = project_root / "data" / "raw" / "weather_data.csv"
    
    print(f"\n📂 Looking for data files...")
    print(f"   Script location: {script_dir}")
    print(f"   Project root: {project_root}")
    print(f"   Data path: {mandi_prices_path.parent}")
    
    
    # Step 2: Load and inspect mandi prices data
    # ========================================================================
    print(f"\n\n--- LOADING MANDI PRICES DATA ---")
    mandi_df = load_csv_safely(mandi_prices_path)
    
    if mandi_df is not None:
        # This is where we use our inspection function!
        inspect_dataframe(mandi_df, "Mandi Prices")
    
    
    # Step 3: Load and inspect weather data (if it exists)
    # ========================================================================
    print(f"\n\n--- LOADING WEATHER DATA ---")
    weather_df = load_csv_safely(weather_data_path)
    
    if weather_df is not None:
        inspect_dataframe(weather_df, "Weather Data")
    else:
        print("\n📝 Note: weather_data.csv not found in data/raw/")
        print("   If you have weather data, place it in: data/raw/weather_data.csv")
    
    
    # Step 4: Comparison (if we have both datasets)
    # ========================================================================
    if mandi_df is not None and weather_df is not None:
        print("\n" + "=" * 80)
        print("📊 COMPARING DATASETS")
        print("=" * 80)
        print(f"\nMandi Prices: {mandi_df.shape[0]} rows × {mandi_df.shape[1]} columns")
        print(f"Weather Data: {weather_df.shape[0]} rows × {weather_df.shape[1]} columns")


# ============================================================================
# STUDENT INSTRUCTIONS & LEARNING GUIDE
# ============================================================================

"""

📚 HOW TO USE THIS SCRIPT - STUDENT GUIDE

1. SETUP: PREPARE YOUR DATA FILES
   ═════════════════════════════════════════════════════════════════════════
   
   Before running this script, make sure you have:
   
   a) Mandi Prices Data:
      Location: data/raw/mandi_prices.csv
      
      Expected columns:
      - date (YYYY-MM-DD format)
      - commodity (crop name: Wheat, Rice, Tomato, etc.)
      - modal_price (price in rupees)
      - market (market name)
      - state (state name)
      
      Sample data:
      date,commodity,modal_price,market,state
      2024-01-01,Wheat,2400,Shimla Mandi,Himachal Pradesh
      2024-01-01,Rice,3200,Chandigarh Mandi,Punjab
   
   b) Weather Data (optional):
      Location: data/raw/weather_data.csv
      
      Expected columns might include:
      - date
      - temperature
      - rainfall
      - humidity
      - state (to match with mandi data)
      
      Note: If you don't have this yet, data/raw/mandi_prices.csv is enough!


2. RUN THE SCRIPT
   ═════════════════════════════════════════════════════════════════════════
   
   Method A: From Command Line (Terminal)
   ────────────────────────────────────────
   
   # Navigate to the agrisense folder
   cd "S84-0426-AKM-Python-Pandas-NumPy-AgriSense"
   
   # Run the script
   python src/inspect_data_agrisense.py
   
   
   Method B: In Jupyter Notebook
   ────────────────────────────────────────
   
   # In a Jupyter cell:
   %run src/inspect_data_agrisense.py
   
   
   Method C: Import in Your Own Script
   ────────────────────────────────────────
   
   from src.inspect_data_agrisense import inspect_dataframe
   import pandas as pd
   
   my_data = pd.read_csv('data/raw/mandi_prices.csv')
   inspect_dataframe(my_data, "My Custom Dataset")


3. UNDERSTAND THE OUTPUT
   ═════════════════════════════════════════════════════════════════════════
   
   The script prints:
   
   ✓ SHAPE: How many rows and columns?
     → More rows = more data but slower processing
     → More columns = more features but more complexity
   
   ✓ COLUMNS: What are we measuring?
     → Each column is a "feature" or "variable"
     → Important for feature engineering!
   
   ✓ DATA TYPES: Numbers vs Text vs Dates
     → int64, float64 = Numeric (good for math operations)
     → object = Usually text/strings
     → datetime64 = Dates and times
     → Wrong types cause analysis errors!
   
   ✓ FIRST 5 ROWS: Does the data look right?
     → Visually inspect for obvious errors
     → Check if data matches your expectations
   
   ✓ SUMMARY STATS: What are typical values?
     → Mean = Average value
     → Std = How spread out the values are
     → Min/Max = Range of values
     → 25%, 50%, 75% = Distribution quartiles
   
   ✓ MISSING VALUES: Are there gaps in the data?
     → NaN or null values cause problems
     → Must be handled before modeling!
     → Options: Remove rows, Fill values, or Keep them
   
   ✓ UNIQUE VALUES: How many different categories?
     → For categorical data (commodities, states, etc.)
     → Check if values make sense
     → Help with groupby operations


4. WHY THIS STEP MATTERS
   ═════════════════════════════════════════════════════════════════════════
   
   Before you:
   ✗ Build ML models
   ✗ Create visualizations
   ✗ Make predictions
   ✗ Calculate statistics
   
   You MUST:
   ✓ Inspect the data
   ✓ Understand the structure
   ✓ Find data quality issues
   ✓ Plan your cleaning strategy
   
   This is called "Exploratory Data Analysis" (EDA).
   It's the MOST important step in data science!
   
   Time spent on EDA:
   - Saves 10x time later in debugging
   - Prevents incorrect conclusions
   - Builds data domain knowledge
   - Catches bad data early


5. NEXT STEPS
   ═════════════════════════════════════════════════════════════════════════
   
   After running this inspection script, move to:
   
   → Section 4.32: Data Cleaning Script
      Clean the data, handle missing values, remove duplicates
   
   → Section 4.33: Feature Engineering Script
      Create new useful features from raw data
   
   → Section 4.34: Exploratory Visualization Script
      Create plots and charts to understand patterns
   
   → Section 4.35: Statistical Analysis Script
      Calculate correlations, test hypotheses
   
   → Section 4.40+: Machine Learning Models
      Build prediction models using clean, inspected data


6. COMMON PATTERNS TO LOOK FOR
   ═════════════════════════════════════════════════════════════════════════
   
   When you inspect data, ask yourself:
   
   ❓ Data Quality Questions:
      - Are there NULL/NaN values?
      - Are there obvious data entry errors?
      - Is the date range what I expected?
      - Are prices/numbers in reasonable ranges?
   
   ❓ Data Understanding Questions:
      - How many unique crops/states/markets?
      - What's the price range for each commodity?
      - Is data balanced across years/seasons?
      - Are there any surprising patterns?
   
   ❓ Data Readiness Questions:
      - Do I need to convert data types?
      - Should I combine/filter some columns?
      - Are row counts what I expected?
      - Is there enough data for modeling?


7. TROUBLESHOOTING
   ═════════════════════════════════════════════════════════════════════════
   
   Q: "File not found" error
   A: Check that CSV files are in: S84-0426-AKM-Python-Pandas-NumPy-AgriSense/data/raw/
   
   Q: "Module not found" error (pandas, etc.)
   A: Install requirements: pip install -r requirements.txt
   
   Q: Script runs but no output appears
   A: Check that CSV files are not empty (at least have headers)
   
   Q: Want to inspect a different CSV file?
   A: Copy the load_csv_safely() and inspect_dataframe() functions!
      They work with ANY CSV file, not just mandi prices.


8. KEY LEARNING OUTCOMES
   ═════════════════════════════════════════════════════════════════════════
   
   After using this script, you'll understand:
   
   ✓ How to use pandas for data exploration
   ✓ What head(), info(), describe() do and why they matter
   ✓ How to find and quantify missing data
   ✓ How to check data types and convert them
   ✓ How to identify categorical vs numeric data
   ✓ How to think about data quality proactively
   ✓ Why data inspection saves time in the long run
   
   These skills apply to ANY data science project!


═════════════════════════════════════════════════════════════════════════════
For more help, see:
- SETUP_GUIDE.md - Initial setup instructions
- README_DATA_SETUP.md - Data preparation guide
- PYTHON_SCRIPTS_SUMMARY.md - Overview of all scripts
- QUICK_REFERENCE.md - Python/pandas quick reference

Happy learning! 🌾📊
═════════════════════════════════════════════════════════════════════════════

"""
