import streamlit as st # pyright: ignore[reportMissingImports]
from utils import get_stock_info

st.title("🔄 Reverse DCF")

ticker = st.text_input(
    "Enter Stock Ticker",
    "AAPL"
)

discount_rate = st.slider(
    "Discount Rate (%)",
    1,
    20,
    10
)

terminal_growth = st.slider(
    "Terminal Growth Rate (%)",
    0,
    5,
    3
)

years = st.slider(
    "Forecast Years",
    1,
    10,
    5
)

if st.button("Calculate Implied Growth"):

    info = get_stock_info(ticker)

    if not info:
        st.error("Invalid ticker")
        st.stop()

    fcf = info.get("freeCashflow")
    shares_outstanding = info.get("sharesOutstanding")
    current_price = info.get("currentPrice")

    if (
        fcf is None
        or shares_outstanding is None
        or current_price is None
    ):
        st.error("Required data unavailable.")
        st.stop()

    discount = discount_rate / 100
    terminal = terminal_growth / 100

    if discount <= terminal:
        st.error(
            "Discount rate must exceed terminal growth rate."
        )
        st.stop()

    best_growth = None
    smallest_difference = float("inf")

    # Search from 0% to 50% growth
    for growth_pct in range(-10, 101):

        growth = growth_pct / 100

        projected_fcf = fcf
        total_present_value = 0

        for year in range(1, years + 1):

            projected_fcf *= (1 + growth)

            discounted_fcf = (
                projected_fcf
                / ((1 + discount) ** year)
            )

            total_present_value += discounted_fcf

        terminal_value = (
            projected_fcf * (1 + terminal)
        ) / (discount - terminal)

        terminal_value_discounted = (
            terminal_value
            / ((1 + discount) ** years)
        )

        total_present_value += terminal_value_discounted

        intrinsic_value = (
            total_present_value
            / shares_outstanding
        )

        difference = abs(
            intrinsic_value - current_price
        )

        if difference < smallest_difference:

            smallest_difference = difference
            best_growth = growth_pct

    implied_growth_rate = best_growth

    st.subheader("Reverse DCF Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Current Price",
            f"${current_price:.2f}"
        )

    with col2:
        st.metric(
            "Implied Growth Rate",
            f"{implied_growth_rate:.1f}%"
        )

    revenue_growth = info.get("revenueGrowth")

    if revenue_growth is not None:

        actual_growth = revenue_growth * 100

        st.metric(
            "Current Revenue Growth",
            f"{actual_growth:.1f}%"
        )

        if implied_growth_rate > actual_growth + 5:

            st.warning(
                "Market expectations appear aggressive."
            )

        elif implied_growth_rate < actual_growth - 5:

            st.success(
                "Market expectations appear conservative."
            )

        else:

            st.info(
                "Market expectations appear reasonable."
            )