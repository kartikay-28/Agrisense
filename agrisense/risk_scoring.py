"""
=============================================================================
Script 1: AgriSense Climate Risk Scoring
=============================================================================

Educational Script: Learn Conditionals (if-elif-else) and Loops

This script demonstrates how to use conditionals and loops to:
1. Read agricultural data (rainfall, temperature)
2. Use IF-ELIF-ELSE to make decisions about risk levels
3. Use LOOPS to process multiple crops and days
4. Generate a risk report for farmers

Key Concepts:
- if-elif-else statements for conditional logic
- for loops to iterate through data
- List of dictionaries for data storage
- String formatting for readable output

Author: AgriSense Educational Series
Date: April 2026

=============================================================================
"""

import pandas as pd
from datetime import datetime, timedelta


# ============================================================================
# STEP 1: CREATE SAMPLE DATA (In real project, this would load from CSV)
# ============================================================================

def create_sample_weather_data():
    """
    Create sample weather data for demonstration.
    Returns a pandas DataFrame with crop, date, rainfall, and temperature.
    """
    # Sample data: List of dictionaries
    weather_data = [
        {'crop': 'Wheat', 'date': '2024-04-01', 'rainfall_mm': 15, 'temperature_c': 28},
        {'crop': 'Wheat', 'date': '2024-04-02', 'rainfall_mm': 25, 'temperature_c': 32},
        {'crop': 'Rice', 'date': '2024-04-01', 'rainfall_mm': 45, 'temperature_c': 30},
        {'crop': 'Rice', 'date': '2024-04-02', 'rainfall_mm': 75, 'temperature_c': 27},
        {'crop': 'Tomato', 'date': '2024-04-01', 'rainfall_mm': 5, 'temperature_c': 38},
        {'crop': 'Tomato', 'date': '2024-04-02', 'rainfall_mm': 55, 'temperature_c': 31},
        {'crop': 'Corn', 'date': '2024-04-01', 'rainfall_mm': 120, 'temperature_c': 26},
        {'crop': 'Corn', 'date': '2024-04-02', 'rainfall_mm': 60, 'temperature_c': 29},
    ]
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(weather_data)
    return df


# ============================================================================
# STEP 2: FUNCTION WITH CONDITIONALS - Determine Risk Level Based on Rainfall
# ============================================================================

def get_rainfall_risk(rainfall_mm):
    """
    Use IF-ELIF-ELSE to determine drought or flood risk based on rainfall.
    
    Rules:
    - rainfall < 30 mm  → HIGH RISK (drought)
    - 30-80 mm          → MEDIUM RISK (normal)
    - > 80 mm           → LOW RISK (but watch for flooding)
    
    Parameters:
    -----------
    rainfall_mm : float
        Amount of rainfall in millimeters
        
    Returns:
    --------
    tuple: (risk_level, message)
        risk_level: "HIGH", "MEDIUM", or "LOW"
        message: Human-readable description
    """
    
    # CONDITIONAL 1: Check for drought risk (too little rain)
    if rainfall_mm < 30:
        risk_level = "HIGH"
        message = f"🚨 DROUGHT ALERT: Only {rainfall_mm:.1f}mm rainfall. Crops need more water!"
    
    # CONDITIONAL 2: Check for normal rainfall
    elif rainfall_mm >= 30 and rainfall_mm <= 80:
        risk_level = "MEDIUM"
        message = f"✅ NORMAL: {rainfall_mm:.1f}mm rainfall. Good conditions for growth."
    
    # CONDITIONAL 3: Check for flood risk (too much rain)
    else:  # rainfall_mm > 80
        risk_level = "LOW"
        message = f"⚠️  HIGH RAINFALL: {rainfall_mm:.1f}mm. Watch for flooding and water logging."
    
    return risk_level, message


# ============================================================================
# STEP 3: FUNCTION WITH CONDITIONALS - Check Temperature Risk
# ============================================================================

def get_temperature_risk(temperature_c):
    """
    Use IF-ELIF-ELSE to determine heat or cold stress risk.
    
    Rules:
    - temperature < 10°C   → COLD STRESS
    - 10-25°C              → IDEAL
    - 25-35°C              → WARM (OK)
    - > 35°C               → HEAT STRESS
    
    Parameters:
    -----------
    temperature_c : float
        Temperature in Celsius
        
    Returns:
    --------
    tuple: (temp_risk, temp_message)
    """
    
    if temperature_c < 10:
        temp_risk = "HIGH"
        temp_message = f"❄️  COLD STRESS: {temperature_c}°C is too cold!"
    
    elif temperature_c >= 10 and temperature_c < 25:
        temp_risk = "LOW"
        temp_message = f"🌤️  IDEAL: {temperature_c}°C is perfect!"
    
    elif temperature_c >= 25 and temperature_c <= 35:
        temp_risk = "LOW"
        temp_message = f"☀️  WARM: {temperature_c}°C is acceptable."
    
    else:  # temperature_c > 35
        temp_risk = "HIGH"
        temp_message = f"🔥 HEAT STRESS: {temperature_c}°C is dangerously hot!"
    
    return temp_risk, temp_message


# ============================================================================
# STEP 4: COMBINED RISK SCORER - Combine Both Conditions
# ============================================================================

def calculate_combined_risk(rainfall_mm, temperature_c):
    """
    Combine rainfall and temperature checks to get overall risk score.
    
    Uses multiple IF-ELIF-ELSE to handle combinations:
    - If any condition is HIGH, overall risk is HIGH
    - If both are MEDIUM, overall is MEDIUM
    - Otherwise, try to keep it low
    """
    
    # Get individual risk levels
    rainfall_risk, r_msg = get_rainfall_risk(rainfall_mm)
    temp_risk, t_msg = get_temperature_risk(temperature_c)
    
    # CONDITIONAL: Combine risks using logic
    if rainfall_risk == "HIGH" or temp_risk == "HIGH":
        # If EITHER rainfall or temperature is high risk, overall is HIGH
        overall_risk = "HIGH"
    elif rainfall_risk == "MEDIUM" or temp_risk == "MEDIUM":
        # If EITHER is medium, overall is MEDIUM
        overall_risk = "MEDIUM"
    else:
        # Both are low
        overall_risk = "LOW"
    
    return {
        'overall_risk': overall_risk,
        'rainfall_risk': rainfall_risk,
        'temp_risk': temp_risk,
        'rainfall_message': r_msg,
        'temp_message': t_msg,
    }


# ============================================================================
# STEP 5: LOOP THROUGH DATA AND GENERATE RISK REPORT
# ============================================================================

def generate_risk_report(df):
    """
    USE LOOPS to go through each row of data and calculate risk.
    
    This demonstrates:
    - FOR LOOP to iterate through rows
    - Using conditionals inside loops
    - Building a report
    """
    
    print("\n" + "="*80)
    print("  ⛅ AgriSense Climate Risk Scoring Report")
    print("="*80 + "\n")
    
    # Store high-risk items for summary
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0
    
    # LOOP through each row in the DataFrame
    for index, row in df.iterrows():
        # Extract data from this row
        crop = row['crop']
        date = row['date']
        rainfall = row['rainfall_mm']
        temperature = row['temperature_c']
        
        # Calculate combined risk for this row
        risk_info = calculate_combined_risk(rainfall, temperature)
        risk_level = risk_info['overall_risk']
        
        # Print this row's information
        print(f"📍 {index + 1}. {crop.upper()} on {date}")
        print(f"   Rainfall: {rainfall:.1f}mm | Temperature: {temperature}°C")
        print(f"   {risk_info['rainfall_message']}")
        print(f"   {risk_info['temp_message']}")
        print(f"   ➜ OVERALL RISK: {risk_level}")
        print()
        
        # COUNT risk levels using conditionals
        if risk_level == "HIGH":
            high_risk_count += 1
        elif risk_level == "MEDIUM":
            medium_risk_count += 1
        else:
            low_risk_count += 1
    
    # ========================================================================
    # PRINT SUMMARY USING CONDITIONALS
    # ========================================================================
    
    print("="*80)
    print("  📊 SUMMARY")
    print("="*80)
    print(f"High Risk:   {high_risk_count} cases  🚨")
    print(f"Medium Risk: {medium_risk_count} cases ⚠️")
    print(f"Low Risk:    {low_risk_count} cases ✅")
    print()
    
    # CONDITIONAL: Give recommendations based on summary
    if high_risk_count > 0:
        print("⚠️  ACTION REQUIRED: {} crops are at HIGH RISK!".format(high_risk_count))
        print("   → Farmers should take immediate action:")
        print("   → For Drought: Increase irrigation")
        print("   → For Heat: Use shade and mulching")
        print("   → For Flood: Ensure drainage")
    else:
        print("✅ All crops are in acceptable conditions!")
    
    print("\n" + "="*80 + "\n")


# ============================================================================
# STEP 6: FIND CROPS WITH HIGH RISK USING LOOPS AND CONDITIONALS
# ============================================================================

def find_high_risk_crops(df):
    """
    USE LOOP to find and list all crops that are at HIGH RISK.
    
    This demonstrates:
    - FOR loop with data filtering
    - CONDITIONALS to check risk levels
    - Collecting results
    """
    
    print("\n" + "-"*80)
    print("🚨 HIGH RISK CROPS ALERT")
    print("-"*80)
    
    high_risk_crops = []
    
    # LOOP through each row
    for index, row in df.iterrows():
        rainfall = row['rainfall_mm']
        temperature = row['temperature_c']
        crop = row['crop']
        
        # Calculate risk
        risk_info = calculate_combined_risk(rainfall, temperature)
        
        # CONDITIONAL: Check if high risk
        if risk_info['overall_risk'] == "HIGH":
            # Add to our high-risk list
            high_risk_crops.append({
                'crop': crop,
                'date': row['date'],
                'rainfall': rainfall,
                'temperature': temperature,
                'reason': risk_info['rainfall_message'] if risk_info['rainfall_risk'] == "HIGH" 
                         else risk_info['temp_message']
            })
    
    # CONDITIONAL: Print results
    if len(high_risk_crops) > 0:
        print(f"\n⚠️  Found {len(high_risk_crops)} high-risk situations:\n")
        for i, alert in enumerate(high_risk_crops, 1):
            print(f"  {i}. {alert['crop']} ({alert['date']})")
            print(f"     {alert['reason']}")
    else:
        print("\n✅ No high-risk situations detected!")
    
    print()


# ============================================================================
# MAIN: Run all functions
# ============================================================================

if __name__ == "__main__":
    """
    Main execution. This runs when you execute the script:
        python risk_scoring.py
    """
    
    print("\n🌾 Welcome to AgriSense Educational Script: Conditionals & Loops\n")
    
    # Create sample data
    print("📊 Creating sample weather data...")
    df = create_sample_weather_data()
    print(f"   Created {len(df)} records\n")
    
    # Display the data
    print("📋 Sample Data:")
    print(df.to_string(index=False))
    
    # Generate risk report (with loops and conditionals)
    generate_risk_report(df)
    
    # Find high-risk crops
    find_high_risk_crops(df)
    
    # ========================================================================
    # INTERACTIVE EXAMPLES
    # ========================================================================
    
    print("\n" + "="*80)
    print("  🎓 TRY THESE EXAMPLES")
    print("="*80 + "\n")
    
    # Example 1: Single rainfall check
    print("Example 1: Check rainfall risk")
    risk, msg = get_rainfall_risk(20)
    print(f"  Rainfall: 20mm → Risk: {risk} → {msg}\n")
    
    # Example 2: Single temperature check
    print("Example 2: Check temperature risk")
    risk, msg = get_temperature_risk(38)
    print(f"  Temperature: 38°C → Risk: {risk} → {msg}\n")
    
    # Example 3: Combined check
    print("Example 3: Combined rainfall + temperature check")
    risk_info = calculate_combined_risk(rainfall_mm=15, temperature_c=36)
    print(f"  Rainfall: 15mm, Temperature: 36°C")
    print(f"  Overall Risk: {risk_info['overall_risk']}")
    print(f"  Details: {risk_info['rainfall_message']}")
    print(f"  Details: {risk_info['temp_message']}\n")
    
    print("="*80 + "\n")
    print("✅ Concepts Learned:")
    print("   ✓ IF-ELIF-ELSE conditionals for decision making")
    print("   ✓ FOR loops to iterate through data")
    print("   ✓ Combining conditions for complex logic")
    print("   ✓ Building reports from data\n")
