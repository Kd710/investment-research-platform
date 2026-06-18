import streamlit as st # pyright: ignore[reportMissingImports]
import yfinance as yf # pyright: ignore[reportMissingImports]
import pandas as pd
from utils import get_recommendation
from utils import get_stock_info
from utils import calculate_piotroski_score
from utils import calculate_scores
from utils import calculate_earnings_quality
st.header("Company Ranking System")

tickers_input = st.text_input(
    "Enter tickers separated by commas",
    "AAPL,MSFT,GOOG,AMZN,NVDA"
)

if st.button("Rank Companies"):

    tickers = [
        t.strip()
        for t in tickers_input.split(",")
    ]

    results = []

    for ticker_symbol in tickers:

        info = get_stock_info(ticker_symbol)

        if not info:
            st.warning(f"{ticker_symbol} not found")
            continue

        growth, quality, strength, valuation, health, overall = (
            calculate_scores(info)
        )
        piotroski_score = calculate_piotroski_score(info)
        earnings_quality= calculate_earnings_quality(info)


        recommendation = get_recommendation(overall)

        results.append({
            "Ticker": ticker_symbol,
            "Company": info.get(
                "longName",
                ticker_symbol
            ),
            "Growth Score": growth,
            "Quality Score": quality,
            "Strength Score": strength,
            "Valuation Score": valuation,
            "Health Score": health,
            "Overall Score": overall,
            "Piotroski Score": piotroski_score,
            "Earnings Quality": earnings_quality,
            "Recommendation": recommendation
        })

    ranking_df = pd.DataFrame(results)

    if ranking_df.empty:
        st.warning("No valid stocks found.")
        st.stop()

    ranking_df = ranking_df.sort_values(
        "Overall Score",
        ascending=False
    )

    ranking_df.reset_index(
        drop=True,
        inplace=True
    )

    ranking_df.index += 1

    st.dataframe(
        ranking_df,
        width="stretch"
    )
    csv = ranking_df.to_csv(index=False)

    st.download_button(
        "📥 Download Rankings",
        csv,
        "rankings.csv",
        "text/csv"
)
