import streamlit as st # pyright: ignore[reportMissingImports]
import yfinance as yf # pyright: ignore[reportMissingImports]
import pandas as pd
import time
from utils import get_stock_info
from utils import calculate_scores
from utils import get_recommendation
from utils import calculate_piotroski_score
from utils import calculate_earnings_quality

st.title("🔍 Stock Screener")
market=st.selectbox("Select Market",["US"])

universe=pd.read_csv("datasets/clean_and_final/us_stocks_cleaned.csv")
max_stocks=st.slider("Stocks to Scan",100,2000,500,100)



max_pe = st.number_input(
    "Maximum PE Ratio",
    value=30.0
)

min_roe = st.number_input(
    "Minimum ROE (%)",
    value=10.0
)

min_growth = st.number_input(
    "Minimum Revenue Growth (%)",
    value=5.0
)

min_market_cap = st.number_input(
    "Minimum Market Cap ($ Billions)",
    value=10.0
)



min_score = st.number_input(
    "Minimum Overall Score",
    value=60.0
)

max_debt = st.number_input(
    "Maximum Debt To Equity",
    value=100.0
)

min_margin = st.number_input(
    "Minimum Profit Margin (%)",
    value=5.0
)

min_roa = st.number_input(
    "Minimum ROA (%)",
    value=5.0
)

min_earnings_quality = st.slider("Minimum Earnings Quality",0,3,2)

min_piotroski_score=st.slider("Minimum Piotroski Score",0,9,5)
if st.button("Run Screener"):
    start_time=time.time()
    results = []

    tickers=universe["Ticker"].head(max_stocks)
    progress=st.progress(0)
    for i,ticker in enumerate(tickers):
        
        progress.progress((i+1)/len(tickers))
        try:
            info = get_stock_info(ticker) # pyright: ignore[reportUndefinedVariable]
        except:
            continue    

        pe = info.get("trailingPE")
        roe = info.get("returnOnEquity")
        growth = info.get("revenueGrowth")
        market_cap = info.get("marketCap", 0)
        debt=info.get("debtToEquity")
        margin = info.get("profitMargins")
        roa = info.get("returnOnAssets")

        growth_score, quality_score, strength_score, valuation_score, health_score, overall_score = (
            calculate_scores(info)
        )
        piotroski_score=calculate_piotroski_score(info)
        earnings_quality = calculate_earnings_quality(info)

        if (
            pe is not None
            and roe is not None
            and growth is not None
            and debt is not None
            and margin is not None
            and roa is not None
            and pe <= max_pe
            and roe * 100 >= min_roe
            and growth * 100 >= min_growth
            and debt <= max_debt
            and margin * 100 >= min_margin
            and roa * 100 >= min_roa
            and market_cap >= min_market_cap * 1_000_000_000
            and overall_score >= min_score
        ):

            
            recommendation = get_recommendation(overall_score)
            if piotroski_score<min_piotroski_score:
                continue

            if earnings_quality<min_earnings_quality:
                continue

            results.append({
    "Company":info.get("longName",ticker),            
    "Ticker": ticker,
    "Price": info.get("currentPrice"),
    "Market Cap ($B)": round(
        market_cap / 1_000_000_000,
        2
    ),
    "PE": round(pe, 2),
    "ROE %": round(roe * 100, 2),
    "Revenue Growth %": round(growth * 100, 2),
    "Growth Score": growth_score,
    "Quality Score": quality_score,
    "Strength Score": strength_score,
    "Valuation Score": valuation_score,
    "Health Score": health_score,
    "Overall Score": overall_score,
    "Piotroski Score": piotroski_score,
    "Earnings Quality": earnings_quality,
    "Recommendation": recommendation
})
    progress.empty()
    if len(results)==0:
        st.warning("No stocks matched your criteria.")
        st.stop()
    if results:

        screener_df = pd.DataFrame(results)

        screener_df = screener_df.sort_values(
            "Overall Score",
            ascending=False
        )
        total_matches=len(screener_df)
        st.success(f"{total_matches} stocks matched")
        elapsed=round(time.time()-start_time,2)
        if elapsed>0:
            stocks_per_second=round(max_stocks/elapsed,2)
            st.info(f"Processed{stocks_per_second} stocks/sec")
            st.info(f"Scan completed in {elapsed} seconds")

        screener_df=screener_df.head(20)
        top_stock = screener_df.iloc[0]
        st.subheader("Best Opportunity Found")
        col1,col2,col3=st.columns(3)
        with col1:
            st.metric("Ticker",top_stock["Ticker"])
        with col2:
            st.metric("Score",top_stock["Overall Score"])
        with col3:
            st.metric("Recommendation",top_stock["Recommendation"])
        st.subheader(top_stock["Company"])
        st.write("Price:", top_stock["Price"])
        st.write("Market Cap ($B):", top_stock["Market Cap ($B)"])
        st.write("PE:", top_stock["PE"])
        st.write("ROE %:", top_stock["ROE %"])
        st.write("Revenue Growth %:", top_stock["Revenue Growth %"])
        st.subheader("Top 20 Matches")
        st.dataframe(screener_df,width="stretch")
        csv=screener_df.to_csv(index=False)
        st.download_button(
            "Download Screener Results",csv,"screener_results.csv","text/csv")

    
