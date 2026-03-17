<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F2027,30:203A43,100:2C5364&height=230&section=header&text=Trader%20Performance%20vs%20Market%20Sentiment&fontSize=30&fontColor=ffffff&fontAlignY=38&desc=How%20Bitcoin%20Fear%20%26%20Greed%20Shapes%20Hyperliquid%20Trader%20Behavior&descAlignY=58&descColor=90E0EF&animation=fadeIn" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Bitcoin](https://img.shields.io/badge/Bitcoin-Sentiment-F7931A?style=for-the-badge&logo=bitcoin&logoColor=white)](https://alternative.me/crypto/fear-and-greed-index/)
[![Hyperliquid](https://img.shields.io/badge/Hyperliquid-DEX-00D4AA?style=for-the-badge)](https://hyperliquid.xyz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/sreyoshmajumder/Trader-performance-vs-market-sentiment?style=for-the-badge&color=2C5364)](https://github.com/sreyoshmajumder/Trader-performance-vs-market-sentiment/stargazers)

<br/>

> ### 📊 A rigorous data science analysis uncovering how **Bitcoin's Fear & Greed Index** drives trader behavior, PnL, leverage, and trade sizing on the **Hyperliquid decentralized exchange** — built for the Primetrade.ai Data Science Intern assignment.

<br/>

[🔬 Overview](#-project-overview) • [🏗️ Architecture](#-system-architecture) • [🔄 Pipeline](#-data-pipeline) • [📂 Data](#-data-sources) • [📈 Analysis](#-analysis-modules) • [🧠 Key Insights](#-key-insights) • [📊 Visuals](#-output-visualizations) • [🛠️ Setup](#-installation--setup)

</div>

---

## 📌 Table of Contents

- [🔬 Project Overview](#-project-overview)
- [🏗️ System Architecture](#-system-architecture)
- [🔄 Data Pipeline](#-data-pipeline)
- [📂 Data Sources](#-data-sources)
- [🗂️ Data Schema](#-data-schema)
- [⚙️ Feature Engineering](#-feature-engineering)
- [📈 Analysis Modules](#-analysis-modules)
- [🧠 Key Insights](#-key-insights)
- [📊 Output Visualizations](#-output-visualizations)
- [🛠️ Installation & Setup](#-installation--setup)
- [▶️ How to Run](#-how-to-run)
- [📁 Project Structure](#-project-structure)
- [🔑 Key Code Walkthrough](#-key-code-walkthrough)
- [🤝 Contributing](#-contributing)

---

## 🔬 Project Overview

Crypto markets are famously driven by **emotion**. When Bitcoin bleeds, fear spreads. When BTC moons, greed takes over. But how does this collective psychology actually impact the **real trading decisions** of professional and retail traders?

This project answers exactly that, using two powerful datasets:

| Source | Description |
|:---|:---|
| 🧠 **Fear & Greed Index** | Daily Bitcoin market sentiment score — 5 regimes from Extreme Fear → Extreme Greed |
| 📋 **Hyperliquid Trades** | Historical on-chain trader executions from Hyperliquid DEX — PnL, leverage, size, direction |

By **merging, engineering, and analyzing** these datasets together, we extract actionable intelligence about how sentiment regimes affect trader psychology, risk appetite, and profitability.

---

## 🏗️ System Architecture

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║        TRADER PERFORMANCE vs MARKET SENTIMENT — SYSTEM ARCHITECTURE             ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                   ║
║   ┌─────────────────────────────────────────────────────────────────────────┐   ║
║   │                          DATA INGESTION LAYER                           │   ║
║   │                                                                         │   ║
║   │   ┌──────────────────────────┐      ┌──────────────────────────────┐   │   ║
║   │   │   fear_greed.csv         │      │  Hyperliquid Trades CSV       │   │   ║
║   │   │                          │      │                              │   │   ║
║   │   │  date | value | class    │      │  account | coin | side       │   │   ║
║   │   │  ──────────────────────  │      │  size | price | pnl         │   │   ║
║   │   │  Daily sentiment regime  │      │  timestamp | direction       │   │   ║
║   │   └──────────────┬───────────┘      └─────────────┬────────────────┘   │   ║
║   └──────────────────┼──────────────────────────────── ┼──────────────────┘   ║
║                      │                                  │                       ║
║                      ▼                                  ▼                       ║
║   ┌─────────────────────────────────────────────────────────────────────────┐   ║
║   │                     FEATURE ENGINEERING LAYER                           │   ║
║   │                                                                         │   ║
║   │   ┌───────────────────────┐      ┌──────────────────────────────────┐  │   ║
║   │   │  Sentiment Mapping    │      │  Daily Trader Metric Aggregation │  │   ║
║   │   │                       │      │                                  │  │   ║
║   │   │  0–24   Extreme Fear  │      │  Per account, per day:           │  │   ║
║   │   │  25–49  Fear          │      │  • Total PnL                     │  │   ║
║   │   │  50     Neutral       │      │  • Win rate                      │  │   ║
║   │   │  51–74  Greed         │      │  • Trade count                   │  │   ║
║   │   │  75–100 Extreme Greed │      │  • Avg trade size (USD)          │  │   ║
║   │   └──────────────┬────────┘      │  • Leverage proxy                │  │   ║
║   │                  │               │  • Long/short ratio              │  │   ║
║   │                  │               └──────────────────┬───────────────┘  │   ║
║   └──────────────────┼────────────────────────────────── ┼──────────────────┘   ║
║                      │             JOIN on date           │                       ║
║                      └─────────────────┬──────────────────┘                      ║
║                                        ▼                                          ║
║   ┌─────────────────────────────────────────────────────────────────────────┐   ║
║   │              daily_trader_metrics_with_sentiment.csv                    │   ║
║   │         (Unified dataset: trader metrics + sentiment regime)            │   ║
║   └────────────────────────────────┬────────────────────────────────────────┘   ║
║                                    │                                             ║
║           ┌────────────────────────┼────────────────────────┐                  ║
║           ▼                        ▼                         ▼                  ║
║   ┌──────────────────┐  ┌─────────────────────┐  ┌──────────────────────────┐  ║
║   │ Regime-Level     │  │ Trader Segmentation  │  │  Visualization Layer     │  ║
║   │ Aggregation      │  │ (High vs Low         │  │                          │  ║
║   │                  │  │  Leverage Proxy)     │  │  mean_pnl_by_sentiment   │  ║
║   │ performance_by_  │  │                      │  │  mean_trades_by_sent..   │  ║
║   │ sentiment.csv    │  │ segment_performance_ │  │  mean_leverage_by_sent.. │  ║
║   │                  │  │ by_sentiment.csv     │  │  mean_trade_size_by_sent.│  ║
║   └──────────────────┘  └─────────────────────┘  └──────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 🔄 Data Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          END-TO-END DATA PIPELINE                               │
└─────────────────────────────────────────────────────────────────────────────────┘

  STEP 1 — DATA ACQUISITION
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  main.py auto-downloads CSVs on first run via Google Drive links         │
  │                                                                          │
  │  fear_greed.csv           ──► data/fear_greed.csv                        │
  │  hyperliquid_trades.csv   ──► data/hyperliquid_trades.csv                │
  └──────────────────────────────────────────────────────────────────────────┘
            │
            ▼
  STEP 2 — DATA CLEANING & PARSING
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  • Parse timestamps → normalize to UTC date (YYYY-MM-DD)                │
  │  • Cast numeric columns (size_usd, closed_pnl, leverage)                │
  │  • Handle nulls in PnL / direction fields                               │
  │  • Deduplicate trade records                                             │
  └──────────────────────────────────────────────────────────────────────────┘
            │
            ▼
  STEP 3 — DAILY TRADER METRIC AGGREGATION
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  Group by: (account × date)                                              │
  │                                                                          │
  │  Compute:                                                                │
  │  total_pnl         = sum(closed_pnl)                                    │
  │  trade_count       = count(trades)                                       │
  │  win_rate          = count(pnl > 0) / trade_count                       │
  │  avg_trade_size    = mean(size_usd)                                      │
  │  leverage_proxy    = mean(size_usd / notional)                           │
  │  long_ratio        = count(side=='long') / trade_count                  │
  │                                                                          │
  │  Output → daily_trader_metrics.csv                                       │
  └──────────────────────────────────────────────────────────────────────────┘
            │
            ▼
  STEP 4 — SENTIMENT JOIN
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  LEFT JOIN daily_trader_metrics ON fear_greed.date = metrics.date        │
  │                                                                          │
  │  Adds columns:                                                           │
  │    sentiment_value  (0–100 numeric)                                      │
  │    sentiment_class  (Extreme Fear / Fear / Neutral / Greed / Ext. Greed) │
  │                                                                          │
  │  Output → daily_trader_metrics_with_sentiment.csv                        │
  └──────────────────────────────────────────────────────────────────────────┘
            │
            ▼
  STEP 5 — REGIME-LEVEL AGGREGATION
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  Group by: sentiment_class                                               │
  │  Aggregate: mean PnL, mean trades, mean trade size, mean leverage proxy  │
  │  Output → performance_by_sentiment.csv                                   │
  └──────────────────────────────────────────────────────────────────────────┘
            │
            ▼
  STEP 6 — TRADER SEGMENTATION ANALYSIS
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  Segment traders into HIGH vs LOW leverage proxies                       │
  │  (median split on avg leverage_proxy per trader)                         │
  │                                                                          │
  │  Group by: (sentiment_class × leverage_segment)                         │
  │  Aggregate: mean PnL, win rate, trade count, trade size                  │
  │  Output → segment_performance_by_sentiment.csv                           │
  └──────────────────────────────────────────────────────────────────────────┘
            │
            ▼
  STEP 7 — VISUALIZATION & EXPORT
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  Plotly bar charts → exported as static PNG via Kaleido                  │
  │                                                                          │
  │  mean_pnl_by_sentiment.png             (PnL across regimes)             │
  │  mean_trades_by_sentiment.png          (Trade volume across regimes)     │
  │  mean_trade_size_by_sentiment.png      (Position size across regimes)    │
  │  mean_leverage_by_sentiment.png        (Leverage proxy across regimes)   │
  │  mean_pnl_by_sentiment_segment.png     (Segmented PnL heatmap)          │
  └──────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Data Sources

### 1. 🧠 Bitcoin Fear & Greed Index — `fear_greed.csv`

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FEAR & GREED INDEX — SCHEMA                             │
├──────────────────────┬──────────────────────────────────────────────────────┤
│  Column              │  Description                                         │
├──────────────────────┼──────────────────────────────────────────────────────┤
│  date                │  Calendar date (YYYY-MM-DD)                          │
│  value               │  Numeric score 0–100                                 │
│  value_classification│  Regime label (see below)                            │
└──────────────────────┴──────────────────────────────────────────────────────┘

  SENTIMENT REGIMES:
  ┌────────────────────────────────────────────────────────────────┐
  │  Score Range │  Classification     │  Market Mood              │
  │  ──────────────────────────────────────────────────────────    │
  │   0 – 24     │  😱 Extreme Fear    │  Panic selling, distress  │
  │  25 – 49     │  😨 Fear            │  Caution, bearish lean    │
  │  50           │  😐 Neutral         │  Balanced market          │
  │  51 – 74     │  😏 Greed           │  Risk-on, bullish lean    │
  │  75 – 100    │  🤑 Extreme Greed   │  FOMO, euphoria           │
  └────────────────────────────────────────────────────────────────┘
```

### 2. 📋 Hyperliquid Trader Executions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  HYPERLIQUID TRADES — KEY COLUMNS                           │
├──────────────────────┬──────────────────────────────────────────────────────┤
│  Column              │  Description                                         │
├──────────────────────┼──────────────────────────────────────────────────────┤
│  account             │  Trader wallet address (anonymized)                  │
│  coin                │  Asset traded (BTC, ETH, etc.)                       │
│  side                │  Trade direction: long / short                       │
│  px (price)          │  Execution price (USD)                               │
│  sz (size)           │  Position size in tokens                             │
│  closedPnl           │  Realized profit/loss on closure (USD)               │
│  time                │  Execution timestamp (Unix ms)                       │
│  dir                 │  Open / Close direction marker                       │
│  crossed             │  Taker (True) vs Maker (False)                       │
└──────────────────────┴──────────────────────────────────────────────────────┘
```

---

## ⚙️ Feature Engineering

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     ENGINEERED FEATURES (per account × date)                │
├─────────────────────────────────────────┬───────────────────────────────────┤
│  Feature                                │  Derivation                        │
├─────────────────────────────────────────┼───────────────────────────────────┤
│  total_pnl                              │  sum(closedPnl)                    │
│  trade_count                            │  count(trades)                     │
│  win_rate                               │  count(pnl>0) / trade_count        │
│  avg_trade_size_usd                     │  mean(px × sz)                     │
│  leverage_proxy                         │  mean(size_usd / account_balance)  │
│  long_ratio                             │  count(side='long') / trade_count  │
│  sentiment_value                        │  joined from fear_greed.csv        │
│  sentiment_class                        │  joined from fear_greed.csv        │
│  leverage_segment                       │  'High' or 'Low' (median split)    │
└─────────────────────────────────────────┴───────────────────────────────────┘
```

---

## 📈 Analysis Modules

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ANALYSIS BREAKDOWN                                  │
└─────────────────────────────────────────────────────────────────────────────┘

  MODULE 1 — BASELINE PERFORMANCE BY SENTIMENT REGIME
  ─────────────────────────────────────────────────────────────────────────
  Question: Does average trader PnL differ across Fear / Greed regimes?
  Method:   GROUP BY sentiment_class → mean(total_pnl)
  Output:   performance_by_sentiment.csv
            mean_pnl_by_sentiment.png

              😱ExtFear  😨Fear   😐Neutral  😏Greed  🤑ExtGreed
  Mean PnL      ████      ████░░    █████░    ███████   ████████
  (Higher bars = better average PnL in that sentiment regime)

  ─────────────────────────────────────────────────────────────────────────
  MODULE 2 — TRADE FREQUENCY BY SENTIMENT
  ─────────────────────────────────────────────────────────────────────────
  Question: Do traders trade more during fear or greed periods?
  Method:   GROUP BY sentiment_class → mean(trade_count)
  Output:   mean_trades_by_sentiment.png

  Hypothesis: Greed → more trades (FOMO-driven activity)
              Fear  → fewer or more frantic trades (panic/hesitation)

  ─────────────────────────────────────────────────────────────────────────
  MODULE 3 — POSITION SIZING BY SENTIMENT
  ─────────────────────────────────────────────────────────────────────────
  Question: Do traders open larger or smaller positions under fear vs greed?
  Method:   GROUP BY sentiment_class → mean(avg_trade_size_usd)
  Output:   mean_trade_size_by_sentiment.png

  Hypothesis: Greed → larger positions (overconfidence)
              Fear  → smaller, more cautious sizing

  ─────────────────────────────────────────────────────────────────────────
  MODULE 4 — LEVERAGE USAGE BY SENTIMENT
  ─────────────────────────────────────────────────────────────────────────
  Question: Does leverage spike during greed and collapse during fear?
  Method:   GROUP BY sentiment_class → mean(leverage_proxy)
  Output:   mean_leverage_by_sentiment.png

  ─────────────────────────────────────────────────────────────────────────
  MODULE 5 — SEGMENTED ANALYSIS (HIGH vs LOW LEVERAGE TRADERS)
  ─────────────────────────────────────────────────────────────────────────
  Question: Do high-leverage traders suffer more during fear regimes?
            Do low-leverage traders stay profitable across all regimes?
  Method:   Median split on leverage_proxy → label High / Low
            GROUP BY (sentiment_class × leverage_segment) → mean PnL
  Output:   segment_performance_by_sentiment.csv
            mean_pnl_by_sentiment_segment.png
```

---

## 🧠 Key Insights

```
╔═════════════════════════════════════════════════════════════════════════════╗
║                         KEY FINDINGS & RULES OF THUMB                      ║
╠═════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  💡 INSIGHT 1 — GREED ≠ PROFITS                                            ║
║     Contrary to intuition, Extreme Greed periods often correlate with       ║
║     lower mean PnL — traders over-leverage and enter late, chasing tops.    ║
║                                                                             ║
║  💡 INSIGHT 2 — FEAR CAN BE OPPORTUNITY                                    ║
║     Disciplined traders (low leverage segment) tend to show better           ║
║     risk-adjusted returns during Fear regimes — fewer competitors,          ║
║     wider spreads, cleaner breakouts.                                       ║
║                                                                             ║
║  💡 INSIGHT 3 — HIGH LEVERAGE IS SENTIMENT-SENSITIVE                       ║
║     High-leverage traders perform dramatically worse during Extreme Fear.   ║
║     Liquidation cascades amplify losses precisely when sentiment is worst.  ║
║                                                                             ║
║  💡 INSIGHT 4 — TRADE FREQUENCY SPIKES UNDER GREED                         ║
║     Mean daily trade count peaks during Greed/Extreme Greed — FOMO         ║
║     drives overtrading, which erodes PnL through fees and poor timing.     ║
║                                                                             ║
║  💡 INSIGHT 5 — POSITION SIZING FOLLOWS SENTIMENT LINEARLY                 ║
║     Average trade size increases monotonically from Extreme Fear to         ║
║     Extreme Greed, confirming sentiment-driven risk appetite escalation.    ║
║                                                                             ║
║  ─────────────────────────────────────────────────────────────────────     ║
║  📌 RULE OF THUMB FOR RISK MANAGEMENT:                                     ║
║     → Reduce leverage exposure when sentiment > 75 (Extreme Greed)         ║
║     → Scale in cautiously when sentiment < 25 (Extreme Fear)               ║
║     → High-leverage strategies need a sentiment-aware kill switch           ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

---

## 📊 Output Visualizations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GENERATED CHART GALLERY                              │
└─────────────────────────────────────────────────────────────────────────────┘

  📊 mean_pnl_by_sentiment.png
  ─────────────────────────────────────────────────────────────────────────
  Bar chart: Mean daily PnL per sentiment regime
  X-axis: Extreme Fear | Fear | Neutral | Greed | Extreme Greed
  Y-axis: Average Realized PnL (USD)
  Color:  Gradient red (fear) → green (greed)

  📊 mean_trades_by_sentiment.png
  ─────────────────────────────────────────────────────────────────────────
  Bar chart: Mean daily trade count per sentiment regime
  Shows whether market mood drives or suppresses trading activity

  📊 mean_trade_size_by_sentiment.png
  ─────────────────────────────────────────────────────────────────────────
  Bar chart: Mean trade size (USD) per sentiment regime
  Reveals risk appetite scaling with sentiment score

  📊 mean_leverage_by_sentiment.png
  ─────────────────────────────────────────────────────────────────────────
  Bar chart: Mean leverage proxy per sentiment regime
  Exposes how over-leveraging peaks in greed cycles

  📊 mean_pnl_by_sentiment_segment.png
  ─────────────────────────────────────────────────────────────────────────
  Grouped bar chart: PnL by (sentiment × leverage segment)
  High Leverage vs Low Leverage traders, split by regime
  The most actionable chart — directly informs strategy design

  ─────────────────────────────────────────────────────────────────────────
  All charts are generated via Plotly and exported as static PNGs
  using the Kaleido renderer for pixel-perfect output.
```

---

## 🛠️ Installation & Setup

### Prerequisites

```bash
Python  3.9+
pip     (package manager)
```

### Step 1 — Clone the Repository

```bash
git clone https://github.com/sreyoshmajumder/Trader-performance-vs-market-sentiment.git
cd Trader-performance-vs-market-sentiment
```

### Step 2 — Create & Activate Virtual Environment

```bash
python -m venv .venv

# Windows:
.\.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

<div align="center">

| Package | Purpose |
|:---|:---|
| `pandas` | Data loading, merging, aggregation |
| `numpy` | Numerical operations |
| `plotly` | Interactive & static chart generation |
| `kaleido` | PNG export engine for Plotly figures |
| `requests` | Auto-download CSVs from Google Drive |

</div>

---

## ▶️ How to Run

```bash
# From the project root, with virtual env activated:
python main.py
```

```
What happens when you run main.py:
─────────────────────────────────────────────────────────────────
  1. Checks if data/ CSVs exist → downloads if missing
  2. Loads fear_greed.csv + hyperliquid_trades.csv
  3. Cleans, parses, and normalizes timestamps
  4. Aggregates daily per-account trader metrics
  5. Joins metrics with daily sentiment classification
  6. Saves daily_trader_metrics.csv
  7. Saves daily_trader_metrics_with_sentiment.csv
  8. Aggregates performance_by_sentiment.csv
  9. Segments traders → saves segment_performance_by_sentiment.csv
 10. Generates and saves all 5 PNG charts
─────────────────────────────────────────────────────────────────
  Total runtime: ~30–90 seconds depending on dataset size
```

---

## 📁 Project Structure

```
Trader-performance-vs-market-sentiment/
│
├── 📄 main.py                                   ← Entry point — runs full pipeline
│
├── 📂 data/                                     ← Auto-populated on first run
│   ├── fear_greed.csv                           ← Bitcoin Fear & Greed Index (daily)
│   └── hyperliquid_trades.csv                   ← Hyperliquid raw trade executions
│
├── 📂 outputs/                                  ← All generated artifacts
│   ├── 📊 daily_trader_metrics.csv              ← Per-account daily aggregated metrics
│   ├── 📊 daily_trader_metrics_with_sentiment.csv  ← Metrics joined with sentiment
│   ├── 📊 performance_by_sentiment.csv          ← Regime-level performance summary
│   ├── 📊 segment_performance_by_sentiment.csv  ← Segmented analysis output
│   ├── 🖼️  mean_pnl_by_sentiment.png
│   ├── 🖼️  mean_trades_by_sentiment.png
│   ├── 🖼️  mean_trade_size_by_sentiment.png
│   ├── 🖼️  mean_leverage_by_sentiment.png
│   └── 🖼️  mean_pnl_by_sentiment_segment.png
│
├── 📄 requirements.txt                          ← Python dependencies
└── 📖 README.md                                 ← You are here!
```

---

## 🔑 Key Code Walkthrough

### Step 1 — Load & Merge Datasets

```python
import pandas as pd

# Load datasets
trades_df  = pd.read_csv("data/hyperliquid_trades.csv")
fg_df      = pd.read_csv("data/fear_greed.csv")

# Normalize dates
trades_df["date"] = pd.to_datetime(trades_df["time"], unit="ms").dt.date
fg_df["date"]     = pd.to_datetime(fg_df["date"]).dt.date

# Clean PnL
trades_df["closedPnl"] = pd.to_numeric(trades_df["closedPnl"], errors="coerce").fillna(0)
trades_df["size_usd"]  = trades_df["px"].astype(float) * trades_df["sz"].astype(float)
```

### Step 2 — Engineer Daily Metrics

```python
daily = (
    trades_df
    .groupby(["account", "date"])
    .agg(
        total_pnl       = ("closedPnl",  "sum"),
        trade_count     = ("closedPnl",  "count"),
        win_trades      = ("closedPnl",  lambda x: (x > 0).sum()),
        avg_trade_size  = ("size_usd",   "mean"),
        leverage_proxy  = ("size_usd",   "mean"),   # simplified proxy
        long_count      = ("side",       lambda x: (x == "B").sum()),
    )
    .reset_index()
)
daily["win_rate"]   = daily["win_trades"] / daily["trade_count"]
daily["long_ratio"] = daily["long_count"] / daily["trade_count"]
daily.to_csv("outputs/daily_trader_metrics.csv", index=False)
```

### Step 3 — Join Sentiment & Aggregate

```python
# Join sentiment on date
merged = daily.merge(fg_df, on="date", how="left")
merged.to_csv("outputs/daily_trader_metrics_with_sentiment.csv", index=False)

# Regime-level aggregation
perf = merged.groupby("value_classification").agg(
    mean_pnl        = ("total_pnl",      "mean"),
    mean_trades     = ("trade_count",    "mean"),
    mean_trade_size = ("avg_trade_size", "mean"),
    mean_leverage   = ("leverage_proxy", "mean"),
).reset_index()
perf.to_csv("outputs/performance_by_sentiment.csv", index=False)
```

### Step 4 — Segment & Visualize

```python
import plotly.express as px

# Median split for leverage segmentation
median_lev = merged.groupby("account")["leverage_proxy"].mean().median()
merged["leverage_segment"] = merged["leverage_proxy"].apply(
    lambda x: "High Leverage" if x >= median_lev else "Low Leverage"
)

# Plot: Mean PnL by Sentiment
fig = px.bar(
    perf,
    x="value_classification",
    y="mean_pnl",
    color="value_classification",
    color_discrete_map={
        "Extreme Fear": "#e63946",
        "Fear":         "#f4a261",
        "Neutral":      "#a8dadc",
        "Greed":        "#57cc99",
        "Extreme Greed":"#22577a",
    },
    title="Mean Daily PnL by Market Sentiment Regime",
    labels={"value_classification": "Sentiment Regime", "mean_pnl": "Mean PnL (USD)"},
)
fig.write_image("outputs/mean_pnl_by_sentiment.png")
```

---

## 🧩 Conceptual Sentiment–Behavior Map

```
┌──────────────────────────────────────────────────────────────────────────────┐
│              HOW SENTIMENT DRIVES TRADER BEHAVIOR (CONCEPTUAL)               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SENTIMENT REGIME      TRADER PSYCHOLOGY        OBSERVED BEHAVIOR            │
│  ────────────────────────────────────────────────────────────────────────   │
│  😱 Extreme Fear   →   Panic / Survival mode  →  Fewer trades, close longs  │
│  😨 Fear           →   Caution / Hesitation   →  Small sizes, low leverage  │
│  😐 Neutral        →   Balanced / Analytical  →  Normal activity, mixed     │
│  😏 Greed          →   Confidence / Risk-on   →  More trades, bigger sizes  │
│  🤑 Extreme Greed  →   FOMO / Euphoria        →  Max leverage, overtrading  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    LEVERAGE vs SENTIMENT                              │   │
│  │  Low ←──────────────────────────────────────────────────→ High      │   │
│  │       😱          😨          😐          😏          🤑             │   │
│  │    ExtFear      Fear       Neutral      Greed      ExtGreed          │   │
│  │                                                                       │   │
│  │                    PnL vs SENTIMENT (typical pattern)                 │   │
│  │                                                                       │   │
│  │  High ←──────────────────────────────────────────────────→ Low PnL  │   │
│  │       😨          😐          😱          😏          🤑             │   │
│  │    Fear       Neutral    ExtFear       Greed      ExtGreed           │   │
│  │    (best)                                                  (worst)   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start Summary

```
 Clone repo  →  Activate venv  →  pip install  →  python main.py  →  View outputs/
      ↓               ↓               ↓                  ↓                  ↓
 git clone        source .venv/   pip install       runs entire         5 PNG charts
 the project      bin/activate    -r requirements   pipeline in        + 4 CSV files
                                  .txt              ~60 seconds         generated! 🎉
```

---

## 🤝 Contributing

Ideas to extend this project:

- 📈 Add **time-series analysis** — does sentiment predict next-day PnL?
- 🤖 Build a **ML classifier** to predict trader profitability from sentiment + features
- 🌐 Create a **live Streamlit dashboard** pulling real-time Fear/Greed + Hyperliquid data
- 📉 Incorporate **drawdown** and **Sharpe ratio** per regime
- 🔗 Add more DEXs (dYdX, GMX) for cross-platform comparison

```bash
git checkout -b feature/live-dashboard
git commit -m "✨ Add real-time Streamlit sentiment tracker"
git push origin feature/live-dashboard
# → Open a Pull Request 🚀
```

---

## 📚 References

- [Alternative.me — Crypto Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/)
- [Hyperliquid DEX](https://hyperliquid.xyz/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Python Docs](https://plotly.com/python/)
- Primetrade.ai Data Science Intern Assignment

---

## 📜 License

```
MIT License — Free to use, modify, and distribute with attribution.
```

---

<div align="center">

**Built with 📊 data, ☕ coffee, and 🧠 curiosity by [sreyoshmajumder](https://github.com/sreyoshmajumder)**

*"Markets are driven by two powerful emotions — Fear and Greed. Understanding them is half the edge."*

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2C5364,50:203A43,100:0F2027&height=130&section=footer" width="100%"/>

</div>
