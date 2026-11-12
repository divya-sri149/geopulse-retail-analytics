import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mobility_data(num_records=1000):
    np.random.seed(42)
    base_time = datetime.now() - timedelta(days=7)
    
    locations = [
        {"store_id": "LOC_01", "name": "Downtown Flagship", "lat": 12.9716, "lon": 77.5946, "category": "Apparel"},
        {"store_id": "LOC_02", "name": "Metro Mall Hub", "lat": 12.9352, "lon": 77.6245, "category": "Electronics"},
        {"store_id": "LOC_03", "name": "Suburban Express", "lat": 13.0358, "lon": 77.5970, "category": "Grocery"},
        {"store_id": "LOC_04", "name": "High Street Outlet", "lat": 12.9250, "lon": 77.5898, "category": "Dining"},
    ]
    
    records = []
    for _ in range(num_records):
        loc = np.random.choice(locations)
        timestamp = base_time + timedelta(
            days=int(np.random.randint(0, 7)),
            hours=int(np.random.randint(8, 22)),
            minutes=int(np.random.randint(0, 60))
        )
        dwell_time = min(int(np.random.exponential(scale=25) + 5), 180)
        footfall_count = np.random.poisson(lam=15)
        
        records.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "store_id": loc["store_id"],
            "store_name": loc["name"],
            "category": loc["category"],
            "latitude": loc["lat"] + np.random.normal(0, 0.001),
            "longitude": loc["lon"] + np.random.normal(0, 0.001),
            "dwell_time_mins": dwell_time,
            "footfall": footfall_count
        })
        
    df = pd.DataFrame(records)
    df.to_csv("data/retail_mobility_data.csv", index=False)
    print("Dataset generated: data/retail_mobility_data.csv")

if __name__ == "__main__":
    generate_mobility_data()