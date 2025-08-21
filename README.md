# 📊 Valuation Model Using Financial Statements & Stock Price

This project builds a data pipeline and valuation model that combines **OpenDART financial statements** and **stock price data** to analyze company fundamentals and estimate intrinsic value.

## Objective

To collect, clean, and analyze multi-year financial data from publicly listed Korean companies, and ultimately develop a data-driven **valuation model**.

---

## Data Sources

- OpenDART API - For financial statements (재무제표)
- Stock Price API - NAVER Finance / Alpha Vantage / Yahoo Finance

---

## Key Features

- Automated download of multi-year financials using OpenDART
- Parses and standardizes key financial metrics:
  - 매출액 (Revenue)
  - 영업이익 (Operating Income)
  - 당기순이익 (Net Profit)
  - 자산총계 / 부채총계 / 자본총계 (Balance Sheet Items)
- Merges company-year records into one clean summary file

---

## Future Goals

- Integrate historical stock prices
- Calculate key ratios (P/E, P/B, ROE, etc.)
- Build intrinsic value estimates using valuation models (e.g., DCF)
- Visualize trends and detect undervalued/overvalued companies

---

## How to Run

1. Set your OpenDART API Key in `.env`:
