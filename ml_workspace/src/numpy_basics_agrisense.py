"""
NumPy Basics with AgriSense Examples
====================================

Learning Objectives (Sections 4.22-4.24):
- Create and manipulate NumPy arrays (1D and 2D)
- Understand array shapes and properties
- Perform basic math operations (.mean(), .std(), arithmetic)
- Normalize and scale data
- Use vectorized operations vs loops
- Apply to real AgriSense climate risk scoring

Examples:
1. Basic statistics: crop yields across fields
2. Rainfall deviation: comparing actual vs normal rainfall
3. Climate Risk Score: weighted calculation using rainfall, temperature, soil moisture

Author: AgriSense Educational Team
"""

import numpy as np


# ============================================================================
# SECTION 1: Creating Arrays and Understanding Shapes
# ============================================================================

def example_1_basic_stats():
    """
    Example 1: Basic Statistics - Crop Yields
    
    Learn: Creating arrays, calculating mean/max/min, percentage change
    AgriSense Context: Analyzing yield across 10 fields to identify productivity patterns
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: BASIC STATISTICS - CROP YIELDS")
    print("="*70)
    
    # Create a 1D NumPy array of crop yields (quintal/hectare) for 10 fields
    yields = np.array([25.3, 28.5, 22.1, 30.2, 26.8, 24.5, 29.1, 23.7, 27.4, 25.9])
    
    print("\nStep 1: Create NumPy array of yields")
    print(f"Yields array: {yields}")
    print(f"Array shape: {yields.shape}")  # (10,) means 1D array with 10 elements
    print(f"Array dtype: {yields.dtype}")  # Data type of elements
    
    # Calculate basic statistics
    avg_yield = np.mean(yields)
    max_yield = np.max(yields)
    min_yield = np.min(yields)
    std_yield = np.std(yields)
    
    print("\nStep 2: Calculate statistics")
    print(f"Average Yield: {avg_yield:.2f} quintal/hectare")
    print(f"Maximum Yield: {max_yield:.2f} quintal/hectare (Field {np.argmax(yields) + 1})")
    print(f"Minimum Yield: {min_yield:.2f} quintal/hectare (Field {np.argmin(yields) + 1})")
    print(f"Std Deviation: {std_yield:.2f} quintal/hectare")
    
    # Price change example
    prices_period_1 = np.array([2400, 2450, 2380, 2500])  # Wheat prices (₹/quintal) 4 markets
    prices_period_2 = np.array([2550, 2480, 2410, 2650])  # Same 4 markets next period
    
    # Calculate percentage change using NumPy subtraction and division
    price_change = ((prices_period_2 - prices_period_1) / prices_period_1) * 100
    
    print("\nStep 3: Price change analysis")
    print(f"Period 1 Prices (₹/quintal): {prices_period_1}")
    print(f"Period 2 Prices (₹/quintal): {prices_period_2}")
    print(f"Price Change (%): {np.round(price_change, 2)}")
    print(f"Average Price Increase: {np.mean(price_change):.2f}%")
    
    return yields


# ============================================================================
# SECTION 2: Array Operations - Rainfall Deviation Analysis
# ============================================================================

def example_2_rainfall_deviation():
    """
    Example 2: Rainfall Deviation - Comparing Actual vs Normal
    
    Learn: Array creation, element-wise subtraction, conditional filtering
    AgriSense Context: Identify drought/flood conditions by comparing to historical norms
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: RAINFALL DEVIATION ANALYSIS")
    print("="*70)
    
    # Create arrays: actual rainfall for last 7 days vs normal rainfall
    actual_rainfall = np.array([15.2, 8.5, 0.0, 22.3, 5.1, 18.6, 2.3])  # mm
    normal_rainfall = np.array([12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0])  # mm
    
    print("\nStep 1: Create rainfall arrays")
    print(f"Actual Rainfall (mm): {actual_rainfall}")
    print(f"Normal Rainfall (mm): {normal_rainfall}")
    
    # Calculate deviation (actual - normal)
    deviation = actual_rainfall - normal_rainfall
    
    print("\nStep 2: Calculate deviation (Actual - Normal)")
    print(f"Rainfall Deviation (mm): {np.round(deviation, 2)}")
    
    # Classify days as drought/normal/flood
    print("\nStep 3: Rainfall classification for each day")
    drought_days = 0
    normal_days = 0
    flood_days = 0
    
    # Method 1: Using loop (for beginners)
    print("\nMethod 1: Using for loop")
    for day in range(len(deviation)):
        if deviation[day] < -5:
            status = "🔴 DROUGHT"
            drought_days += 1
        elif deviation[day] > 5:
            status = "🔵 FLOOD"
            flood_days += 1
        else:
            status = "🟢 NORMAL"
            normal_days += 1
        print(f"  Day {day+1}: {actual_rainfall[day]:5.1f}mm vs {normal_rainfall[day]:5.1f}mm = {deviation[day]:+6.1f}mm → {status}")
    
    # Method 2: Vectorized NumPy way (more efficient)
    print("\nMethod 2: Vectorized NumPy approach")
    drought_mask = deviation < -5
    flood_mask = deviation > 5
    print(f"  Days with drought (deviation < -5mm): {np.sum(drought_mask)} days")
    print(f"  Days with flood (deviation > 5mm): {np.sum(flood_mask)} days")
    print(f"  Days with normal rainfall: {np.sum(~drought_mask & ~flood_mask)} days")
    
    # Calculate statistics
    print("\nStep 4: Deviation statistics")
    print(f"Average deviation: {np.mean(deviation):.2f} mm")
    print(f"Cumulative deviation: {np.sum(deviation):.2f} mm")
    if np.mean(deviation) < -2:
        print("⚠️  Overall: Drier than normal conditions")
    elif np.mean(deviation) > 2:
        print("⚠️  Overall: Wetter than normal conditions")
    else:
        print("✓ Overall: Close to normal conditions")
    
    return actual_rainfall, normal_rainfall


# ============================================================================
# SECTION 3: Climate Risk Score - Main AgriSense Application
# ============================================================================

def example_3_climate_risk_score():
    """
    Example 3: Climate Risk Score - Weighted Multi-factor Analysis
    
    Learn: 2D arrays, normalization/scaling, weighted calculations
    AgriSense Context: Calculate daily climate risk for crop to guide farmers
    
    Formula:
    risk_score = (0.5 * rainfall_deviation) + (0.3 * temperature_stress) + (0.2 * soil_dryness)
    
    Risk Categories:
    - < 0.3 → Low Risk (🟢)
    - 0.3-0.6 → Medium Risk (🟡)
    - > 0.6 → High Risk (🔴)
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: CLIMATE RISK SCORE - WEIGHTED MULTI-FACTOR ANALYSIS")
    print("="*70)
    
    # Raw climate data for 5 days
    rainfall = np.array([18.0, 5.0, 0.0, 25.0, 10.0])      # mm
    temperature = np.array([28.0, 35.0, 38.0, 26.0, 32.0])  # °C
    soil_moisture = np.array([65.0, 35.0, 15.0, 80.0, 40.0]) # %
    
    print("\nStep 1: Create climate data arrays (5 days)")
    print(f"Rainfall (mm):        {rainfall}")
    print(f"Temperature (°C):     {temperature}")
    print(f"Soil Moisture (%):    {soil_moisture}")
    print(f"All arrays have shape: {rainfall.shape}")
    
    # Step 2: Calculate deviations/stress components
    print("\nStep 2: Calculate individual stress components")
    
    # Rainfall deviation from optimal (25 mm is optimal for most crops)
    optimal_rainfall = 25.0
    rainfall_deviation = np.abs(rainfall - optimal_rainfall) / optimal_rainfall
    print(f"Rainfall Deviation (0-1): {np.round(rainfall_deviation, 3)}")
    
    # Temperature stress (optimal 25-30°C)
    temp_stress = np.zeros_like(temperature, dtype=float)
    for i in range(len(temperature)):
        if temperature[i] < 15 or temperature[i] > 35:
            temp_stress[i] = 1.0  # Maximum stress
        elif temperature[i] < 20 or temperature[i] > 32:
            temp_stress[i] = 0.5  # Medium stress
        else:
            temp_stress[i] = 0.0  # No stress
    print(f"Temperature Stress (0-1): {temp_stress}")
    
    # Soil dryness (inverse of moisture: 1 - normalized_moisture)
    soil_dryness = 1.0 - (soil_moisture / 100.0)
    print(f"Soil Dryness (0-1):    {np.round(soil_dryness, 3)}")
    
    # Step 3: Calculate weighted risk score
    print("\nStep 3: Calculate weighted climate risk score")
    weights = {'rainfall': 0.5, 'temperature': 0.3, 'soil': 0.2}
    print(f"Weights: Rainfall={weights['rainfall']}, Temperature={weights['temperature']}, Soil={weights['soil']}")
    
    # Weighted formula using NumPy
    risk_score = (weights['rainfall'] * rainfall_deviation + 
                  weights['temperature'] * temp_stress + 
                  weights['soil'] * soil_dryness)
    
    print(f"\nRisk Scores (0-1): {np.round(risk_score, 3)}")
    
    # Step 4: Classify risk levels
    print("\nStep 4: Risk classification for each day")
    print("-" * 70)
    
    for day in range(len(risk_score)):
        score = risk_score[day]
        
        # Determine risk level
        if score < 0.3:
            risk_level = "LOW RISK 🟢"
            recommendation = "Conditions favorable for crop growth"
        elif score < 0.6:
            risk_level = "MEDIUM RISK 🟡"
            recommendation = "Monitor conditions; may need intervention"
        else:
            risk_level = "HIGH RISK 🔴"
            recommendation = "Take protective measures (irrigation, shade, etc.)"
        
        print(f"\nDay {day+1}:")
        print(f"  Rainfall: {rainfall[day]:5.1f}mm | Temp: {temperature[day]:5.1f}°C | Soil Moisture: {soil_moisture[day]:5.1f}%")
        print(f"  Risk Score: {score:.3f} → {risk_level}")
        print(f"  Action: {recommendation}")
    
    # Summary statistics
    print("\n" + "-" * 70)
    print("RISK SUMMARY:")
    high_risk_days = np.sum(risk_score > 0.6)
    medium_risk_days = np.sum((risk_score >= 0.3) & (risk_score <= 0.6))
    low_risk_days = np.sum(risk_score < 0.3)
    avg_risk = np.mean(risk_score)
    
    print(f"High Risk Days:   {high_risk_days} out of {len(risk_score)}")
    print(f"Medium Risk Days: {medium_risk_days} out of {len(risk_score)}")
    print(f"Low Risk Days:    {low_risk_days} out of {len(risk_score)}")
    print(f"Average Risk Score: {avg_risk:.3f}")
    
    if avg_risk > 0.6:
        print("\n⚠️  ALERT: Overall HIGH RISK conditions - consider protective measures")
    elif avg_risk > 0.3:
        print("\n⚠️  CAUTION: Overall MEDIUM RISK - monitor daily conditions")
    else:
        print("\n✓ GOOD: Overall LOW RISK - conditions suitable for crop growth")
    
    return risk_score


# ============================================================================
# ADVANCED: 2D Arrays for Multi-Crop/Multi-Day Analysis
# ============================================================================

def example_4_multi_crop_analysis():
    """
    Example 4: BONUS - 2D Array Analysis for Multiple Crops
    
    Learn: 2D arrays, broadcasting, matrix operations
    AgriSense Context: Compare climate risk across 4 crops with historical data
    """
    print("\n" + "="*70)
    print("EXAMPLE 4 (BONUS): MULTI-CROP 2D ARRAY ANALYSIS")
    print("="*70)
    
    # 2D array: Rows = Crops, Columns = Days
    # Data: Average yields (quintal/ha) for 4 crops over 5 days of different weather
    crop_names = ['Wheat', 'Rice', 'Tomato', 'Corn']
    
    # Simulated potential yields under different daily conditions
    yields_by_crop = np.array([
        [24.0, 22.5, 18.0, 26.5, 25.0],  # Wheat
        [22.0, 21.0, 16.0, 24.0, 23.0],  # Rice
        [45.0, 42.0, 28.0, 48.0, 46.0],  # Tomato (in units of 100s)
        [26.0, 24.0, 19.0, 28.0, 27.0],  # Corn
    ])
    
    print("\nStep 1: Create 2D array (Crops × Days)")
    print(f"Shape: {yields_by_crop.shape} (4 crops, 5 days)")
    print("\nYields by crop (quintal/hectare):")
    for i, crop in enumerate(crop_names):
        print(f"  {crop:10s}: {yields_by_crop[i]}")
    
    print("\nStep 2: Calculate statistics by crop")
    crop_avg = np.mean(yields_by_crop, axis=1)  # Average across days (axis=1)
    crop_max = np.max(yields_by_crop, axis=1)
    crop_min = np.min(yields_by_crop, axis=1)
    
    print("\nCrop Performance (averaged across days):")
    for i, crop in enumerate(crop_names):
        print(f"  {crop:10s}: Avg={crop_avg[i]:.1f}, Max={crop_max[i]:.1f}, Min={crop_min[i]:.1f}")
    
    print("\nStep 3: Calculate statistics by day")
    day_avg = np.mean(yields_by_crop, axis=0)  # Average across crops (axis=0)
    
    print("\nDaily Average Yield (across all crops):")
    for day in range(len(day_avg)):
        print(f"  Day {day+1}: {day_avg[day]:.1f} quintal/hectare")
    
    print("\nStep 4: Identify best-performing crop-day combination")
    max_yield_idx = np.unravel_index(np.argmax(yields_by_crop), yields_by_crop.shape)
    best_crop = crop_names[max_yield_idx[0]]
    best_day = max_yield_idx[1] + 1
    best_yield = yields_by_crop[max_yield_idx]
    
    print(f"Best Performance: {best_crop} on Day {best_day} with {best_yield:.1f} quintal/hectare")
    
    print("\nStep 5: Vectorized comparison with threshold")
    threshold = 20.0
    high_performing = yields_by_crop > threshold
    print(f"Days when each crop exceeded {threshold} quintal/hectare:")
    for i, crop in enumerate(crop_names):
        days = np.where(high_performing[i])[0] + 1
        print(f"  {crop:10s}: Days {days.tolist()}")


# ============================================================================
# PRACTICAL EXERCISE: Try Modifying This!
# ============================================================================

def exercise_template():
    """
    EXERCISE FOR STUDENTS:
    
    Try modifying the climate risk score calculation:
    
    1. Change the weights (currently 0.5, 0.3, 0.2):
       - What happens if you make rainfall weight 0.3?
       - What if soil moisture becomes more important (0.4)?
    
    2. Add more days of data:
       - Extend rainfall, temperature, soil_moisture arrays to 10 days
       - See how the average risk changes
    
    3. Add a new factor:
       - Include wind speed data
       - Calculate wind stress
       - Add it to the formula with weight 0.1
    
    4. Compare two locations:
       - Create separate arrays for Location A and Location B
       - Calculate risk for both
       - Which location is safer?
    
    5. Save results to file:
       - Export risk scores to a CSV file
       - Use NumPy's np.savetxt() or np.save()
    
    Bonus: Create a 2D array with risk scores for 5 different crops
           and find which crop is most resilient!
    """
    print("\n" + "="*70)
    print("EXERCISES FOR YOU TO TRY:")
    print("="*70)
    print(exercise_template.__doc__)


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "AGRISENSE: NumPy BASICS LEARNING GUIDE" + " " * 15 + "║")
    print("║" + " " * 10 + "Sections 4.22-4.24: Arrays, Shapes, Basic Math" + " " * 12 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Run all examples
    yields = example_1_basic_stats()
    actual_rf, normal_rf = example_2_rainfall_deviation()
    risk = example_3_climate_risk_score()
    example_4_multi_crop_analysis()
    exercise_template()
    
    # Final summary and next steps
    print("\n" + "="*70)
    print("LEARNING SUMMARY & NEXT STEPS")
    print("="*70)
    print("""
📚 What You Learned:
   ✓ Creating 1D and 2D NumPy arrays
   ✓ Understanding array shapes and properties
   ✓ Calculating statistics: mean, max, min, std
   ✓ Performing element-wise operations (add, subtract, divide)
   ✓ Using boolean indexing to filter data
   ✓ Vectorized operations vs loops
   ✓ Applying NumPy to real AgriSense problems

🚀 Next Steps:
   1. Modify the climate risk weights and see impact
   2. Add more days of weather data
   3. Try creating your own 2D array with crops × metrics
   4. Experiment with np.reshape(), np.flatten(), np.transpose()
   5. Learn about np.random for generating synthetic data
   6. Explore np.loadtxt() and np.savetxt() for file I/O

📝 Key NumPy Functions Used:
   - np.array()           Create arrays
   - np.shape / .shape    Get array dimensions
   - np.mean()            Calculate average
   - np.max() / np.min()  Find max and min values
   - np.std()             Calculate standard deviation
   - np.sum()             Sum all elements
   - np.abs()             Absolute value
   - Boolean masks        Filter data (array > value)
   - np.where()           Find indices matching condition
   - np.unravel_index()   Convert flat index to multi-dim coordinates

💡 Pro Tip:
   NumPy's vectorized operations (broadcast operations across entire arrays)
   are MUCH faster than loops in Python. As you work with larger datasets,
   using .mean(), .sum(), etc. instead of for loops will significantly
   improve performance!

🌾 AgriSense Insight:
   This climate risk score calculation is exactly what farmers need
   to make daily decisions: Should I irrigate? Is frost risk high?
   Can I apply pesticides? Your NumPy skills are directly applicable
   to solving real farming problems!
""")
    print("="*70)
    print("\n✓ Script completed successfully! Run this script again and")
    print("  try the exercises to deepen your understanding.\n")
