import pandas as pd
import numpy as np
from datetime import timedelta

def generate_footfall_forecast(data_path="data/cleaned_mobility_data.csv", output_path="data/footfall_forecast.csv", forecast_days=7):
    df = pd.read_csv(data_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["day_of_week"] = df["timestamp"].dt.day_name()

    # Aggregate daily footfall per store
    daily_store = df.groupby(["store_id", "store_name", "category", "date", "day_of_week"]).agg(
        daily_footfall=("footfall", "sum"),
        avg_dwell=("dwell_time_mins", "mean")
    ).reset_index()

    # Compute day-of-week baseline profile per store
    dow_profile = daily_store.groupby(["store_id", "store_name", "category", "day_of_week"]).agg(
        baseline_footfall=("daily_footfall", "mean"),
        expected_dwell=("avg_dwell", "mean")
    ).reset_index()

    # Generate next N days forecast
    last_date = pd.to_datetime(daily_store["date"]).max()
    stores = daily_store[["store_id", "store_name", "category"]].drop_duplicates()

    forecast_records = []
    np.random.seed(42)

   