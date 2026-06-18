import streamlit as st # pyright: ignore[reportMissingImports]
import yfinance as yf # type: ignore
import pandas as pd
from utils import get_stock_info

from utils import percent
st.header("Compare Two Companies")

ticker1 = st.text_input(
    "Company 1",
    "AAPL"
)

ticker2 = st.text_input(
    "Company 2",
    "MSFT"
)

if st.button("Compare"):

    info1 = get_stock_info(ticker1)
    if not info1:
        st.error(f"Invalid ticker: {ticker1}")
        st.stop()
    info2 = get_stock_info(ticker2)
    if not info2:
        st.error(f"Invalid ticker: {ticker2}")
        st.stop()

    comparison = pd.DataFrame({
    "Metric": [
        "Price",
        "PE Ratio",
        "Revenue Growth %",
        "ROE %",
        "Profit Margin %",
        "Debt To Equity"
    ],

        ticker1: [
            info1.get("currentPrice"),
            info1.get("trailingPE"),
            round((info1.get("revenueGrowth") or 0) * 100,2),
            round((info1.get("returnOnEquity") or 0) * 100,2),
            round((info1.get("profitMargins") or 0) * 100,2),
            info1.get("debtToEquity")
        ],

        ticker2: [
            info2.get("currentPrice"),
            info2.get("trailingPE"),
            round((info2.get("revenueGrowth") or 0) * 100,2),
            round((info2.get("returnOnEquity") or 0) * 100,2),
            round((info2.get("profitMargins") or 0) * 100,2),
            info2.get("debtToEquity")
        ]
    })

    st.dataframe(
        comparison,
        width="stretch"
    )
    csv = comparison.to_csv(index=False)

    st.download_button(
        "📥 Download Comparison",
        csv,
        "comparison.csv",
        "text/csv"
    )