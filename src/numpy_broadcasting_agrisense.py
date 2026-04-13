"""
================================================================================
                        AGRISENSE: NUMPY BROADCASTING
              Learn How to Work with Different-Shaped Arrays Easily
================================================================================

NumPy Broadcasting is a powerful feature that allows you to perform operations
on arrays of different shapes WITHOUT writing loops. This is extremely useful
when working with agricultural data where you need to compare multiple fields
against a single expected value.

Key Learning Goals:
    1. Understand what broadcasting is and when it happens
    2. Learn to recognize compatible array shapes
    3. Perform calculations across multiple fields with different array shapes
    4. Calculate risk and deviation across all fields at once

Real-World Example:
    Comparing actual rainfall from 10 fields over 7 days against the normal
    rainfall for each day. You don't need to loop through each field!

Author: AgriSense Education Team
Version: 1.0
================================================================================
"""

import numpy as np


# ============================================================================
# SECTION 1: CREATE SAMPLE AGRICULTURAL DATA
# ============================================================================

def create_agrisense_arrays():
    """
    Create realistic agricultural data arrays with different shapes.
    This demonstrates the core issue that Broadcasting solves!
    
    Returns:
        Tuple containing:
        - actual_rainfall: 2D array of shape (10 fields, 7 days)
        - normal_rainfall: 1D array of shape (7 days,)
        - avg_temperature: 1D array of shape (7 days,)
        - field_ids: List of field names
    """
    
    # ---- ACTUAL RAINFALL DATA ----
    # 10 different fields, rainfall data for 7 consecutive days
    # Shape: (10, 7) - meaning 10 rows (fields) and 7 columns (days)
    actual_rainfall = np.array([
        [12.5, 14.2, 11.3, 15.8, 10.2, 13.5, 14.1],  # Field 1
        [11.8, 13.5, 10.9, 16.2, 9.8,  12.8, 13.9],   # Field 2
        [13.2, 15.1, 12.4, 17.5, 11.5, 14.2, 15.3],   # Field 3
        [10.5, 12.8, 9.7,  14.5, 8.2,  11.5, 12.4],   # Field 4
        [14.1, 16.2, 13.8, 18.9, 12.3, 15.5, 16.7],   # Field 5
        [11.2, 13.1, 10.2, 15.3, 9.5,  12.2, 13.1],   # Field 6
        [12.8, 14.9, 12.1, 16.8, 10.8, 13.9, 14.8],   # Field 7
        [10.9, 12.6, 9.9,  14.8, 9.0,  11.8, 12.7],   # Field 8
        [13.5, 15.4, 13.2, 18.1, 11.9, 14.8, 15.6],   # Field 9
        [12.1, 14.1, 11.8, 16.5, 10.4, 13.2, 14.0]    # Field 10
    ])
    
    # ---- NORMAL/EXPECTED RAINFALL ----
    # Expected rainfall for each day (based on historical data)
    # Shape: (7,) - only 7 days, no field dimension!
    # This is where Broadcasting becomes useful!
    normal_rainfall = np.array([12.0, 14.0, 11.0, 16.0, 10.0, 13.0, 14.0])
    
    # ---- AVERAGE TEMPERATURE DATA ----
    # Average temperature for each day across all fields
    # Shape: (7,) - only 7 days
    avg_temperature = np.array([22.5, 23.1, 24.2, 25.3, 26.1, 27.4, 28.2])
    
    # ---- NORMAL TEMPERATURE ----
    # "Ideal" temperature for this crop (example: wheat prefers ~25°C)
    normal_temp = 25.0
    
    # ---- FIELD IDENTIFIERS ----
    field_ids = [f"Field_{i+1}" for i in range(10)]
    
    return actual_rainfall, normal_rainfall, avg_temperature, normal_temp, field_ids


# ============================================================================
# SECTION 2: WHAT IS BROADCASTING? - EXPLANATION WITH EXAMPLES
# ============================================================================

def explain_broadcasting():
    """
    Print a clear explanation of what broadcasting is and why it matters.
    """
    explanation = """
╔════════════════════════════════════════════════════════════════════════════╗
║                         WHAT IS BROADCASTING?                             ║
╚════════════════════════════════════════════════════════════════════════════╝

PROBLEM WITHOUT BROADCASTING:
────────────────────────────
Imagine you have:
  • Actual rainfall: 10 fields × 7 days (shape: 10, 7)
  • Normal rainfall:         7 days    (shape: 7,)

The shapes DON'T match! So what do you do?

Option 1: Write a loop (SLOW ❌)
    for each field:
        for each day:
            deviation[field][day] = actual[field][day] - normal[day]

This is tedious and slow!

SOLUTION WITH BROADCASTING (FAST ✓):
─────────────────────────────────────
NumPy automatically "stretches" the smaller array to match the larger one:

    actual_rainfall (10, 7)  - 10 fields, 7 days
    normal_rainfall (7,)     - just 7 days
    
NumPy "broadcasts" normal_rainfall to match:
    
    actual_rainfall (10, 7):    [[12.5, 14.2, 11.3, ...],
                                 [11.8, 13.5, 10.9, ...],
                                 ...]
    
    normal_rainfall (10, 7):    [[12.0, 14.0, 11.0, ...],  ← stretched!
                                 [12.0, 14.0, 11.0, ...],  ← same for all fields
                                 ...]
    
Then it does the subtraction:
    
    deviation = actual_rainfall - normal_rainfall
    
Result: Each field gets compared against the same normal rainfall values!

WHY BROADCASTING IS FAST:
─────────────────────────
✓ No loops - calculation happens on entire arrays at once
✓ Uses optimized C code under the hood
✓ Memory efficient - doesn't actually copy the array
✓ Clean, readable code: just write `larger_array - smaller_array`

BROADCASTING RULES:
──────────────────
NumPy compares shapes from RIGHT to LEFT:

Example 1 (WORKS ✓):
    Shape 1: (10, 7)  → 10 rows, 7 columns
    Shape 2: (7,)     → 7 elements
    Result:  (10, 7)  → Broadcasts (7,) to (1, 7) then to (10, 7)

Example 2 (WORKS ✓):
    Shape 1: (10, 7)  → 10 rows, 7 columns
    Shape 2: ()       → scalar (single number)
    Result:  (10, 7)  → Broadcasts scalar to all 70 elements

Example 3 (FAILS ❌):
    Shape 1: (10, 7)  → 10 rows, 7 columns
    Shape 2: (5,)     → 5 elements (INCOMPATIBLE!)
    Error!  Cannot broadcast

The rule: Dimensions must be EQUAL or one of them must be 1 (or missing)
"""
    print(explanation)


# ============================================================================
# SECTION 3: RAINFALL DEVIATION WITH BROADCASTING
# ============================================================================

def rainfall_deviation_without_broadcast(actual, normal, field_ids):
    """
    SLOW METHOD: Calculate rainfall deviation using a loop.
    This is what we'd do WITHOUT broadcasting.
    
    Args:
        actual: 2D array of actual rainfall (fields × days)
        normal: 1D array of normal rainfall (days only)
        field_ids: List of field names
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: RAINFALL DEVIATION (WITHOUT BROADCASTING - USING LOOP)")
    print("="*80)
    
    print(f"\nArray Shapes:")
    print(f"  actual_rainfall shape: {actual.shape}  (10 fields, 7 days)")
    print(f"  normal_rainfall shape: {normal.shape}  (7 days only)")
    
    # Manual loop approach
    deviation = np.zeros((actual.shape[0], actual.shape[1]))
    
    for field_idx in range(len(field_ids)):
        for day_idx in range(len(normal)):
            # Compare each field's rainfall against normal for that day
            deviation[field_idx, day_idx] = actual[field_idx, day_idx] - normal[day_idx]
    
    print(f"\nUsing Explicit Loop:")
    print(f"  for each field (10 times)")
    print(f"    for each day (7 times)")
    print(f"      deviation = actual_field - normal_day")
    print(f"\nTotal loop iterations: {len(field_ids)} × {len(normal)} = {len(field_ids) * len(normal)}")
    
    # Display some results
    print(f"\nExample Results (first 3 fields, all 7 days):")
    print(f"{'Field':<10} {'Day1':<8} {'Day2':<8} {'Day3':<8} {'Day4':<8} {'Day5':<8} {'Day6':<8} {'Day7':<8}")
    print("-" * 70)
    for i in range(3):
        print(f"{field_ids[i]:<10}", end="")
        for j in range(7):
            print(f"{deviation[i, j]:+6.1f}  ", end="")
        print()
    
    return deviation


def rainfall_deviation_with_broadcast(actual, normal, field_ids):
    """
    FAST METHOD: Calculate rainfall deviation using NumPy Broadcasting.
    This is the modern, efficient way!
    
    Args:
        actual: 2D array of actual rainfall (fields × days)
        normal: 1D array of normal rainfall (days only)
        field_ids: List of field names
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: RAINFALL DEVIATION (WITH BROADCASTING - FASTER)")
    print("="*80)
    
    print(f"\nArray Shapes:")
    print(f"  actual_rainfall shape: {actual.shape}  (10 fields, 7 days)")
    print(f"  normal_rainfall shape: {normal.shape}  (7 days only)")
    
    print(f"\nHow Broadcasting Works:")
    print(f"  Step 1: Recognize shape mismatch - (10, 7) vs (7,)")
    print(f"  Step 2: Align shapes from right (compare rightmost dimensions)")
    print(f"  Step 3: NumPy stretches (7,) to (1, 7) then broadcasts to (10, 7)")
    print(f"  Step 4: Perform subtraction on entire arrays - NO LOOP NEEDED!")
    
    # Single vectorized operation - this is the power of broadcasting!
    deviation = actual - normal
    
    print(f"\nThe Code:")
    print(f"  deviation = actual_rainfall - normal_rainfall")
    print(f"  # That's it! No loops needed!")
    
    # Display some results
    print(f"\nExample Results (same as loop method, but computed in one line):")
    print(f"{'Field':<10} {'Day1':<8} {'Day2':<8} {'Day3':<8} {'Day4':<8} {'Day5':<8} {'Day6':<8} {'Day7':<8}")
    print("-" * 70)
    for i in range(3):
        print(f"{field_ids[i]:<10}", end="")
        for j in range(7):
            print(f"{deviation[i, j]:+6.1f}  ", end="")
        print()
    
    # Interpret the results
    print(f"\nInterpretation of Results:")
    print(f"  Positive value = More rain than normal (wet day)")
    print(f"  Negative value = Less rain than normal (dry day)")
    
    # Show a specific example
    field_3 = 2  # 0-indexed, so field 3 is index 2
    day_5 = 4    # 0-indexed, so day 5 is index 4
    dev_value = deviation[field_3, day_5]
    
    print(f"\nSpecific Example:")
    print(f"  Field 3, Day 5:")
    print(f"    Actual rainfall: {actual[field_3, day_5]:.1f} mm")
    print(f"    Normal rainfall: {normal[day_5]:.1f} mm")
    print(f"    Deviation:      {dev_value:+.1f} mm", end="")
    
    if dev_value < 0:
        print(f" (Drier than normal)")
    elif dev_value > 0:
        print(f" (Wetter than normal)")
    else:
        print(f" (Exactly normal)")
    
    return deviation


# ============================================================================
# SECTION 4: HEAT STRESS WITH SCALAR BROADCASTING
# ============================================================================

def heat_stress_calculation(avg_temp, normal_temp, field_ids):
    """
    Calculate heat stress: deviation from normal temperature.
    
    This demonstrates broadcasting with a SCALAR (single number).
    Even simpler than the rainfall example!
    
    Args:
        avg_temp: 1D array of temperature for 7 days
        normal_temp: Single float value (ideal temperature)
        field_ids: List of field names
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: HEAT STRESS (SCALAR BROADCASTING)")
    print("="*80)
    
    print(f"\nArray Shapes:")
    print(f"  avg_temperature shape: {avg_temp.shape}  (7 days)")
    print(f"  normal_temp:           scalar             (just one number: {normal_temp})")
    
    print(f"\nHow Broadcasting Works:")
    print(f"  Step 1: Compare shapes - (7,) vs scalar")
    print(f"  Step 2: Scalar broadcasts to (7,) - no explicit stretching needed")
    print(f"  Step 3: Perform subtraction")
    
    # Broadcasting with a scalar is the simplest case!
    heat_stress = avg_temp - normal_temp
    
    print(f"\nThe Code:")
    print(f"  heat_stress = avg_temperature - normal_temp")
    print(f"  # NumPy automatically broadcasts {normal_temp} to all 7 elements")
    
    print(f"\nResults:")
    print(f"{'Day':<6} {'Temperature':<15} {'Normal':<10} {'Heat Stress':<15}")
    print("-" * 50)
    for day in range(len(avg_temp)):
        stress = heat_stress[day]
        print(f"Day {day+1:<2} {avg_temp[day]:<15.1f} {normal_temp:<10.1f}", end="")
        if stress > 0:
            print(f"{stress:+7.1f}°C  (TOO HOT)")
        elif stress < 0:
            print(f"{stress:+7.1f}°C  (TOO COLD)")
        else:
            print(f"{stress:+7.1f}°C  (PERFECT)")
    
    return heat_stress


# ============================================================================
# SECTION 5: ADVANCED BROADCASTING - CLIMATE RISK
# ============================================================================

def climate_risk_with_broadcasting(actual_rainfall, normal_rainfall, 
                                    avg_temperature, normal_temp):
    """
    Calculate climate risk using multiple broadcasting operations.
    This shows how powerful broadcasting becomes when combining multiple
    calculations!
    
    Climate Risk = 0.6 * rainfall_deviation + 0.4 * temperature_deviation
    
    Args:
        actual_rainfall: 2D array of actual rainfall (fields × days)
        normal_rainfall: 1D array of normal rainfall (days)
        avg_temperature: 1D array of temperature (days)
        normal_temp: Float value of ideal temperature
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: CLIMATE RISK (COMBINING MULTIPLE BROADCASTS)")
    print("="*80)
    
    print(f"\nArray Shapes:")
    print(f"  actual_rainfall:   {actual_rainfall.shape}  (10 fields, 7 days)")
    print(f"  normal_rainfall:   {normal_rainfall.shape}  (7 days)")
    print(f"  avg_temperature:   {avg_temperature.shape}  (7 days)")
    print(f"  normal_temp:       scalar  (single value)")
    
    print(f"\nFormula:")
    print(f"  climate_risk = 0.6 * (actual_rainfall - normal_rainfall)")
    print(f"               + 0.4 * (avg_temperature - normal_temp)")
    
    # Step 1: Calculate rainfall deviation with broadcasting (10, 7) - (7,)
    rainfall_dev = actual_rainfall - normal_rainfall
    print(f"\nStep 1: Rainfall Deviation")
    print(f"  actual_rainfall (10, 7) - normal_rainfall (7,)")
    print(f"  Result shape: {rainfall_dev.shape}  (10 fields, 7 days)")
    
    # Step 2: Calculate temperature deviation with broadcasting (7,) - scalar
    temp_dev = avg_temperature - normal_temp
    print(f"\nStep 2: Temperature Deviation")
    print(f"  avg_temperature (7,) - normal_temp (scalar)")
    print(f"  Result shape: {temp_dev.shape}  (7 days)")
    
    # Step 3: Combine with another broadcast! (10, 7) with (7,)
    # When we multiply temp_dev by a coefficient and add to rainfall_dev,
    # NumPy broadcasts temp_dev (7,) to match rainfall_dev (10, 7)
    climate_risk = 0.6 * rainfall_dev + 0.4 * temp_dev
    print(f"\nStep 3: Combine Components (Another Broadcast!)")
    print(f"  0.6 * rainfall_dev (10, 7) + 0.4 * temp_dev (7,)")
    print(f"  temp_dev (7,) broadcasts to (10, 7) automatically")
    print(f"  Result shape: {climate_risk.shape}  (10 fields, 7 days)")
    
    # Normalize the risk to 0-100 scale for interpretation
    # Using broadcasting again: subtract min from all, divide by range
    min_risk = climate_risk.min()
    max_risk = climate_risk.max()
    normalized_risk = 100 * (climate_risk - min_risk) / (max_risk - min_risk)
    
    print(f"\nNormalized Risk (0-100 scale):")
    print(f"{'Field':<10} {'Day1':<8} {'Day2':<8} {'Day3':<8} {'Day4':<8}")
    print("-" * 45)
    for field in range(min(3, actual_rainfall.shape[0])):
        print(f"Field_{field+1:<4}", end=" ")
        for day in range(4):
            risk_val = normalized_risk[field, day]
            print(f"{risk_val:5.0f}  ", end="")
        print()
    
    return climate_risk, normalized_risk


# ============================================================================
# SECTION 6: COMPARISON AND SUMMARY
# ============================================================================

def print_broadcasting_summary():
    """
    Print a summary of when to use broadcasting and when to avoid it.
    """
    summary = """
╔════════════════════════════════════════════════════════════════════════════╗
║                      BROADCASTING SUMMARY & BEST PRACTICES                 ║
╚════════════════════════════════════════════════════════════════════════════╝

WHEN TO USE BROADCASTING (✓ RECOMMENDED):
──────────────────────────────────────────

1. COMPARING MULTIPLE FIELDS TO SINGLE NORMAL VALUE:
   ✓ Compare 10 fields' rainfall against 1 normal rainfall for each day
   ✓ Compare all fields' temperature against optimal temperature
   ✓ Calculate deviation for all fields at once

2. NORMALIZING DATA ACROSS ARRAYS:
   ✓ Subtract mean from all values: data - data.mean()
   ✓ Divide by standard deviation: data / data.std()
   ✓ Scale multiple arrays together

3. COMBINING METRICS WITH DIFFERENT DIMENSIONS:
   ✓ weight_1 * metric_1 (10, 7) + weight_2 * metric_2 (7,)
   ✓ Automatically broadcasts without explicit loops

4. COMPUTING STATISTICS ACROSS DIMENSION:
   ✓ Subtract each row's mean: arr - arr.mean(axis=1, keepdims=True)
   ✓ Normalize each column: arr / arr.max(axis=0)


WHEN TO AVOID BROADCASTING (✗ DON'T USE):
──────────────────────────────────────────

1. INCOMPATIBLE SHAPES:
   ✗ (10, 5) cannot broadcast with (3,)  → Will cause ERROR
   ✗ Check shapes carefully before relying on broadcasting

2. CONFUSING CODE:
   ✗ If broadcasting isn't obvious, use .reshape() to make shapes explicit
   ✗ Code clarity matters more than cleverness!

3. SEQUENTIAL DEPENDENCIES:
   ✗ If result[i] depends on result[i-1], use loops (can't broadcast)
   ✗ Broadcasting works only for element-wise operations


PRACTICAL TIPS FOR MVP FEATURES:
────────────────────────────────

For Climate Risk Advisor:
  ✓ Use broadcasting to calculate risk for all fields at once
  ✓ Subtract normal_temp from all fields' temperatures with one operation
  ✓ Multiply risk scores by weights without looping

For Yield Prediction:
  ✓ Compare yields from multiple fields against average
  ✓ Broadcast weights across crop groups
  ✓ Calculate percentile positions with fewer operations

For Market Prices:
  ✓ Subtract average price from all prices: prices - prices.mean()
  ✓ Calculate price deviation for all crops: prices - normal_prices

For Rainfall Analysis:
  ✓ Create rainfall deviation for all fields: rainfall - normal_rainfall
  ✓ Calculate moving averages with broadcasting
  ✓ Classify risk levels for all data at once


MEMORY EFFICIENCY:
──────────────────
One of the best things about broadcasting is that NumPy doesn't actually
duplicate the data. The smaller array isn't copied - NumPy smartly reuses it:

  Without broadcasting (inefficient):
    normal = [12.0, 14.0, 11.0, ...]  (original)
    normal = [[12.0, 14.0, 11.0, ...],  ← copied to 10 rows!
              [12.0, 14.0, 11.0, ...],   (wastes memory)
              ...
              [12.0, 14.0, 11.0, ...]]

  With broadcasting (efficient):
    normal = [12.0, 14.0, 11.0, ...]  ← reused for all rows
    (No copy made - NumPy handles it internally!)


DEBUGGING BROADCASTING ERRORS:
──────────────────────────────
If you get "ValueError: operands could not be broadcast together":

1. Print the shapes: print(arr1.shape, arr2.shape)
2. Align them right-to-left in your mind
3. Check if rightmost dimensions are equal or one is 1
4. Use .reshape() to make dimensions explicit if unsure

Example:
    arr1.shape = (10, 7, 1)  ← has extra dimension
    arr2.shape = (7,)        ← missing dimensions

    Reshape to match: arr2.reshape(1, 7, 1) or arr1.reshape(10, 7)

"""
    print(summary)


# ============================================================================
# SECTION 7: STUDENT EXERCISE
# ============================================================================

def print_student_exercise():
    """
    Print suggested exercises for students to practice broadcasting.
    """
    exercise = """
╔════════════════════════════════════════════════════════════════════════════╗
║                              PRACTICE EXERCISE                             ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 CHALLENGE 1: Calculate Watering Needed
   Task: Fields need extra water if rainfall < 70% of normal
   
   Given:
     - actual_rainfall: (10, 7) array
     - normal_rainfall: (7,) array
   
   Calculate:
     - threshold = normal_rainfall * 0.7
     - water_needed = threshold - actual_rainfall (use broadcasting!)
     - Only include positive values (fields that need water)
   
   Hint: Use np.maximum(water_needed, 0) to set negatives to zero
   
   Question: How many fields need watering on Day 3?


🎯 CHALLENGE 2: Risk Classification Across Fields
   Task: Classify climate risk for all fields and days
   
   Given:
     - climate_risk: (10, 7) array with risk scores 0-100
   
   Classify:
     - "Low"    if risk < 30
     - "Medium" if 30 <= risk < 70
     - "High"   if risk >= 70
   
   Hint: Use np.where() with nested conditions (from earlier script)
      risk_class = np.where(risk < 30, "Low",
                           np.where(risk < 70, "Medium", "High"))
   
   Output: A (10, 7) array of strings


🎯 CHALLENGE 3: Relative Deviation
   Task: Calculate relative deviation as percentage
   
   Formula: relative_dev = (actual - normal) / normal * 100
   
   Try:
     1. Calculate for rainfall (broadcasting 2D with 1D)
     2. Calculate for temperature (broadcasting 1D with scalar)
     3. Print which field has highest relative deviation on Day 1
   
   Hint: Use np.argmax() to find index of maximum value


🎯 CHALLENGE 4: Multi-Field Average Rainfall
   Task: Calculate average rainfall for each day across all fields
   
   Code:
     avg_rainfall_per_day = actual_rainfall.mean(axis=0)
     
   Result should have shape (7,)
   
   Then broadcast it: days_vs_normal = avg_rainfall_per_day - normal_rainfall
   
   Question: On which days is average rainfall BELOW normal?


🎯 CHALLENGE 5 (Advanced): Field-Wise Risk Score
   Task: Calculate which field is "riskiest" overall
   
   Calculate:
     1. Rainfall risk per field: (actual - normal) for each field-day combo
     2. Temperature risk per day: (temp - normal) for all days
     3. Combine: risk = 0.6 * rainfall + 0.4 * temperature
     4. Find: Which field has HIGHEST average risk score?
   
   Hint: Use .mean(axis=1) to average across days for each field


⭐ BONUS CHALLENGE: Real-World Application
   Create a function that:
     1. Takes actual rainfall (10, 7) and actual temperature (7,)
     2. Calculates climate risk using broadcasting
     3. Returns a recommendation for each field:
        "WATER NOW", "MONITOR", "OK", "REDUCE WATER"
     
   Remember: Use broadcasting for all calculations - NO LOOPS!


📝 HOW TO CHECK YOUR WORK:
   1. Print the shape of your result
      print(result.shape)  # Should match expected shape
   
   2. Print example values
      print(result[0, :])  # First field, all days
   
   3. Compare with the sample calculations above
      # Your values should match or be similar
   
   4. Check for NaN or inf values
      print(np.isnan(result).sum())  # Should be 0
      print(np.isinf(result).sum())  # Should be 0

"""
    print(exercise)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    
    # Print header
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*18 + "AGRISENSE: NUMPY BROADCASTING TUTORIAL" + " "*22 + "║")
    print("║" + " "*14 + "Work with Different-Shaped Arrays Without Loops" + " "*16 + "║")
    print("╚" + "="*78 + "╝")
    
    # SECTION 1: Explanation
    explain_broadcasting()
    
    # SECTION 2: Get sample data
    actual_rainfall, normal_rainfall, avg_temperature, normal_temp, field_ids = \
        create_agrisense_arrays()
    
    # SECTION 3: Example 1 - Rainfall Deviation
    rainfall_deviation_without_broadcast(actual_rainfall, normal_rainfall, field_ids)
    rainfall_deviation_with_broadcast(actual_rainfall, normal_rainfall, field_ids)
    
    # SECTION 4: Example 2 - Heat Stress
    heat_stress_calculation(avg_temperature, normal_temp, field_ids)
    
    # SECTION 5: Example 3 - Climate Risk
    climate_risk, normalized_risk = climate_risk_with_broadcasting(
        actual_rainfall, normal_rainfall, avg_temperature, normal_temp
    )
    
    # SECTION 6: Summary and best practices
    print_broadcasting_summary()
    
    # SECTION 7: Student Exercise
    print_student_exercise()
    
    # Final message
    print("\n" + "="*80)
    print("HOW TO RUN THIS SCRIPT")
    print("="*80)
    print("""
1. Run it:
   python src/numpy_broadcasting_agrisense.py

2. Read through each section carefully - notice:
   - Array shapes and how they change
   - Why broadcasting is useful
   - How the code becomes simpler without loops

3. Modify and experiment:
   - Change the field count from 10 to 20
   - Add more days (extend arrays)
   - Add a third metric and combine with broadcasting
   - Try the practice exercises

4. Check your understanding:
   - Can you recognize situations where broadcasting applies?
   - Can you identify compatible array shapes?
   - Can you explain why broadcasting is faster than loops?

5. Apply to AgriSense:
   - Use broadcasting in Climate Risk calculations
   - Use broadcasting to compare fields against averages
   - Use broadcasting in Yield and Price analysis features

""")
    
    print("="*80)
    print("Made with ❤️ for AgriSense - Understanding NumPy Broadcasting")
    print("="*80 + "\n")
