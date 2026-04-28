"""
=============================================================================
Script 2: AgriSense Functions - Reusable Building Blocks
=============================================================================

Educational Script: Learn Functions with Parameters, Returns, and Docstrings

This script demonstrates how to create reusable functions for AgriSense:
1. Functions with parameters and return values
2. Docstrings for documentation
3. Different types of returns (dict, float, list, etc.)
4. How to call and use functions
5. Importing functions into other scripts

Key Concepts:
- Function definition (def keyword)
- Parameters and arguments
- Return values
- Type hints (optional but good practice)
- Docstrings for documentation
- Calling functions

Author: AgriSense Educational Series
Date: April 2026

=============================================================================
"""

import pandas as pd
from typing import Dict, List


# ============================================================================
# FUNCTION 1: Calculate Risk Score
# ============================================================================

def calculate_risk_score(rainfall: float, temperature: float) -> Dict:
    """
    Calculate climate risk score based on rainfall and temperature.
    
    This function demonstrates:
    - Function parameters with type hints
    - Return type hints (returns a Dict)
    - Docstrings explaining what the function does
    - Using conditionals inside functions
    
    Parameters:
    -----------
    rainfall : float
        Amount of rainfall in millimeters (mm)
    temperature : float
        Temperature in Celsius (°C)
        
    Returns:
    --------
    Dict with keys:
        - 'risk_score': Float between 0-100 (0=low risk, 100=high risk)
        - 'risk_level': String ("LOW", "MEDIUM", "HIGH")
        - 'reason': String explaining the risk
        
    Example:
    --------
    >>> risk = calculate_risk_score(rainfall=15, temperature=38)
    >>> print(risk)
    {'risk_score': 88, 'risk_level': 'HIGH', 'reason': 'Drought + Heat stress'}
    """
    
    # Initialize risk score
    risk_score = 0
    reasons = []
    
    # Check rainfall conditions
    if rainfall < 30:
        risk_score += 50  # High drought risk
        reasons.append("drought (low rainfall)")
    elif rainfall > 100:
        risk_score += 30  # Flood risk
        reasons.append("heavy rainfall (flood risk)")
    
    # Check temperature conditions
    if temperature < 10:
        risk_score += 40  # Cold stress
        reasons.append("cold stress")
    elif temperature > 35:
        risk_score += 40  # Heat stress
        reasons.append("heat stress")
    
    # Cap risk score at 100
    risk_score = min(risk_score, 100)
    
    # Determine risk level based on score
    if risk_score < 30:
        risk_level = "LOW"
    elif risk_score < 70:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
    
    # Build reason string
    reason = f"Risk factors: {', '.join(reasons)}" if reasons else "Optimal conditions"
    
    return {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'reason': reason,
    }


# ============================================================================
# FUNCTION 2: Get Price Summary
# ============================================================================

def get_price_summary(prices_list: List[float]) -> Dict:
    """
    Calculate summary statistics for a list of prices.
    
    This function demonstrates:
    - Taking a list as parameter
    - Calculating multiple statistics
    - Returning a dictionary with multiple values
    - Error handling (checking if list is empty)
    
    Parameters:
    -----------
    prices_list : List[float]
        List of prices in Rupees (₹)
        
    Returns:
    --------
    Dict with keys:
        - 'average': Average price
        - 'min': Minimum price
        - 'max': Maximum price
        - 'median': Median price
        - 'count': Number of prices
        
    Example:
    --------
    >>> prices = [2500, 3000, 2800, 3500]
    >>> summary = get_price_summary(prices)
    >>> print(f"Average price: ₹{summary['average']:.2f}")
    Average price: ₹2975.00
    """
    
    # Handle empty list
    if len(prices_list) == 0:
        return {
            'average': 0,
            'min': 0,
            'max': 0,
            'median': 0,
            'count': 0,
            'error': 'Empty price list'
        }
    
    # Convert to pandas Series for easy calculations
    prices_series = pd.Series(prices_list)
    
    # Calculate statistics
    summary = {
        'average': prices_series.mean(),
        'min': prices_series.min(),
        'max': prices_series.max(),
        'median': prices_series.median(),
        'count': len(prices_list),
        'std_dev': prices_series.std(),
    }
    
    return summary


# ============================================================================
# FUNCTION 3: Estimate Yield
# ============================================================================

def estimate_yield(crop: str, rainfall: float, fertilizer: float) -> float:
    """
    Estimate crop yield based on crop type, rainfall, and fertilizer.
    
    This function demonstrates:
    - String parameter (crop name)
    - Multiple parameters of different types
    - Using conditionals with parameters
    - Returning a single value (not a dict)
    - Using realistic agricultural formulas
    
    Parameters:
    -----------
    crop : str
        Name of crop (e.g., "Wheat", "Rice", "Tomato")
    rainfall : float
        Amount of rainfall in mm
    fertilizer : float
        Amount of fertilizer in kg/hectare
        
    Returns:
    --------
    float
        Estimated yield in kg/hectare
        
    Formula Logic:
    - Base yield depends on crop type
    - Multiply by rainfall factor (optimal ~60mm)
    - Multiply by fertilizer factor (optimal ~100kg/ha)
    
    Example:
    --------
    >>> yield_est = estimate_yield(crop="Wheat", rainfall=60, fertilizer=100)
    >>> print(f"Estimated yield: {yield_est:.0f} kg/ha")
    Estimated yield: 4800 kg/ha
    """
    
    # Step 1: Base yield by crop type
    # Using realistic potential yields for Indian crops
    base_yields = {
        'Wheat': 4800,
        'Rice': 5200,
        'Tomato': 50000,  # Note: much higher, different unit usually
        'Corn': 5500,
        'Potato': 40000,
        'Cotton': 1500,
    }
    
    # Get base yield for crop (default to 5000 if not found)
    base_yield = base_yields.get(crop, 5000)
    
    # Step 2: Calculate rainfall factor (optimal is 60mm)
    # Too little rain or too much reduces yield
    rainfall_factor = 1.0
    if rainfall < 20:
        rainfall_factor = 0.4  # Severe drought: 40% yield
    elif rainfall < 40:
        rainfall_factor = 0.7  # Drought: 70% yield
    elif rainfall < 60:
        rainfall_factor = 0.9  # Below optimal: 90% yield
    elif rainfall <= 80:
        rainfall_factor = 1.0  # Optimal: 100% yield
    elif rainfall < 120:
        rainfall_factor = 0.95  # Excess water: 95% yield
    else:
        rainfall_factor = 0.7  # Too much water: 70% yield
    
    # Step 3: Calculate fertilizer factor (optimal is 100kg/ha)
    fertilizer_factor = 1.0
    if fertilizer < 20:
        fertilizer_factor = 0.5  # Very low: 50% yield
    elif fertilizer < 50:
        fertilizer_factor = 0.7  # Low: 70% yield
    elif fertilizer < 100:
        fertilizer_factor = 0.9  # Below optimal: 90% yield
    elif fertilizer <= 150:
        fertilizer_factor = 1.0  # Optimal: 100% yield
    elif fertilizer < 200:
        fertilizer_factor = 0.95  # Above optimal: 95% yield
    else:
        fertilizer_factor = 0.9  # Too much: 90% yield (diminishing returns)
    
    # Step 4: Calculate final yield
    estimated_yield = base_yield * rainfall_factor * fertilizer_factor
    
    return estimated_yield


# ============================================================================
# FUNCTION 4: Generate Comprehensive Risk Report
# ============================================================================

def generate_risk_report(data: List[Dict]) -> Dict:
    """
    Generate a comprehensive risk report from a list of farm data.
    
    This function demonstrates:
    - Taking a list of dictionaries as input
    - Using loops inside functions
    - Calling other functions from within this function
    - Returning complex data structures
    - Real-world data processing
    
    Parameters:
    -----------
    data : List[Dict]
        List of dictionaries with keys: 'crop', 'rainfall', 'temperature'
        Example: [{'crop': 'Wheat', 'rainfall': 50, 'temperature': 25}, ...]
        
    Returns:
    --------
    Dict with:
        - 'total_records': Number of records processed
        - 'high_risk_count': Number of high-risk situations
        - 'medium_risk_count': Number of medium-risk situations
        - 'low_risk_count': Number of low-risk situations
        - 'average_risk_score': Average risk score across all
        - 'details': List with details for each record
        
    Example:
    --------
    >>> data = [
    ...     {'crop': 'Wheat', 'rainfall': 15, 'temperature': 36},
    ...     {'crop': 'Rice', 'rainfall': 70, 'temperature': 28},
    ... ]
    >>> report = generate_risk_report(data)
    >>> print(f"High risk: {report['high_risk_count']}")
    High risk: 1
    """
    
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0
    total_risk_score = 0
    details = []
    
    # LOOP through each record in data
    for record in data:
        # Extract fields from record
        crop = record.get('crop', 'Unknown')
        rainfall = record.get('rainfall', 0)
        temperature = record.get('temperature', 25)
        
        # Call calculate_risk_score function
        risk_info = calculate_risk_score(rainfall, temperature)
        risk_level = risk_info['risk_level']
        risk_score = risk_info['risk_score']
        
        # Count by risk level
        if risk_level == "HIGH":
            high_risk_count += 1
        elif risk_level == "MEDIUM":
            medium_risk_count += 1
        else:
            low_risk_count += 1
        
        # Add to total for averaging
        total_risk_score += risk_score
        
        # Store details
        details.append({
            'crop': crop,
            'rainfall': rainfall,
            'temperature': temperature,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'reason': risk_info['reason'],
        })
    
    # Calculate average
    total_records = len(data)
    average_risk_score = total_risk_score / total_records if total_records > 0 else 0
    
    # Build report dictionary
    report = {
        'total_records': total_records,
        'high_risk_count': high_risk_count,
        'medium_risk_count': medium_risk_count,
        'low_risk_count': low_risk_count,
        'average_risk_score': average_risk_score,
        'details': details,
    }
    
    return report


# ============================================================================
# FUNCTION 5: Print Report Nicely (Helper Function)
# ============================================================================

def print_report_summary(report: Dict) -> None:
    """
    Print a risk report in a readable format.
    
    This function demonstrates:
    - Taking a dictionary as parameter
    - Returning None (just prints, doesn't return data)
    - Using data from other function results
    - String formatting for output
    
    Parameters:
    -----------
    report : Dict
        Report dictionary (from generate_risk_report function)
    """
    
    print("\n" + "="*70)
    print("  📊 RISK REPORT SUMMARY")
    print("="*70)
    
    print(f"\nTotal Records Analyzed: {report['total_records']}")
    print(f"Average Risk Score: {report['average_risk_score']:.1f}/100")
    print(f"\nRisk Distribution:")
    print(f"  🟢 LOW RISK:    {report['low_risk_count']} records")
    print(f"  🟡 MEDIUM RISK: {report['medium_risk_count']} records")
    print(f"  🔴 HIGH RISK:   {report['high_risk_count']} records")
    
    print(f"\nDetailed Analysis:")
    print("-"*70)
    
    for i, detail in enumerate(report['details'], 1):
        print(f"\n{i}. {detail['crop']}")
        print(f"   Rainfall: {detail['rainfall']}mm | Temp: {detail['temperature']}°C")
        print(f"   Risk Level: {detail['risk_level']} (Score: {detail['risk_score']}/100)")
        print(f"   Reason: {detail['reason']}")
    
    print("\n" + "="*70 + "\n")


# ============================================================================
# MAIN: Demonstration of all functions
# ============================================================================

if __name__ == "__main__":
    """
    Main execution. This runs when you execute the script:
        python agrisense_functions.py
    """
    
    print("\n🌾 AgriSense Educational Script: Functions\n")
    print("Demonstrating how to use reusable functions for data processing\n")
    
    # ========================================================================
    # DEMO 1: Use calculate_risk_score function
    # ========================================================================
    
    print("="*70)
    print("DEMO 1: calculate_risk_score() function")
    print("="*70)
    
    print("\nCalculating risk for different weather conditions:\n")
    
    test_conditions = [
        (15, 38),    # Low rainfall, high temperature
        (60, 25),    # Optimal conditions
        (120, 28),   # High rainfall, normal temp
        (40, 20),    # Moderate rain, cool temp
    ]
    
    for rainfall, temp in test_conditions:
        result = calculate_risk_score(rainfall, temp)
        print(f"Rainfall: {rainfall}mm, Temp: {temp}°C")
        print(f"  → Risk Score: {result['risk_score']}/100")
        print(f"  → Level: {result['risk_level']}")
        print(f"  → {result['reason']}\n")
    
    # ========================================================================
    # DEMO 2: Use get_price_summary function
    # ========================================================================
    
    print("="*70)
    print("DEMO 2: get_price_summary() function")
    print("="*70)
    
    wheat_prices = [2400, 2500, 2450, 2600, 2550]
    print(f"\nWheat market prices: {wheat_prices}\n")
    
    summary = get_price_summary(wheat_prices)
    print(f"Average Price:  ₹{summary['average']:.2f}")
    print(f"Min Price:      ₹{summary['min']:.2f}")
    print(f"Max Price:      ₹{summary['max']:.2f}")
    print(f"Median Price:   ₹{summary['median']:.2f}")
    print(f"Std Deviation:  ₹{summary['std_dev']:.2f}")
    print(f"Number of prices: {summary['count']}\n")
    
    # ========================================================================
    # DEMO 3: Use estimate_yield function
    # ========================================================================
    
    print("="*70)
    print("DEMO 3: estimate_yield() function")
    print("="*70)
    
    print("\nEstimating yield for different crops and conditions:\n")
    
    yield_estimates = [
        ("Wheat", 50, 90),
        ("Wheat", 20, 100),  # Drought
        ("Rice", 70, 110),   # Optimal
        ("Tomato", 60, 80),  # Less fertilizer
    ]
    
    for crop, rainfall, fertilizer in yield_estimates:
        yield_est = estimate_yield(crop, rainfall, fertilizer)
        print(f"{crop}: {rainfall}mm rain, {fertilizer}kg/ha fertilizer")
        print(f"  → Estimated Yield: {yield_est:.0f} kg/ha\n")
    
    # ========================================================================
    # DEMO 4: Use generate_risk_report function
    # ========================================================================
    
    print("="*70)
    print("DEMO 4: generate_risk_report() function")
    print("="*70)
    
    # Create sample farm data
    farm_data = [
        {'crop': 'Wheat', 'rainfall': 15, 'temperature': 36},
        {'crop': 'Rice', 'rainfall': 70, 'temperature': 28},
        {'crop': 'Tomato', 'rainfall': 5, 'temperature': 38},
        {'crop': 'Corn', 'rainfall': 80, 'temperature': 26},
    ]
    
    # Generate report
    report = generate_risk_report(farm_data)
    
    # Print nicely
    print_report_summary(report)
    
    # ========================================================================
    # DEMO 5: Show how to import and use these in other scripts
    # ========================================================================
    
    print("="*70)
    print("HOW TO USE THESE FUNCTIONS IN OTHER SCRIPTS")
    print("="*70)
    
    print("""
To use these functions in another script, import them at the top:

    from agrisense_functions import (
        calculate_risk_score,
        get_price_summary,
        estimate_yield,
        generate_risk_report,
        print_report_summary
    )

Then call them:

    risk = calculate_risk_score(rainfall=50, temperature=28)
    prices = get_price_summary([2500, 2600, 2550])
    yield_est = estimate_yield("Wheat", rainfall=60, fertilizer=100)
    
That's it! Functions are reusable building blocks for your code.
    """)
    
    print("\n" + "="*70)
    print("✅ Concepts Learned:")
    print("   ✓ Creating functions with parameters")
    print("   ✓ Type hints for clarity")
    print("   ✓ Docstrings for documentation")
    print("   ✓ Different return types (dict, float, None)")
    print("   ✓ Calling functions from other functions")
    print("   ✓ Using functions in main block")
    print("   ✓ How to import functions in other scripts")
    print("="*70 + "\n")
