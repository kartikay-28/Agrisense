"""
NumPy Basics Quick Start Guide
==============================

File: src/numpy_basics_agrisense.py
Sections: 4.22-4.24 (Arrays, Shapes, Basic Math Operations)
Difficulty: Beginner
Time: 15-20 minutes to complete + 20 minutes to experiment
"""

# ============================================================================
# HOW TO RUN THE SCRIPT
# ============================================================================

# From the agrisense folder:
python src/numpy_basics_agrisense.py

# Or from any directory (with full path):
python "d:\D files\AgriSense\S84-0426-AKM-Python-Pandas-NumPy-AgriSense\agrisense\src\numpy_basics_agrisense.py"


# ============================================================================
# WHAT EACH EXAMPLE TEACHES
# ============================================================================

EXAMPLE 1: BASIC STATISTICS - CROP YIELDS
──────────────────────────────────────────
📌 Concepts Covered:
   - Creating 1D NumPy arrays with np.array()
   - Understanding array shape: (10,) means 10 elements
   - Basic statistics: mean(), max(), min(), std()
   - Element-wise operations: subtraction for price change
   - Using np.argmax() and np.argmin() to find indices

🌾 Real AgriSense Problem:
   Farmer has yield data from 10 fields. Which field has highest yield?
   By how much did prices change between market periods?

Key Output:
   ✓ Average yield across fields
   ✓ Which field performed best/worst
   ✓ Price change percentage for each market
   ✓ Overall yield consistency (std deviation)

Try This:
   Change the yields array and re-run to see updated statistics


EXAMPLE 2: RAINFALL DEVIATION ANALYSIS
───────────────────────────────────────
📌 Concepts Covered:
   - Create two arrays with same shape for comparison
   - Element-wise subtraction to find deviation
   - Conditional statements in a loop (if-elif-else)
   - Boolean masks: rainfall_deviation < -5
   - np.sum() to count matching elements
   - Combining conditions: (~drought & ~flood)

🌾 Real AgriSense Problem:
   Last week's rainfall was different from normal. Was it drought, flood, or normal?
   Which days were unusual?

Key Output:
   ✓ Daily rainfall deviation from normal
   ✓ Classification for each day (Drought/Normal/Flood)
   ✓ Count of each type with vectorized method (faster!)
   ✓ Summary: Was overall period wetter/drier/normal?

Try This:
   - Modify the threshold values (-5 and +5)
   - Add more days of data
   - Change the normal rainfall value


EXAMPLE 3: CLIMATE RISK SCORE (MAIN EXAMPLE)
──────────────────────────────────────────────
📌 Concepts Covered:
   - Create 3 separate arrays for different metrics
   - Normalize/scale each factor to 0-1 range
   - Weighted formula combining multiple factors
   - Convert scores to risk categories
   - Printing formatted output with emojis

🌾 Real AgriSense Problem:
   Today's weather has three factors: rainfall, temperature, soil moisture.
   Each affects crop differently. How much TOTAL risk?
   Should farmer irrigate, use shade cloth, or spray fungicide?

Key Output:
   ✓ Stress component for each factor (0-1 scale)
   ✓ Weighted risk score for each day
   ✓ Risk category (Low/Medium/High) with emoji
   ✓ Specific recommendations based on risk
   ✓ Summary: Overall 5-day forecast

Formula Used:
   risk_score = (0.5 × rainfall_dev) + (0.3 × temp_stress) + (0.2 × soil_dry)

Weights Explained:
   - Rainfall: 0.5 weight (most important for most crops)
   - Temperature: 0.3 weight (significant if extreme)
   - Soil Moisture: 0.2 weight (secondary factor)

Try This (IMPORTANT EXERCISE):
   1. Change weights: Try rainfall=0.3, temperature=0.5, soil=0.2
      → What happens to overall risk?
   
   2. Add more days: Extend arrays to 10 days with your own data
      → Does average risk increase or decrease?
   
   3. Add wind speed: Create wind_speed array, calculate wind_stress,
      add to formula with 0.1 weight, reduce others to sum to 1.0


EXAMPLE 4: MULTI-CROP 2D ARRAY ANALYSIS (BONUS)
────────────────────────────────────────────────
📌 Concepts Covered:
   - Create 2D arrays: rows = crops, columns = days
   - Understanding multi-dimensional shapes: (4, 5)
   - Using axis parameter: axis=0 (down) vs axis=1 (across)
   - np.unravel_index() to find position of maximum value

🌾 Real AgriSense Problem:
   Compare 4 different crops over 5 days. Which crop is most resilient?
   Which day had best conditions for all crops?

Key Output:
   ✓ 2D array structure and shape
   ✓ Average yield per crop (across all days)
   ✓ Average yield per day (across all crops)
   ✓ Best crop-day combination
   ✓ Performance rankings

Try This:
   - Add a 5th crop (Potato or Cotton)
   - Change the 2D array shape to 6 crops × 10 days
   - Calculate yield volatility (std dev) for each crop


# ============================================================================
# KEY NumPy FUNCTIONS REFERENCE
# ============================================================================

1. CREATING ARRAYS
   ─────────────────
   np.array([1, 2, 3])           → [1 2 3]
   np.zeros(5)                   → [0. 0. 0. 0. 0.]
   np.ones(5)                    → [1. 1. 1. 1. 1.]
   np.arange(0, 10, 2)           → [0 2 4 6 8]
   np.linspace(0, 10, 5)         → [ 0.   2.5  5.   7.5 10. ]


2. PROPERTIES
   ───────────
   array.shape                   → Dimensions: (10,) or (4, 5)
   array.dtype                   → Data type: int64, float64, etc
   array.size                    → Total elements
   array.ndim                    → Number of dimensions


3. STATISTICS (returns single value)
   ──────────────────────────────────
   np.mean(array)                → Average
   np.median(array)              → Middle value
   np.std(array)                 → Standard deviation
   np.var(array)                 → Variance
   np.min(array)                 → Minimum value
   np.max(array)                 → Maximum value
   np.sum(array)                 → Total sum
   np.argmin(array)              → Index of minimum
   np.argmax(array)              → Index of maximum


4. ELEMENT-WISE OPERATIONS (works on each element)
   ────────────────────────────────────────────────
   array1 + array2               → Element-wise addition
   array1 - array2               → Element-wise subtraction
   array1 * array2               → Element-wise multiplication
   array1 / array2               → Element-wise division
   np.abs(array)                 → Absolute values
   np.sqrt(array)                → Square roots


5. BOOLEAN INDEXING (filtering)
   ─────────────────────────────
   array > 20                    → Boolean mask [True, False, ...]
   array[array > 20]             → Values greater than 20
   np.sum(array > 20)            → Count of values > 20
   np.where(array > 20)          → Indices where condition true
   (array > 10) & (array < 20)   → Multiple conditions


6. FOR 2D ARRAYS
   ────────────────
   array.shape                   → (rows, cols)
   np.mean(array, axis=0)        → Average down (per column)
   np.mean(array, axis=1)        → Average across (per row)
   np.unravel_index(idx, shape)  → Convert flat index to (row, col)


# ============================================================================
# PRACTICE EXERCISES (TRY THESE!)
# ============================================================================

EXERCISE 1: YIELD VARIANCE
──────────────────────────
📝 Task: The script shows 10 fields with different yields. Some are very high,
   some very low. Identify which fields are underperforming.

🎯 Steps:
   1. Copy the yields array from Example 1
   2. Calculate the average yield
   3. Create a boolean mask for below-average fields
   4. Print which field numbers are underperforming
   5. Calculate how much each is below average

```python
yields = np.array([25.3, 28.5, 22.1, 30.2, 26.8, 24.5, 29.1, 23.7, 27.4, 25.9])
avg = np.mean(yields)
underperforming = yields < avg
fields_below_avg = np.where(underperforming)[0] + 1  # +1 because fields are numbered 1-10
print(f"Underperforming fields: {fields_below_avg}")
```


EXERCISE 2: WEATHER ALERTS
───────────────────────────
📝 Task: Modify Example 3 to add wind speed as a risk factor

🎯 Steps:
   1. Create wind_speed array (0-50 km/h)
   2. Calculate wind_stress (0-1 scale): high wind = high stress
   3. Update formula: weights should sum to 1.0
   4. New formula might be: 0.4*rainfall + 0.2*temp + 0.2*soil + 0.2*wind
   5. Re-run and compare high-risk days

```python
wind_speed = np.array([5, 25, 45, 10, 15])  # km/h
wind_stress = np.where(wind_speed > 30, 1.0, wind_speed / 30)
# Now add to risk_score calculation...
```


EXERCISE 3: PRICE PREDICTIONS
──────────────────────────────
📝 Task: Track weekly prices for a crop and predict if prices are rising or falling

🎯 Steps:
   1. Create array of weekly prices (8-10 weeks)
   2. Calculate week-over-week change
   3. Find trend: are prices going up or down?
   4. Calculate average weekly change
   5. Simple prediction: if trend continues, what will price be next week?


EXERCISE 4: MULTI-LOCATION CLIMATE RISK
──────────────────────────────────────────
📝 Task: Compare climate risk across 3 different locations

🎯 Steps:
   1. Create separate arrays for 3 locations (or use 2D array)
   2. Calculate risk score for each location
   3. Find which location has highest average risk
   4. Which location is safest for the crop?


EXERCISE 5: EXTEND TO 2D CROP ANALYSIS
──────────────────────────────────────
📝 Task: Combine climate risk with crop-specific sensitivity

🎯 Steps:
   1. Create climate risk array (as in Example 3)
   2. Create crop sensitivity array (how sensitive each crop is: 0-1)
   3. Combine: effective_risk = climate_risk × crop_sensitivity
   4. Find which crop is most at-risk given current climate


# ============================================================================
# COMMON MISTAKES TO AVOID
# ============================================================================

❌ MISTAKE 1: Forgetting to import NumPy
   ✓ FIX: Always include: import numpy as np

❌ MISTAKE 2: Using Python list instead of NumPy array
   ❌ yields = [25.3, 28.5, 22.1]  # This is a list
   ✓ yields = np.array([25.3, 28.5, 22.1])  # This is NumPy array
   (Operations on lists are slow; NumPy arrays are fast!)

❌ MISTAKE 3: Forgetting axis parameter in 2D arrays
   ❌ np.mean(yields_by_crop)  # Which direction?
   ✓ np.mean(yields_by_crop, axis=0)  # Across crops
   ✓ np.mean(yields_by_crop, axis=1)  # Across days

❌ MISTAKE 4: Shape mismatch when combining arrays
   ❌ array1 = np.array([1, 2, 3])       # shape (3,)
       array2 = np.array([10, 20])       # shape (2,) - WRONG!
       result = array1 + array2          # ERROR!
   ✓ Make sure all arrays have compatible shapes

❌ MISTAKE 5: Integer division problems
   ❌ percentage = (change / original) * 100  # If integers, might round
   ✓ Convert to float: float(change) or use 100.0


# ============================================================================
# NEXT LEARNING STEPS
# ============================================================================

After mastering NumPy basics (this script):

📚 NEXT TOPIC: Pandas (Section 4.25+)
   - vs NumPy: Pandas works with DataFrames (labeled rows/columns)
   - Load CSV files: pd.read_csv()
   - Filter rows: df[df['yield'] > 25]
   - Group by: df.groupby('crop').mean()

📚 THEN: Data Visualization (Matplotlib, Seaborn)
   - Plot yields vs rainfall
   - Create heatmaps for 2D climate data
   - Time series for price trends

📚 THEN: Statistical Analysis
   - Correlation between rainfall and yield
   - Regression models to predict yield
   - Hypothesis testing

📚 THEN: Machine Learning
   - Train models to predict crop risk
   - Use historical weather + yield data
   - Make recommendations


# ============================================================================
# HELPFUL TIPS FOR LEARNING
# ============================================================================

💡 TIP 1: Read Error Messages Carefully
   Error messages in Python are helpful!
   - "ValueError: shape mismatch" → Arrays have different sizes
   - "AttributeError: 'list' has no attribute 'mean'" → Used list, not array
   - "IndexError: index out of bounds" → Tried to access element that doesn't exist

💡 TIP 2: Print Intermediate Results
   Add print statements to see what your arrays look like at each step:
   ```python
   rainfall = np.array([15.2, 8.5, 0.0])
   print(f"Rainfall: {rainfall}")
   print(f"Shape: {rainfall.shape}")
   deviation = rainfall - 12.0
   print(f"Deviation: {deviation}")
   ```

💡 TIP 3: NumPy is Vectorized (Fast!)
   ✓ FAST: risk_score = (0.5 * rainfall_dev) + (0.3 * temp_stress)
   ❌ SLOW: for i in range(...): risk_score[i] = 0.5*rainfall[i] + ...
   
   As data grows, NumPy way is 100x faster!

💡 TIP 4: Use Documentation
   - Forget function name? Google "NumPy mean function"
   - In terminal: python -c "import numpy as np; help(np.mean)"
   - Or: python -c "import numpy as np; print(np.mean.__doc__)"

💡 TIP 5: Build Gradually
   Don't try to understand everything at once:
   1. Get data into arrays ✓
   2. Calculate one statistic (mean) ✓
   3. Add another calculation ✓
   4. Combine multiple operations ✓
   5. Create full analysis ✓


# ============================================================================
# AGRISENSE LEARNING PATH SUMMARY
# ============================================================================

What We Covered (This Script):
─────────────────────────────
✓ Section 4.22: Creating and Understanding Arrays
  - 1D arrays, shapes, dtypes
  - Creating with np.array(), np.zeros(), np.ones(), np.arange()

✓ Section 4.23: Array Shapes and Properties  
  - Understanding (10,) vs (4,5) shapes
  - Using .shape, .ndim, .size properties
  - When to use axis parameter

✓ Section 4.24: Basic Math Operations
  - Statistics: mean, max, min, std, sum
  - Element-wise: add, subtract, multiply, divide
  - Boolean indexing for filtering
  - Weighted calculations

Real-World Application:
──────────────────────
Climate Risk Score for farmers:
- Input: Rainfall, temperature, soil moisture (arrays)
- Process: Normalize, weight, combine (NumPy operations)
- Output: Risk category + recommendation (IF statements)
- Result: Farmer knows if they should irrigate/apply fungicide/harvest early

This exact workflow is used in production AgriSense systems!


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

Q: "ModuleNotFoundError: No module named 'numpy'"
A: NumPy not installed. Run: pip install numpy

Q: Script runs but output looks wrong
A: Check that you're using NumPy (import numpy as np), not just Python lists

Q: Why is my array dtype 'int64' instead of 'float64'?
A: Created array with integers: np.array([1, 2, 3])
   Use floats: np.array([1.0, 2.0, 3.0]) or np.array([1, 2, 3], dtype=float)

Q: Boolean mask gives "ValueError: operands could not be broadcast together"
A: Arrays have different shapes. Check with print(array.shape)

Q: How do I save my results to a file?
A: np.savetxt('results.txt', array)
   Or: np.save('results.npy', array)


# ============================================================================
# FINAL REMINDER
# ============================================================================

✨ NumPy is the foundation of data science in Python!

Every data scientist, machine learning engineer, and computational analyst
uses NumPy daily. By learning NumPy arrays, shapes, and operations, you're
building a skill that directly enables:

• Climate prediction models
• Yield forecasting systems
• Price analysis for fair trade
• Pest/disease early warning systems
• Irrigation optimization
• Crop recommender systems

Your AgriSense journey continues with Pandas, Visualization, and ML!

Happy learning! 🌾📊🐍
"""
