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
    df["is_weekend"] = df["timestamp"].dt.dayofweek.isin([5, 6])
    df["hour"] = df["timestamp"].dt.hour
    df["time_slot"] = pd.cut(
        df["hour"],
        bins=[0, 11, 16, 20, 24],
        labels=["Morning (8-11)", "Afternoon (12-16)", "Evening Peak (17-20)", "Night (21+)"],
        right=False
    )

    df.to_csv(output_path, index=False)
    print(f"Validation complete: {len(df)}/{initial_count} valid records saved to {output_path}")
    return df

if __name__ == "__main__":
    clean_and_validate()