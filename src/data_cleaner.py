import pandas as pd

def clean_and_validate(input_path="data/retail_mobility_data.csv", output_path="data/cleaned_mobility_data.csv"):
    df = pd.read_csv(input_path)
    initial_count = len(df)

    # 1. Drop duplicates and missing critical fields
    df = df.drop_duplicates()
    df = df.dropna(subset=["timestamp", "store_id", "latitude", "longitude", "footfall"])

    # 2. Validate coordinate boundaries and positive metrics
    df = df[(df["latitude"].between(-90, 90)) & (df["longitude"].between(-180, 180))]
    df = df[(df["footfall"] >= 0) & (df["dwell_time_mins"] > 0)]

    # 3. Feature Engineering for temporal pattern analysis
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["day_of_week"] = df["timestamp"].dt.day_name()
 