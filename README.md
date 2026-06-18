# Investment Research Platform

A multi-page Streamlit application for stock analysis, valuation, screening, and portfolio analytics.

## Overview

The Investment Research Platform is a Python-based investment research tool built using Streamlit, Pandas, Plotly, and Yahoo Finance data.

The platform combines company analysis, valuation models, portfolio analytics, stock screening, and investment research tools into a single dashboard.

## Features

### Company Analysis

* Company Profile
* Valuation Metrics
* Growth Metrics
* Quality Metrics
* Cash Flow Analysis
* Financial Health Analysis
* Analyst Sentiment
* Analyst Expected Return
* Dividend Information
* Market Cap Classification
* Interactive Price Charts

### Proprietary Scoring System

The platform calculates:

* Growth Score
* Quality Score
* Strength Score
* Valuation Score
* Health Score
* Overall Score

### Valuation Tools

* Discounted Cash Flow (DCF) Valuation
* Margin of Safety Analysis
* DCF Sensitivity Analysis
* Reverse DCF
* EV/EBITDA Analysis

### Quality Analysis

* Piotroski Score
* Earnings Quality Score

### Portfolio Analytics

* Portfolio Tracker
* Portfolio Performance Tracker
* Portfolio Score
* Portfolio Beta
* Diversification Analysis
* Sector Exposure Analysis
* Market Cap Exposure Analysis
* Expected Portfolio Return
* Analyst Coverage Tracking

### Research Tools

* Company Comparison
* Watchlist
* Ranking System
* Stock Screener
* Dividend Analyzer
* News Dashboard

## Technology Stack

* Python
* Streamlit
* Pandas
* Plotly
* Yahoo Finance (yfinance)

## Project Structure

```text
app.py
utils.py
pages/
datasets/
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Kd710/investment-research-platform.git
cd investment-research-platform
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Future Enhancements

### Version 2 Roadmap

* SIP Tracker
* Mutual Fund Analyzer
* Goal Planning Dashboard
* Portfolio Quality Score
* Full Piotroski F-Score
* Factor Investing Models
* Backtesting Engine

## Disclaimer

This project is intended for educational and research purposes only and does not constitute investment advice. Investors should conduct their own research before making investment decisions.
