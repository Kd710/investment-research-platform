import pandas as pd
from data_collector import get_company_data
from financial_analyzer import get_financial_summary
from ratio_calculator import calculate_ratios
from scoring_engine import overall_score
from scoring_engine import investment_rating

def compare_companies(companies):
    comparison_data=[]
    for ticker in companies:
        try:
            company_data=get_company_data(ticker)
            summary=get_financial_summary(ticker)
            ratios=calculate_ratios(summary)
            scores=overall_score(company_data,ratios)
            comparison_data.append({
                "Ticker":ticker,
                "Company": company_data["name"],
                "Current Price": company_data["currentPrice"],
                "PE":round(company_data["trailingPE"],2),
                "Revenue Growth(%)": round(company_data["revenueGrowth"]*100,2),
                "ROE(%)":round(company_data["returnOnEquity"]*100,2),
                "Overall Score": scores["Overall Score"],
                "Rating":investment_rating(scores["Overall Score"])})
        except Exception as e:
            print(f"Error with {ticker}: {e}")
    return pd.DataFrame(
        comparison_data
    )            
        
    
               