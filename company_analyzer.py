from utils import format_currency, format_percent
def display_company_report(data):

    print("\n" + "=" * 50)
    print(data["name"])
    print("=" * 50)

    print(f"Sector: {data['sector']}")
    print(f"Industry: {data['industry']}")
    print(f"Country: {data['country']}")

    print("\n--- Market Data ---")
    print(f"Current Price: {format_currency(data['currentPrice'])}")
    print(f"Market Cap: {format_currency(data['marketCap'])}")

    print("\n--- Valuation ---")
    print(f"Trailing PE: {data['trailingPE']}")
    print(f"Forward PE: {data['forwardPE']}")
    print(f"PEG Ratio: {data['pegRatio']}")

    print("\n--- Growth ---")
    print(f"Revenue Growth: {data['revenueGrowth']:.2%}")
    print(f"Earnings Growth: {data['earningsGrowth']:.2%}")

    print("\n--- Profitability ---")
    print(f"ROE: {data['returnOnEquity']:.2%}")
    print(f"ROA: {data['returnOnAssets']:.2%}")
    print(f"Profit Margin: {data['profitMargins']:.2%}")

    print("\n--- Financial Health ---")
    print(f"Debt To Equity: {data['debtToEquity']:.2f}")
    print(f"Current Ratio: {data['currentRatio']}")
    print(f"Quick Ratio: {data['quickRatio']}")

    print("\n--- Cash Flow ---")
    print(f"Operating Cash Flow: {format_currency(data['operatingCashflow'])}")
    print(f"Free Cash Flow: {format_currency(data['freeCashflow'])}")

    print("\n--- Analyst View ---")
    print(f"Recommendation: {data['recommendationKey']}")
    print(f"Target Price: ${data['targetMeanPrice']:.2f}")

    print("=" * 50)