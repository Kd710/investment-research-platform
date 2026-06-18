from data_collector import get_company_data
from financial_analyzer import get_financial_summary
from ratio_calculator import calculate_ratios
from scoring_engine import overall_score
from report_generator import generate_report

ticker="AAPL"

company_data=get_company_data(ticker)
summary=get_financial_summary(ticker)
ratios=calculate_ratios(summary)
scores=overall_score(company_data,ratios)
report=generate_report(company_data,ratios,scores)
print(report)
