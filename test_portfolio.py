from portfolio_tracker import analyze_portfolio

portfolio={
    "AAPL":10,
    "MSFT":5,
    "GOOG":3
}
results=analyze_portfolio(portfolio)
print("\nPORTFOLIO SUMMARY")
print("-" * 60)

for holding in results["Holdings"]:

    print(f"\n{holding['Company']}")
    print(f"Ticker: {holding['Ticker']}")
    print(f"Shares: {holding['Shares']}")
    print(f"Current Price: ${holding['Current Price']:.2f}")
    print(f"Holding Value: ${holding['Holding Value']:.2f}")
    print(f"Score: {holding['Score']}")

print("\n" + "-" * 60)

print(f"Portfolio Value: ${results['Portfolio Value']:.2f}")
print(f"Average Score: {results['Average Score']:.2f}")
print(f"Portfolio Rating: {results['Portfolio Rating']}")