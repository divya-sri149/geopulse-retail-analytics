import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_insights(data_path="data/cleaned_mobility_data.csv"):
    df = pd.read_csv(data_path)
    sns.set_theme(style="whitegrid")

    # 1. Store Performance Summary
    store_summary = df.groupby(["store_name", "category"]).agg(
        total_footfall=("footfall", "sum"),
        avg_dwell_mins=("dwell_time_mins", "mean"),
        visit_records=("footfall", "count")
    ).reset_index().sort_values(by="total_footfall", ascending=False)

    print("\n--- Store Performance Summary ---")
    print(store_summary.to_string(index=False))

    # 2. Generate Weekday vs Weekend Footfall Chart
    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=df,
        x="time_slot",
        y="footfall",
        hue="is_weekend",
        estimator=sum,
        errorbar=None,
        palette=["#2b5cff", "#ff6b4a"]
    )
    plt.title("Total Footfall by Time Slot (Weekday vs. Weekend)")
    plt.xlabel("Time Window")
    plt.ylabel("Total Observed Footfall")
    plt.legend(title="Is Weekend")
    plt.tight_layout()
    plt.savefig("reports/footfall_by_timeslot.png", dpi=300)
    plt.close()

    # 3. Generate Dwell Time Distribution by Category
    plt.figure(figsize=(10, 5))
   