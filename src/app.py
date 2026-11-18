import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="GeoPulse Analytics", layout="wide")

st.title("GeoPulse: Hyper-Local Retail Mobility Analytics")
st.markdown("Footfall patterns, dwell times, and spatial visitor distribution across retail locations.")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/cleaned_mobility_data.csv")
    except FileNotFoundError:
        df = pd.read_csv("data/retail_mobility_data.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    if "day_of_week" not in df.columns:
        df["day_of_week"] = df["timestamp"].dt.day_name()
    return df

try:
    df = load_data()
except Exception:
    st.error("Dataset not found. Run `python src/generate_data.py` and `python src/data_cleaner.py` first.")
    st.stop()

# Sidebar Filters & Data Export
st.sidebar.header("Filter Criteria")
categories = ["All"] + sorted(df["category"].unique().tolist())
selected_category = st.sidebar.selectbox("Retail Category", categories)

filtered_df = df if selected_category == "All" else df[df["category"] == selected_category]

st.sidebar.markdown("---")
st.sidebar.subheader("Export Report")
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="Download Filtered CSV",
    data=csv_data,
    file_name=f"geopulse_{selected_category.lower()}_report.csv",
    mime="text/csv"
)

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Observed Visits", f"{filtered_df['footfall'].sum():,}")
col2.metric("Avg Dwell Time", f"{filtered_df['dwell_time_mins'].mean():.1f} mins")
col3.metric("Unique Locations", f"{filtered_df['store_id'].nunique()}")
col4.metric("Peak Activity Hour", f"{filtered_df['timestamp'].dt.hour.mode()[0]}:00")

# Spatial Map
st.subheader("Hyper-Local Footprint Map")
m = folium.Map(
    location=[filtered_df["latitude"].mean(), filtered_df["longitude"].mean()],
    zoom_start=12,
    tiles="CartoDB positron"
)

store_geo = filtered_df.groupby(["store_name", "category", "latitude", "longitude"])["footfall"].sum().reset_index()
for _, row in store_geo.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=min(max(row["footfall"] / 100, 6), 25),
        popup=f"<b>{row['store_name']}</b><br>Category: {row['category']}<br>Footfall: {row['footfall']}",
        color="#2b5cff",
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

st_folium(m, width=1100, height=420)

# Two-Column Analytical Breakdown
