# Trader Performance vs Market Sentiment

This project analyzes how Bitcoin market sentiment (Fear/Greed) relates to trader behavior and performance on Hyperliquid, as part of the Primetrade.ai Data Science Intern assignment.

## Project Overview

We combine a daily Fear/Greed sentiment dataset with historical Hyperliquid trader executions to:

- Engineer daily per-account metrics (PnL, win rate, trade frequency, trade size, long/short bias).
- Compare these metrics across different sentiment regimes (Fear vs Greed and intermediates).
- Segment traders (e.g., high vs low leverage proxy) and study how their behavior and performance shift with sentiment.
- Derive simple, actionable rules of thumb that can inform risk management or strategy design.

## Data

Two input CSV files are used:

1. **Bitcoin Market Sentiment (Fear/Greed)**  
   - Columns: date, sentiment classification (e.g., Extreme Fear, Fear, Neutral, Greed, Extreme Greed).  
   - Used to define the **daily sentiment regime**.

2. **Historical Trader Data (Hyperliquid)**  
   - Columns include: account, coin, execution price, size (tokens / USD), side (long/short), timestamps, direction, closed PnL, etc.  
   - Used to compute **per-trader daily behavior and performance metrics**.

During the first run, the script auto-downloads both CSVs into the `data/` folder using the Google Drive links from the assignment email.

## Repository Structure

```text
.
├─ data/
│  ├─ fear_greed.csv              # downloaded automatically if missing
│  └─ hyperliquid_trades.csv      # downloaded automatically if missing
│
├─ outputs/
│  ├─ daily_trader_metrics.csv                # daily trader-level metrics
│  ├─ daily_trader_metrics_with_sentiment.csv # metrics joined with daily sentiment
│  ├─ performance_by_sentiment.csv            # aggregate metrics by sentiment regime
│  ├─ segment_performance_by_sentiment.csv    # metrics by sentiment × leverage segment
│  ├─ mean_pnl_by_sentiment.png
│  ├─ mean_trades_by_sentiment.png
│  ├─ mean_trade_size_by_sentiment.png
│  └─ mean_pnl_by_sentiment_segment.png
│
├─ main.py
└─ requirements.txt

Setup

    Clone the repository

bash
git clone https://github.com/<your-username>/trader-performance-vs-market-sentiment.git
cd trader-performance-vs-market-sentiment

    Create and activate a virtual environment

bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

    Install dependencies

bash
pip install -r requirements.txt

requirements.txt includes core libraries for data analysis (pandas, numpy), charting (plotly + kaleido for PNG export), and HTTP requests (requests).
How to Run

From the project root (with the virtual environment activated):

bash
python main.py
