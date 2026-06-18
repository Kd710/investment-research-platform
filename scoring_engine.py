def valuation_score(data):
    score=0

    pe=data.get("trailingPE")
    peg=data.get("pegRatio")

    if pe:
        if pe<15:
            score+=25
        elif pe<25:
            score+=15
        elif pe<35:
            score+=10

    if peg:                
        if peg < 1:
            score += 25
        elif peg < 2:
            score += 15
        elif peg < 3:
            score += 10

    return score

def growth_score(data):

    score = 0

    revenue_growth = data.get("revenueGrowth")
    earnings_growth = data.get("earningsGrowth")

    if revenue_growth:
        if revenue_growth > 0.20:
            score += 25
        elif revenue_growth > 0.10:
            score += 15
        elif revenue_growth > 0:
            score += 10

    if earnings_growth:
        if earnings_growth > 0.20:
            score += 25
        elif earnings_growth > 0.10:
            score += 15
        elif earnings_growth > 0:
            score += 10

    return score


def quality_score(data, ratios):

    score = 0

    roe = data.get("returnOnEquity")

    if roe:
        if roe > 0.20:
            score += 25
        elif roe > 0.15:
            score += 15
        elif roe > 0.10:
            score += 10

    profit_margin = ratios.get("Profit Margin")

    if profit_margin:
        if profit_margin > 0.20:
            score += 25
        elif profit_margin > 0.10:
            score += 15
        elif profit_margin > 0:
            score += 10

    return score


def overall_score(data, ratios):

    valuation = valuation_score(data)
    growth = growth_score(data)
    quality = quality_score(data, ratios)

    total = valuation + growth + quality

    return {
        "Valuation Score": valuation,
        "Growth Score": growth,
        "Quality Score": quality,
        "Overall Score": total
    }

def investment_rating(score):

    if score >= 120:
        return "STRONG BUY"

    elif score >= 90:
        return "BUY"

    elif score >= 60:
        return "HOLD"

    else:
        return "SELL"