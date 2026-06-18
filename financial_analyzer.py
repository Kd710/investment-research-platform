from utils import get_stock_info
import yfinance as yf # pyright: ignore[reportMissingImports]
def get_value(df,row_name):
    try:
        return df.loc[row_name].iloc[0]
    except:
        return None
def get_financial_summary(ticker):
    info=get_stock_info(ticker)
    stock = yf.Ticker(ticker)

    financials=stock.financials # pyright: ignore[reportUndefinedVariable]
    balance_sheet=stock.balance_sheet # pyright: ignore[reportUndefinedVariable]
    cashflow=stock.cashflow # pyright: ignore[reportUndefinedVariable]
    summary={}
    try:
        summary["Revenue"] = financials.loc["Total Revenue"].iloc[0]
    except:
        summary["Revenue"]=None
    try: 
        summary["Gross Profit"] = financials.loc["Gross Profit"].iloc[0]  
    except:
        summary["Gross Profit"]=None
    try:
        summary["Net Income"] = financials.loc["Net Income"].iloc[0]
    except:
        summary["Net Income"]=None
    try:
        summary["Total Assets"] = balance_sheet.loc["Total Assets"].iloc[0]
    except:
        summary["Total Assets"] = None
    try:
        summary["Total Debt"] = balance_sheet.loc["Total Debt"].iloc[0]
    except:
        summary["Total Debt"] = None

    try:
        summary["Cash"] = balance_sheet.loc["Cash And Cash Equivalents"].iloc[0]
    except:
        summary["Cash"] = None

    try:
        summary["Operating Cash Flow"] = cashflow.loc["Operating Cash Flow"].iloc[0]
    except:
        summary["Operating Cash Flow"] = None

    try:
        summary["Free Cash Flow"] = cashflow.loc["Free Cash Flow"].iloc[0]
    except:
        summary["Free Cash Flow"] = None

    return summary    
