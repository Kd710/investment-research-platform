from comparison_engine import compare_companies

companies=[
    "AAPL",
    "MSFT",
    "GOOG"
]


df=compare_companies(
    companies
)
print(df)