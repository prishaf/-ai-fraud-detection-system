import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="AI Fraud Dashboard", layout="wide")
st.title("🔥 AI Real-Time Fraud Detection Dashboard")

# Auto refresh every 2 seconds
st_autorefresh(interval=5000, key="refresh")

# Fetch data
try:
    response = requests.get("http://localhost:8000/events")
    data = response.json()
except:
    st.error("Cannot connect to FastAPI")
    st.stop()

if not data:
    st.warning("Waiting for fraud events...")
    st.stop()

df = pd.DataFrame(data)

# Ensure timestamp format
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

# =======================
# 🔹 METRICS SECTION
# =======================

total = len(df)
high = len(df[df["risk"] == "HIGH"])
avg = round(df["fraud_score"].mean(), 2)
loss = df[df["risk"] == "HIGH"]["amount"].sum()
fraud_rate = round((high / total) * 100, 2)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Events", total)
c2.metric("High Risk", high)
c3.metric("Avg Fraud Score", avg)
c4.metric("Potential Loss ₹", round(loss, 2))
c5.metric("Fraud Rate %", fraud_rate)

if high > 0:
    st.error(f"🚨 {high} HIGH risk transactions detected!")

# =======================
# 🔹 PIE & BAR CHARTS
# =======================

left, right = st.columns(2)

with left:
    fig1 = px.pie(df, names="risk", hole=0.6, title="Risk Distribution")
    st.plotly_chart(fig1, use_container_width=True)

with right:
    fig2 = px.bar(
        df["location"].value_counts(),
        title="Fraud by Location"
    )
    st.plotly_chart(fig2, use_container_width=True)

# =======================
# 🔹 FRAUD SCATTER
# =======================

st.subheader("📊 Fraud Scatter Analysis")
fig3 = px.scatter(
    df,
    x="amount",
    y="fraud_score",
    color="risk",
    title="Amount vs Fraud Score"
)
st.plotly_chart(fig3, use_container_width=True)

# =======================
# 🔹 FRAUD TREND LINE
# =======================

if "timestamp" in df.columns:
    st.subheader("📈 Fraud Score Trend Over Time")
    df_sorted = df.sort_values("timestamp")
    fig_trend = px.line(
        df_sorted,
        x="timestamp",
        y="fraud_score",
        title="Fraud Score Timeline"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# =======================
# 🔹 FRAUD RATE GAUGE
# =======================

st.subheader("🎯 Fraud Risk Gauge")

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=fraud_rate,
    title={"text": "Fraud Rate %"},
    gauge={
        "axis": {"range": [0, 100]},
        "steps": [
            {"range": [0, 30], "color": "green"},
            {"range": [30, 70], "color": "orange"},
            {"range": [70, 100], "color": "red"},
        ],
    }
))

st.plotly_chart(fig_gauge, use_container_width=True)

# =======================
# 🔹 TOP RISK USERS
# =======================

if "user_id" in df.columns:
    st.subheader("👤 Top Risk Users")

    top_users = (
        df.groupby("user_id")["fraud_score"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    st.dataframe(top_users, use_container_width=True)

# =======================
# 🔹 INDIA GEO MAP
# =======================

st.subheader("🗺 Fraud Location Heatmap (India)")

city_coords = {
    "Mumbai": [19.0760, 72.8777],
    "Delhi": [28.7041, 77.1025],
    "Bangalore": [12.9716, 77.5946],
    "Chennai": [13.0827, 80.2707],
    "Kolkata": [22.5726, 88.3639],
    "Hyderabad": [17.3850, 78.4867],
    "Pune": [18.5204, 73.8567],
}

location_data = df["location"].value_counts().reset_index()
location_data.columns = ["city", "count"]

location_data["lat"] = location_data["city"].map(
    lambda x: city_coords.get(x, [None, None])[0]
)
location_data["lon"] = location_data["city"].map(
    lambda x: city_coords.get(x, [None, None])[1]
)

location_data = location_data.dropna()

if not location_data.empty:
    fig_map = px.scatter_mapbox(
        location_data,
        lat="lat",
        lon="lon",
        size="count",
        hover_name="city",
        zoom=4,
        height=500,
        title="Fraud Hotspots in India"
    )

    fig_map.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig_map, use_container_width=True)
