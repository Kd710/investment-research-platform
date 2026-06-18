from scoring_engine import overall_score
from data_collector import get_company_data
from company_analyzer import display_company_report
from financial_analyzer import get_financial_summary
from ratio_calculator import calculate_ratios


ticker = input("Enter ticker: ").upper()

try:
    # Company Information
    company_data = get_company_data(ticker)

    if company_data["name"] is None:
        print("Invalid ticker.")
        exit()

    # Display Company Report
    display_company_report(company_data)

    # Financial Summary
    summary = get_financial_summary(ticker)

    # Ratios
    ratios = calculate_ratios(summary)
    scores=overall_score(company_data,ratios)

    print("\nFINANCIAL RATIOS")
    print("-" * 50)

    print("\n COMPANY SCORES")
    print("-"*50)
    for key,value in scores.items():
        print(f"{key}: {value}")

    for key, value in ratios.items():
        if value is not None:
            print(f"{key}: {value:.2%}")
        else:
            print(f"{key}: N/A")

except Exception as e:
    print("Error:", e)