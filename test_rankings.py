from ranking_engine import rank_companies

companies=[
    "AAPL",
    "MSFT",
    "GOOG",
    "META",
    "AMZN"
]
rankings=rank_companies(companies)

print("\n RANKINGS")
print("-"*50)
for i, company in enumerate(rankings,start=1):
    print(
        f" {i}"
        f" {company['Company']}"
        f" Score: {company['Score']}"
        f" {company['Rating']}"
    )