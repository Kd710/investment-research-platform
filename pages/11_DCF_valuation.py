import streamlit as st  # pyright: ignore[reportMissingImports]
import yfinance as yf  # pyright: ignore[reportMissingImports]
from utils import get_stock_info
import pandas as pd

st.title("💰 DCF Valuation Calculator")

ticker = st.text_input(
    "Enter Stock Ticker",
    "AAPL"
)

growth_rate = st.slider(
    "Expected Growth Rate (%)",
    0,
    30,
    10
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

if st.button("Calculate DCF"):

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
        st.error("DCF data unavailable.")

    else:

        growth = growth_rate / 100
        discount = discount_rate / 100
        terminal = terminal_growth / 100

        if discount <= terminal:
            st.error(
                "Discount rate must exceed terminal growth rate."
            )
            st.stop()

        total_present_value = 0
        projected_fcf = fcf

        # Forecast FCF
        for year in range(1, years + 1):
            projected_fcf *= (1 + growth)

            discounted_fcf = (
                projected_fcf
                / ((1 + discount) ** year)
            )

            total_present_value += discounted_fcf

        # Terminal Value
        terminal_value = (
            projected_fcf * (1 + terminal)
        ) / (discount - terminal)

        terminal_value_discounted = (
            terminal_value
            / ((1 + discount) ** years)
        )

        total_present_value += terminal_value_discounted

        # Intrinsic Value
        intrinsic_value = (
            total_present_value
            / shares_outstanding
        )

        upside = (
            (intrinsic_value - current_price)
            / current_price
        ) * 100

        margin_of_safety = (
            (intrinsic_value - current_price)
            / intrinsic_value
        ) * 100

        # Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Current Price",
                f"${current_price:.2f}"
            )

        with col2:
            st.metric(
                "Intrinsic Value",
                f"${intrinsic_value:.2f}"
            )

        with col3:
            st.metric(
                "Upside %",
                f"{upside:.2f}%"
            )

        with col4:
            st.metric(
                "Margin of Safety",
                f"{margin_of_safety:.2f}%"
            )

        # Valuation Verdict
        if margin_of_safety >= 40:
            st.success("🟢 Deep Value Opportunity")

        elif margin_of_safety >= 20:
            st.success("🟢 Attractive Valuation")

        elif margin_of_safety >= 0:
            st.info("🟡 Fairly Valued")

        else:
            st.warning("🔴 Overvalued")

        st.write(
            f"The stock trades "
            f"{abs(margin_of_safety):.2f}% "
            f"{'below' if margin_of_safety >= 0 else 'above'} "
            f"its estimated intrinsic value."
        )

        # Sensitivity Analysis
        st.subheader("DCF Sensitivity Analysis")

        sensitivity_data = []

        for scenario, scenario_growth in [
            ("Bear", max(growth - 0.03, 0)),
            ("Base", growth),
            ("Bull", growth + 0.03)
        ]:

            pv = 0
            projected = fcf

            for year in range(1, years + 1):

                projected *= (1 + scenario_growth)

                pv += (
                    projected
                    / ((1 + discount) ** year)
                )

            terminal_value = (
                projected * (1 + terminal)
            ) / (discount - terminal)

            terminal_value_discounted = (
                terminal_value
                / ((1 + discount) ** years)
            )

            pv += terminal_value_discounted

            intrinsic = (
                pv
                / shares_outstanding
            )

            sensitivity_data.append({
                "Scenario": scenario,
                "Growth Rate (%)": round(
                    scenario_growth * 100,
                    2
                ),
                "Intrinsic Value": round(
                    intrinsic,
                    2
                )
            })

        sensitivity_df = pd.DataFrame(
            sensitivity_data
        )

        st.dataframe(
            sensitivity_df,
            width="stretch"
        )

        # Export
        csv = sensitivity_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Sensitivity Analysis",
            csv,
            file_name=f"{ticker}_dcf_sensitivity.csv",
            mime="text/csv"
        )
