import streamlit as st  # pyright: ignore[reportMissingImports]
import pandas as pd
import plotly.express as px  # pyright: ignore[reportMissingImports]
from utils import calculate_piotroski_score
from utils import get_stock_info
from utils import calculate_scores
from utils import get_recommendation

st.header("Portfolio Tracker")

portfolio_input = st.text_area(
    "Enter holdings (Ticker,Shares)",
    "AAPL,10\nMSFT,5\nGOOG,3"
)

if st.button("Analyze Portfolio"):

    portfolio_data = []

    total_value = 0
    weighted_score = 0
    weighted_expected_return = 0
    covered_value = 0

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
                st.warning(
                    f"{ticker_symbol} not found"
                )
                continue

        except Exception:
            st.warning(
                f"Could not load {ticker_symbol}"
            )
            continue

        price = info.get("currentPrice", 0)

        holding_value = price * shares

        target_price = info.get("targetMeanPrice")

        expected_return = None

        if(target_price is not None and price > 0):
            expected_return = ((target_price - price)/ price)*100

        growth, quality, strength, valuation, health, overall = (
            calculate_scores(info)
        )
        piotroski_score=calculate_piotroski_score(info)

        total_value += holding_value

        weighted_score += (
            overall * holding_value
        )
        if expected_return is not None:
            weighted_expected_return+=(expected_return * holding_value)
            covered_value += holding_value

        portfolio_data.append({
            "Ticker": ticker_symbol,
            "Shares": shares,
            "Price": round(price, 2),
            "Value": round(holding_value, 2),
            "Piotroski Score": piotroski_score,
            "Expected Return %":(round(expected_return,2)if expected_return is not None
                                 else None),
            "Score": overall
        })

    portfolio_df = pd.DataFrame(portfolio_data)

    if portfolio_df.empty:
        st.warning(
            "No valid holdings found."
        )
        st.stop()

    portfolio_df["Allocation %"] = (
        portfolio_df["Value"]
        / total_value
        * 100
    ).round(2)

    avg_piotroski = round(portfolio_df["Piotroski Score"].mean(),1)
    coverage_pct = round((covered_value/total_value)*100,1)if total_value>0 else 0

    portfolio_score = round(
        weighted_score / total_value,
        1
    ) if total_value > 0 else 0

    portfolio_expected_return = round(
        weighted_expected_return / covered_value,
        2
        ) if covered_value > 0 else 0

    st.subheader("Portfolio Holdings")

    st.dataframe(
        portfolio_df,
        width="stretch"
    )

    csv = portfolio_df.to_csv(index=False)

    st.download_button(
        "📥 Download Portfolio",
        csv,
        "portfolio.csv",
        "text/csv"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Portfolio Value",
            f"${total_value:,.2f}"
        )

    with col2:
        st.metric(
            "Portfolio Score",
            portfolio_score
        )
    
    with col3:
        st.metric("Avg Piotroski",f"{avg_piotroski}/9")
    
    with col4:
        st.metric("Expected Return",f"{portfolio_expected_return:.2f}%")
    portfolio_recommendation = (
        get_recommendation(portfolio_score)
    )
    with col5:
        st.metric("Analyst Coverage",f"{coverage_pct}%")

    st.subheader(
        "Portfolio Recommendation"
    )

    st.success(
        portfolio_recommendation
    )

    st.subheader(
        "Portfolio Allocation"
    )

    fig = px.pie(
        portfolio_df,
        names="Ticker",
        values="Value",
        title="Portfolio Allocation"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    if portfolio_expected_return >= 20:

        st.success(
            "Portfolio has strong expected upside."
        )

    elif portfolio_expected_return >= 10:

        st.info(
            "Portfolio has moderate expected upside."
        )

    elif portfolio_expected_return >= 0:

        st.info(
            "Portfolio has limited expected upside."
        )

    else:

        st.warning(
            "Analysts expect portfolio downside."
        )