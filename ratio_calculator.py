def calculate_ratios(summary):

    ratios = {}

    revenue = summary.get("Revenue")
    net_income = summary.get("Net Income")
    assets = summary.get("Total Assets")
    debt = summary.get("Total Debt")
    operating_cf = summary.get("Operating Cash Flow")
    free_cf = summary.get("Free Cash Flow")

    # Profit Margin

    if revenue and net_income:
        ratios["Profit Margin"] = net_income / revenue
    else:
        ratios["Profit Margin"] = None

    # Debt Ratio

    if assets and debt:
        ratios["Debt Ratio"] = debt / assets
    else:
        ratios["Debt Ratio"] = None

    # Cash Conversion Ratio

    if net_income and operating_cf:
        ratios["Cash Conversion"] = operating_cf / net_income
    else:
        ratios["Cash Conversion"] = None

    # Free Cash Flow Margin

    if revenue and free_cf:
        ratios["FCF Margin"] = free_cf / revenue
    else:
        ratios["FCF Margin"] = None

    return ratios