"""
AgriSense Complete Workflow Example

This script demonstrates the complete workflow:
1. Load raw data
2. Preprocess data
3. Engineer features
4. Save processed data
5. Generate summary statistics

Run this script from the project root directory:
    python example_workflow.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import pandas as pd
import numpy as np
from data_preprocessing import DataPreprocessor
from feature_engineering import engineer_features_pipeline
from utils import (
    print_data_summary,
    get_unique_values,
    save_predictions,
    filter_by_crop,
    filter_by_region,
    get_best_selling_date,
    calculate_profitability,
)


def main():
    """
    Execute the complete AgriSense workflow.
    """
    
    print("\n" + "="*70)
    print(" "*15 + "AgriSense Data Science Workflow")
    print("="*70 + "\n")
    
    # ========================================================================
    # STEP 1: Initialize Data Preprocessor
    # ========================================================================
    print("STEP 1: Initializing Data Preprocessor...")
    print("-" * 70)
    
    preprocessor = DataPreprocessor(
        raw_data_path="data/raw",
        processed_data_path="data/processed"
    )
    
    # ========================================================================
    # STEP 2: Create Sample Data
    # ========================================================================
    print("\nSTEP 2: Creating Sample Agricultural Data...")
    print("-" * 70)
    
    # Create more realistic sample data
    np.random.seed(42)
    n_samples = 100
    
    crops = ['Rice', 'Wheat', 'Maize', 'Cotton']
    regions = ['Punjab', 'Haryana', 'UP', 'Maharashtra', 'Karnataka']
    
    sample_data = {
        'crop': np.random.choice(crops, n_samples),
        'region': np.random.choice(regions, n_samples),
        'date': pd.date_range('2023-01-01', periods=n_samples),
        'yield_kg_per_hectare': np.random.uniform(2500, 5500, n_samples),
        'rainfall_mm': np.random.uniform(10, 250, n_samples),
        'temperature_celsius': np.random.uniform(12, 38, n_samples),
        'market_price_per_kg': np.random.uniform(20, 60, n_samples),
        'demand_index': np.random.uniform(0.6, 1.8, n_samples),
    }
    
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv('data/raw/agricultural_data_sample.csv', index=False)
    print(f"✓ Created sample data: {sample_df.shape[0]} rows, {sample_df.shape[1]} columns")
    print(f"  Saved to: data/raw/agricultural_data_sample.csv")
    
    # ========================================================================
    # STEP 3: Preprocess Data
    # ========================================================================
    print("\nSTEP 3: Preprocessing Data...")
    print("-" * 70)
    
    processed_df = preprocessor.process_pipeline(
        filename='agricultural_data_sample.csv',
        date_column='date',
        output_filename='agricultural_data_preprocessed.csv',
        handle_missing=True,
        remove_dupes=True,
        remove_outlier_cols=['yield_kg_per_hectare', 'market_price_per_kg', 'temperature_celsius']
    )
    
    # ========================================================================
    # STEP 4: Engineer Features
    # ========================================================================
    print("\nSTEP 4: Engineering Features...")
    print("-" * 70)
    
    engineered_df = engineer_features_pipeline(processed_df.copy(), date_column='date')
    engineered_df.to_csv('data/processed/agricultural_data_engineered.csv', index=False)
    print(f"✓ Engineered features saved with {engineered_df.shape[1]} total columns")
    
    # ========================================================================
    # STEP 5: Data Exploration & Analysis
    # ========================================================================
    print("\nSTEP 5: Data Exploration & Analysis...")
    print("-" * 70)
    
    # Print summary
    print_data_summary(engineered_df)
    
    # Get unique values
    unique_vals = get_unique_values(engineered_df, columns=['crop', 'region'])
    print("\nUnique Values in Data:")
    for col, values in unique_vals.items():
        print(f"  {col}: {values}")
    
    # ========================================================================
    # STEP 6: Sample Analytics
    # ========================================================================
    print("\nSTEP 6: Sample Analytics...")
    print("-" * 70)
    
    # Analysis by crop
    print("\n📊 Analysis by Crop:")
    for crop in engineered_df['crop'].unique():
        crop_data = filter_by_crop(engineered_df, crop)
        avg_price = crop_data['market_price_per_kg'].mean()
        avg_yield = crop_data['yield_kg_per_hectare'].mean()
        print(f"\n  {crop}:")
        print(f"    - Average Price: ₹{avg_price:.2f}/kg")
        print(f"    - Average Yield: {avg_yield:.2f} kg/ha")
        print(f"    - Total Records: {len(crop_data)}")
    
    # Analysis by region
    print("\n\n📍 Analysis by Region:")
    for region in engineered_df['region'].unique()[:3]:  # Show first 3 regions
        region_data = filter_by_region(engineered_df, region)
        avg_price = region_data['market_price_per_kg'].mean()
        print(f"  {region}: Average Price = ₹{avg_price:.2f}/kg ({len(region_data)} records)")
    
    # ========================================================================
    # STEP 7: Profitability Estimation (Example)
    # ========================================================================
    print("\n\nSTEP 7: Profitability Estimation (Example)...")
    print("-" * 70)
    
    # Select a sample crop-region combination
    sample_crop = engineered_df['crop'].iloc[0]
    sample_region = engineered_df['region'].iloc[0]
    crop_region_data = engineered_df[
        (engineered_df['crop'] == sample_crop) & 
        (engineered_df['region'] == sample_region)
    ]
    
    if len(crop_region_data) > 0:
        estimated_yield = crop_region_data['yield_kg_per_hectare'].mean()
        predicted_price = crop_region_data['market_price_per_kg'].mean()
        
        print(f"\n📈 Scenario: {sample_crop} in {sample_region}")
        print(f"   Estimated Yield: {estimated_yield:.2f} kg/ha")
        print(f"   Predicted Price: ₹{predicted_price:.2f}/kg")
        
        profitability = calculate_profitability(
            estimated_yield=estimated_yield,
            predicted_price=predicted_price,
            cost_per_hectare=50000
        )
        
        print(f"\n   💰 Financial Projection (per hectare):")
        print(f"      - Gross Income: {profitability['gross_income_display']}")
        print(f"      - Production Cost: ₹50,000.00")
        print(f"      - Estimated Profit: {profitability['profit_display']}")
        print(f"      - ROI: {profitability['roi_percent']:.1f}%")
    
    # ========================================================================
    # STEP 8: Save Summary Report
    # ========================================================================
    print("\n\nSTEP 8: Generating Summary Report...")
    print("-" * 70)
    
    summary_data = {
        'total_records': len(engineered_df),
        'total_features': engineered_df.shape[1],
        'unique_crops': engineered_df['crop'].nunique(),
        'unique_regions': engineered_df['region'].nunique(),
        'avg_price': engineered_df['market_price_per_kg'].mean(),
        'avg_yield': engineered_df['yield_kg_per_hectare'].mean(),
        'date_range': f"{engineered_df['date'].min()} to {engineered_df['date'].max()}",
    }
    
    summary_df = pd.DataFrame([summary_data])
    summary_df.to_csv('outputs/predictions/summary_report.csv', index=False)
    
    print("\n✓ Summary Report Generated:")
    for key, value in summary_data.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    print(f"\n  Saved to: outputs/predictions/summary_report.csv")
    
    # ========================================================================
    # Final Summary
    # ========================================================================
    print("\n" + "="*70)
    print(" "*20 + "Workflow Completed Successfully!")
    print("="*70)
    print("\n📁 Output Files Generated:")
    print("  ✓ data/raw/agricultural_data_sample.csv")
    print("  ✓ data/processed/agricultural_data_preprocessed.csv")
    print("  ✓ data/processed/agricultural_data_engineered.csv")
    print("  ✓ outputs/predictions/summary_report.csv")
    print("\n📚 Next Steps:")
    print("  1. Review the processed data in data/processed/")
    print("  2. Run Jupyter notebooks in notebooks/ for deeper analysis")
    print("  3. Train ML models using the engineered features")
    print("  4. Create visualizations and dashboards")
    print("\n💡 Tip: Check out the example notebooks for more advanced usage!")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
