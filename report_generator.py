from scoring_engine import investment_rating


def generate_report(company_data, ratios, scores):

    report = []

    report.append("=" * 60)
    report.append("INVESTMENT RESEARCH REPORT")
    report.append("=" * 60)

    report.append(f"\nCompany: {company_data['name']}")
    report.append(f"Sector: {company_data['sector']}")
    report.append(f"Industry: {company_data['industry']}")

    report.append("\nVALUATION")

    report.append(
        f"Trailing PE: {company_data['trailingPE']}"
    )

    report.append(
        f"Forward PE: {company_data['forwardPE']}"
    )

    report.append(
        f"PEG Ratio: {company_data['pegRatio']}"
    )

    report.append("\nGROWTH")

    report.append(
        f"Revenue Growth: "
        f"{company_data['revenueGrowth']:.2%}"
    )

    report.append(
        f"Earnings Growth: "
        f"{company_data['earningsGrowth']:.2%}"
    )

    report.append("\nPROFITABILITY")

    report.append(
        f"ROE: "
        f"{company_data['returnOnEquity']:.2%}"
    )

    report.append(
        f"Profit Margin: "
        f"{company_data['profitMargins']:.2%}"
    )

    report.append("\nFINANCIAL HEALTH")

    report.append(
        f"Debt Ratio: "
        f"{ratios['Debt Ratio']:.2%}"
    )

    report.append(
        f"Cash Conversion: "
        f"{ratios['Cash Conversion']:.2%}"
    )

    report.append("\nSCORES")

    report.append(
        f"Valuation Score: "
        f"{scores['Valuation Score']}"
    )

    report.append(
        f"Growth Score: "
        f"{scores['Growth Score']}"
    )

    report.append(
        f"Quality Score: "
        f"{scores['Quality Score']}"
    )

    report.append(
        f"Overall Score: "
        f"{scores['Overall Score']}"
    )

    report.append(
        f"Recommendation: "
        f"{investment_rating(scores['Overall Score'])}"
    )

    report.append("\nSTRENGTHS")

    if company_data["revenueGrowth"] > 0.10:
        report.append("✓ Strong Revenue Growth")

    if company_data["returnOnEquity"] > 0.15:
        report.append("✓ Strong Return on Equity")

    if ratios["Profit Margin"] > 0.15:
        report.append("✓ Strong Profit Margin")

    report.append("\nWEAKNESSES")

    if company_data["trailingPE"] > 30:
        report.append("✗ High PE Ratio")

    if ratios["Debt Ratio"] > 0.50:
        report.append("✗ High Debt Ratio")

    if company_data["revenueGrowth"] < 0.05:
        report.append("✗ Weak Revenue Growth")

    report.append("\n" + "=" * 60)

    return "\n".join(report)