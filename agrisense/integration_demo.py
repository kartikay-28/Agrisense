"""
=============================================================================
BONUS: Integration Demo - Using Functions from Script 2 in Script 1 Context
=============================================================================

This demo shows how to import and use functions from agrisense_functions.py
to enhance the risk_scoring.py workflow.

This teaches:
- How to import functions from other modules
- Combining functions from different scripts
- Building more complex workflows
- Reusable code architecture

Author: AgriSense Educational Series
Date: April 2026
"""

# Import functions from agrisense_functions module
from agrisense_functions import (
    calculate_risk_score,
    get_price_summary,
    estimate_yield,
    generate_risk_report,
)

import pandas as pd


def create_farm_data():
    """Create sample farm data with both weather and price info."""
    
    farm_data = {
        'crop': ['Wheat', 'Rice', 'Tomato', 'Corn'],
        'rainfall': [50, 70, 25, 80],
        'temperature': [28, 26, 35, 25],
        'market_prices': [
            [2450, 2500, 2480],      # Wheat prices
            [3100, 3150, 3120],      # Rice prices
            [800, 850, 820],         # Tomato prices
            [1800, 1850, 1820],      # Corn prices
        ]
    }
    
    return farm_data


def integrated_analysis():
    """
    Demonstrate using functions from agrisense_functions.py
    to create a comprehensive farm analysis.
    """
    
    print("\n" + "="*80)
    print("  🌾 INTEGRATED ANALYSIS: Combining Risk + Price + Yield")
    print("="*80 + "\n")
    
    farm_data = create_farm_data()
    
    # Convert to format needed for risk report
    risk_data = []
    
    print(f"{'Crop':<10} | {'Rainfall':<8} | {'Temp':<5} | Risk  | Yield       | Prices")
    print("-"*80)
    
    for i, crop in enumerate(farm_data['crop']):
        rainfall = farm_data['rainfall'][i]
        temperature = farm_data['temperature'][i]
        prices = farm_data['market_prices'][i]
        
        # FUNCTION 1: Calculate risk using imported function
        risk_info = calculate_risk_score(rainfall, temperature)
        risk_level = risk_info['risk_level']
        
        # FUNCTION 2: Calculate price summary using imported function
        price_summary = get_price_summary(prices)
        avg_price = price_summary['average']
        
        # FUNCTION 3: Estimate yield using imported function
        yield_estimate = estimate_yield(crop, rainfall, fertilizer=100)
        
        # Create record for report
        risk_data.append({
            'crop': crop,
            'rainfall': rainfall,
            'temperature': temperature,
        })
        
        # Print row
        print(f"{crop:<10} | {rainfall:>6}mm | {temperature:>3}°C | {risk_level:<5} | "
              f"{yield_estimate:>6.0f} kg/ha | ₹{avg_price:.0f}")
    
    print("-"*80)
    
    # FUNCTION 4: Generate full risk report
    print("\n\n📊 COMPREHENSIVE RISK REPORT:")
    report = generate_risk_report(risk_data)
    
    print(f"Total Records: {report['total_records']}")
    print(f"High Risk: {report['high_risk_count']} | "
          f"Medium Risk: {report['medium_risk_count']} | "
          f"Low Risk: {report['low_risk_count']}")
    print(f"Average Risk Score: {report['average_risk_score']:.1f}/100")
    
    # Profitability analysis combining yield and price
    print("\n\n💰 PROFITABILITY ANALYSIS (Yield × Price):")
    print("-"*80)
    
    for i, crop in enumerate(farm_data['crop']):
        rainfall = farm_data['rainfall'][i]
        prices = farm_data['market_prices'][i]
        
        yield_est = estimate_yield(crop, rainfall, fertilizer=100)
        price_summary = get_price_summary(prices)
        avg_price = price_summary['average']
        
        gross_income = (yield_est / 1000) * avg_price  # Convert kg to tons
        print(f"{crop}: {yield_est:.0f} kg/ha × ₹{avg_price:.0f}/kg = ₹{gross_income:.0f}/ha")
    
    print("\n" + "="*80 + "\n")


def compare_risk_scenarios():
    """
    Use calculate_risk_score to compare different weather scenarios.
    """
    
    print("\n" + "="*80)
    print("  🌦️  SCENARIO COMPARISON: What If Analysis")
    print("="*80 + "\n")
    
    print("Scenario 1: NORMAL CONDITIONS")
    risk1 = calculate_risk_score(rainfall=60, temperature=28)
    print(f"  Rainfall: 60mm, Temp: 28°C → Risk: {risk1['risk_level']} (Score: {risk1['risk_score']}/100)")
    print(f"  {risk1['reason']}\n")
    
    print("Scenario 2: DROUGHT")
    risk2 = calculate_risk_score(rainfall=20, temperature=35)
    print(f"  Rainfall: 20mm, Temp: 35°C → Risk: {risk2['risk_level']} (Score: {risk2['risk_score']}/100)")
    print(f"  {risk2['reason']}\n")
    
    print("Scenario 3: EXCESSIVE RAINFALL")
    risk3 = calculate_risk_score(rainfall=150, temperature=25)
    print(f"  Rainfall: 150mm, Temp: 25°C → Risk: {risk3['risk_level']} (Score: {risk3['risk_score']}/100)")
    print(f"  {risk3['reason']}\n")
    
    print("Scenario 4: OPTIMAL CONDITIONS")
    risk4 = calculate_risk_score(rainfall=70, temperature=25)
    print(f"  Rainfall: 70mm, Temp: 25°C → Risk: {risk4['risk_level']} (Score: {risk4['risk_score']}/100)")
    print(f"  {risk4['reason']}\n")
    
    print("="*80 + "\n")


def crop_comparison():
    """
    Compare yield potential for different crops under same conditions.
    """
    
    print("\n" + "="*80)
    print("  🌱 CROP COMPARISON: Yield Potential")
    print("="*80 + "\n")
    
    rainfall = 60
    fertilizer = 100
    
    crops_to_test = ['Wheat', 'Rice', 'Tomato', 'Corn', 'Cotton', 'Potato']
    
    print(f"Conditions: Rainfall={rainfall}mm, Fertilizer={fertilizer}kg/ha\n")
    print(f"{'Crop':<12} | {'Estimated Yield':<25} | {'Viability'}")
    print("-"*60)
    
    for crop in crops_to_test:
        yield_est = estimate_yield(crop, rainfall, fertilizer)
        
        # Determine viability based on yield
        if yield_est > 4000:
            viability = "✅ EXCELLENT"
        elif yield_est > 3000:
            viability = "✅ GOOD"
        elif yield_est > 2000:
            viability = "⚠️  FAIR"
        else:
            viability = "❌ POOR"
        
        print(f"{crop:<12} | {yield_est:>8.0f} kg/ha{'':<13} | {viability}")
    
    print("\n" + "="*80 + "\n")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n🌾 BONUS: Integrated Analysis - Combining Multiple Scripts\n")
    
    print("This demo shows how functions from agrisense_functions.py")
    print("can be used together for comprehensive farm analysis.\n")
    
    # Run integrated analysis
    integrated_analysis()
    
    # Compare scenarios
    compare_risk_scenarios()
    
    # Compare crops
    crop_comparison()
    
    print("\n✅ CONCEPTS DEMONSTRATED:")
    print("   ✓ Importing functions from other modules")
    print("   ✓ Using multiple functions together")
    print("   ✓ Building complex analysis pipelines")
    print("   ✓ Combining results into reports")
    print("   ✓ Scenario analysis and what-if modeling")
    print("   ✓ Comparative analysis across crops\n")
    
    print("💡 KEY TAKEAWAY:")
    print("   Functions are reusable building blocks. By importing functions")
    print("   from different modules, you can build powerful analysis tools!")
    print("   This is the foundation of professional Python development.\n")
