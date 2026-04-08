# 📊 load_crop_prices.py - Quick Start Guide

## Overview

`load_crop_prices.py` is your first AgriSense data loading script. It:
- Loads agricultural market price data from CSV files
- Automatically standardizes column names
- Prints a comprehensive data summary
- Can be imported and reused in other scripts

## ✅ What It Does

When you run the script, it displays:
1. **Dataset Shape** - Number of rows and columns
2. **First 5 Rows** - Preview of the data
3. **Data Types** - Column data types (string, float, datetime)
4. **Date Range** - From/To dates in the dataset
5. **Unique Crops** - List of all commodities
6. **Price Statistics** - Average, median, min, max, std deviation
7. **Top 10 Most Expensive Crops** - With visual bars
8. **Statistical Summary** - Quartiles, counts, etc.
9. **Missing Values** - Any data quality issues

## 🚀 How to Use

### Option 1: Run Directly (Simplest)

```bash
cd agrisense
python load_crop_prices.py
```

**Output:** Formatted summary of your crop price data

### Option 2: Import and Use in Other Scripts

```python
from load_crop_prices import load_and_summarize_prices

# Load data with summary output
df = load_and_summarize_prices("mandi_prices.csv")

# Use the dataframe for further analysis
print(df.head())
```

### Option 3: Load Without Summary Output

```python
from load_crop_prices import load_and_summarize_prices

# Load quietly (no summary printed)
df = load_and_summarize_prices("mandi_prices.csv", print_summary=False)

# Do your own analysis
print(df.describe())
```

### Option 4: Use Just the Loading Function

```python
from load_crop_prices import load_csv_file, standardize_column_names

# Step by step
df = load_csv_file("mandi_prices.csv", data_dir="data/raw")
df = standardize_column_names(df)
print(df)
```

## 📋 Available Functions

| Function | Purpose |
|----------|---------|
| `load_csv_file()` | Load CSV with error handling |
| `standardize_column_names()` | Convert column names to lowercase_with_underscores |
| `get_date_range()` | Extract min/max dates from data |
| `calculate_price_statistics()` | Get average, median, min, max, std dev |
| `get_unique_crops()` | List all unique crops in data |
| `get_average_price_by_crop()` | Group by crop and calculate average price |
| `load_and_summarize_prices()` | **Main function** - Complete workflow |

## 📁 Expected Data Format

Your CSV file should have columns like:

| Column Name | Type | Example |
|------------|------|---------|
| commodity | string | Rice, Wheat, Tomato |
| state | string | Punjab, Haryana, UP |
| mandi | string | Delhi, Mumbai, Chandigarh |
| modal_price | float | 2450.75 |
| min_price | float | 2300.00 |
| max_price | float | 2600.00 |
| date | datetime | 2024-01-15 |

**Note:** Column names are flexible - the script handles variations like "Commodity", "COMMODITY", "commodity", "Crop Name", etc.

## 💡 Example: How to Customize

### Change the data file:
```python
df = load_and_summarize_prices(filename="my_prices.csv")
```

### Load data from a different directory:
```python
df = load_and_summarize_prices(
    filename="prices.csv",
    data_dir="data/external"
)
```

### Get specific crop information:
```python
from load_crop_prices import load_and_summarize_prices, get_average_price_by_crop

df = load_and_summarize_prices("mandi_prices.csv", print_summary=False)

# Get top 5 most expensive crops
top_crops = get_average_price_by_crop(df, top_n=5)
print(top_crops)
```

## ⚠️ Troubleshooting

### "File not found" error?
```
❌ File not found: data/raw/mandi_prices.csv
   Please ensure 'mandi_prices.csv' is in the 'data/raw/' folder.
```

**Solution:** 
1. Make sure the CSV file is in `data/raw/` folder
2. Check the filename is spelled correctly
3. For testing, run `python example_workflow.py` to generate sample data

### Column names not recognized?
The script tries these column names automatically:
- For crops: `commodity`, `crop`, `crop_name`, `product`
- For prices: `modal_price`, `price`, `mandi_price`, `market_price`
- For dates: `date`, `arrival_date`, `market_date`, `trading_date`

If your CSV has different column names, the script still loads it but may skip some analysis.

## 🔮 Future Use

This script will be:
1. **Expanded** with more analysis functions
2. **Integrated** into FastAPI backend as `/api/market-data`
3. **Extended** to handle real-time data APIs
4. **Optimized** for large datasets with caching

## 📝 Code Examples

### Find cheapest crops:
```python
from load_crop_prices import load_and_summarize_prices, get_average_price_by_crop

df = load_and_summarize_prices("mandi_prices.csv", print_summary=False)

# Get prices
avg_prices = get_average_price_by_crop(df, top_n=10)

# Show cheapest
cheapest = avg_prices.sort_values()
print("Cheapest crops:")
print(cheapest)
```

### Filter for specific crop:
```python
from load_crop_prices import load_and_summarize_prices

df = load_and_summarize_prices("mandi_prices.csv", print_summary=False)

# Get only Rice data
rice_data = df[df['commodity'] == 'Rice']
print(f"Rice records: {len(rice_data)}")
print(f"Average Rice price: ₹{rice_data['modal_price'].mean():.2f}")
```

### Export to new file:
```python
from load_crop_prices import load_and_summarize_prices

df = load_and_summarize_prices("mandi_prices.csv", print_summary=False)

# Your processing here...

# Save processed data
df.to_csv("data/processed/cleaned_prices.csv", index=False)
```

---

## ✨ Pro Tips

1. **Use with Jupyter Notebooks** - Import and use interactively
2. **Combine with utils** - Import profitability functions from `src/utils.py`
3. **Chain with preprocessing** - Use output of this script with `src/data_preprocessing.py`
4. **Schedule with backend** - Will be called by FastAPI routes

## 📚 Next Steps

- Run the script successfully ✅
- Try importing and using functions in a notebook
- Integrate with `src/feature_engineering.py` for advanced analysis
- Use output data for ML model training

---

**Happy analyzing!** 📊🚀
