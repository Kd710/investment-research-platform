import streamlit as st # pyright: ignore[reportMissingImports]
import yfinance as yf # pyright: ignore[reportMissingImports]
import pandas as pd
import plotly.express as px # pyright: ignore[reportMissingImports]
from utils import get_stock_info
st.title("⚠️ Portfolio Risk Dashboard")

portfolio_input = st.text_area(
    "Enter holdings (Ticker,Shares)",
    "AAPL,10\nMSFT,5\nGOOG,3"
)

if st.button("Analyze Risk"):

    portfolio_data = []
    total_value = 0

    large_cap_value = 0
    mid_cap_value = 0
    small_cap_value = 0
    portfolio_beta_numerator = 0

    sector_data = {}

    for line in portfolio_input.strip().split("\n"):

        parts=line.split(",")
        if len(parts)!=2:
            st.warning(f"Skipping invalid row: {line}")
            continue
        ticker_symbol,shares=parts
        ticker_symbol=ticker_symbol.strip().upper()
        try:
            shares=float(shares)
        except:
            st.warning(f"Invalid shares value: {line}")
            continue


        info = get_stock_info(ticker_symbol) # pyright: ignore[reportUndefinedVariable]

        price = info.get("currentPrice", 0)
        market_cap = info.get("marketCap", 0)
        sector = info.get("sector", "Unknown")
        beta = info.get("beta",1)

        holding_value = price * shares
        portfolio_beta_numerator+=(beta*holding_value)

        total_value += holding_value

        # Market Cap Classification

        if market_cap >= 10_000_000_000:
            cap_category = "Large Cap"
            large_cap_value += holding_value

        elif market_cap >= 2_000_000_000:
            cap_category = "Mid Cap"
            mid_cap_value += holding_value

        else:
            cap_category = "Small Cap"
            small_cap_value += holding_value

        # Sector Exposure

        if sector not in sector_data:
            sector_data[sector] = 0

        sector_data[sector] += holding_value

        portfolio_data.append({
            "Ticker": ticker_symbol,
            "Value": holding_value,
            "Sector": sector,
            "Market Cap Group": cap_category
        })
    
    portfolio_df=pd.DataFrame(portfolio_data)
    if portfolio_df.empty:
        st.warning("No valid holdings found.")
        st.stop()
    portfolio_df["Allocation %"]=(portfolio_df["Value"]/total_value *100).round(2)
    portfolio_beta=round(portfolio_beta_numerator/total_value,2)
    # ====================
    # Risk Metrics
    # ====================

    largest_position = max(
        row["Value"]
        for row in portfolio_data
    )

    largest_position_pct = round(
        largest_position / total_value * 100,
        2
    )

    diversification_score = round(
    100 - largest_position_pct,
    1
)

    if diversification_score > 100:
        diversification_score = 100

    # ====================
    # Market Cap Exposure
    # ====================

    large_cap_pct = round(
        large_cap_value / total_value * 100,
        2
    )

    mid_cap_pct = round(
        mid_cap_value / total_value * 100,
        2
    )

    small_cap_pct = round(
        small_cap_value / total_value * 100,
        2
    )

    # ====================
    # Sector Exposure
    # ====================

    sector_df = pd.DataFrame({
        "Sector": sector_data.keys(),
        "Value": sector_data.values()
    })

    sector_df["Allocation %"] = (
        sector_df["Value"]
        / total_value
        * 100
    ).round(2)
    largest_sector=sector_df.loc[sector_df["Allocation %"].idxmax()]
    if largest_sector["Allocation %"]>40:
        st.warning(f"{largest_sector['Sector']} accounts for "
        f"{largest_sector['Allocation %']}% "
        f"of the portfolio."
    )

    # ====================
    # Risk Rating
    # ====================

    if portfolio_beta > 1.3:
        risk_rating = "AGGRESSIVE"

    elif small_cap_pct > 40:
        risk_rating = "AGGRESSIVE"

    elif largest_position_pct > 40:
        risk_rating = "CONCENTRATED"

    elif large_cap_pct > 70 and portfolio_beta < 1:
        risk_rating = "CONSERVATIVE"

    else:
        risk_rating = "MODERATE"

    # ====================
    # Display Metrics
    # ====================

    st.header("Risk Summary")

    c1, c2, c3,c4 = st.columns(4)

    with c1:
        st.metric(
            "Largest Position %",
            f"{largest_position_pct}%"
        )

    with c2:
        st.metric(
            "Diversification Score",
            diversification_score
        )

    with c3:
        st.metric(
            "Risk Rating",
            risk_rating
        )
    with c4:
        st.metric("Portfolio Beta",
                  portfolio_beta)

    # ====================
    # Market Cap Exposure
    # ====================
    st.subheader("Position Allocation")
    st.dataframe(portfolio_df[["Ticker", "Allocation %"]].sort_values("Allocation %",ascending=False),width="stretch")
    largest_stock=portfolio_df.loc[portfolio_df["Allocation %"].idxmax()]
    if largest_stock["Allocation %"]>25:
        st.warning(f"{largest_stock['Ticker']} represents"
                   f"{largest_stock['Allocation %']} %"
                   f"of the portfolio")


    st.subheader("Market Cap Exposure")

    cap_df = pd.DataFrame({
        "Category": [
            "Large Cap",
            "Mid Cap",
            "Small Cap"
        ],
        "Allocation": [
            large_cap_pct,
            mid_cap_pct,
            small_cap_pct
        ]
    })

    st.dataframe(cap_df)

    fig1 = px.pie(
        cap_df,
        names="Category",
        values="Allocation",
        title="Market Cap Allocation"
    )

    st.plotly_chart(
        fig1,
        width="stretch"
    )

    # ====================
    # Sector Exposure
    # ====================

    st.subheader("Sector Exposure")

    st.dataframe(
        sector_df,
        width="stretch"
    )

    fig2 = px.pie(
        sector_df,
        names="Sector",
        values="Allocation %",
        title="Sector Allocation"
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

    # ====================
    # Verdict
    # ====================

    st.subheader("Risk Verdict")

    if risk_rating == "CONSERVATIVE":
        st.success(
            "Portfolio is primarily large-cap and relatively stable."
        )

    elif risk_rating == "MODERATE":
        st.info(
            "Portfolio has a balanced risk profile."
        )

    elif risk_rating == "CONCENTRATED":
        st.warning(
            "Portfolio is heavily dependent on one position."
        )

    else:
        st.error(
            "Portfolio has significant small-cap exposure."
        )
    st.subheader("Market Risk")
    if portfolio_beta>1.2:
        st.warning(
        "Portfolio is more volatile than the market."
    )

    elif portfolio_beta < 0.8:
        st.success(
            "Portfolio is relatively defensive."
        )

    else:
        st.info(
            "Portfolio risk is close to the overall market."
        )
            