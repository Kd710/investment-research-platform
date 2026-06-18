import streamlit as st # type: ignore
import yfinance as yf # pyright: ignore[reportMissingImports]
@st.cache_data(ttl=3600)
def get_stock_info(ticker):
    return yf.Ticker(ticker).info
def format_currency(number):

    if number is None:
        return "N/A"

    if abs(number) >= 1_000_000_000_000:
        return f"${number / 1_000_000_000_000:.2f} Trillion"

    if abs(number) >= 1_000_000_000:
        return f"${number / 1_000_000_000:.2f} Billion"

    if abs(number) >= 1_000_000:
        return f"${number / 1_000_000:.2f} Million"

    return f"${number:,.2f}"


def format_percent(number):

    if number is None:
        return "N/A"

    return f"{number * 100:.2f}%"
def percent(value):
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def billions(value):
    if value is None:
        return "N/A"
    return f"${value / 1_000_000_000:.2f}B"

def score_revenue_growth(growth):

    if growth is None:
        return 0

    if growth < 0:
        return 0
    elif growth < 0.05:
        return 20
    elif growth < 0.10:
        return 40
    elif growth < 0.15:
        return 60
    elif growth < 0.20:
        return 80
    else:
        return 100


def score_earnings_growth(growth):

    if growth is None:
        return 0

    if growth < 0:
        return 0
    elif growth < 0.05:
        return 20
    elif growth < 0.10:
        return 40
    elif growth < 0.15:
        return 60
    elif growth < 0.20:
        return 80
    else:
        return 100


def score_roe(roe):

    if roe is None:
        return 0

    if roe < 0.05:
        return 20
    elif roe < 0.10:
        return 40
    elif roe < 0.15:
        return 60
    elif roe < 0.20:
        return 80
    else:
        return 100


def score_margin(margin):

    if margin is None:
        return 0

    if margin < 0.05:
        return 20
    elif margin < 0.10:
        return 40
    elif margin < 0.20:
        return 60
    elif margin < 0.30:
        return 80
    else:
        return 100


def score_fcf(fcf):

    if fcf is None:
        return 0

    return 100 if fcf > 0 else 0


def score_debt(debt):

    if debt is None:
        return 0

    if debt < 20:
        return 100
    elif debt < 50:
        return 80
    elif debt < 100:
        return 60
    elif debt < 200:
        return 40
    else:
        return 20

def score_roa(roa):

    if roa is None:
        return 0

    if roa < 0.03:
        return 20
    elif roa < 0.07:
        return 40
    elif roa < 0.10:
        return 60
    elif roa < 0.15:
        return 80
    else:
        return 100
    
def score_pb(pb):

    if pb is None or pb <= 0:
        return 0

    if pb < 1:
        return 100
    elif pb < 3:
        return 80
    elif pb < 5:
        return 60
    elif pb < 10:
        return 40
    else:
        return 20


def score_current_ratio(ratio):

    if ratio is None:
        return 0

    if ratio > 2:
        return 100
    elif ratio > 1.5:
        return 80
    elif ratio > 1:
        return 60
    else:
        return 20


def score_pe(pe):

    if pe is None or pe <= 0:
        return 0

    if pe < 15:
        return 100
    elif pe < 25:
        return 80
    elif pe < 35:
        return 60
    elif pe < 50:
        return 40
    else:
        return 20


def score_peg(peg):

    if peg is None or peg <= 0:
        return 0

    if peg < 1:
        return 100
    elif peg < 2:
        return 80
    elif peg < 3:
        return 60
    elif peg < 5:
        return 40
    else:
        return 20


def score_ev_ebitda(enterprise_value, ebitda):

    if (
        enterprise_value is None
        or ebitda is None
        or enterprise_value <= 0
        or ebitda <= 0
    ):
        return 0

    ev_ebitda = enterprise_value / ebitda

    if ev_ebitda < 8:
        return 100
    elif ev_ebitda < 12:
        return 80
    elif ev_ebitda < 15:
        return 60
    elif ev_ebitda < 20:
        return 40
    else:
        return 20

def calculate_piotroski_score(info):
    score = 0
    net_income=info.get("netIncomeToCommon")
    operating_cashflow = info.get("operatingCashflow")
    debt_to_equity = info.get("debtToEquity")
    current_ratio = info.get("currentRatio")
    roa = info.get("returnOnAssets")
    profit_margin = info.get("profitMargins")
    revenue_growth = info.get("revenueGrowth")
    earnings_growth = info.get("earningsGrowth")

    #Profitability

    if net_income is not None and net_income > 0:
        score+=1

    if operating_cashflow is not None and operating_cashflow > 0:
        score+=1
    
    if(operating_cashflow is not None and net_income is not None and operating_cashflow > net_income):
        score+=1

    #Financial Strength

    if debt_to_equity is not None and debt_to_equity < 100:
        score+=1

    if current_ratio is not None and current_ratio > 1.5: 
        score+=1

    #Business Quality

    if roa is not None and roa> 0:
        score+=1

    if profit_margin is not None and profit_margin > 0.1:
        score+=1

    #Growth

    if revenue_growth is not None and revenue_growth > 0:
        score+=1

    if earnings_growth is not None and earnings_growth > 0:
        score+=1

    return score            

def calculate_earnings_quality(info):
    score = 0
    net_income = info.get("netIncomeToCommon")
    operating_cashflow = info.get("operatingCashflow")
    free_cashflow = info.get("freeCashflow")

    if operating_cashflow is not None and operating_cashflow > 0:
        score+=1

    if free_cashflow is not None and free_cashflow>0:
        score+=1

    if(operating_cashflow is not None and net_income is not None and operating_cashflow> net_income):
        score+=1

    return score        




def score_quick_ratio(ratio):

    if ratio is None:
        return 0

    if ratio > 2:
        return 100
    elif ratio > 1.5:
        return 80
    elif ratio > 1:
        return 60
    else:
        return 20
def get_recommendation(score):

    if score >= 85:
        return "STRONG BUY"
    elif score >= 70:
        return "BUY"
    elif score >= 50:
        return "HOLD"
    else:
        return "SELL"
    
def calculate_scores(info):

    growth_score = round(
        (
            score_revenue_growth(
                info.get("revenueGrowth")
            )
            +
            score_earnings_growth(
                info.get("earningsGrowth")
            )
        ) / 2,
        1
    )

    quality_score = round(
    (
        score_roe(info.get("returnOnEquity"))
        +
        score_roa(info.get("returnOnAssets"))
        +
        score_margin(info.get("profitMargins"))
        +
        score_fcf(info.get("freeCashflow"))
    ) / 4,
    1
)

    strength_score = round(
    (
        score_debt(info.get("debtToEquity"))
        +
        score_current_ratio(info.get("currentRatio"))
        +
        score_quick_ratio(info.get("quickRatio"))
    ) / 3,
    1
)

    valuation_score = round(
    (
        score_pe(info.get("trailingPE"))
        +
        score_peg(info.get("pegRatio"))
        +
        score_pb(info.get("priceToBook"))
        +
        score_ev_ebitda(
            info.get("enterpriseValue"),
            info.get("ebitda")
        )
    ) / 4,
    1
)
    health_score=0
    if(info.get("returnOnEquity") or 0)>0.15:
        health_score+=20
    if (info.get("profitMargins") or 0)>0.10:
        health_score+=20
    if(info.get("currentRatio") or 0)>1.5:
        health_score+=20
    if(info.get("debtToEquity") or 999)<100:
        health_score+=20
    if(info.get("revenueGrowth") or 0)>0.05:
        health_score+=20                

    overall_score = round(
        growth_score * 0.25 +
        quality_score * 0.25 +
        strength_score * 0.15 +
        valuation_score * 0.15 +
        health_score * 0.20,
        1
    )

    return (
        growth_score,
        quality_score,
        strength_score,
        valuation_score,
        health_score,
        overall_score
    )
