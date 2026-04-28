"""
Feature Engineering Module
=========================
This module provides functions for creating domain-specific features
from agricultural data to improve model performance in machine learning tasks.

Usage:
    Import and use the feature engineering functions to transform raw dataframes
    before model training or inference.

Author: AgriSense Team
Date: April 2026
Non-functional update: Expanded module docstring for clarity (April 2026).
"""

import pandas as pd
import numpy as np
from typing import List, Tuple


def create_lag_features(df: pd.DataFrame, columns: List[str], lags: List[int] = [1, 7, 30]) -> pd.DataFrame:
    """
    Create lag features for time-series analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe (must be sorted by date)
    columns : List[str]
        Columns to create lags for
    lags : List[int]
        Lag periods to create. Default: [1, 7, 30] (daily, weekly, monthly)
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with lag features
    """
    for col in columns:
        for lag in lags:
            df[f'{col}_lag_{lag}'] = df[col].shift(lag)
    
    print(f"Created lag features for {columns} with lags {lags}")
    return df


def create_rolling_features(
    df: pd.DataFrame, 
    columns: List[str], 
    windows: List[int] = [7, 14, 30]
) -> pd.DataFrame:
    """
    Create rolling window statistics (mean, std, min, max).
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe (must be sorted by date)
    columns : List[str]
        Columns to create rolling features for
    windows : List[int]
        Rolling window sizes. Default: [7, 14, 30]
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with rolling features
    """
    for col in columns:
        for window in windows:
            df[f'{col}_rolling_mean_{window}'] = df[col].rolling(window=window).mean()
            df[f'{col}_rolling_std_{window}'] = df[col].rolling(window=window).std()
            df[f'{col}_rolling_min_{window}'] = df[col].rolling(window=window).min()
            df[f'{col}_rolling_max_{window}'] = df[col].rolling(window=window).max()
    
    print(f"Created rolling window features for {columns} with windows {windows}")
    return df


def create_seasonal_features(df: pd.DataFrame, date_column: str = 'date') -> pd.DataFrame:
    """
    Create seasonal features using sine/cosine transforms (circular encoding).
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with date column
    date_column : str
        Name of the date column
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with seasonal features
    """
    if date_column not in df.columns:
        print(f"Warning: {date_column} not found")
        return df
    
    # Month seasonality (12-month cycle)
    month = df[date_column].dt.month
    df['month_sin'] = np.sin(2 * np.pi * month / 12)
    df['month_cos'] = np.cos(2 * np.pi * month / 12)
    
    # Day of year seasonality (365-day cycle)
    day_of_year = df[date_column].dt.dayofyear
    df['day_of_year_sin'] = np.sin(2 * np.pi * day_of_year / 365)
    df['day_of_year_cos'] = np.cos(2 * np.pi * day_of_year / 365)
    
    # Quarter seasonality
    quarter = df[date_column].dt.quarter
    df['quarter_sin'] = np.sin(2 * np.pi * quarter / 4)
    df['quarter_cos'] = np.cos(2 * np.pi * quarter / 4)
    
    print("Created seasonal features with sine/cosine encoding")
    return df


def create_crop_region_features(df: pd.DataFrame, crop_col: str = 'crop', region_col: str = 'region') -> pd.DataFrame:
    """
    Create categorical encoding and aggregation features by crop and region.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    crop_col : str
        Name of crop column
    region_col : str
        Name of region column
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with crop-region features
    """
    # One-hot encode crops (if limited number of unique values)
    if df[crop_col].nunique() <= 10:
        crop_dummies = pd.get_dummies(df[crop_col], prefix='crop')
        df = pd.concat([df, crop_dummies], axis=1)
    
    # One-hot encode regions (if limited number)
    if df[region_col].nunique() <= 10:
        region_dummies = pd.get_dummies(df[region_col], prefix='region')
        df = pd.concat([df, region_dummies], axis=1)
    
    print(f"Created categorical features for {crop_col} and {region_col}")
    return df


def create_interaction_features(
    df: pd.DataFrame,
    feature_pairs: List[Tuple[str, str]]
) -> pd.DataFrame:
    """
    Create interaction features between pairs of columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    feature_pairs : List[Tuple[str, str]]
        List of (col1, col2) tuples to create interactions from
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with interaction features
    """
    for col1, col2 in feature_pairs:
        if col1 in df.columns and col2 in df.columns:
            df[f'{col1}_x_{col2}'] = df[col1] * df[col2]
    
    print(f"Created {len(feature_pairs)} interaction features")
    return df


def normalize_features(df: pd.DataFrame, numeric_cols: List[str] = None) -> Tuple[pd.DataFrame, dict]:
    """
    Normalize numeric features using min-max scaling.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    numeric_cols : List[str], optional
        Columns to normalize. If None, normalizes all numeric columns
        
    Returns:
    --------
    Tuple[pd.DataFrame, dict]
        Normalized dataframe and scaling parameters
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    scaling_params = {}
    
    for col in numeric_cols:
        if col in df.columns:
            min_val = df[col].min()
            max_val = df[col].max()
            scaling_params[col] = {'min': min_val, 'max': max_val}
            df[col] = (df[col] - min_val) / (max_val - min_val + 1e-8)
    
    print(f"Normalized {len(numeric_cols)} features")
    return df, scaling_params


def create_climate_risk_score(
    df: pd.DataFrame,
    rainfall_col: str = 'rainfall_mm',
    temp_col: str = 'temperature_celsius'
) -> pd.DataFrame:
    """
    Create a composite climate risk score (0-1 scale).
    
    Risk factors:
    - Too little rain (<50mm/month)
    - Too much rain (>200mm/month)
    - Extreme temperatures (<10°C or >35°C)
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    rainfall_col : str
        Name of rainfall column
    temp_col : str
        Name of temperature column
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with climate_risk_score column
    """
    risk_score = 0
    
    if rainfall_col in df.columns:
        # Rainfall risk: below 50mm or above 200mm
        rainfall_risk = ((df[rainfall_col] < 50) | (df[rainfall_col] > 200)).astype(float) * 0.4
        risk_score += rainfall_risk
    
    if temp_col in df.columns:
        # Temperature risk: below 10°C or above 35°C
        temp_risk = ((df[temp_col] < 10) | (df[temp_col] > 35)).astype(float) * 0.6
        risk_score += temp_risk
    
    df['climate_risk_score'] = np.clip(risk_score, 0, 1)
    
    print("Created climate_risk_score feature")
    return df


def create_demand_supply_ratio(
    df: pd.DataFrame,
    demand_col: str = 'demand_index',
    production_col: str = 'yield_kg_per_hectare'
) -> pd.DataFrame:
    """
    Create demand-to-supply ratio feature.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    demand_col : str
        Name of demand column
    production_col : str
        Name of production/yield column
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with demand_supply_ratio column
    """
    if demand_col in df.columns and production_col in df.columns:
        df['demand_supply_ratio'] = df[demand_col] / (df[production_col] + 1e-8)
    
    print("Created demand_supply_ratio feature")
    return df


def engineer_features_pipeline(df: pd.DataFrame, date_column: str = 'date') -> pd.DataFrame:
    """
    Complete feature engineering pipeline combining multiple techniques.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    date_column : str
        Name of date column
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with all engineered features
    """
    print("\n" + "="*60)
    print("Starting Feature Engineering Pipeline")
    print("="*60 + "\n")
    
    # Sort by date for lag features
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.sort_values(date_column)
    
    # Seasonal features
    if date_column in df.columns:
        df = create_seasonal_features(df, date_column)
    
    # Lag features for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    df = create_lag_features(df, numeric_cols[:3], lags=[1, 7, 30])
    
    # Rolling features
    df = create_rolling_features(df, numeric_cols[:3], windows=[7, 14, 30])
    
    # Crop and region features
    if 'crop' in df.columns and 'region' in df.columns:
        df = create_crop_region_features(df)
    
    # Climate risk score
    if 'rainfall_mm' in df.columns and 'temperature_celsius' in df.columns:
        df = create_climate_risk_score(df)
    
    # Demand-supply ratio
    if 'demand_index' in df.columns and 'yield_kg_per_hectare' in df.columns:
        df = create_demand_supply_ratio(df)
    
    # Handle NaN from lag/rolling operations
    df = df.dropna()
    
    print("\n" + "="*60)
    print(f"Feature Engineering Complete! New shape: {df.shape}")
    print("="*60 + "\n")
    
    return df


if __name__ == "__main__":
    """
    Example: Test feature engineering on sample data
    """
    print("Feature Engineering Module - Demonstration")
    print("=" * 60)
    
    # Load processed data
    df = pd.read_csv('data/processed/sample_agriculture_processed.csv')
    
    # Apply feature engineering
    df_engineered = engineer_features_pipeline(df, date_column='date')
    
    # Save engineered features
    df_engineered.to_csv('data/processed/sample_agriculture_engineered.csv', index=False)
    print("\nEngineered features saved to data/processed/sample_agriculture_engineered.csv")
    
    # Display results
    print("\nEngineered DataFrame:")
    print(df_engineered.head())
    print(f"\nNew columns created: {set(df_engineered.columns) - set(df.columns)}")
