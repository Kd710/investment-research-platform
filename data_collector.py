import yfinance as yf # pyright: ignore[reportMissingImports]


def get_company_data(ticker):
    from utils import get_stock_info

    info = get_stock_info(ticker)

    return {
        "name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),

        "currentPrice": info.get("currentPrice"),
        "marketCap": info.get("marketCap"),

        "trailingPE": info.get("trailingPE"),
        "forwardPE": info.get("forwardPE"),
        "pegRatio": info.get("pegRatio"),

        "returnOnEquity": info.get("returnOnEquity"),
        "returnOnAssets": info.get("returnOnAssets"),

        "revenueGrowth": info.get("revenueGrowth"),
        "earningsGrowth": info.get("earningsGrowth"),

        "profitMargins": info.get("profitMargins"),

        "debtToEquity": info.get("debtToEquity"),

        "currentRatio": info.get("currentRatio"),
        "quickRatio": info.get("quickRatio"),

        "freeCashflow": info.get("freeCashflow"),
        "operatingCashflow": info.get("operatingCashflow"),

        "recommendationKey": info.get("recommendationKey"),
        "targetMeanPrice": info.get("targetMeanPrice")
    }