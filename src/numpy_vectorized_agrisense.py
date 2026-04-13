"""
================================================================================
                    AGRISENSE: NUMPY VECTORIZED OPERATIONS
                 Learning Guide for Vectorized Agricultural Data
================================================================================

This script demonstrates how to replace slow Python loops with fast NumPy
vectorized operations using real AgriSense agricultural examples.

Key Learning Goals:
    1. Understand why vectorization is faster than loops
    2. Learn to work with rainfall, temperature, soil moisture, and crop data
    3. Calculate climate risk scores efficiently without loops
    4. Replace loops with NumPy operations in real agricultural workflows

Author: AgriSense Education Team
Version: 1.0
================================================================================
"""

import numpy as np
import time
from typing import Tuple, List


# ============================================================================
# SECTION 1: CREATE SAMPLE AGRICULTURAL DATA
# ============================================================================

def create_sample_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray, 
                                  np.ndarray, np.ndarray, np.ndarray]:
    """
    Create realistic sample agricultural data for demonstration.
    
    Returns:
        Tuple containing:
        - rainfall: Daily rainfall for 30 days (mm)
        - temperature: Daily temperature for 30 days (°C)
        - soil_moisture: Daily soil moisture for 30 days (%)
        - crop_yield: Yield from 20 fields (quintal/hectare)
        - modal_price: Daily prices for 5 crops over 30 days
        - field_names: Names of crop types for each field
    """
    # ---- WEATHER DATA ----
    # Rainfall for 30 days (mm)
    rainfall = np.array([10.5, 15.3, 8.2, 12.4, 18.1, 22.5, 14.3, 11.2, 
                        19.8, 9.5, 13.2, 16.4, 20.1, 11.5, 14.8, 17.2, 
                        12.3, 15.1, 18.9, 13.6, 16.7, 14.2, 19.3, 10.8, 
                        15.5, 13.4, 17.8, 12.1, 14.6, 16.3])
    
    # Temperature for 30 days (°C)
    temperature = np.array([22.5, 23.1, 24.2, 25.3, 26.1, 27.4, 28.2, 29.1, 
                           28.5, 27.2, 26.3, 25.1, 24.5, 23.8, 23.2, 22.9, 
                           24.1, 25.2, 26.4, 27.8, 28.3, 27.5, 26.2, 25.0, 
                           24.3, 23.6, 22.8, 23.4, 24.8, 25.9])
    
    # Soil moisture for 30 days (%)
    soil_moisture = np.array([45, 48, 50, 52, 55, 58, 56, 54, 52, 50, 48, 
                             46, 44, 42, 44, 46, 48, 50, 52, 54, 56, 55, 
                             52, 50, 48, 46, 44, 45, 47, 49])
    
    # ---- CROP YIELD DATA ----
    # Yield from 20 different fields (quintal/hectare)
    crop_yield = np.array([45.2, 48.7, 52.1, 41.3, 55.8, 39.2, 48.6, 51.2,
                          47.9, 53.5, 46.1, 50.4, 49.8, 44.2, 54.6, 42.3,
                          51.7, 48.3, 45.9, 52.4])
    
    # ---- CROP PRICE DATA ----
    # Modal prices for 5 crops: Wheat, Rice, Maize, Pulses, Cotton (in ₹/quintal)
    # Shape: 5 crops × 30 days
    modal_price = np.array([
        [2500, 2510, 2520, 2515, 2525, 2535, 2540, 2550, 2560, 2555, 2545, 
         2540, 2535, 2530, 2540, 2550, 2560, 2565, 2570, 2575, 2580, 2575, 
         2570, 2560, 2550, 2540, 2535, 2530, 2525, 2520],  # Wheat
        [3200, 3210, 3225, 3220, 3235, 3245, 3255, 3265, 3275, 3270, 3260, 
         3250, 3240, 3235, 3245, 3260, 3270, 3280, 3290, 3300, 3310, 3305, 
         3300, 3290, 3280, 3270, 3260, 3250, 3240, 3235],  # Rice
        [1800, 1810, 1820, 1815, 1825, 1835, 1845, 1850, 1860, 1855, 1845, 
         1835, 1825, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1885, 
         1880, 1870, 1860, 1850, 1840, 1835, 1825, 1820],  # Maize
        [4100, 4110, 4125, 4120, 4135, 4150, 4160, 4170, 4180, 4175, 4165, 
         4155, 4145, 4140, 4150, 4165, 4180, 4190, 4200, 4210, 4220, 4215, 
         4210, 4200, 4190, 4180, 4170, 4160, 4150, 4145],  # Pulses
        [5800, 5810, 5825, 5820, 5835, 5850, 5860, 5875, 5890, 5885, 5875, 
         5860, 5850, 5845, 5860, 5875, 5890, 5905, 5920, 5935, 5950, 5945, 
         5935, 5920, 5905, 5890, 5875, 5860, 5850, 5845]   # Cotton
    ], dtype=float)
    
    # Field names (crop types)
    field_names = ['Wheat', 'Rice', 'Maize', 'Pulses', 'Cotton', 'Wheat',
                   'Rice', 'Maize', 'Pulses', 'Cotton', 'Wheat', 'Rice',
                   'Maize', 'Pulses', 'Cotton', 'Wheat', 'Rice', 'Maize',
                   'Pulses', 'Cotton']
    
    return rainfall, temperature, soil_moisture, crop_yield, modal_price, field_names


# ============================================================================
# SECTION 2: RAINFALL DEVIATION ANALYSIS
# ============================================================================

def rainfall_deviation_slow(rainfall: np.ndarray, expected_rainfall: float) -> List[float]:
    """
    SLOW METHOD: Calculate rainfall deviation using a Python loop.
    
    Deviation = Actual Rainfall - Expected Rainfall
    
    Args:
        rainfall: Array of daily rainfall values
        expected_rainfall: Expected rainfall value
        
    Returns:
        List of deviation values
    """
    deviation = []
    for rain in rainfall:
        dev = rain - expected_rainfall
        deviation.append(dev)
    return deviation


def rainfall_deviation_vectorized(rainfall: np.ndarray, 
                                   expected_rainfall: float) -> np.ndarray:
    """
    FAST METHOD: Calculate rainfall deviation using NumPy vectorization.
    
    This subtracts a scalar from an entire array in one operation.
    NumPy automatically broadcasts the scalar to all elements.
    
    Args:
        rainfall: Array of daily rainfall values
        expected_rainfall: Expected rainfall value
        
    Returns:
        NumPy array of deviation values
    """
    # Single vectorized operation - operates on entire array at once
    return rainfall - expected_rainfall


def demo_rainfall_deviation():
    """Demonstrate the rainfall deviation comparison."""
    print("\n" + "="*80)
    print("EXAMPLE 1: RAINFALL DEVIATION CALCULATION")
    print("="*80)
    
    rainfall, _, _, _, _, _ = create_sample_data()
    expected_rainfall = 15.0  # Expected daily rainfall in mm
    
    # TIME THE SLOW METHOD
    start_time = time.time()
    for _ in range(10000):
        result_slow = rainfall_deviation_slow(rainfall, expected_rainfall)
    slow_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # TIME THE FAST METHOD
    start_time = time.time()
    for _ in range(10000):
        result_vectorized = rainfall_deviation_vectorized(rainfall, expected_rainfall)
    fast_time = (time.time() - start_time) * 1000
    
    # DISPLAY RESULTS
    print(f"\nExpected Rainfall: {expected_rainfall} mm")
    print(f"Days Analyzed: {len(rainfall)}")
    print(f"\nFirst 5 days comparison:")
    print(f"  Rainfall (mm):        {rainfall[:5]}")
    print(f"  Deviation (mm):       {result_vectorized[:5]}")
    print(f"\nInterpretation: Positive values = MORE rain than expected")
    print(f"                Negative values = LESS rain than expected")
    
    print(f"\n⏱️  TIMING COMPARISON (10,000 iterations):")
    print(f"   Loop Method:       {slow_time:.4f} ms")
    print(f"   Vectorized Method: {fast_time:.4f} ms")
    print(f"   Speedup Factor:    {slow_time/fast_time:.1f}x FASTER ⚡")


# ============================================================================
# SECTION 3: CROP PRICE PERCENTAGE CHANGE
# ============================================================================

def price_change_slow(prices: np.ndarray) -> List[float]:
    """
    SLOW METHOD: Calculate day-to-day price change percentage using a loop.
    
    Price Change % = ((New Price - Old Price) / Old Price) * 100
    
    Args:
        prices: 1D array of daily prices for a crop
        
    Returns:
        List of percentage changes
    """
    price_change_pct = []
    for i in range(1, len(prices)):
        change = ((prices[i] - prices[i-1]) / prices[i-1]) * 100
        price_change_pct.append(change)
    return price_change_pct


def price_change_vectorized(prices: np.ndarray) -> np.ndarray:
    """
    FAST METHOD: Calculate day-to-day price change using vectorized operations.
    
    This uses NumPy array slicing to compare consecutive days:
    - prices[1:] gets all prices except the first day
    - prices[:-1] gets all prices except the last day
    
    Args:
        prices: 1D array of daily prices for a crop
        
    Returns:
        NumPy array of percentage changes
    """
    # Vectorized calculation: gets changes for all days at once
    return ((prices[1:] - prices[:-1]) / prices[:-1]) * 100


def demo_price_change():
    """Demonstrate the price change percentage comparison."""
    print("\n" + "="*80)
    print("EXAMPLE 2: CROP PRICE PERCENTAGE CHANGE")
    print("="*80)
    
    _, _, _, _, modal_price, _ = create_sample_data()
    
    # Use Wheat prices (first crop)
    wheat_prices = modal_price[0, :]
    
    # TIME THE SLOW METHOD
    start_time = time.time()
    for _ in range(10000):
        result_slow = price_change_slow(wheat_prices)
    slow_time = (time.time() - start_time) * 1000
    
    # TIME THE FAST METHOD
    start_time = time.time()
    for _ in range(10000):
        result_vectorized = price_change_vectorized(wheat_prices)
    fast_time = (time.time() - start_time) * 1000
    
    # DISPLAY RESULTS
    print(f"\nCrop: Wheat")
    print(f"Days of Price Data: {len(wheat_prices)}")
    print(f"\nFirst 5 days:")
    print(f"  Day 1 Price (₹): {wheat_prices[0]}")
    print(f"  Day 2 Price (₹): {wheat_prices[1]} → Change: {result_vectorized[0]:+.2f}%")
    print(f"  Day 3 Price (₹): {wheat_prices[2]} → Change: {result_vectorized[1]:+.2f}%")
    print(f"  Day 4 Price (₹): {wheat_prices[3]} → Change: {result_vectorized[2]:+.2f}%")
    print(f"  Day 5 Price (₹): {wheat_prices[4]} → Change: {result_vectorized[3]:+.2f}%")
    
    print(f"\nPrice Statistics (₹/quintal):")
    print(f"   Highest Price: ₹{wheat_prices.max():.0f}")
    print(f"   Lowest Price:  ₹{wheat_prices.min():.0f}")
    print(f"   Avg Change:    {result_vectorized.mean():+.2f}%")
    
    print(f"\n⏱️  TIMING COMPARISON (10,000 iterations):")
    print(f"   Loop Method:       {slow_time:.4f} ms")
    print(f"   Vectorized Method: {fast_time:.4f} ms")
    print(f"   Speedup Factor:    {slow_time/fast_time:.1f}x FASTER ⚡")


# ============================================================================
# SECTION 4: CLIMATE RISK SCORE (MOST IMPORTANT EXAMPLE)
# ============================================================================

def calculate_climate_risk_slow(rainfall: np.ndarray, 
                               temperature: np.ndarray,
                               soil_moisture: np.ndarray,
                               normal_rainfall: float = 15.0) -> Tuple[List[float], List[str]]:
    """
    SLOW METHOD: Calculate climate risk score using a loop.
    
    Risk Score = (0.5 * (1 - rainfall / normal_rain)) +
                 (0.3 * (temperature - 25) / 15) +
                 (0.2 * (50 - soil_moisture) / 50)
    
    This formula combines three factors:
    - 50% weight on rainfall (lower rainfall = higher risk)
    - 30% weight on temperature (deviation from ideal 25°C = higher risk)
    - 20% weight on soil moisture (lower moisture = higher risk)
    
    Args:
        rainfall: Array of daily rainfall (mm)
        temperature: Array of daily temperature (°C)
        soil_moisture: Array of daily soil moisture (%)
        normal_rainfall: Expected daily rainfall (mm)
        
    Returns:
        Tuple of (risk scores list, risk levels list)
    """
    risk_scores = []
    risk_levels = []
    
    for i in range(len(rainfall)):
        # Calculate the weighted risk score for this day
        rainfall_factor = 0.5 * (1 - rainfall[i] / normal_rainfall)
        temp_factor = 0.3 * (temperature[i] - 25) / 15
        moisture_factor = 0.2 * (50 - soil_moisture[i]) / 50
        
        risk_score = rainfall_factor + temp_factor + moisture_factor
        risk_scores.append(risk_score)
        
        # Classify risk level based on score
        if risk_score < 0.35:
            risk_levels.append("Low")
        elif risk_score < 0.65:
            risk_levels.append("Medium")
        else:
            risk_levels.append("High")
    
    return risk_scores, risk_levels


def calculate_climate_risk_vectorized(rainfall: np.ndarray,
                                      temperature: np.ndarray,
                                      soil_moisture: np.ndarray,
                                      normal_rainfall: float = 15.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    FAST METHOD: Calculate climate risk score using NumPy vectorization.
    
    Instead of looping through each day, NumPy performs ALL calculations
    simultaneously on the entire array. This is the key advantage!
    
    Args:
        rainfall: Array of daily rainfall (mm)
        temperature: Array of daily temperature (°C)
        soil_moisture: Array of daily soil moisture (%)
        normal_rainfall: Expected daily rainfall (mm)
        
    Returns:
        Tuple of (risk scores array, risk levels array)
    """
    # VECTORIZED: All three factors calculated for ALL days at once
    rainfall_factor = 0.5 * (1 - rainfall / normal_rainfall)
    temp_factor = 0.3 * (temperature - 25) / 15
    moisture_factor = 0.2 * (50 - soil_moisture) / 50
    
    # VECTORIZED: Sum all components for all days at once
    risk_scores = rainfall_factor + temp_factor + moisture_factor
    
    # VECTORIZED: Classify all risk levels at once using np.where()
    # np.where() is a powerful function that applies conditions vectorized
    risk_levels = np.where(risk_scores < 0.35, "Low",
                          np.where(risk_scores < 0.65, "Medium", "High"))
    
    return risk_scores, risk_levels


def demo_climate_risk():
    """Demonstrate the climate risk score comparison."""
    print("\n" + "="*80)
    print("EXAMPLE 3: CLIMATE RISK SCORE CALCULATION (MOST IMPORTANT)")
    print("="*80)
    print("\nFormula: risk_score = (0.5 * rainfall_risk) +")
    print("                      (0.3 * temperature_risk) +")
    print("                      (0.2 * soil_moisture_risk)")
    
    rainfall, temperature, soil_moisture, _, _, _ = create_sample_data()
    normal_rainfall = 15.0
    
    # TIME THE SLOW METHOD
    start_time = time.time()
    for _ in range(1000):
        risk_slow, levels_slow = calculate_climate_risk_slow(
            rainfall, temperature, soil_moisture, normal_rainfall
        )
    slow_time = (time.time() - start_time) * 1000
    
    # TIME THE FAST METHOD
    start_time = time.time()
    for _ in range(1000):
        risk_vectorized, levels_vectorized = calculate_climate_risk_vectorized(
            rainfall, temperature, soil_moisture, normal_rainfall
        )
    fast_time = (time.time() - start_time) * 1000
    
    # DISPLAY RESULTS
    print(f"\nDays Analyzed: {len(rainfall)}")
    print(f"\nDetailed Risk Analysis for First 5 Days:")
    print(f"{'Day':<4} {'Rain':<6} {'Temp':<6} {'Moisture':<8} {'Risk Score':<12} {'Level':<8}")
    print("-" * 50)
    
    for i in range(5):
        print(f"{i+1:<4} {rainfall[i]:<6.1f} {temperature[i]:<6.1f} "
              f"{soil_moisture[i]:<8.0f} {risk_vectorized[i]:<12.3f} "
              f"{levels_vectorized[i]:<8}")
    
    # Summary statistics
    high_risk_days = np.sum(levels_vectorized == "High")
    medium_risk_days = np.sum(levels_vectorized == "Medium")
    low_risk_days = np.sum(levels_vectorized == "Low")
    
    print(f"\nRisk Summary for All 30 Days:")
    print(f"   Low Risk Days:    {low_risk_days} days ({low_risk_days/len(rainfall)*100:.1f}%)")
    print(f"   Medium Risk Days: {medium_risk_days} days ({medium_risk_days/len(rainfall)*100:.1f}%)")
    print(f"   High Risk Days:   {high_risk_days} days ({high_risk_days/len(rainfall)*100:.1f}%)")
    print(f"   Average Risk Score: {risk_vectorized.mean():.3f}")
    
    print(f"\n⏱️  TIMING COMPARISON (1,000 iterations):")
    print(f"   Loop Method:       {slow_time:.4f} ms")
    print(f"   Vectorized Method: {fast_time:.4f} ms")
    print(f"   Speedup Factor:    {slow_time/fast_time:.1f}x FASTER ⚡")


# ============================================================================
# SECTION 5: AVERAGE YIELD PER CROP GROUP
# ============================================================================

def average_yield_slow(crop_yield: np.ndarray, 
                       field_names: List[str],
                       crop_type: str) -> float:
    """
    SLOW METHOD: Calculate average yield for a crop type using a loop.
    
    Args:
        crop_yield: Array of yields from all fields
        field_names: List of crop type names for each field
        crop_type: The crop type to filter for
        
    Returns:
        Average yield for the specified crop type
    """
    total_yield = 0
    count = 0
    
    for i in range(len(field_names)):
        if field_names[i] == crop_type:
            total_yield += crop_yield[i]
            count += 1
    
    return total_yield / count if count > 0 else 0


def average_yield_vectorized(crop_yield: np.ndarray,
                             field_names: List[str],
                             crop_type: str) -> float:
    """
    FAST METHOD: Calculate average yield for a crop type using vectorization.
    
    NumPy's boolean indexing automatically creates a filter and selects
    matching elements without explicit loops.
    
    Args:
        crop_yield: Array of yields from all fields
        field_names: List of crop type names for each field
        crop_type: The crop type to filter for
        
    Returns:
        Average yield for the specified crop type
    """
    # Convert field_names to NumPy array for vectorized comparison
    field_names_array = np.array(field_names)
    
    # VECTORIZED: Create boolean mask where crop matches
    mask = field_names_array == crop_type
    
    # VECTORIZED: Use mask to select matching yields and calculate mean
    return crop_yield[mask].mean()


def demo_average_yield():
    """Demonstrate the average yield comparison."""
    print("\n" + "="*80)
    print("EXAMPLE 4: AVERAGE YIELD PER CROP GROUP")
    print("="*80)
    
    _, _, _, crop_yield, _, field_names = create_sample_data()
    
    # Get unique crop types
    unique_crops = list(set(field_names))
    
    # TIME THE SLOW METHOD
    start_time = time.time()
    for _ in range(10000):
        for crop in unique_crops:
            result_slow = average_yield_slow(crop_yield, field_names, crop)
    slow_time = (time.time() - start_time) * 1000
    
    # TIME THE FAST METHOD
    start_time = time.time()
    for _ in range(10000):
        for crop in unique_crops:
            result_vectorized = average_yield_vectorized(crop_yield, field_names, crop)
    fast_time = (time.time() - start_time) * 1000
    
    # DISPLAY RESULTS
    print(f"\nTotal Fields: {len(field_names)}")
    print(f"Crop Types: {', '.join(unique_crops)}")
    
    print(f"\nAverage Yield per Crop (quintal/hectare):")
    print(f"{'Crop':<12} {'Avg Yield':<15} {'Fields':<8}")
    print("-" * 35)
    
    for crop in sorted(unique_crops):
        avg = average_yield_vectorized(crop_yield, field_names, crop)
        count = sum(1 for name in field_names if name == crop)
        print(f"{crop:<12} {avg:<15.2f} {count:<8}")
    
    # Overall statistics
    print(f"\nOverall Yield Statistics:")
    print(f"   Highest Field: {crop_yield.max():.2f} quintal/hectare")
    print(f"   Lowest Field:  {crop_yield.min():.2f} quintal/hectare")
    print(f"   Average:       {crop_yield.mean():.2f} quintal/hectare")
    print(f"   Std Dev:       {crop_yield.std():.2f} quintal/hectare")
    
    print(f"\n⏱️  TIMING COMPARISON (10,000 iterations, all crops):")
    print(f"   Loop Method:       {slow_time:.4f} ms")
    print(f"   Vectorized Method: {fast_time:.4f} ms")
    print(f"   Speedup Factor:    {slow_time/fast_time:.1f}x FASTER ⚡")


# ============================================================================
# SECTION 6: KEY TEACHING POINTS
# ============================================================================

def print_teaching_guide():
    """Print key learning points about vectorization."""
    print("\n" + "="*80)
    print("KEY TEACHING POINTS: WHY VECTORIZATION IS FASTER")
    print("="*80)
    
    guide = """
1. THE PROBLEM WITH LOOPS:
   ✗ Python loops iterate one element at a time
   ✗ Each iteration has overhead (function call, memory access)
   ✗ With 1000 weather days, you do 1000 separate operations
   
2. THE SOLUTION - VECTORIZATION:
   ✓ NumPy operates on ENTIRE ARRAYS at once
   ✓ Uses optimized C code under the hood
   ✓ All 1000 calculations happen simultaneously
   ✓ Minimal overhead regardless of array size

3. VECTORIZATION TECHNIQUES SHOWN:
   
   a) Direct Arithmetic Operations:
      Slow:  [element - value for element in array]
      Fast:  array - value  (broadcasts to all elements)
   
   b) Element-wise Operations:
      Slow:  [math.sqrt(x) for x in array]
      Fast:  np.sqrt(array)  (applies to entire array)
   
   c) Array Slicing:
      Slow:  [array[i] - array[i-1] for i in range(1, len(array))]
      Fast:  array[1:] - array[:-1]  (vectorized comparison)
   
   d) Boolean Indexing & np.where():
      Slow:  [value for i, value in enumerate(array) if condition[i]]
      Fast:  array[condition_mask]  (filter in one operation)
      
      np.where() for classification:
      Slow:  [classify(score) for score in scores]
      Fast:  np.where(scores < 0.35, "Low", "High")

4. PRACTICAL SPEEDUP FACTORS:
   - Small arrays (30 elements):  3-5x faster
   - Medium arrays (1000s):        10-20x faster
   - Large arrays (millions):      100-1000x faster
   
5. WHEN TO USE VECTORIZATION:
   ✓ Working with weather data (rainfall, temperature)
   ✓ Processing yield data from multiple fields
   ✓ Price calculations across days/crops
   ✓ Risk scoring and classification
   ✗ NOT suitable when each iteration depends on previous results

6. COMMON VECTORIZATION PATTERNS IN AGRISENSE:
   
   Pattern 1 - Normalization:
      (values - min_val) / (max_val - min_val)
      
   Pattern 2 - Weighted Sum:
      (0.5 * factor1) + (0.3 * factor2) + (0.2 * factor3)
      
   Pattern 3 - Condition Classification:
      np.where(condition, value_if_true, value_if_false)
      
   Pattern 4 - Filtering & Aggregation:
      filtered = data[condition_mask]
      result = filtered.sum() / filtered.mean()

7. DEBUGGING VECTORIZED CODE:
   - Use print() to check shapes: print(array.shape)
   - Test with small data first
   - Compare loop vs vectorized results to verify correctness
   - Use np.allclose() to compare float results with tolerance
"""
    print(guide)


# ============================================================================
# SECTION 7: EXPERIMENTATION GUIDE
# ============================================================================

def print_experimentation_guide():
    """Print suggestions for students to experiment with the code."""
    print("\n" + "="*80)
    print("EXPERIMENTATION GUIDE: WHAT YOU CAN TRY")
    print("="*80)
    
    experiments = """
🔬 EXPERIMENT 1: Change Risk Score Weights
   Location: calculate_climate_risk_vectorized() function
   Try: Change the weights (0.5, 0.3, 0.2) to prioritize different factors
   Example: rainfall_factor = 0.7 * (1 - rainfall / normal_rainfall)
   Observe: How do risk classifications change?

🔬 EXPERIMENT 2: Add More Crops
   Location: create_sample_data() function
   Try: Add a 6th crop to the modal_price array
   Observe: Does the code still work? (It should - that's the beauty of vectors!)

🔬 EXPERIMENT 3: Extend Time Period
   Location: create_sample_data() function
   Try: Change 30 days to 365 days of weather data
   Observe: What is the new speedup factor for loops vs vectors?

🔬 EXPERIMENT 4: Calculate Additional Metrics
   Try vectorizing these calculations:
   a) 7-day moving average rainfall: np.convolve(rainfall, np.ones(7)/7)
   b) Standard deviation of prices per crop: np.std(modal_price, axis=1)
   c) Days above temperature threshold: np.sum(temperature > 28)

🔬 EXPERIMENT 5: Add More Risk Factors
   Try adding a 4th factor to climate risk (e.g., humidity, wind speed)
   Example:
   humidity_factor = 0.1 * ((humidity - 60) / 40)
   risk_scores = ... + humidity_factor

🔬 EXPERIMENT 6: Create Your Own Comparison
   Try: Write a slow loop version for a calculation NOT shown here
   Then: Write a vectorized version
   Compare: Timing and correctness

🔬 EXPERIMENT 7: Explore NumPy Functions
   Try these NumPy functions on the sample data:
   - np.max(), np.min(), np.mean(), np.median()
   - np.percentile(data, 75)  # 75th percentile
   - np.argmax(), np.argmin()  # Index of max/min
   - np.unique()  # Unique values
   - np.sort()  # Sorted values

🔬 EXPERIMENT 8: Measure Impact with Larger Data
   Try: Create arrays with 10,000+ elements
   Run timing comparisons again
   Observe: The speedup factor grows exponentially!

💡 CHALLENGE: Real-World Application
   Can you combine multiple calculations into a single function that:
   1. Calculates climate risk scores
   2. Calculates price changes
   3. Calculates rainfall deviation
   4. Returns a single "farm recommendation" based on all factors?
"""
    print(experiments)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Print header
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "AGRISENSE: NUMPY VECTORIZATION TUTORIAL" + " "*20 + "║")
    print("║" + " "*15 + "Learn Fast Data Processing for Agricultural AI" + " "*18 + "║")
    print("╚" + "="*78 + "╝")
    
    # Run all demonstrations
    demo_rainfall_deviation()
    demo_price_change()
    demo_climate_risk()
    demo_average_yield()
    
    # Print teaching material
    print_teaching_guide()
    print_experimentation_guide()
    
    # Print final instructions
    print("\n" + "="*80)
    print("HOW TO USE THIS SCRIPT")
    print("="*80)
    
    instructions = """
1. RUN THE SCRIPT:
   python src/numpy_vectorized_agrisense.py
   
2. OBSERVE THE OUTPUT:
   - Each example shows the slow loop version
   - Each example shows the fast vectorized version
   - Timing comparisons show the speedup factor
   
3. UNDERSTAND THE PATTERNS:
   - Read the comments explaining each function
   - Note how vectorized code is shorter and clearer
   - See how np.where() replaces if/else chains
   
4. MODIFY AND EXPERIMENT:
   - Change risk score weights
   - Add new crops
   - Extend the time period
   - Create your own vectorized calculations
   
5. APPLY TO AGRISENSE FEATURES:
   - Climate Risk Advisor: Use climate_risk_vectorized()
   - Market Prices: Use price_change_vectorized()
   - Yield Prediction: Use vectorized aggregations
   - Rainfall Analysis: Use rainfall_deviation_vectorized()

6. NEXT STEPS:
   - Try the experiments listed above
   - Look for loops in existing code - can you vectorize them?
   - Use NumPy functions: np.sum, np.mean, np.std, np.var
   - Combine multiple vectorized operations in sequence
   - Consider using pandas for even more powerful data operations

❓ COMMON QUESTIONS:
   Q: Why is vectorization faster?
   A: NumPy uses optimized C code. Loops use slow Python interpretation.
   
   Q: Should I ALWAYS vectorize?
   A: Yes, when working with arrays. Loops are rarely needed in NumPy code.
   
   Q: Can I mix loops and vectors?
   A: Yes, but try to minimize loops - they defeat the purpose!
   
   Q: What if I can't vectorize something?
   A: Use NumPy functions (sum, mean, where, etc.) or pandas instead.
   
   Q: How do I debug vectorized code?
   A: Print shapes, test with small data, compare against loop versions.
"""
    print(instructions)
    
    print("\n" + "="*80)
    print("Made with ❤️ for AgriSense - Teaching NumPy to Future Farmers")
    print("="*80 + "\n")
