# ==================================================
# SINGLE COMPANY ANALYZER
# ==================================================
from utils import get_stock_info
import streamlit as st # pyright: ignore[reportMissingImports]
import yfinance as yf # pyright: ignore[reportMissingImports]

from utils import (
    percent,
    billions,
    calculate_scores,
    get_recommendation,
    calculate_piotroski_score,
    calculate_earnings_quality
)

st.header("Single Company Analysis")

ticker = st.text_input(
    "Enter Stock Ticker",
    value="AAPL"
)

if st.button("Analyze"):

    info=get_stock_info(ticker) # pyright: ignore[reportUndefinedVariable]
    if not info:
        st.error("Invalid ticker symbol")
        st.stop()
    stock=yf.Ticker(ticker)
    target_price = info.get("targetMeanPrice")
    current_price = info.get("currentPrice")

    expected_return=None
    if(target_price is not None and current_price is not None and current_price>0):
        expected_return=((target_price-current_price)/current_price)*100

    

    st.subheader(info.get("longName", ticker))

    # Company Profile

    st.subheader("Company Profile")
    st.write("Sector:", info.get("sector"))
    st.write("Industry:", info.get("industry"))

    # Valuation

    st.subheader("Valuation")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Price", info.get("currentPrice"))

    with col2:
        st.metric(
            "Market Cap",
            billions(info.get("marketCap"))
        )

    with col3:
        st.metric(
            "PE Ratio",
            info.get("trailingPE")
        )

    with col4:
        st.metric(
            "PEG Ratio",
            info.get("pegRatio")
        )

    st.write("P/B Ratio:", info.get("priceToBook"))

    enterprise_value = info.get("enterpriseValue")
    ebitda = info.get("ebitda")

    ev_ebitda= None

    if(enterprise_value is not None and ebitda is not None and ebitda>0):
        ev_ebitda=enterprise_value/ebitda
        st.write("EV/EBITDA:",round(ev_ebitda,2))

        if ev_ebitda<8:
            st.success(
            "Appears inexpensive on an EV/EBITDA basis."
        )
        elif ev_ebitda < 15:
            st.info(
                "Appears fairly valued on an EV/EBITDA basis."
            )

        else:
            st.warning(
                "Appears expensive on an EV/EBITDA basis."
            )

    else:
        st.info("EV/EBITDA data unavailable.")


    # Growth

    st.subheader("Growth")

    st.write(
        "Revenue Growth:",
        percent(info.get("revenueGrowth"))
    )

    st.write(
        "Earnings Growth:",
        percent(info.get("earningsGrowth"))
    )

    # Quality
 
    st.subheader("Quality")

    st.write(
        "ROE:",
        percent(info.get("returnOnEquity"))
    )

    st.write(
        "Profit Margin:",percent(info.get("profitMargins")))
    st.write("ROA:",percent(info.get("returnOnAssets")))
    # Cash Flow

    st.subheader("Cash Flow")

    st.write(
        "Free Cash Flow:",
        billions(info.get("freeCashflow"))
    )

    st.write(
        "Operating Cash Flow:",
        billions(info.get("operatingCashflow"))
    )

    # Financial Health

    st.subheader("Financial Health")

    st.write(
        "Debt To Equity:",
        info.get("debtToEquity")
    )

    st.write(
        "Current Ratio:",
        info.get("currentRatio")
    )
    st.write("Quick Ratio:",info.get("quickRatio"))

    # Analyst Sentiment

    st.subheader("Analyst Sentiment")

    st.write(
        "Recommendation:",
        info.get("recommendationKey")
    )

    # Scores

    growth_score, quality_score, strength_score,valuation_score,health_score, overall_score = (
        calculate_scores(info)
    )
    piotroski_score=calculate_piotroski_score(info)
    earnings_quality = calculate_earnings_quality(info)

    recommendation=get_recommendation(overall_score)

    st.subheader("Platform Scores")

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        st.metric("Growth Score", growth_score)

    with c2:
        st.metric("Quality Score", quality_score)

    with c3:
        st.metric("Strength Score", strength_score)

    with c4:
        st.metric("Valuation Score",valuation_score)    

    with c5:
        st.metric("Health Score", health_score)
    
    with c6:
        st.metric("Overall Score", overall_score)

    st.subheader("Platform Recommendation")
    st.success(recommendation)
    st.subheader("Overall Score Visual")
    st.progress(overall_score/100)
    market_cap = info.get("marketCap") or 0

    if market_cap >= 10_000_000_000:
        cap_type = "Large Cap"
    elif market_cap >= 2_000_000_000:
        cap_type = "Mid Cap"
    else:
        cap_type = "Small Cap"
    st.subheader("Market Cap Classification")
    st.write("Market Cap Category:", cap_type)
    st.subheader("Dividend Information")

    st.write(
        "Dividend Yield:",
        percent(info.get("dividendYield"))
    )

    st.write(
        "Dividend Rate:",
        info.get("dividendRate")
    )

    st.subheader("Valuation Assessment")
    pe=info.get("trailingPE")
    if pe is not None:
        if pe<15:
            st.success("Appears attractively valued.")
        elif pe<30:
            st.info("Appears fairly valued.")    
        else:
            st.warning("Appears expensive relative to earnings.")
    st.subheader("Financial Strength Assessment")
    debt=info.get("debtToEquity") or 999
    if debt<50:
        st.success("Low debt burden.")
    elif debt<100:
        st.info("Moderate debt burden.")
    else:
        st.warning("High debt burden.")            
    

    st.divider()
    
    st.subheader("Intrinsic Value")

    st.info(
        "DCF valuation available in the DCF Dashboard."
    )
    st.divider()
    st.subheader("Stock Price Chart")
    period=st.selectbox( "Select Time Period",
    ["1mo", "3mo", "6mo", "1y", "5y"])
    history=stock.history(period=period)
    if history.empty:
        st.warning("No price history available.")
        st.stop()
    st.line_chart(history["Close"])
    
    start_price=history["Close"].iloc[0]
    end_price=history["Close"].iloc[-1]
    return_pct=(
        (end_price-start_price)/start_price
    )*100
    st.metric("Period Return",
              f"{return_pct:.2f}%")
    
    st.subheader("Analyst Expectations")
    if expected_return is not None:
        col1,col2=st.columns(2)
        with col1:
            st.metric(
                "Analyst Target Price",
                f"${target_price:.2f}"
            )
        with col2:
            st.metric(
                "Analyst Expected Return",
                f"{expected_return:.2f}%"
            )   
    if expected_return is not None:

        if expected_return >= 20:
            st.success(
                "Analysts expect strong upside."
            )

        elif expected_return >= 10:
            st.info(
                "Analysts expect moderate upside."
            )

        elif expected_return >= 0:
            st.info(
                "Analysts expect limited upside."
            )

        else:
            st.warning(
                "Analysts expect downside."
            )        
    else:st.info("No analyst target price available")    

    if expected_return is not None:

        if expected_return > 20 and overall_score > 70:
            st.success("High-conviction opportunity")

    st.subheader("Piotroski Score")
    st.metric("Piotroski Score", f"{piotroski_score}/9")
    if piotroski_score>=7:
        st.success("Storng Financial Quality")
    elif piotroski_score>=4:
        st.info("Average Financial Quality")
    else:
        st.warning("Weak Financial Quality")
    
    st.subheader("Earnings Quality")
    st.metric("Earning Quality",f"{earnings_quality}/3")
    
    if earnings_quality==3:
        st.success("Excellent earnings quality")
    elif earnings_quality == 2:

        st.info(
            "Good earnings quality."
        )

    elif earnings_quality == 1:

        st.warning(
            "Weak earnings quality."
        )

    else:

        st.error(
            "Poor earnings quality."
        )