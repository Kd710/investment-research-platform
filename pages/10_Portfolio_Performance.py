import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd
import plotly.express as px # pyright: ignore[reportMissingImports]
from utils import get_stock_info
st.title("📊 Portfolio Performance Tracker")

portfolio_input = st.text_area(
    "Enter holdings (Ticker,Shares,Purchase Price)",
    "AAPL,10,180\nMSFT,5,420\nGOOG,3,160"
)
if st.button("Analyze Performance"):
    performance_data=[]
    total_cost=0
    total_value=0
    lines=portfolio_input.strip().split("\n")
    for line in lines:

        parts = line.split(",")

        if len(parts) != 3:
            st.warning(
                f"Skipping invalid row: {line}"
            )
            continue

        ticker_symbol, shares, purchase_price = parts

        ticker_symbol = ticker_symbol.strip().upper()

        try:
            shares = float(shares)
            purchase_price = float(purchase_price)
        except:
            st.warning(
                f"Invalid numeric value: {line}"
            )
            continue
        info=get_stock_info(ticker_symbol) # pyright: ignore[reportUndefinedVariable]
        current_price=info.get("currentPrice",0)
        cost_basis=shares*purchase_price
        current_value=shares*current_price
        gain_loss=current_value-cost_basis
        return_pct=(gain_loss/cost_basis*100
        if cost_basis>0
        else 0)
        total_cost+=cost_basis
        total_value+=current_value
        performance_data.append({
                "Ticker": ticker_symbol,
            "Shares": shares,
            "Purchase Price": round(purchase_price, 2),
            "Current Price": round(current_price, 2),
            "Cost Basis": round(cost_basis, 2),
            "Current Value": round(current_value, 2),
            "Gain/Loss": round(gain_loss, 2),
            "Return %": round(return_pct, 2)
        })
    if len(performance_data)==0:
        st.warning("No valid holdings found")
        st.stop()    
    performance_df=pd.DataFrame(performance_data)
    fig=px.pie(performance_df,names="Ticker",values="Current Value",title="Portfolio Allocation")
    st.plotly_chart(fig,width="stretch")
    st.dataframe(performance_df, width="stretch")
    csv = performance_df.to_csv(index=False)
    st.download_button("Downlaod Portfolio Report",csv,"portfolio_report.csv","text/csv") # pyright: ignore[reportUndefinedVariable]
    total_gain_loss=(total_value-total_cost)
    portfolio_return=(total_gain_loss/total_cost*100
    if total_cost>0
    else 0)
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Total invested", f"{total_cost:,.2f}")
    with col2:
        st.metric(
            "Current Value",
            f"${total_value:,.2f}"
        )

    with col3:
        st.metric(
            "Profit/Loss",
            f"${total_gain_loss:,.2f}"
        )

    with col4:
        st.metric(
            "Portfolio Return %",
            f"{portfolio_return:.2f}%"
        )        
    st.subheader("Performance Verdict")
    if portfolio_return>20:
        st.success("Excellent portfolio performance")
    elif portfolio_return>0:
        st.info("Portfolio is currently profitable")    
    else:
        st.warning("Portfolio is currently at a loss")
    best_stock=performance_df.loc[performance_df["Return %"].idxmax()]
    worst_stock = performance_df.loc[performance_df["Return %"].idxmin()]
    st.success(
    f"🏆 Best Performer: "
    f"{best_stock['Ticker']} "
    f"({best_stock['Return %']}%)")
    st.error(
    f"📉 Worst Performer: "
    f"{worst_stock['Ticker']} "
    f"({worst_stock['Return %']}%)")
               
