import streamlit as st # pyright: ignore[reportMissingImports]
import yfinance as yf # pyright: ignore[reportMissingImports]
from utils import get_stock_info
st.title("📰 News Dashboard")

ticker = st.text_input(
    "Enter Stock Ticker",
    "AAPL"
).upper()

if st.button("Get News"):
     
    
    info = get_stock_info(ticker)

    if not info:
        st.error("Invalid ticker")
        st.stop()

    stock = yf.Ticker(ticker)
    news = stock.news

    if not news:

        st.warning("No news found.")

    else:

        for article in news:

            title = article.get(
                "title",
                "No title"
            )

            publisher = article.get(
                "publisher",
                "Unknown Publisher"
            )

            link = article.get("link")

            st.subheader(title)

            st.write(
                f"**Publisher:** {publisher}"
            )

            if link:
                st.markdown(
                    f"[Read Article]({link})"
                )

            st.divider()