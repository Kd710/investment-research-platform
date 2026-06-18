import json
import pandas as pd

with open(
    "datasets/us_stocks.json",
    "r",
    encoding="utf-8"
) as file:
    data = json.load(file)

rows = []

for item in data.values():
    rows.append({
        "Ticker": item["ticker"],
        "Company": item["title"]
    })

df = pd.DataFrame(rows)

df.to_csv(
    "us_stocks_cleaned.csv",
    index=False
)

print(df.head())
print(f"Saved {len(df)} stocks")