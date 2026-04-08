# AgriSense: Complete Setup & Quickstart Guide

## 📋 What Has Been Created

Your AgriSense project now has a fully organized data science structure with:

### ✅ Folder Structure
```
agrisense/
├── data/                          # Data storage
│   ├── raw/                      # Original CSV files (immutable)
│   ├── processed/                # Cleaned & prepared data
│   └── external/                 # External datasets
│
├── notebooks/                     # Jupyter notebooks for exploration
├── outputs/                       # Results & visualizations
│   ├── figures/
│   ├── predictions/
│   └── models/
│
├── src/                           # Main Python modules
│   ├── __init__.py
│   ├── data_preprocessing.py     # ✅ Created - Data loading & cleaning
│   ├── feature_engineering.py    # ✅ Created - Feature creation
│   ├── utils.py                  # ✅ Created - Helper functions
│   └── models/                   # Placeholder for ML models
│
├── backend/                       # FastAPI backend (future)
├── frontend/                      # Next.js frontend (existing)
├── .gitignore                    # ✅ Created - Git ignore patterns
├── requirements.txt              # ✅ Created - pip dependencies
├── environment.yml               # ✅ Created - conda environment
├── example_workflow.py            # ✅ Created - Complete workflow demo
├── README_DATA_SETUP.md           # ✅ Created - This guide
└── PROJECT_PLAN.md               # Project definition document
```

### ✅ Python Modules Created

#### 1. **data_preprocessing.py**
Core data processing module with the `DataPreprocessor` class.

**Key Functions:**
- `load_raw_data()` - Load CSV files from data/raw/
- `standardize_column_names()` - Normalize column names
- `handle_missing_values()` - Fill or remove NaN values
- `create_date_features()` - Extract temporal features
- `remove_duplicates()` - Remove duplicate rows
- `remove_outliers()` - Remove outliers using IQR/Z-score
- `process_pipeline()` - Complete preprocessing workflow

**Usage Example:**
```python
from src.data_preprocessing import DataPreprocessor

preprocessor = DataPreprocessor()
df = preprocessor.process_pipeline(
    filename='raw_agriculture.csv',
    date_column='date',
    output_filename='processed_agriculture.csv'
)
```

#### 2. **feature_engineering.py**
Advanced feature creation with time-series and domain-specific features.

**Key Functions:**
- `create_lag_features()` - Time-series lags
- `create_rolling_features()` - Rolling statistics
- `create_seasonal_features()` - Sine/cosine encoding
- `create_crop_region_features()` - Categorical encoding
- `create_climate_risk_score()` - Composite risk metric
- `engineer_features_pipeline()` - Complete feature pipeline

**Usage Example:**
```python
from src.feature_engineering import engineer_features_pipeline

df_engineered = engineer_features_pipeline(df, date_column='date')
```

#### 3. **utils.py**
General-purpose utilities for common operations.

**Key Functions:**
- `ensure_directory()` - Create directories
- `save_predictions()` / `load_predictions()` - File I/O
- `print_data_summary()` - Data overview
- `filter_by_crop()`, `filter_by_region()`, `filter_by_date_range()` - Filtering
- `format_price_display()`, `format_yield_display()` - Formatting
- `get_best_selling_date()` - Optimal selling analysis
- `calculate_profitability()` - ROI calculations
- `export_to_json()` / `load_from_json()` - JSON export

**Usage Example:**
```python
from src.utils import calculate_profitability

profit = calculate_profitability(
    estimated_yield=4500,
    predicted_price=35,
    cost_per_hectare=50000
)
print(f"Profit: {profit['profit_display']}")
# Output: Profit: ₹107,500.00
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Create & Activate Environment
```bash
# Using Conda (Recommended)
conda env create -f environment.yml
conda activate agrisense

# OR using pip
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 2: Verify Installation
```bash
python -c "import pandas; import numpy; print('✅ Ready to go!')"
```

### Step 3: Run the Example Workflow
```bash
python example_workflow.py
```

This will:
- Create sample agricultural data
- Preprocess and clean it
- Engineer features
- Generate analytics and profitability estimates
- Save results to `outputs/predictions/`

### Step 4: Check the Outputs
```bash
# View created files
ls data/processed/
ls outputs/predictions/
```

---

## 📊 Data Format & Column Names

When adding your own data, use these standard column names:

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `crop` | string | Crop type | Rice, Wheat, Maize |
| `region` | string | Geographic region | Punjab, Haryana, UP |
| `date` | datetime | Date of observation | 2023-01-15 |
| `yield_kg_per_hectare` | float | Crop yield | 4200 |
| `rainfall_mm` | float | Monthly rainfall | 75.5 |
| `temperature_celsius` | float | Average temperature | 28.3 |
| `market_price_per_kg` | float | Wholesale price | 35.50 |
| `demand_index` | float | Relative demand | 1.2 |

**Note:** If your columns have different names, the `standardize_column_names()` function will convert them to lowercase with underscores (e.g., "Market Price" → "market_price").

---

## 📚 Working with Notebooks

### Start Jupyter
```bash
jupyter notebook
```

### Create a New Analysis Notebook
1. Navigate to `notebooks/` folder
2. Create a new file: `05_my_analysis.ipynb`
3. Use this template:

```python
# Cell 1: Imports
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd().parent / 'src'))
from data_preprocessing import DataPreprocessor
from feature_engineering import engineer_features_pipeline
from utils import print_data_summary

# Cell 2: Load and explore data
preprocessor = DataPreprocessor()
df = pd.read_csv('data/processed/agricultural_data_preprocessed.csv')
print_data_summary(df)

# Cell 3: Your analysis here
...
```

---

## 🔄 Complete Workflow

### For Raw Data Processing:
```python
from src.data_preprocessing import DataPreprocessor

preprocessor = DataPreprocessor()

# Step 1: Load
df = preprocessor.load_raw_data('my_data.csv')

# Step 2: Preprocess
df = preprocessor.process_pipeline(
    filename='my_data.csv',
    date_column='date',
    output_filename='my_data_processed.csv',
    remove_outlier_cols=['yield_kg_per_hectare', 'market_price_per_kg']
)
```

### For Feature Engineering:
```python
from src.feature_engineering import engineer_features_pipeline

# Engineering pipeline (assumes data is preprocessed)
df_engineered = engineer_features_pipeline(df, date_column='date')

# Save engineered features
df_engineered.to_csv('data/processed/my_data_engineered.csv', index=False)
```

### For Analysis & Export:
```python
from src.utils import (
    filter_by_crop,
    calculate_profitability,
    save_predictions,
)

# Filter by crop
rice_data = filter_by_crop(df_engineered, crop='Rice')

# Calculate profitability
profit = calculate_profitability(
    estimated_yield=rice_data['yield_kg_per_hectare'].mean(),
    predicted_price=rice_data['market_price_per_kg'].mean()
)

# Save results
save_predictions(rice_data, filename='rice_analysis.csv')
```

---

## 📂 Adding Your Own Data

### To add your agricultural data:

1. **Prepare your CSV** with columns matching the standard format
2. **Copy to `data/raw/` folder**
   ```bash
   cp your_agriculture_data.csv data/raw/
   ```
3. **Process with the pipeline**
   ```python
   from src.data_preprocessing import DataPreprocessor
   
   preprocessor = DataPreprocessor()
   df = preprocessor.process_pipeline(
       filename='your_agriculture_data.csv',
       date_column='date',
       output_filename='your_agriculture_data_processed.csv'
   )
   ```
4. **Engineer features**
   ```python
   from src.feature_engineering import engineer_features_pipeline
   
   df_engineered = engineer_features_pipeline(df)
   df_engineered.to_csv('data/processed/your_agriculture_data_engineered.csv', index=False)
   ```
5. **Analyze and export**
   ```python
   from src.utils import save_predictions
   
   save_predictions(df_engineered, filename='results.csv')
   ```

---

## 🎯 Next Steps

### Immediate Tasks:
1. ✅ Environment setup (done via conda/pip)
2. ✅ Run example workflow (done)
3. 📝 Explore sample data using Jupyter notebooks
4. 📊 Add your own agricultural data to `data/raw/`

### Development Tasks:
1. **Week 1:** Data exploration & validation
2. **Week 2:** Feature engineering & selection
3. **Week 3:** Model training (price prediction, yield prediction)
4. **Week 4:** Backend API development (FastAPI)
5. **Week 5:** Frontend integration (Next.js)

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pandas'`
**Solution:** Activate the environment first
```bash
conda activate agrisense
```

### Issue: Data file not found
**Solution:** Ensure CSV is in `data/raw/` with correct filename
```bash
ls data/raw/
```

### Issue: Missing date column
**Solution:** Specify the correct date column name or add one
```python
df_processed = preprocessor.process_pipeline(
    filename='my_data.csv',
    date_column='date',  # Change to your date column
)
```

### Issue: Too many NaN values after preprocessing
**Solution:** Try different missing value strategy
```python
df_processed = preprocessor.handle_missing_values(df, strategy='median')
```

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Activate environment | `conda activate agrisense` |
| Install dependencies | `pip install -r requirements.txt` |
| Run example | `python example_workflow.py` |
| Start Jupyter | `jupyter notebook` |
| Check Python version | `python --version` |
| List installed packages | `pip list` |

---

## 📖 Documentation Files

- **README_DATA_SETUP.md** (this file) - Setup & quickstart guide
- **PROJECT_PLAN.md** - Project definition and MVP scope
- **README.md** (main folder) - Optional main project readme

---

## 🎓 Learning Resources

**For Data Science with Pandas & NumPy:**
- [Pandas Official Tutorial](https://pandas.pydata.org/docs/)
- [NumPy User Guide](https://numpy.org/doc/stable/user/index.html)

**For Feature Engineering:**
- Feature engineering techniques in time-series data
- Domain-specific features for agriculture

**For ML Models (Next Phase):**
- Time-series forecasting with Prophet/LSTM
- Tree-based models (Random Forest, XGBoost)

---

## ✨ Happy Farming with Data! 🚜

You're all set to start building AgriSense. Good luck!

For questions or issues, refer to the module docstrings:
```python
from src.data_preprocessing import DataPreprocessor
help(DataPreprocessor)
```

---

**Version:** 1.0  
**Last Updated:** April 8, 2026  
**AgriSense Team**
