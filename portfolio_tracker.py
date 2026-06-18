from data_collector import get_company_data
from financial_analyzer import get_financial_summary
from ratio_calculator import calculate_ratios
from scoring_engine import overall_score, investment_rating

def analyze_portfolio(portfolio):
    holdings=[]

    total_value=0
    total_score=0
    company_count=0

    for ticker,shares in portfolio.items():
        try:
            company_data=get_company_data(ticker)
            summary=get_financial_summary(ticker)
            ratios=calculate_ratios(summary)
            scores=overall_score(company_data,ratios)
            current_price=company_data["currentPrice"]
            holding_value=current_price*shares
            total_value+=holding_value
            total_score+=scores["Overall Score"]
            company_count+=1
            holdings.append({
                "Ticker": ticker,
                "Company": company_data["name"],
                "Shares": shares,
                "Current Price": current_price,
                "Holding Value": holding_value,
                "Score": scores["Overall Score"]
            })
        except Exception as e:
                print(f"Error with {ticker}: {e}")
    if company_count>0:
        average_score=total_score/company_count
    else:
        average_score=0

    portfolio_rating=investment_rating(average_score)

    return{
         "Holdings":holdings,
         "Portfolio Value": total_value,
         "Average Score": average_score,
         "Portfolio Rating": portfolio_rating
    }    
