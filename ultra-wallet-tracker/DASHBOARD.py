import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ultra Wallet Tracker", layout="wide")

# Optional: Compact styling
st.markdown("""
    <style>
    h1, h2, h3, h4, h5 {
        font-size: 1.25rem !important;
    }
    .stMetric {
        font-size: 0.9rem !important;
    }
    .css-1d391kg {
        font-size: 0.85rem !important;
    }
    .element-container {
        padding-top: 0.25rem !important;
        padding-bottom: 0.25rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title and intro
st.title("🔍 Ultra Wallet Creation Dashboard")
st.caption("Visualizing new wallet activity on the Ultra blockchain")

# Load CSV
csv_path = os.path.join("data", "wallet_growth_timeseries.csv")

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Add cumulative total
    df["cumulative_wallets"] = df["wallets_created"].cumsum()
    total_wallets = int(df["wallets_created"].sum())

    # --- Metric Row ---
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("🧾 Total Wallets Created", f"{total_wallets:,}")
        with col2:
            st.metric("📅 Date Range", f"{df['date'].min().date()} → {df['date'].max().date()}")

    st.markdown("---")

    # --- Chart Row ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Daily Wallet Creation (Histogram)")
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(df["date"], df["wallets_created"], color="#1f77b4", width=1)
        ax.set_xlabel("Date")
        ax.set_ylabel("Count")
        ax.set_title("Daily Creations", fontsize=10)
        st.pyplot(fig)

    with col2:
        st.subheader("📈 Cumulative Wallets Over Time")
        st.line_chart(df.set_index("date")["cumulative_wallets"])

    st.markdown("---")

    # --- Data Table ---
    st.subheader("🗃️ Daily Data Table")
    st.dataframe(df[::-1], use_container_width=True)

else:
    st.warning("No data available. Run the tracker script first.")
