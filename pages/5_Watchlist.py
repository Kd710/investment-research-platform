import streamlit as st # pyright: ignore[reportMissingImports]
import yfinance as yf # pyright: ignore[reportMissingImports]
import pandas as pd
from utils import get_stock_info
from utils import calculate_scores
from utils import get_recommendation
from utils import calculate_piotroski_score

st.title("👀 Watchlist Dashboard")

watchlist_input = st.text_input(
    "Enter watchlist tickers separated by commas",
    "AAPL,MSFT,NVDA,GOOG"
)

if st.button("Analyze Watchlist"):

    tickers = [
        t.strip().upper()
        for t in watchlist_input.split(",")
    ]

    watchlist_data = []

    for ticker_symbol in tickers:
        try:
            info = get_stock_info(ticker_symbol) # pyright: ignore[reportUndefinedVariable]
            if not info:
                st.warning(f"{ticker_symbol} not found")
                continue
        except Exception:
            st.warning(f"Could not load {ticker_symbol}")
            continue


        growth, quality, strength, valuation, health, overall = (
            calculate_scores(info)
        )
        piotroski_score= calculate_piotroski_score(info)

        recommendation=get_recommendation(overall)

        watchlist_data.append({
            "Ticker": ticker_symbol,
            "Price": info.get("currentPrice"),
            "Growth Score": growth,
            "Quality Score": quality,
            "Strength Score": strength,
            "Valuation Score": valuation,
            "Overall Score": overall,
            "Piotroski Score": piotroski_score,
            "Recommendation": recommendation
        })

    watchlist_df = pd.DataFrame(watchlist_data)
    if watchlist_df.empty:
        st.warning("No valid stocks found.")
        st.stop()

    watchlist_df = watchlist_df.sort_values(
        "Overall Score",
        ascending=False
    )

    st.dataframe(
        watchlist_df,
        width="stretch"
    )
    csv = watchlist_df.to_csv(index=False)

    st.download_button(
        "📥 Download Watchlist",
        csv,
        "watchlist.csv",
        "text/csv"
    )

    top_stock = watchlist_df.iloc[0]

    st.success(
        f"🏆 Top Pick: {top_stock['Ticker']} "
        f"(Score: {top_stock['Overall Score']})"
    )