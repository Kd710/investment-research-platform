from data_collector import get_company_data
from financial_analyzer import get_financial_summary
from ratio_calculator import calculate_ratios
from scoring_engine import overall_score
from scoring_engine import investment_rating
def rank_companies(companies):
    rankings=[]
    for ticker in companies:
        try:
            company_data=get_company_data(ticker)
            summary=get_financial_summary(ticker)
            ratios=calculate_ratios(summary)
            scores=overall_score(company_data,ratios)
            rating=investment_rating(scores["Overall Score"])
            rankings.append({
                "Ticker":ticker,
                "Company": company_data["name"],
                "Score": scores["Overall Score"],
                "Rating":rating
            })
        except Exception as e:
            print(f"Error with {ticker}:{e}")
    rankings.sort(
        key=lambda company:company["Score"],
        reverse=True
    )            
    return rankings

