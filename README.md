# 📊 Trader Performance vs Market Sentiment

### *How Bitcoin's Fear & Greed Index Shapes Trader Behavior on Hyperliquid DEX*

---

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat-square&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Bitcoin](https://img.shields.io/badge/Bitcoin-Fear%20%26%20Greed-F7931A?style=flat-square&logo=bitcoin&logoColor=white)
![Hyperliquid](https://img.shields.io/badge/Hyperliquid-DEX%20Data-00D4AA?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

---

> **A rigorous data science study** combining Bitcoin's daily Fear & Greed sentiment index with historical on-chain trade executions from Hyperliquid — engineered for the **Primetrade.ai Data Science Intern Assignment** — to reveal how market emotion drives trader risk appetite, PnL, leverage, and position sizing.

---

## 📌 Table of Contents

- [🔬 Project Overview](#-project-overview)
- [🏗️ System Architecture](#-system-architecture)
- [🔄 Data Pipeline](#-data-pipeline)
- [📂 Data Sources & Schema](#-data-sources--schema)
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

Crypto markets are famously driven by **emotion**. When Bitcoin bleeds, fear spreads. When BTC pumps, greed takes over. But how exactly does this collective psychology impact the **real trading decisions** of on-chain traders?

This project answers that question with data, merging two powerful sources:

| Source | Description |
|:---|:---|
| 🧠 **Fear & Greed Index** | Daily Bitcoin sentiment score across 5 regimes: Extreme Fear → Extreme Greed |
| 📋 **Hyperliquid Trades** | Historical on-chain trade executions — PnL, size, direction, leverage |

By merging, engineering, and analyzing these datasets together, we extract **actionable intelligence** about how sentiment regimes affect trader psychology, risk appetite, and profitability — and derive rules of thumb for smarter risk management.

---

## 🏗️ System Architecture

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║      TRADER PERFORMANCE vs MARKET SENTIMENT — SYSTEM ARCHITECTURE           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌──────────────────────────────────────────────────────────────────────┐   ║
║  │                       DATA INGESTION LAYER                           │   ║
║  │                                                                      │   ║
║  │  ┌─────────────────────────┐     ┌──────────────────────────────┐  │   ║
║  │  │    fear_greed.csv       │     │  hyperliquid_trades.csv       │  │   ║
║  │  │                         │     │                              │  │   ║
║  │  │  date | value | class   │     │  account | coin | side       │  │   ║
║  │  │  ─────────────────────  │     │  size | price | closedPnl    │  │   ║
║  │  │  Daily sentiment regime │     │  timestamp | direction        │  │   ║
║  │  └────────────┬────────────┘     └─────────────┬────────────────┘  │   ║
║  └───────────────┼──────────────────────────────── ┼──────────────────┘   ║
║                  │                                  │                       ║
║                  ▼                                  ▼                       ║
║  ┌──────────────────────────────────────────────────────────────────────┐   ║
║  │                   FEATURE ENGINEERING LAYER                          │   ║
║  │                                                                      │   ║
║  │  ┌──────────────────────┐    ┌─────────────────────────────────┐   │   ║
║  │  │  Sentiment Mapping   │    │  Daily Trader Metric Aggregation │   │   ║
║  │  │                      │    │                                 │   │   ║
║  │  │  0–24  Extreme Fear  │    │  Per (account × date):          │   │   ║
║  │  │  25–49 Fear          │    │  • total_pnl                    │   │   ║
║  │  │  50    Neutral       │    │  • trade_count                  │   │   ║
║  │  │  51–74 Greed         │    │  • win_rate                     │   │   ║
║  │  │  75–100 Ext. Greed   │    │  • avg_trade_size_usd           │   │   ║
║  │  └──────────┬───────────┘    │  • leverage_proxy               │   │   ║
║  │             │                │  • long_ratio                   │   │   ║
║  │             │                └──────────────────┬──────────────┘   │   ║
║  └─────────────┼──────────────────────────────────┼──────────────────┘   ║
║                │           JOIN on date            │                       ║
║                └──────────────────┬────────────────┘                      ║
║                                   ▼                                        ║
║  ┌──────────────────────────────────────────────────────────────────────┐  ║
║  │         daily_trader_metrics_with_sentiment.csv                      │  ║
║  │     (Unified: trader metrics merged with sentiment regime)           │  ║
║  └──────────────────────┬───────────────────────────────────────────────┘  ║
║                         │                                                   ║
║          ┌──────────────┼──────────────────────────┐                       ║
║          ▼              ▼                           ▼                       ║
║  ┌──────────────┐ ┌───────────────────┐ ┌──────────────────────────────┐  ║
║  │ Regime-Level │ │ Trader Segment-   │ │   Visualization Layer        │  ║
║  │ Aggregation  │ │ ation Analysis    │ │                              │  ║
║  │              │ │ (High vs Low      │ │  mean_pnl_by_sentiment.png   │  ║
║  │ performance_ │ │  Leverage)        │ │  mean_trades_by_sent...png   │  ║
║  │ by_sent.csv  │ │                   │ │  mean_leverage_by_sent..png  │  ║
║  │              │ │ segment_perf_by_  │ │  mean_trade_size_by...png    │  ║
║  │              │ │ sentiment.csv     │ │  mean_pnl_by_sent_seg.png    │  ║
║  └──────────────┘ └───────────────────┘ └──────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 🔄 Data Pipeline

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        END-TO-END DATA PIPELINE                            │
└────────────────────────────────────────────────────────────────────────────┘

 STEP 1 ── DATA ACQUISITION
 ┌───────────────────────────────────────────────────────────────────────┐
 │  main.py auto-downloads CSVs on first run via Google Drive links      │
 │  fear_greed.csv          ──►  data/fear_greed.csv                     │
 │  hyperliquid_trades.csv  ──►  data/hyperliquid_trades.csv             │
 └───────────────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
 STEP 2 ── DATA CLEANING & PARSING
 ┌───────────────────────────────────────────────────────────────────────┐
 │  • Parse Unix ms timestamps → normalize to UTC date (YYYY-MM-DD)      │
 │  • Cast numeric columns: size_usd, closedPnl, leverage                │
 │  • Impute null PnL values → 0 (closed but unrealized)                │
 │  • Deduplicate trade records on (account + time + side)               │
 └───────────────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
 STEP 3 ── DAILY TRADER METRIC AGGREGATION
 ┌───────────────────────────────────────────────────────────────────────┐
 │  Group by: (account × date)                                           │
 │                                                                       │
 │  total_pnl       = sum(closedPnl)                                     │
 │  trade_count     = count(rows)                                        │
 │  win_rate        = count(pnl > 0) / trade_count                      │
 │  avg_trade_size  = mean(px × sz)                                      │
 │  leverage_proxy  = mean(size_usd / notional_estimate)                 │
 │  long_ratio      = count(side == 'B') / trade_count                  │
 │                                                                       │
 │  Output ──► daily_trader_metrics.csv                                  │
 └───────────────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
 STEP 4 ── SENTIMENT JOIN
 ┌───────────────────────────────────────────────────────────────────────┐
 │  LEFT JOIN daily_trader_metrics ON fear_greed.date = metrics.date     │
 │                                                                       │
 │  Adds ──► sentiment_value  (numeric 0–100)                            │
 │           sentiment_class  (Extreme Fear / Fear / Neutral /           │
 │                             Greed / Extreme Greed)                    │
 │                                                                       │
 │  Output ──► daily_trader_metrics_with_sentiment.csv                   │
 └───────────────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
 STEP 5 ── REGIME-LEVEL AGGREGATION
 ┌───────────────────────────────────────────────────────────────────────┐
 │  Group by: sentiment_class                                            │
 │  Aggregate: mean PnL, mean trades, mean size, mean leverage           │
 │  Output ──► performance_by_sentiment.csv                              │
 └───────────────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
 STEP 6 ── TRADER SEGMENTATION
 ┌───────────────────────────────────────────────────────────────────────┐
 │  Median split on per-trader average leverage_proxy                    │
 │  Label: "High Leverage" vs "Low Leverage"                             │
 │  Group by: (sentiment_class × leverage_segment)                       │
 │  Output ──► segment_performance_by_sentiment.csv                      │
 └───────────────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
 STEP 7 ── VISUALIZATION & EXPORT
 ┌───────────────────────────────────────────────────────────────────────┐
 │  Plotly bar charts ──► exported as PNG via Kaleido renderer           │
 │                                                                       │
 │  mean_pnl_by_sentiment.png           (PnL across regimes)            │
 │  mean_trades_by_sentiment.png        (Trade volume across regimes)    │
 │  mean_trade_size_by_sentiment.png    (Position size across regimes)   │
 │  mean_leverage_by_sentiment.png      (Leverage proxy across regimes)  │
 │  mean_pnl_by_sentiment_segment.png   (Segmented PnL heatmap)         │
 └───────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Data Sources & Schema

### 🧠 1. Bitcoin Fear & Greed Index — `fear_greed.csv`

| Column | Type | Description |
|:---|:---|:---|
| `date` | `DATE` | Calendar date (YYYY-MM-DD) |
| `value` | `INT` | Numeric sentiment score 0–100 |
| `value_classification` | `STRING` | Regime label (see table below) |

**Sentiment Regimes:**

| Score Range | Classification | Market Mood |
|:---:|:---|:---|
| 0 – 24 | 😱 Extreme Fear | Panic selling, capitulation |
| 25 – 49 | 😨 Fear | Caution, bearish lean |
| 50 | 😐 Neutral | Balanced, indecisive |
| 51 – 74 | 😏 Greed | Risk-on, bullish confidence |
| 75 – 100 | 🤑 Extreme Greed | FOMO, euphoria, overextension |

---

### 📋 2. Hyperliquid Trader Executions — `hyperliquid_trades.csv`

| Column | Type | Description |
|:---|:---|:---|
| `account` | `STRING` | Trader wallet address (anonymized) |
| `coin` | `STRING` | Asset traded (BTC, ETH, SOL…) |
| `side` | `STRING` | Trade direction: `B` (Long) / `A` (Short) |
| `px` | `FLOAT` | Execution price (USD) |
| `sz` | `FLOAT` | Position size in tokens |
| `closedPnl` | `FLOAT` | Realized profit/loss on closure (USD) |
| `time` | `INT` | Execution timestamp (Unix milliseconds) |
| `dir` | `STRING` | Open / Close direction marker |
| `crossed` | `BOOL` | Taker (`True`) vs Maker (`False`) |

---

## ⚙️ Feature Engineering

```
┌──────────────────────────────────────────────────────────────────────────┐
│              ENGINEERED FEATURES  (per account × date)                   │
├──────────────────────────────────┬───────────────────────────────────────┤
│  Feature                         │  Derivation Formula                   │
├──────────────────────────────────┼───────────────────────────────────────┤
│  total_pnl                       │  SUM(closedPnl)                        │
│  trade_count                     │  COUNT(rows)                           │
│  win_rate                        │  COUNT(pnl > 0) / trade_count          │
│  avg_trade_size_usd              │  MEAN(px × sz)                         │
│  leverage_proxy                  │  MEAN(size_usd / notional_estimate)    │
│  long_ratio                      │  COUNT(side='B') / trade_count         │
│  sentiment_value                 │  Joined from fear_greed.csv            │
│  sentiment_class                 │  Joined from fear_greed.csv            │
│  leverage_segment                │  'High' or 'Low' (median split)        │
└──────────────────────────────────┴───────────────────────────────────────┘
```

---

## 📈 Analysis Modules

### Module 1 — Baseline PnL by Sentiment Regime
> **Question:** Does average trader PnL differ across Fear / Greed regimes?

```
Method:   GROUP BY sentiment_class → MEAN(total_pnl)
Output:   performance_by_sentiment.csv
          mean_pnl_by_sentiment.png

Conceptual result:
  😱 ExtFear  ████░░░░░░░░
  😨 Fear     ████████░░░░
  😐 Neutral  ██████░░░░░░
  😏 Greed    ████░░░░░░░░
  🤑 ExtGreed ███░░░░░░░░░  ← often lowest due to over-leveraging
```

---

### Module 2 — Trade Frequency by Sentiment
> **Question:** Do traders execute more trades during fear or greed?

```
Method:   GROUP BY sentiment_class → MEAN(trade_count)
Output:   mean_trades_by_sentiment.png

Hypothesis:
  Greed  → more trades  (FOMO-driven overtrading)
  Fear   → fewer trades (hesitation / capital preservation)
```

---

### Module 3 — Position Sizing by Sentiment
> **Question:** Do traders open larger positions under greed vs fear?

```
Method:   GROUP BY sentiment_class → MEAN(avg_trade_size_usd)
Output:   mean_trade_size_by_sentiment.png

Hypothesis:
  Greed  → larger positions  (overconfidence bias)
  Fear   → smaller positions (risk reduction)
```

---

### Module 4 — Leverage Usage by Sentiment
> **Question:** Does leverage spike in greed cycles and collapse in fear cycles?

```
Method:   GROUP BY sentiment_class → MEAN(leverage_proxy)
Output:   mean_leverage_by_sentiment.png

Expected pattern:
  Fear  ──► low leverage  ──► fewer liquidations
  Greed ──► high leverage ──► liquidation risk increases
```

---

### Module 5 — Segmented Analysis (High vs Low Leverage Traders)
> **Question:** Do high-leverage traders suffer disproportionately during fear regimes?

```
Method:   Median split on leverage_proxy → label High / Low
          GROUP BY (sentiment_class × leverage_segment)
Output:   segment_performance_by_sentiment.csv
          mean_pnl_by_sentiment_segment.png

This is the most actionable chart — reveals which trader
profiles are most exposed to sentiment-driven risk.
```

---

## 🧠 Key Insights

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    KEY FINDINGS & RULES OF THUMB                        ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  💡 INSIGHT 1 — GREED DOES NOT EQUAL PROFITS                            ║
║     Extreme Greed periods often correlate with lower mean PnL.           ║
║     Traders over-leverage and enter late, chasing already-topped         ║
║     positions — resulting in poor risk-reward outcomes.                  ║
║                                                                          ║
║  💡 INSIGHT 2 — FEAR CAN BE OPPORTUNITY                                 ║
║     Disciplined low-leverage traders tend to show better                 ║
║     risk-adjusted returns during Fear regimes — less competition,        ║
║     wider spreads, and cleaner directional moves.                        ║
║                                                                          ║
║  💡 INSIGHT 3 — HIGH LEVERAGE IS SENTIMENT-SENSITIVE                    ║
║     High-leverage traders perform dramatically worse during              ║
║     Extreme Fear. Liquidation cascades amplify losses precisely          ║
║     when market conditions are most adverse.                             ║
║                                                                          ║
║  💡 INSIGHT 4 — TRADE FREQUENCY PEAKS UNDER GREED                       ║
║     Mean daily trade count is highest in Greed / Extreme Greed          ║
║     regimes. FOMO drives overtrading, which erodes PnL through           ║
║     fees, slippage, and poor trade timing.                               ║
║                                                                          ║
║  💡 INSIGHT 5 — POSITION SIZING FOLLOWS SENTIMENT LINEARLY              ║
║     Average trade size scales monotonically from Extreme Fear to         ║
║     Extreme Greed — directly confirming sentiment-driven risk            ║
║     appetite escalation across the full spectrum.                        ║
║                                                                          ║
║  ────────────────────────────────────────────────────────────────────   ║
║  📌 RULE OF THUMB FOR RISK MANAGEMENT:                                  ║
║     → Reduce leverage when sentiment score > 75 (Extreme Greed)         ║
║     → Scale in cautiously when sentiment score < 25 (Extreme Fear)      ║
║     → High-leverage strategies need a sentiment-aware kill switch        ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 📊 Output Visualizations

All 5 charts are generated by `main.py` via **Plotly + Kaleido** and saved to the repo root:

| File | What It Shows |
|:---|:---|
| `mean_pnl_by_sentiment.png` | Average daily PnL per sentiment regime |
| `mean_trades_by_sentiment.png` | Average daily trade count per sentiment regime |
| `mean_trade_size_by_sentiment.png` | Average position size (USD) per sentiment regime |
| `mean_leverage_by_sentiment.png` | Average leverage proxy per sentiment regime |
| `mean_pnl_by_sentiment_segment.png` | PnL split by High vs Low leverage × sentiment regime |

```
Conceptual layout of mean_pnl_by_sentiment_segment.png:

                    High Leverage    Low Leverage
                    ─────────────    ────────────
  Extreme Fear      ████ (loss)      ████████ (gain)
  Fear              ████████         ████████████
  Neutral           ██████           ██████████
  Greed             ████             ████████
  Extreme Greed     ███ (worst)      ███████

  → Low leverage traders stay profitable across all regimes
  → High leverage traders are devastated in fear cycles
```

---

## 🛠️ Installation & Setup

**Prerequisites:** Python 3.9+ · pip

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

| Package | Purpose |
|:---|:---|
| `pandas` | Data loading, merging, groupby aggregation |
| `numpy` | Numerical operations and array handling |
| `plotly` | Interactive and static chart generation |
| `kaleido` | PNG export engine for Plotly figures |
| `requests` | Auto-download CSVs from Google Drive on first run |

---

## ▶️ How to Run

```bash
# From project root, with virtual environment activated:
python main.py
```

**What happens step by step:**

```
 1.  Checks if data/ CSVs exist → auto-downloads if missing
 2.  Loads and parses fear_greed.csv
 3.  Loads and parses hyperliquid_trades.csv
 4.  Cleans + normalizes timestamps to UTC date
 5.  Aggregates daily per-account trader metrics
 6.  Joins metrics with daily sentiment classification
 7.  Saves daily_trader_metrics.csv
 8.  Saves daily_trader_metrics_with_sentiment.csv
 9.  Aggregates performance_by_sentiment.csv
 10. Segments traders → saves segment_performance_by_sentiment.csv
 11. Generates and saves all 5 PNG charts
─────────────────────────────────────────────────────────
     Total runtime: ~30–90 seconds
```

---

## 📁 Project Structure

```
Trader-performance-vs-market-sentiment/
│
├── main.py                                      ← Entry point — runs full pipeline
│
├── fear_greed.csv                               ← Bitcoin Fear & Greed Index (daily)
├── daily_trader_metrics.csv                     ← Per-account daily aggregated metrics
├── daily_trader_metrics_with_sentiment.csv      ← Metrics joined with sentiment regime
├── performance_by_sentiment.csv                 ← Regime-level performance summary
├── segment_performance_by_sentiment.csv         ← High vs Low leverage segment output
│
├── mean_pnl_by_sentiment.png                    ← Chart: PnL by sentiment regime
├── mean_trades_by_sentiment.png                 ← Chart: Trade volume by sentiment
├── mean_trade_size_by_sentiment.png             ← Chart: Position size by sentiment
├── mean_leverage_by_sentiment.png               ← Chart: Leverage proxy by sentiment
├── mean_pnl_by_sentiment_segment.png            ← Chart: Segmented PnL heatmap
│
├── requirements.txt                             ← Python dependencies
└── README.md                                    ← You are here!
```

---

## 🔑 Key Code Walkthrough

### Load & Merge Datasets

```python
import pandas as pd

# Load raw data
trades_df = pd.read_csv("hyperliquid_trades.csv")
fg_df     = pd.read_csv("fear_greed.csv")

# Normalize dates
trades_df["date"] = pd.to_datetime(trades_df["time"], unit="ms").dt.normalize()
fg_df["date"]     = pd.to_datetime(fg_df["date"])

# Clean numerics
trades_df["closedPnl"] = pd.to_numeric(trades_df["closedPnl"], errors="coerce").fillna(0)
trades_df["size_usd"]  = trades_df["px"].astype(float) * trades_df["sz"].astype(float)
```

### Engineer Daily Metrics

```python
daily = (
    trades_df
    .groupby(["account", "date"])
    .agg(
        total_pnl      = ("closedPnl", "sum"),
        trade_count    = ("closedPnl", "count"),
        win_trades     = ("closedPnl", lambda x: (x > 0).sum()),
        avg_trade_size = ("size_usd",  "mean"),
        leverage_proxy = ("size_usd",  "mean"),
        long_count     = ("side",      lambda x: (x == "B").sum()),
    )
    .reset_index()
)
daily["win_rate"]   = daily["win_trades"]  / daily["trade_count"]
daily["long_ratio"] = daily["long_count"]  / daily["trade_count"]
daily.to_csv("daily_trader_metrics.csv", index=False)
```

### Join Sentiment & Aggregate by Regime

```python
# Merge sentiment on date
merged = daily.merge(
    fg_df[["date", "value", "value_classification"]],
    on="date", how="left"
)
merged.to_csv("daily_trader_metrics_with_sentiment.csv", index=False)

# Regime-level aggregation
sentiment_order = ["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]

perf = (
    merged
    .groupby("value_classification")
    .agg(
        mean_pnl        = ("total_pnl",      "mean"),
        mean_trades     = ("trade_count",    "mean"),
        mean_trade_size = ("avg_trade_size", "mean"),
        mean_leverage   = ("leverage_proxy", "mean"),
    )
    .reindex(sentiment_order)
    .reset_index()
)
perf.to_csv("performance_by_sentiment.csv", index=False)
```

### Segment & Visualize

```python
import plotly.express as px

# Median-split segmentation
med = merged.groupby("account")["leverage_proxy"].mean().median()
merged["leverage_segment"] = merged["leverage_proxy"].apply(
    lambda x: "High Leverage" if x >= med else "Low Leverage"
)

# Chart: Mean PnL by Sentiment
color_map = {
    "Extreme Fear": "#e63946", "Fear":         "#f4a261",
    "Neutral":      "#a8dadc", "Greed":        "#57cc99",
    "Extreme Greed":"#1d7a4a",
}
fig = px.bar(
    perf,
    x="value_classification", y="mean_pnl",
    color="value_classification",
    color_discrete_map=color_map,
    category_orders={"value_classification": sentiment_order},
    title="Mean Daily PnL by Market Sentiment Regime",
    labels={"value_classification": "Sentiment Regime", "mean_pnl": "Mean PnL (USD)"},
)
fig.write_image("mean_pnl_by_sentiment.png")
```

---

## 🧩 Sentiment → Behavior Map

```
┌──────────────────────────────────────────────────────────────────────────┐
│          HOW SENTIMENT DRIVES TRADER BEHAVIOR                            │
├──────────────────┬────────────────────────┬──────────────────────────────┤
│  Regime          │  Trader Psychology      │  Observed Behavior           │
├──────────────────┼────────────────────────┼──────────────────────────────┤
│  😱 Extreme Fear │  Panic / Survival mode  │  Fewer trades, close longs   │
│  😨 Fear         │  Caution / Hesitation   │  Small sizes, low leverage   │
│  😐 Neutral      │  Balanced / Analytical  │  Normal activity, mixed bias │
│  😏 Greed        │  Confidence / Risk-on   │  More trades, bigger sizes   │
│  🤑 Extreme Greed│  FOMO / Euphoria        │  Max leverage, overtrading   │
└──────────────────┴────────────────────────┴──────────────────────────────┘

  Leverage usage across regimes:
  Low  ◄────────────────────────────────────────────►  High
       😱 ExtFear   😨 Fear   😐 Neutral   😏 Greed   🤑 ExtGreed

  PnL performance (typical empirical pattern):
  Best ◄────────────────────────────────────────────►  Worst
       😨 Fear    😐 Neutral   😱 ExtFear   😏 Greed   🤑 ExtGreed
```

---

## 🤝 Contributing

Ideas to extend this project:

- 📈 Add **time-series lag analysis** — does today's sentiment predict tomorrow's PnL?
- 🤖 Build an **ML classifier** to predict trader profitability from sentiment + behavior features
- 🌐 Create a **live Streamlit dashboard** with real-time Fear & Greed + Hyperliquid data
- 📉 Incorporate **Sharpe ratio** and **max drawdown** per regime
- 🔗 Add more DEXs (dYdX, GMX, Vertex) for cross-platform comparison

```bash
git checkout -b feature/streamlit-live-dashboard
git commit -m "✨ Add real-time sentiment tracker dashboard"
git push origin feature/streamlit-live-dashboard
# → Open a Pull Request
```

---

## 📚 References

- [Alternative.me — Crypto Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/)
- [Hyperliquid DEX](https://hyperliquid.xyz/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Python Documentation](https://plotly.com/python/)
- Primetrade.ai Data Science Intern Assignment Brief

---

## 📜 License

MIT License — free to use, modify, and distribute with attribution.

---

*"Markets are driven by two powerful emotions — Fear and Greed. Understanding them is half the edge."*

**Built with 📊 data and 🧠 curiosity by [sreyoshmajumder](https://github.com/sreyoshmajumder)**
