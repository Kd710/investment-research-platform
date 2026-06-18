import json
import pandas as pd

with open(
    f"datasets/us_stocks.json",
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)

tickers = []

for item in data.values():

    tickers.append({
        "Ticker": item["ticker"],
        "Company": item["title"]
    })

df = pd.DataFrame(tickers)

df.to_csv(
    "us_stocks.csv",
    index=False
)

print(
    f"Saved {len(df)} tickers."
)