"""
Utility Functions for AgriSense

General-purpose utilities for data handling, visualization,
and common operations across the project.

Author: AgriSense Team
Date: April 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List
import json


def ensure_directory(path: str) -> Path:
    """
    Ensure a directory exists; create if it doesn't.
    
    Parameters:
    -----------
    path : str
        Directory path
        
    Returns:
    --------
    Path
        Path object of the directory
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_predictions(df: pd.DataFrame, filename: str, output_dir: str = 'outputs/predictions/') -> None:
    """
    Save predictions to a CSV file.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Predictions dataframe
    filename : str
        Output filename
    output_dir : str
        Output directory
    """
    output_path = Path(output_dir)
    ensure_directory(output_dir)
    filepath = output_path / filename
    df.to_csv(filepath, index=False)
    print(f"Predictions saved to {filepath}")


def load_predictions(filename: str, input_dir: str = 'outputs/predictions/') -> pd.DataFrame:
    """
    Load predictions from CSV file.
    
    Parameters:
    -----------
    filename : str
        Input filename
    input_dir : str
        Input directory
        
    Returns:
    --------
    pd.DataFrame
        Loaded predictions
    """
    filepath = Path(input_dir) / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Predictions file not found: {filepath}")
    
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} predictions from {filepath}")
    return df


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Generate a summary statistics dictionary for a dataframe.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    dict
        Summary statistics including shape, dtypes, missing values, etc.
    """
    summary = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_summary': df.describe().to_dict(),
    }
    return summary


def print_data_summary(df: pd.DataFrame) -> None:
    """
    Pretty print data summary.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    """
    print("\n" + "="*60)
    print("DATA SUMMARY")
    print("="*60)
    print(f"Shape: {df.shape}")
    print(f"\nColumns ({len(df.columns)}): {df.columns.tolist()}")
    print(f"\nData Types:\n{df.dtypes}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nBasic Statistics:\n{df.describe()}")
    print("="*60 + "\n")


def filter_by_crop(df: pd.DataFrame, crop: str, crop_col: str = 'crop') -> pd.DataFrame:
    """
    Filter dataframe by crop type.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    crop : str
        Crop type to filter
    crop_col : str
        Name of crop column
        
    Returns:
    --------
    pd.DataFrame
        Filtered dataframe
    """
    if crop_col not in df.columns:
        raise ValueError(f"Column '{crop_col}' not found in dataframe")
    
    filtered_df = df[df[crop_col] == crop].copy()
    print(f"Filtered {len(df)} rows to {len(filtered_df)} rows for crop: {crop}")
    return filtered_df


def filter_by_region(df: pd.DataFrame, region: str, region_col: str = 'region') -> pd.DataFrame:
    """
    Filter dataframe by region.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    region : str
        Region to filter
    region_col : str
        Name of region column
        
    Returns:
    --------
    pd.DataFrame
        Filtered dataframe
    """
    if region_col not in df.columns:
        raise ValueError(f"Column '{region_col}' not found in dataframe")
    
    filtered_df = df[df[region_col] == region].copy()
    print(f"Filtered {len(df)} rows to {len(filtered_df)} rows for region: {region}")
    return filtered_df


def filter_by_date_range(
    df: pd.DataFrame,
    start_date: str,
    end_date: str,
    date_col: str = 'date'
) -> pd.DataFrame:
    """
    Filter dataframe by date range.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    start_date : str
        Start date (YYYY-MM-DD format)
    end_date : str
        End date (YYYY-MM-DD format)
    date_col : str
        Name of date column
        
    Returns:
    --------
    pd.DataFrame
        Filtered dataframe
    """
    if date_col not in df.columns:
        raise ValueError(f"Column '{date_col}' not found in dataframe")
    
    df[date_col] = pd.to_datetime(df[date_col])
    mask = (df[date_col] >= start_date) & (df[date_col] <= end_date)
    filtered_df = df[mask].copy()
    
    print(f"Filtered {len(df)} rows to {len(filtered_df)} rows for date range: {start_date} to {end_date}")
    return filtered_df


def get_unique_values(df: pd.DataFrame, columns: Optional[List[str]] = None) -> dict:
    """
    Get unique values for specified columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : List[str], optional
        Columns to get unique values from. If None, returns for categorical columns.
        
    Returns:
    --------
    dict
        Dictionary of unique values per column
    """
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns.tolist()
    
    result = {}
    for col in columns:
        if col in df.columns:
            result[col] = df[col].unique().tolist()
    
    return result


def format_price_display(price: float, decimals: int = 2) -> str:
    """
    Format price for display (with ₹ symbol).
    
    Parameters:
    -----------
    price : float
        Price value
    decimals : int
        Number of decimal places
        
    Returns:
    --------
    str
        Formatted price string
    """
    return f"₹{price:,.{decimals}f}"


def format_yield_display(yield_kg: float, decimals: int = 2) -> str:
    """
    Format yield for display (with kg/ha).
    
    Parameters:
    -----------
    yield_kg : float
        Yield in kg/hectare
    decimals : int
        Number of decimal places
        
    Returns:
    --------
    str
        Formatted yield string
    """
    return f"{yield_kg:,.{decimals}f} kg/ha"


def categorize_risk_level(risk_score: float) -> str:
    """
    Categorize climate risk score into qualitative levels.
    
    Parameters:
    -----------
    risk_score : float
        Risk score between 0 and 1
        
    Returns:
    --------
    str
        Risk level: 'Low', 'Medium', or 'High'
    """
    if risk_score < 0.33:
        return "Low"
    elif risk_score < 0.67:
        return "Medium"
    else:
        return "High"


def get_best_selling_date(df: pd.DataFrame, price_col: str = 'market_price_per_kg', date_col: str = 'date') -> dict:
    """
    Find the date with highest predicted price (best selling date).
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with price predictions
    price_col : str
        Name of price column
    date_col : str
        Name of date column
        
    Returns:
    --------
    dict
        Dictionary with best date and price
    """
    if price_col not in df.columns or date_col not in df.columns:
        raise ValueError(f"Columns not found")
    
    max_idx = df[price_col].idxmax()
    best_date = df.loc[max_idx, date_col]
    best_price = df.loc[max_idx, price_col]
    
    return {
        'best_selling_date': best_date,
        'predicted_price': best_price,
        'price_display': format_price_display(best_price)
    }


def calculate_profitability(
    estimated_yield: float,
    predicted_price: float,
    cost_per_hectare: float = 50000
) -> dict:
    """
    Calculate estimated profitability of a crop.
    
    Parameters:
    -----------
    estimated_yield : float
        Estimated yield in kg/hectare
    predicted_price : float
        Predicted price per kg
    cost_per_hectare : float
        Cost of production per hectare. Default: ₹50,000
        
    Returns:
    --------
    dict
        Profitability metrics
    """
    gross_income = estimated_yield * predicted_price
    profit = gross_income - cost_per_hectare
    roi = (profit / cost_per_hectare) * 100
    
    return {
        'gross_income': gross_income,
        'profit': profit,
        'roi_percent': roi,
        'gross_income_display': format_price_display(gross_income),
        'profit_display': format_price_display(profit),
    }


def export_to_json(df: pd.DataFrame, filename: str, output_dir: str = 'outputs/predictions/') -> None:
    """
    Export dataframe to JSON format.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    filename : str
        Output filename
    output_dir : str
        Output directory
    """
    output_path = Path(output_dir)
    ensure_directory(output_dir)
    filepath = output_path / filename
    
    df.to_json(filepath, orient='records', indent=2)
    print(f"Data exported to {filepath}")


def load_from_json(filename: str, input_dir: str = 'outputs/predictions/') -> pd.DataFrame:
    """
    Load dataframe from JSON file.
    
    Parameters:
    -----------
    filename : str
        Input filename
    input_dir : str
        Input directory
        
    Returns:
    --------
    pd.DataFrame
        Loaded dataframe
    """
    filepath = Path(input_dir) / filename
    if not filepath.exists():
        raise FileNotFoundError(f"JSON file not found: {filepath}")
    
    df = pd.read_json(filepath)
    print(f"Loaded data from {filepath}")
    return df


if __name__ == "__main__":
    print("AgriSense Utilities Module")
    print("="*60)
    print("Available functions:")
    print("  - ensure_directory()")
    print("  - save_predictions() / load_predictions()")
    print("  - get_data_summary() / print_data_summary()")
    print("  - filter_by_crop() / filter_by_region() / filter_by_date_range()")
    print("  - get_unique_values()")
    print("  - format_price_display() / format_yield_display()")
    print("  - categorize_risk_level()")
    print("  - get_best_selling_date()")
    print("  - calculate_profitability()")
    print("  - export_to_json() / load_from_json()")
    print("="*60)
