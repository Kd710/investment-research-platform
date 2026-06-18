import yfinance as yf # pyright: ignore[reportMissingImports]
import pandas as pd
import streamlit as st # pyright: ignore[reportMissingImports]
import plotly.express as px # pyright: ignore[reportMissingImports]
st.title("📈 Investment Research Platform")

st.write(
    "Analyze companies, compare stocks, rank investments and track portfolios."
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Stocks Database",
        "10,400+"
    )

with col2:
    st.metric(
        "Analysis Tools",
        "11"
    )

with col3:
    st.metric(
        "Markets Supported",
        "US"
    )

st.divider()

st.subheader("Available Tools")

st.markdown("""
- 🔍 Stock Screener
- 📊 Portfolio Performance Tracker
- ⚠️ Portfolio Risk Dashboard
- 💰 DCF Valuation Calculator
- 👀 Watchlist Dashboard
- 🏆 Company Rankings
- ⚖️ Company Comparison
- 📈 Single Company Analysis
- 💵 Dividend Analyzer
- 📰 Stock News Dashboard
""")

if st.sidebar.button("Clear Cache"):
    st.cache_data.clear()
    st.sidebar.success("Cache Cleared")

st.divider()

st.caption(
    "Data Source: Yahoo Finance | "
    "For educational purposes only. "
    "Not investment advice."
)