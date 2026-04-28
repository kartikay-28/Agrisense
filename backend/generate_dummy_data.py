import pandas as pd
import numpy as np
import datetime
import os

dst_dir = r'D:\D files\AgriSense\S84-0426-AKM-Python-Pandas-NumPy-AgriSense\data\processed'
os.makedirs(dst_dir, exist_ok=True)

crops = ['Wheat', 'Rice']
states = ['Punjab', 'Haryana']
base_date = datetime.datetime.now() - datetime.timedelta(days=100)

data = []
for crop in crops:
    price = 2000.0 if crop == 'Wheat' else 3500.0
    for state in states:
        for i in range(100):
            d = base_date + datetime.timedelta(days=i)
            # Add some randomness
            price += np.random.normal(0, 15)
            data.append({
                'commodity': crop,
                'state': state,
                'date': d.strftime('%Y-%m-%d'),
                'modal_price': price,
                'price_pct_change': np.random.normal(0, 0.05),
                'price_rolling_avg_7d': price + np.random.normal(0, 5),
                'price_rolling_avg_30d': price + np.random.normal(0, 10),
                'price_volatility_7d': np.random.normal(5, 2)
            })

df = pd.DataFrame(data)
df.to_csv(os.path.join(dst_dir, 'agrisense_features.csv'), index=False)
print('Generated dummy agrisense_features.csv successfully.')
