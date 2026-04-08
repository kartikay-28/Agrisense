# 🎓 Python Educational Scripts: Conditionals, Loops & Functions

## 📚 Overview

Two complete, beginner-friendly Python scripts to learn core programming concepts using the AgriSense project as context:

1. **risk_scoring.py** - Learn Conditionals (if-elif-else) and Loops (for)
2. **agrisense_functions.py** - Learn Functions (parameters, returns, docstrings)

Both scripts are production-ready, well-commented, and immediately testable.

---

## 📋 Script 1: risk_scoring.py - Conditionals & Loops

### What It Teaches

**Conditionals (if-elif-else):**
- Making decisions based on conditions
- Multiple branches of logic
- Nested conditionals

**Loops (for):**
- Iterating through data
- Processing multiple records
- Building collections during loops

### How to Run

```bash
cd agrisense
python risk_scoring.py
```

### What It Does

1. **Creates sample data** - 8 weather records with rainfall and temperature
2. **Calculates risk scores** using conditionals:
   - Rainfall < 30mm → HIGH RISK (drought)
   - Rainfall 30-80mm → MEDIUM RISK
   - Rainfall > 80mm → LOW RISK (flood watch)
   - Temperature > 35°C → HEAT STRESS
3. **Loops through data** to generate a risk report
4. **Prints actionable insights** for farmers

### Key Functions Demonstrated

```python
get_rainfall_risk(rainfall_mm)          # Conditionals for rainfall
get_temperature_risk(temperature_c)     # Conditionals for temperature
calculate_combined_risk(...)            # Combining multiple conditions
generate_risk_report(df)                # LOOP + conditionals
find_high_risk_crops(df)                # Filtering with loops
```

### Sample Output

```
📍 1. WHEAT on 2024-04-01
   Rainfall: 15.0mm | Temperature: 28°C
   🚨 DROUGHT ALERT: Only 15.0mm rainfall. Crops need more water!
   ☀️  WARM: 28°C is acceptable.
   ➜ OVERALL RISK: HIGH

📊 SUMMARY
High Risk:   3 cases  🚨
Medium Risk: 4 cases ⚠️
Low Risk:    1 cases ✅
```

### Code Pattern You'll Learn

**Conditional Pattern:**
```python
if condition1:
    # Do something
    result = "value_a"
elif condition2:
    # Do something else
    result = "value_b"
else:
    # Default
    result = "value_c"
```

**Loop Pattern:**
```python
for row in dataframe.iterrows():
    value = row['column']
    
    if value < threshold:
        count += 1
    
    print(f"Processing: {value}")
```

---

## 📋 Script 2: agrisense_functions.py - Functions

### What It Teaches

**Functions:**
- Creating reusable functions
- Parameters and arguments
- Return values
- Type hints
- Docstrings
- Calling functions

### How to Run

```bash
cd agrisense
python agrisense_functions.py
```

### What It Does

Demonstrates 5 reusable functions:

1. **`calculate_risk_score(rainfall, temperature)`**
   - Combines rainfall and temperature into risk score (0-100)
   - Returns dict with risk_level, risk_score, and reason
   - Uses scoring algorithm

2. **`get_price_summary(prices_list)`**
   - Takes list of prices
   - Calculates average, min, max, median, std deviation
   - Returns dict with all statistics

3. **`estimate_yield(crop, rainfall, fertilizer)`**
   - Estimates crop yield based on multiple factors
   - Different base yields for different crops
   - Realistic agricultural formulas
   - Returns single float value

4. **`generate_risk_report(data)`**
   - Takes list of farm records
   - LOOPS through each record
   - Calls `calculate_risk_score()` inside the loop
   - Generates comprehensive report
   - Returns dict with details

5. **`print_report_summary(report)`**
   - Takes report dict
   - Prints nicely formatted output
   - Returns None (just prints)

### Sample Output

```
====== DEMO 1: calculate_risk_score() ======

Rainfall: 15mm, Temp: 38°C
  → Risk Score: 90/100
  → Level: HIGH
  → Risk factors: drought (low rainfall), heat stress

Rainfall: 60mm, Temp: 25°C
  → Risk Score: 0/100
  → Level: LOW
  → Optimal conditions

====== DEMO 2: get_price_summary() ======

Wheat market prices: [2400, 2500, 2450, 2600, 2550]

Average Price:  ₹2500.00
Min Price:      ₹2400.00
Max Price:      ₹2600.00

====== DEMO 3: estimate_yield() ======

Wheat: 50mm rain, 90kg/ha fertilizer
  → Estimated Yield: 3888 kg/ha

Rice: 70mm rain, 110kg/ha fertilizer
  → Estimated Yield: 5200 kg/ha
```

### Code Pattern You'll Learn

**Function Definition Pattern:**
```python
def function_name(parameter1: type, parameter2: type) -> return_type:
    """
    Docstring describing what this function does.
    
    Parameters:
    -----------
    parameter1 : type
        Description of parameter1
        
    Returns:
    --------
    return_type
        Description of what is returned
    """
    
    # Function body
    result = parameter1 + parameter2
    
    return result
```

**Calling Functions:**
```python
# Call the function
result = function_name(parameter1=value1, parameter2=value2)

# Use the result
print(result['key'])
```

### Type Hints Explained

```python
def function(
    rainfall: float,              # Input is float
    crop: str                     # Input is string
) -> Dict:                        # Output is dictionary
    pass
```

Type hints help:
- Make code clearer (what type expected)
- Enable IDE autocompletion
- Catch errors early

---

## 🔗 How These Scripts Connect

### Risk Scoring Script
Perfect for understanding:
- How to make decisions in code
- Processing multiple records
- Building reports

### Functions Script
Perfect for understanding:
- How to organize code into reusable pieces
- How to document code
- How to design reusable components

**Together:**
You can use functions from Script 2 inside loops from Script 1!

---

## 📖 How to Use Them

### Step 1: Run Them Individually

```bash
python risk_scoring.py
python agrisense_functions.py
```

### Step 2: Import Functions Into Other Scripts

Create a new file `my_analysis.py`:

```python
from agrisense_functions import (
    calculate_risk_score,
    get_price_summary,
    estimate_yield,
)

# Use the functions
risk = calculate_risk_score(rainfall=50, temperature=28)
print(f"Risk level: {risk['risk_level']}")

prices = [2500, 2600, 2550]
summary = get_price_summary(prices)
print(f"Average: ₹{summary['average']:.2f}")
```

Then run:
```bash
python my_analysis.py
```

### Step 3: Modify and Experiment

Try changing:
- Rainfall values
- Temperature thresholds
- Crop data
- Risk scoring formula

---

## 💡 Exercise Ideas

### Practice Conditionals
1. Modify rainfall thresholds
2. Add more conditions (e.g., soil moisture)
3. Create multi-level risk scoring

**Example:**
```python
if rainfall < 20 and temperature > 35:
    # Both drought AND heat
    risk = "CRITICAL"
elif rainfall > 150:
    # Flood risk
    risk = "WARNING"
```

### Practice Loops
1. Add more crops to sample data
2. Calculate average risk across all crops
3. Find most at-risk crop

**Example:**
```python
max_risk = 0
highest_risk_crop = ""

for row in df.iterrows():
    risk_score = calculate_combined_risk(row['rainfall_mm'], row['temperature_c'])
    if risk_score > max_risk:
        max_risk = risk_score
        highest_risk_crop = row['crop']

print(f"Highest risk: {highest_risk_crop}")
```

### Practice Functions
1. Create new function `estimate_profit()`
2. Create function `categorize_yield()`
3. Combine functions into a pipeline

**Example:**
```python
def estimate_profit(yield_kg, price_per_kg, cost_per_ha=50000):
    """Calculate profit from yield and price."""
    gross = yield_kg * price_per_kg
    profit = gross - cost_per_ha
    return profit

# Use it
profit = estimate_profit(5200, 2500)
```

---

## 🎯 Learning Outcomes

After working with these scripts, you can:

✅ **Use conditionals:**
- Write if-elif-else statements
- Combine conditions with AND/OR
- Handle multiple cases

✅ **Use loops:**
- Iterate through data
- Collect results during loops
- Process multiple records

✅ **Create functions:**
- Define reusable functions
- Use parameters and arguments
- Return different types (dict, list, float, etc.)
- Write clear docstrings
- Use type hints

✅ **Understand data processing:**
- Load and explore data
- Calculate statistics
- Generate reports
- Make decisions based on data

---

## 📂 File Locations

```
agrisense/
├── risk_scoring.py                # Script 1: Conditionals & Loops
├── agrisense_functions.py         # Script 2: Functions
├── EDUCATIONAL_SCRIPTS_GUIDE.md   # This guide
└── load_crop_prices.py            # Related: Data loading
```

---

## 🚀 Next Steps After These Scripts

1. **Advanced Functions:**
   - Default parameters
   - *args and **kwargs
   - Lambda functions

2. **Data Processing:**
   - Pandas operations
   - Filter and group data
   - Merge datasets

3. **Integration:**
   - Use these functions in FastAPI backend
   - Call from frontend
   - Create API endpoints

4. **Advanced Topics:**
   - Error handling (try-except)
   - Classes and objects
   - Working with APIs

---

## ❓ Common Questions

**Q: Can I modify these scripts?**  
A: Yes! That's encouraged. Try changing thresholds, adding conditions, creating new functions.

**Q: How do I debug if something breaks?**  
A: Add print() statements to see values at each step:
```python
print(f"Rainfall: {rainfall}")
print(f"Risk: {risk_level}")
```

**Q: Can I use these functions in my project?**  
A: Absolutely! Copy functions into your own scripts or import them:
```python
from agrisense_functions import calculate_risk_score
```

**Q: What if I want to add more crops?**  
A: Edit `create_sample_weather_data()` in Script 1 or `base_yields` dict in Script 2.

**Q: How do I measure success?**  
A: You understand when you can:
1. Modify the threshold values
2. Add new conditions
3. Create your own function
4. Explain what the code does

---

## 📞 Tips for Success

1. **Run the scripts first** - See them work before modifying
2. **Read the comments** - Every section is explained
3. **Use docstrings** - Read the `help()` for functions:
   ```python
   help(calculate_risk_score)
   ```
4. **Experiment** - Change values and see what happens
5. **Ask questions** - If something doesn't make sense, modify it to see the effect

---

## ✨ What These Teach in Real-World Terms

These scripts teach you skills used by:
- **Data Scientists** - Process data with conditionals and loops
- **Backend Developers** - Create reusable functions for APIs
- **AutomationEngineers** - Decision logic in workflows
- **Data Engineers** - ETL pipelines (Extract, Transform, Load)

Your AgriSense project will use these concepts in:
- Risk calculation engine
- ML model pipelines
- FastAPI backend routes
- Data processing workflows

---

**Happy Learning!** 🚀

Start with running the scripts, then modify them, then create your own functions!
