"""
=============================================================================
AgriSense - Crop Price Data Loader
=============================================================================

A beginner-friendly Python script to load and analyze market price data
from CSV files. This script serves as the foundation for the future
/api/market-data endpoint in the AgriSense backend.

Author: AgriSense Team
Date: April 2026
Version: 1.0

Usage:
    python load_crop_prices.py
    
    Or import and use the function:
    from load_crop_prices import load_and_summarize_prices
    df = load_and_summarize_prices("mandi_prices.csv")

=============================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Tuple


def load_csv_file(filename: str, data_dir: str = "data/raw") -> pd.DataFrame:
    """
    Load a CSV file from the data/raw directory with proper error handling.
    
    This function handles:
    - File path creation using pathlib (cross-platform compatible)
    - Proper error messages if file doesn't exist
    - Flexible file extension handling
    
    Parameters:
    -----------
    filename : str
        Name of the CSV file to load (e.g., "mandi_prices.csv")
    data_dir : str
        Directory where raw data is stored. Default: "data/raw"
    
    Returns:
    --------
    pd.DataFrame
        Loaded dataframe from CSV
        
    Raises:
    -------
    FileNotFoundError
        If the specified file doesn't exist in the data directory
    """
    # Create path object (works on Windows, Mac, and Linux)
    file_path = Path(data_dir) / filename
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"❌ File not found: {file_path}\n"
            f"   Please ensure '{filename}' is in the '{data_dir}/' folder."
        )
    
    # Load the CSV file
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Successfully loaded: {filename}")
        return df
    except Exception as e:
        raise Exception(f"❌ Error loading file: {str(e)}")


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to lowercase and remove extra spaces.
    
    This helps handle inconsistencies in data formatting:
    - "Commodity" becomes "commodity"
    - "Modal Price" becomes "modal_price"
    - Extra spaces are removed
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with standardized column names
    """
    # Convert to lowercase, replace spaces with underscores, strip whitespace
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(' ', '_')
        .str.replace('-', '_')
    )
    return df


def get_date_range(df: pd.DataFrame, date_column: Optional[str] = None) -> Tuple[str, str]:
    """
    Extract date range from dataframe if a date column exists.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    date_column : str, optional
        Name of the date column. If None, tries common names like 'date', 'Date', 'DATE'
        
    Returns:
    --------
    Tuple[str, str]
        (min_date, max_date) as strings, or ("N/A", "N/A") if no date column found
    """
    # Try to find date column if not specified
    if date_column is None:
        possible_date_cols = ['date', 'arrival_date', 'market_date', 'trading_date']
        for col in possible_date_cols:
            if col in df.columns:
                date_column = col
                break
    
    # If date column found, convert and get range
    if date_column and date_column in df.columns:
        try:
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            min_date = df[date_column].min()
            max_date = df[date_column].max()
            
            # Format dates nicely
            if pd.notna(min_date) and pd.notna(max_date):
                return str(min_date.date()), str(max_date.date())
        except Exception:
            pass
    
    return "N/A", "N/A"


def calculate_price_statistics(df: pd.DataFrame, price_column: Optional[str] = None) -> dict:
    """
    Calculate price statistics for the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    price_column : str, optional
        Name of the price column. If None, tries common names.
        
    Returns:
    --------
    dict
        Dictionary with price statistics
    """
    # Find price column
    if price_column is None:
        possible_price_cols = ['modal_price', 'price', 'mandi_price', 'market_price']
        for col in possible_price_cols:
            if col in df.columns:
                price_column = col
                break
    
    # Calculate statistics
    stats = {}
    if price_column and price_column in df.columns:
        stats = {
            'average': df[price_column].mean(),
            'median': df[price_column].median(),
            'min': df[price_column].min(),
            'max': df[price_column].max(),
            'std_dev': df[price_column].std(),
        }
    
    return stats


def get_unique_crops(df: pd.DataFrame, crop_column: Optional[str] = None) -> list:
    """
    Get list of unique crops/commodities in the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    crop_column : str, optional
        Name of the crop column. If None, tries common names.
        
    Returns:
    --------
    list
        List of unique crop names
    """
    # Find crop column
    if crop_column is None:
        possible_crop_cols = ['commodity', 'crop', 'crop_name', 'product']
        for col in possible_crop_cols:
            if col in df.columns:
                crop_column = col
                break
    
    # Get unique values
    if crop_column and crop_column in df.columns:
        return sorted(df[crop_column].unique().tolist())
    
    return []


def get_average_price_by_crop(
    df: pd.DataFrame,
    crop_column: Optional[str] = None,
    price_column: Optional[str] = None,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Calculate average price grouped by crop.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    crop_column : str, optional
        Name of crop column
    price_column : str, optional
        Name of price column
    top_n : int
        Number of top crops to return. Default: 10
        
    Returns:
    --------
    pd.DataFrame
        Average prices sorted in descending order
    """
    # Find columns if not specified
    if crop_column is None:
        possible_crop_cols = ['commodity', 'crop', 'crop_name']
        for col in possible_crop_cols:
            if col in df.columns:
                crop_column = col
                break
    
    if price_column is None:
        possible_price_cols = ['modal_price', 'price', 'market_price']
        for col in possible_price_cols:
            if col in df.columns:
                price_column = col
                break
    
    # Calculate average if columns found
    if crop_column and price_column and crop_column in df.columns and price_column in df.columns:
        avg_prices = (
            df.groupby(crop_column)[price_column]
            .mean()
            .sort_values(ascending=False)
            .head(top_n)
        )
        return avg_prices
    
    return pd.Series()


def load_and_summarize_prices(
    filename: str = "mandi_prices.csv",
    data_dir: str = "data/raw",
    print_summary: bool = True
) -> pd.DataFrame:
    """
    Complete workflow: Load CSV, standardize, and optionally print summary.
    
    This is the main function that can be imported and reused in other
    scripts or in the FastAPI backend.
    
    Parameters:
    -----------
    filename : str
        Name of the CSV file to load. Default: "mandi_prices.csv"
    data_dir : str
        Directory containing raw data. Default: "data/raw"
    print_summary : bool
        Whether to print summary information. Default: True
        
    Returns:
    --------
    pd.DataFrame
        Loaded and standardized dataframe
        
    Example:
    --------
    from load_crop_prices import load_and_summarize_prices
    
    # Load and print summary
    df = load_and_summarize_prices("mandi_prices.csv")
    
    # Or load without printing
    df = load_and_summarize_prices("mandi_prices.csv", print_summary=False)
    """
    
    print("\n" + "="*70)
    print("  AgriSense - Crop Price Data Loader")
    print("="*70 + "\n")
    
    # Load CSV file
    print(f"📂 Loading data from: {data_dir}/{filename}")
    df = load_csv_file(filename, data_dir)
    
    # Standardize column names
    df = standardize_column_names(df)
    print("✅ Column names standardized\n")
    
    if not print_summary:
        return df
    
    # ========================================================================
    # PRINT SUMMARY INFORMATION
    # ========================================================================
    
    # 1. Basic Information
    print("📊 DATASET OVERVIEW")
    print("-" * 70)
    rows, cols = df.shape
    print(f"  Shape: {rows:,} rows × {cols} columns")
    print(f"  Columns: {', '.join(df.columns.tolist())}\n")
    
    # 2. First Few Rows
    print("📋 FIRST 5 ROWS:")
    print("-" * 70)
    print(df.head().to_string())
    print()
    
    # 3. Data Types
    print("🔢 DATA TYPES:")
    print("-" * 70)
    for col, dtype in df.dtypes.items():
        print(f"  {col:.<30} {dtype}")
    print()
    
    # 4. Date Range
    min_date, max_date = get_date_range(df)
    print("📅 DATE RANGE:")
    print("-" * 70)
    print(f"  From: {min_date}")
    print(f"  To:   {max_date}\n")
    
    # 5. Unique Crops
    crops = get_unique_crops(df)
    print("🌾 UNIQUE CROPS/COMMODITIES:")
    print("-" * 70)
    print(f"  Total: {len(crops)}")
    print(f"  List: {', '.join(crops[:20])}")
    if len(crops) > 20:
        print(f"         ... and {len(crops) - 20} more")
    print()
    
    # 6. Price Statistics
    price_stats = calculate_price_statistics(df)
    if price_stats:
        print("💰 PRICE STATISTICS (all data):")
        print("-" * 70)
        print(f"  Average:  ₹{price_stats.get('average', 0):>10,.2f}")
        print(f"  Median:   ₹{price_stats.get('median', 0):>10,.2f}")
        print(f"  Min:      ₹{price_stats.get('min', 0):>10,.2f}")
        print(f"  Max:      ₹{price_stats.get('max', 0):>10,.2f}")
        print(f"  Std Dev:  ₹{price_stats.get('std_dev', 0):>10,.2f}\n")
    
    # 7. Average Price by Crop (Top 10)
    avg_prices = get_average_price_by_crop(df, top_n=10)
    if not avg_prices.empty:
        print("💹 TOP 10 MOST EXPENSIVE CROPS (Average Price):")
        print("-" * 70)
        for crop, price in avg_prices.items():
            price_bar = "█" * int(price / 100)  # Simple bar visualization
            print(f"  {crop:.<25} ₹{price:>7,.2f}  {price_bar}")
        print()
    
    # 8. Statistical Summary
    print("📈 STATISTICAL SUMMARY:")
    print("-" * 70)
    print(df.describe().to_string())
    print()
    
    # 9. Missing Values
    print("❓ MISSING VALUES:")
    print("-" * 70)
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("  ✅ No missing values found!")
    else:
        for col, count in missing[missing > 0].items():
            pct = (count / len(df)) * 100
            print(f"  {col:.<30} {count:>5} ({pct:.1f}%)")
    print()
    
    # Final message
    print("="*70)
    print("✅ Data loading complete! Ready for analysis.")
    print("="*70 + "\n")
    
    return df


# ============================================================================
# MAIN: Run this script directly
# ============================================================================

if __name__ == "__main__":
    """
    Main execution block. This runs when you execute the script directly:
        python load_crop_prices.py
    
    It will attempt to load the default 'mandi_prices.csv' file and print
    a comprehensive summary.
    """
    
    try:
        # Load and summarize prices
        # Change the filename if your data has a different name
        df = load_and_summarize_prices(
            filename="mandi_prices.csv",
            data_dir="data/raw",
            print_summary=True
        )
        
        # You can now perform additional analysis on df here
        # For example:
        # print("\n🔍 ADDITIONAL ANALYSIS:")
        # print(df.groupby('commodity')['modal_price'].mean().sort_values(ascending=False))
        
    except FileNotFoundError as e:
        print(f"\n{e}\n")
        print("💡 Create sample data to test this script:")
        print("   1. Ensure your CSV file is in the 'data/raw/' folder")
        print("   2. Or run example_workflow.py to generate sample data")
        print("   3. Then run this script again\n")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}\n")
        import traceback
        traceback.print_exc()
