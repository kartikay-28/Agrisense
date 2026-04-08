# AgriSense: AI-Powered Agricultural Decision Support Platform

## 📋 Overview

**AgriSense** is a data-driven platform designed to help small and medium-scale farmers make informed, profitable decisions using machine learning and AI. By analyzing historical crop data, weather patterns, and market prices, AgriSense provides:

- 📊 **Demand & Price Forecasts** - Predict when to sell for maximum returns
- 🌦️ **Climate Risk Alerts** - 10-day forecasts with actionable irrigation advice
- 🌾 **Yield Predictions** - Interactive scenarios to optimize farming strategies
- 💬 **AI Advisor** - Natural language recommendations powered by LLMs

## 🗂️ Project Structure

```
agrisense/
├── data/
│   ├── raw/                    # Original, immutable CSV/data files
│   ├── processed/              # Cleaned & feature-engineered datasets
│   └── external/               # Third-party datasets (e.g., weather APIs)
│
├── notebooks/                  # Jupyter notebooks for exploration
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_modeling.ipynb
│
├── outputs/
│   ├── figures/                # Visualizations & charts
│   ├── predictions/            # Model predictions (CSV/JSON)
│   └── models/                 # Saved trained models
│
├── src/
│   ├── data_preprocessing.py   # Data loading & cleaning functions
│   ├── feature_engineering.py  # Feature creation utilities
│   ├── utils.py                # General utilities
│   └── models/
│       ├── price_predictor.py
│       └── yield_predictor.py
│
├── backend/                    # FastAPI backend (future)
├── frontend/                   # Next.js frontend (future)
├── .gitignore
├── requirements.txt            # Python dependencies (pip)
├── environment.yml             # Conda environment file
├── README.md
└── PROJECT_PLAN.md             # MVP definition
```

## 🚀 Getting Started

### Prerequisites
- Python 3.12 or higher
- Conda (recommended) or pip
- Git

### 1. Clone the Repository
```bash
cd agrisense
```

### 2. Create & Activate Conda Environment

**Using Conda (Recommended):**
```bash
conda env create -f environment.yml
conda activate agrisense
```

**Using pip (Alternative):**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python -c "import pandas; import numpy; print('✅ Dependencies installed successfully!')"
```

### 4. Run the Data Preprocessing Example
```bash
python src/data_preprocessing.py
```

This will:
- Create sample agricultural data in `data/raw/`
- Process and clean the data
- Save the cleaned data to `data/processed/`
- Display data statistics

## 📊 Data Structure

Expected columns in raw CSV files:
```
crop                    - Crop name (e.g., Rice, Wheat, Maize)
region                  - Geographic region (e.g., Punjab, Haryana)
date                    - Date of observation (YYYY-MM-DD format)
yield_kg_per_hectare    - Crop yield in kg/ha
rainfall_mm             - Rainfall in mm
temperature_celsius     - Temperature in °C
market_price_per_kg     - Wholesale price in ₹/kg
demand_index            - Relative demand (0-2 scale)
```

## 🔧 Key Modules

### `data_preprocessing.py`
Handles all data loading and cleaning operations:
- `load_raw_data()` - Read CSV from data/raw/
- `standardize_column_names()` - Normalize column names
- `handle_missing_values()` - Impute or remove NaN values
- `create_date_features()` - Extract temporal features (year, month, quarter, etc.)
- `remove_duplicates()` - Remove duplicate rows
- `remove_outliers()` - Identify and remove outliers using IQR/Z-score
- `process_pipeline()` - Execute complete preprocessing workflow

### Example Usage:
```python
from src.data_preprocessing import DataPreprocessor

preprocessor = DataPreprocessor(
    raw_data_path="data/raw",
    processed_data_path="data/processed"
)

df = preprocessor.process_pipeline(
    filename='agriculture_data.csv',
    date_column='date',
    output_filename='agriculture_processed.csv',
    remove_outlier_cols=['yield_kg_per_hectare', 'market_price_per_kg']
)
```

## 📈 Workflow

1. **Data Collection** → Place raw CSV files in `data/raw/`
2. **Preprocessing** → Run `data_preprocessing.py` to clean data
3. **Exploration** → Use Jupyter notebooks in `notebooks/` to visualize patterns
4. **Feature Engineering** → Create domain-specific features
5. **Modeling** → Train ML models for predictions
6. **Outputs** → Save predictions, models, and charts to `outputs/`

## 🧪 Running Jupyter Notebooks

```bash
jupyter notebook
```

Navigate to the `notebooks/` folder and open any `.ipynb` file.

## 📦 Dependencies Overview

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.1.4 | Data manipulation |
| numpy | 1.24.3 | Numerical computing |
| scikit-learn | 1.3.2 | ML algorithms |
| xgboost | 2.0.3 | Gradient boosting |
| prophet | 1.1.5 | Time-series forecasting |
| fastapi | 0.104.1 | Backend API |
| plotly | 5.18.0 | Interactive visualizations |

For full list, see `requirements.txt` and `environment.yml`.

## 🛣️ MVP Roadmap

**Phase 1 (Current):**
- ✅ Data preprocessing pipeline
- ✅ Sample data generation
- 🔄 Exploratory data analysis

**Phase 2:**
- Price forecasting model (Prophet/LSTM)
- Yield prediction (Random Forest/XGBoost)
- Climate risk classification

**Phase 3:**
- FastAPI backend integration
- Frontend dashboard (Next.js)
- LLM-powered advisor

**Phase 4+:**
- Real-time API integration
- Mobile app
- User authentication & farm profiles

## 📝 Contributing

To contribute to AgriSense:
1. Create a new branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Commit & push: `git push origin feature/your-feature`
4. Create a pull request

## ❓ FAQ

**Q: Where do I place raw data?**  
A: Place all raw CSV files in the `data/raw/` folder.

**Q: Can I use different column names?**  
A: Yes! The `standardize_column_names()` function normalizes them to lowercase with underscores.

**Q: How do I add more ML models?**  
A: Create new Python files in `src/models/` following the structure of existing predictors.

**Q: Is the LLM advisor included in the MVP?**  
A: Not yet—it's planned for Phase 3. Currently, the focus is on data and ML models.

## 📞 Support

For issues, questions, or feedback:
- Open an issue on GitHub
- Check existing documentation in PROJECT_PLAN.md
- Review the example notebooks for usage patterns

## 📄 License

This project is part of an educational hackathon/agri-tech initiative.

---

**Happy farming! 🚜** Let data guide your decisions.
