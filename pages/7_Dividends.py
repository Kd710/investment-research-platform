import streamlit as st # pyright: ignore[reportMissingImports]
import yfinance as yf # pyright: ignore[reportMissingImports]
import pandas as pd
import plotly.express as px # pyright: ignore[reportMissingImports]
from utils import get_stock_info
st.title("💰 Dividend Dashboard")

portfolio_input = st.text_area(
    "Enter holdings (Ticker,Shares)",
    "AAPL,10\nMSFT,5\nKO,20"
)
if st.button("Analyze Dividends"):

    dividend_data = []

    total_income = 0

    lines = portfolio_input.strip().split("\n")

    for line in lines:

        parts = line.split(",")

        if len(parts) != 2:
            st.warning(
                f"Skipping invalid row: {line}"
            )
            continue

        ticker_symbol, shares = parts

        ticker_symbol = ticker_symbol.strip().upper()

        try:
            shares = float(shares)
        except:
            st.warning(
                f"Invalid numeric value: {line}"
            )
            continue

        try:
            info = get_stock_info(ticker_symbol)

            if not info:
                continue

        except Exception:
            continue

        dividend_rate = info.get(
            "dividendRate",
            0
        )

        dividend_yield = info.get(
            "dividendYield",
            0
        )

        annual_income = (
            dividend_rate * shares
        )

        total_income += annual_income

        dividend_data.append({
            "Ticker": ticker_symbol,
            "Shares": shares,
            "Dividend/Share": dividend_rate,
            "Yield %": round(
                dividend_yield * 100,
                2
            ) if dividend_yield else 0,
            "Annual Income": round(
                annual_income,
                2
            )
        })
    dividend_df = pd.DataFrame(
        dividend_data
    )

    if dividend_df.empty:
        st.warning("No valid dividend holdings found.")
        st.stop()

    st.dataframe(
        dividend_df,
        width="stretch"
    )

    st.metric(
        "Estimated Annual Dividend Income",
        f"${total_income:,.2f}"
    )

    st.metric(
        "Estimated Monthly Income",
        f"${total_income/12:,.2f}"
    )        
    if total_income > 5000:
        st.success(
            "Strong dividend income portfolio."
        )

    elif total_income > 1000:
        st.info(
            "Moderate dividend income portfolio."
        )

    else:
        st.warning(
            "Limited dividend income."
        )
    fig=px.pie(
        dividend_df,
        names="Ticker",
        values="Annual Income",
        title="Dividend Income Sources"
    )    
    st.plotly_chart(
        fig,
        width="stretch"
    )
