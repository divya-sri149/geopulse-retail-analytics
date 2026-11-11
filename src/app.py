# src/app.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="GeoPulse Analytics", layout="wide")

st.title("GeoPulse: Hyper-Local Retail Mobility Analytics")
st.markdown("Real-time footfall patterns, dwell times, and spatial visitor distribution across store locations.")

@st.cache_data
def load_data():
    df = pd.read_csv("data/retail_mobility_data.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

try:
    df = load_data()
except Exception:
    st.error("Dataset not found. Please run `python src/generate_data.py` first.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter Criteria")
categories = ["All"] + sorted(df["category"].unique().tolist())
selected_category = st.sidebar.selectbox("Retail Category", categories)

if selected_category != "All":
    filtered_df = df[df["category"] == selected_category]
else:
    filtered_df = df

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Observed Visits", f"{filtered_df['footfall'].sum():,}")
col2.metric("Avg Dwell Time", f"{filtered_df['dwell_time_mins'].mean():.1f} mins")
col3.metric("Unique Locations", f"{filtered_df['store_id'].nunique()}")
col4.metric("Peak Activity Hour", f"{filtered_df['timestamp'].dt.hour.mode()[0]}:00")

# Spatial Map
st.subheader("Hyper-Local Footprint Map")
center_lat = filtered_df["latitude"].mean()
center_lon = filtered_df["longitude"].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="CartoDB positron")

for _, row in filtered_df.groupby(["store_name", "category", "latitude", "longitude"])["footfall"].sum().reset_index().iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=min(max(row["footfall"] / 100, 6), 25),
        popup=f"<b>{row['store_name']}</b><br>Footfall: {row['footfall']}",
        color="#2b5cff",
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

st_folium(m, width=1100, height=450)

# Aggregated Visualizations
st.subheader("Hourly Footfall Trend")
hourly_trends = filtered_df.copy()
hourly_trends["hour"] = hourly_trends["timestamp"].dt.hour
chart_data = hourly_trends.groupby("hour")["footfall"].sum()
st.bar_chart(chart_data)