"""
AgriSense Data Preprocessing Module

This module handles loading raw agricultural data, performing cleaning operations,
and preparing it for ML modeling. It standardizes column names, handles missing values,
and creates useful date-based features.

Author: AgriSense Team
Date: April 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class DataPreprocessor:
    """
    A class to handle data loading, cleaning, and preprocessing for AgriSense.
    """
    
    def __init__(self, raw_data_path: str = "data/raw", processed_data_path: str = "data/processed"):
        """
        Initialize the DataPreprocessor.
        
        Parameters:
        -----------
        raw_data_path : str
            Path to the raw data directory
        processed_data_path : str
            Path to the processed data directory
        """
        self.raw_data_path = Path(raw_data_path)
        self.processed_data_path = Path(processed_data_path)
        
        # Ensure directories exist
        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        self.processed_data_path.mkdir(parents=True, exist_ok=True)


    def load_raw_data(self, filename: str) -> pd.DataFrame:
        """
        Load a CSV file from the raw data directory.
        
        Parameters:
        -----------
        filename : str
            Name of the CSV file to load
            
        Returns:
        --------
        pd.DataFrame
            The loaded dataframe
        """
        filepath = self.raw_data_path / filename
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        print(f"Loading {filename}...")
        df = pd.read_csv(filepath)
        print(f"Loaded {filename} with shape {df.shape}")
        return df


    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names to lowercase and replace spaces with underscores.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with standardized column names
        """
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
        return df


    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """
        Handle missing values in the dataframe.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        strategy : str
            Strategy to use ('mean', 'median', 'forward_fill', 'drop'). Default: 'mean'
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with missing values handled
        """
        print(f"Missing values before handling:\n{df.isnull().sum()}")
        
        if strategy == 'mean':
            df = df.fillna(df.mean(numeric_only=True))
        elif strategy == 'median':
            df = df.fillna(df.median(numeric_only=True))
        elif strategy == 'forward_fill':
            df = df.fillna(method='ffill').fillna(method='bfill')
        elif strategy == 'drop':
            df = df.dropna()
        
        print(f"Missing values after handling:\n{df.isnull().sum()}")
        return df


    def create_date_features(self, df: pd.DataFrame, date_column: str = 'date') -> pd.DataFrame:
        """
        Create useful date-based features from a date column.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        date_column : str
            Name of the date column. Default: 'date'
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with additional date features
        """
        if date_column not in df.columns:
            print(f"Warning: {date_column} not found in dataframe. Skipping date feature creation.")
            return df
        
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        
        df['year'] = df[date_column].dt.year
        df['month'] = df[date_column].dt.month
        df['day'] = df[date_column].dt.day
        df['quarter'] = df[date_column].dt.quarter
        df['day_of_year'] = df[date_column].dt.dayofyear
        df['week_of_year'] = df[date_column].dt.isocalendar().week
        
        print("Date features created: year, month, day, quarter, day_of_year, week_of_year")
        return df


    def remove_duplicates(self, df: pd.DataFrame, subset: Optional[list] = None) -> pd.DataFrame:
        """
        Remove duplicate rows.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        subset : list, optional
            Column names to consider for identifying duplicates
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with duplicates removed
        """
        initial_shape = df.shape
        df = df.drop_duplicates(subset=subset, keep='first')
        print(f"Removed {initial_shape[0] - df.shape[0]} duplicate rows")
        return df


    def remove_outliers(self, df: pd.DataFrame, columns: list, method: str = 'iqr') -> pd.DataFrame:
        """
        Remove outliers from specified columns using IQR or Z-score method.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        columns : list
            List of numeric column names to check for outliers
        method : str
            Method to use: 'iqr' or 'zscore'. Default: 'iqr'
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with outliers removed
        """
        initial_shape = df.shape
        
        if method == 'iqr':
            for col in columns:
                if col in df.columns and df[col].dtype in [np.float64, np.int64]:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]
        
        elif method == 'zscore':
            from scipy import stats
            z_scores = np.abs(stats.zscore(df[columns].select_dtypes([np.float64, np.int64])))
            df = df[(z_scores < 3).all(axis=1)]
        
        print(f"Removed {initial_shape[0] - df.shape[0]} outlier rows using {method}")
        return df


    def save_processed_data(self, df: pd.DataFrame, filename: str) -> None:
        """
        Save the processed dataframe to the processed data directory.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Dataframe to save
        filename : str
            Name of the file to save (without path)
        """
        filepath = self.processed_data_path / filename
        df.to_csv(filepath, index=False)
        print(f"Processed data saved to {filepath}")


    def process_pipeline(
        self, 
        filename: str,
        date_column: Optional[str] = None,
        output_filename: Optional[str] = None,
        handle_missing: bool = True,
        remove_dupes: bool = True,
        remove_outlier_cols: Optional[list] = None
    ) -> pd.DataFrame:
        """
        Complete data preprocessing pipeline.
        
        Parameters:
        -----------
        filename : str
            Raw data filename
        date_column : str, optional
            Name of date column for feature engineering
        output_filename : str, optional
            Output filename. If None, uses input filename
        handle_missing : bool
            Whether to handle missing values. Default: True
        remove_dupes : bool
            Whether to remove duplicates. Default: True
        remove_outlier_cols : list, optional
            Columns to check for outliers
            
        Returns:
        --------
        pd.DataFrame
            Processed dataframe
        """
        print(f"\n{'='*60}")
        print(f"Starting preprocessing pipeline for {filename}")
        print(f"{'='*60}\n")
        
        # Load
        df = self.load_raw_data(filename)
        
        # Standardize
        df = self.standardize_column_names(df)
        
        # Remove duplicates
        if remove_dupes:
            df = self.remove_duplicates(df)
        
        # Handle missing values
        if handle_missing:
            df = self.handle_missing_values(df, strategy='mean')
        
        # Remove outliers
        if remove_outlier_cols:
            df = self.remove_outliers(df, remove_outlier_cols, method='iqr')
        
        # Create date features
        if date_column:
            df = self.create_date_features(df, date_column)
        
        # Save
        output_file = output_filename or filename
        self.save_processed_data(df, output_file)
        
        print(f"\n{'='*60}")
        print(f"Preprocessing complete! Final shape: {df.shape}")
        print(f"{'='*60}\n")
        
        return df


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example: Process a sample agriculture dataset
    """
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor(
        raw_data_path="data/raw",
        processed_data_path="data/processed"
    )
    
    # Example 1: Create sample data for testing
    print("Creating sample agricultural data for demonstration...")
    sample_data = {
        'crop': ['Rice', 'Wheat', 'Maize', 'Rice', 'Wheat', 'Maize'] * 5,
        'region': ['Punjab', 'Haryana', 'UP', 'Punjab', 'Haryana', 'UP'] * 5,
        'date': pd.date_range('2023-01-01', periods=30),
        'yield_kg_per_hectare': np.random.uniform(3000, 5000, 30),
        'rainfall_mm': np.random.uniform(0, 200, 30),
        'temperature_celsius': np.random.uniform(15, 35, 30),
        'market_price_per_kg': np.random.uniform(15, 50, 30),
        'demand_index': np.random.uniform(0.5, 1.5, 30),
    }
    
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv('data/raw/sample_agriculture.csv', index=False)
    print("Sample data saved to data/raw/sample_agriculture.csv\n")
    
    # Example 2: Process the sample data
    processed_df = preprocessor.process_pipeline(
        filename='sample_agriculture.csv',
        date_column='date',
        output_filename='sample_agriculture_processed.csv',
        handle_missing=True,
        remove_dupes=True,
        remove_outlier_cols=['yield_kg_per_hectare', 'market_price_per_kg']
    )
    
    # Display processed data info
    print("\nProcessed Data Info:")
    print(processed_df.head())
    print(f"\nDataframe Info:\n{processed_df.info()}")
    print(f"\nStatistical Summary:\n{processed_df.describe()}")
