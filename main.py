import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import requests


# ------------- Paths and Google Drive config -------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "outputs"

DATA_DIR.mkdir(exist_ok=True, parents=True)
OUT_DIR.mkdir(exist_ok=True, parents=True)

# Google Drive file IDs from the assignment links
FEAR_GREED_ID = "1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf"
TRADES_ID = "1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs"

FEAR_GREED_URL = f"https://drive.google.com/uc?export=download&id={FEAR_GREED_ID}"
TRADES_URL = f"https://drive.google.com/uc?export=download&id={TRADES_ID}"

FEAR_GREED_PATH = DATA_DIR / "fear_greed.csv"
TRADES_PATH = DATA_DIR / "hyperliquid_trades.csv"


# ------------- Utility: download from Google Drive -------------

def download_if_missing(url: str, dest: Path):
    """
    Download a CSV from Google Drive if it's not already present locally.
    """
    if dest.exists():
        print(f"[INFO] Using existing file: {dest}")
        return

    print(f"[INFO] Downloading {url} -> {dest}")
    resp = requests.get(url)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    print(f"[INFO] Saved: {dest}")


# ------------- Load data -------------

def load_datasets():
    download_if_missing(FEAR_GREED_URL, FEAR_GREED_PATH)
    download_if_missing(TRADES_URL, TRADES_PATH)

    fear_df = pd.read_csv(FEAR_GREED_PATH)
    trades_df = pd.read_csv(TRADES_PATH)

    print("[INFO] Fear/Greed shape:", fear_df.shape)
    print("[INFO] Trades shape:", trades_df.shape)

    return fear_df, trades_df


# ------------- Clean and align sentiment dataset -------------

def prepare_sentiment(fear_df: pd.DataFrame) -> pd.DataFrame:
    # Find date column
    fg_date_candidates = [c for c in fear_df.columns if "date" in c.lower()]
    fg_date_col = fg_date_candidates[0] if fg_date_candidates else fear_df.columns[0]

    fear_df["date"] = pd.to_datetime(fear_df[fg_date_col])

    # Find classification / sentiment column
    fg_class_candidates = [
        c for c in fear_df.columns
        if any(k in c.lower() for k in ["class", "sentiment", "fear", "greed"])
    ]
    fg_class_col = fg_class_candidates[0] if fg_class_candidates else fear_df.columns[1]

    fear_df["sentiment"] = fear_df[fg_class_col].astype(str).str.strip().str.title()
    fear_df["day"] = fear_df["date"].dt.date

    fear_df = fear_df[["day", "sentiment"]].drop_duplicates()

    print("[INFO] Prepared sentiment dataset:")
    print(fear_df.head())

    return fear_df


# ------------- Clean trades and engineer features -------------

def prepare_trades(trades_df: pd.DataFrame):
    # Time column
    time_cols = [c for c in trades_df.columns
                 if "time" in c.lower() or "timestamp" in c.lower()]
    tr_time_col = time_cols[0] if time_cols else trades_df.columns[0]

    trades_df["time_dt"] = pd.to_datetime(
        trades_df[tr_time_col],
        dayfirst=True,
        errors="coerce",
    )
    trades_df["day"] = trades_df["time_dt"].dt.date

    # Account column
    acct_cols = [c for c in trades_df.columns
                 if any(k in c.lower() for k in ["account", "user", "trader"])]
    acct_col = acct_cols[0] if acct_cols else "account"
    if acct_col not in trades_df.columns:
        trades_df[acct_col] = "unknown"

    # Side column
    side_cols = [c for c in trades_df.columns
                 if "side" in c.lower() or "direction" in c.lower()]
    side_col = side_cols[0] if side_cols else None

    # PnL column
    pnl_cols = [c for c in trades_df.columns if "pnl" in c.lower()]
    pnl_col = pnl_cols[0] if pnl_cols else None

    # Size column
    size_cols = [c for c in trades_df.columns
                 if any(k in c.lower() for k in ["size", "qty", "quantity"])]
    size_col = size_cols[0] if size_cols else None

    # Leverage column
    lev_cols = [c for c in trades_df.columns if "lev" in c.lower()]
    lev_col = lev_cols[0] if lev_cols else None

    # Numeric features
    if pnl_col:
        trades_df["pnl"] = pd.to_numeric(trades_df[pnl_col], errors="coerce").fillna(0)
    else:
        trades_df["pnl"] = 0.0
    trades_df["is_win"] = (trades_df["pnl"] > 0).astype(int)

    if size_col:
        trades_df["trade_size"] = pd.to_numeric(trades_df[size_col], errors="coerce").abs()
    else:
        trades_df["trade_size"] = np.nan

    if lev_col:
        trades_df["leverage"] = pd.to_numeric(trades_df[lev_col], errors="coerce")
    else:
        trades_df["leverage"] = np.nan

    if side_col:
        trades_df["side_std"] = trades_df[side_col].astype(str).str.lower().str[0]  # 'l'/'s'
    else:
        trades_df["side_std"] = np.nan

    return trades_df, acct_col


def compute_daily_metrics(trades_df: pd.DataFrame, acct_col: str) -> pd.DataFrame:
    group_cols = ["day", acct_col]

    daily_metrics = (
        trades_df
        .groupby(group_cols)
        .agg(
            daily_pnl      = ("pnl", "sum"),
            trade_count    = ("pnl", "count"),
            win_rate       = ("is_win", "mean"),
            avg_trade_size = ("trade_size", "mean"),
            avg_leverage   = ("leverage", "mean"),
            long_ratio     = ("side_std", lambda x: np.mean(x == "l") if x.notna().any() else np.nan),
        )
        .reset_index()
    )

    out_path = OUT_DIR / "daily_trader_metrics.csv"
    daily_metrics.to_csv(out_path, index=False)
    print(f"[INFO] Saved daily metrics: {out_path}")

    return daily_metrics


# ------------- Merge with sentiment and compute aggregates -------------

def merge_with_sentiment(daily_metrics: pd.DataFrame, fear_df: pd.DataFrame) -> pd.DataFrame:
    merged = daily_metrics.merge(fear_df, on="day", how="left")
    out_path = OUT_DIR / "daily_trader_metrics_with_sentiment.csv"
    merged.to_csv(out_path, index=False)
    print(f"[INFO] Saved merged daily metrics: {out_path}")
    return merged


def performance_by_sentiment(merged: pd.DataFrame) -> pd.DataFrame:
    perf_by_sent = (
        merged
        .dropna(subset=["sentiment"])
        .groupby("sentiment")
        .agg(
            mean_daily_pnl      = ("daily_pnl", "mean"),
            median_daily_pnl    = ("daily_pnl", "median"),
            mean_win_rate       = ("win_rate", "mean"),
            mean_trade_count    = ("trade_count", "mean"),
            mean_avg_trade_size = ("avg_trade_size", "mean"),
            mean_long_ratio     = ("long_ratio", "mean"),
        )
        .reset_index()
    )

    out_path = OUT_DIR / "performance_by_sentiment.csv"
    perf_by_sent.to_csv(out_path, index=False)
    print(f"[INFO] Saved performance by sentiment: {out_path}")

    return perf_by_sent



def segment_high_low_leverage(daily_metrics: pd.DataFrame, merged: pd.DataFrame, acct_col: str) -> pd.DataFrame:
    trader_lev = (
        daily_metrics
        .groupby(acct_col)["avg_leverage"]
        .median()
        .reset_index(name="median_leverage")
    )

    lev_threshold = trader_lev["median_leverage"].median()
    trader_lev["lev_segment"] = np.where(
        trader_lev["median_leverage"] >= lev_threshold,
        "high_lev",
        "low_lev",
    )

    merged_seg = merged.merge(trader_lev[[acct_col, "lev_segment"]], on=acct_col, how="left")

    seg_perf = (
        merged_seg
        .dropna(subset=["sentiment", "lev_segment"])
        .groupby(["sentiment", "lev_segment"])
        .agg(
            mean_daily_pnl    = ("daily_pnl", "mean"),
            mean_win_rate     = ("win_rate", "mean"),
            mean_trade_count  = ("trade_count", "mean"),
            mean_avg_leverage = ("avg_leverage", "mean"),
        )
        .reset_index()
    )

    out_path = OUT_DIR / "segment_performance_by_sentiment.csv"
    seg_perf.to_csv(out_path, index=False)
    print(f"[INFO] Saved segment performance by sentiment: {out_path}")

    return seg_perf


# ------------- Plotting functions -------------

def plot_mean_pnl_by_sentiment(perf_by_sent: pd.DataFrame):
    fig = px.bar(
        perf_by_sent,
        x="sentiment",
        y="mean_daily_pnl",
        title="Mean daily PnL by market sentiment",
    )
    fig.update_xaxes(title_text="Sentiment")
    fig.update_yaxes(title_text="Mean daily PnL")
    out_path = OUT_DIR / "mean_pnl_by_sentiment.png"
    fig.write_image(out_path)
    print(f"[INFO] Saved chart: {out_path}")


def plot_mean_trades_by_sentiment(perf_by_sent: pd.DataFrame):
    fig = px.bar(
        perf_by_sent,
        x="sentiment",
        y="mean_trade_count",
        title="Mean daily trades by market sentiment",
    )
    fig.update_xaxes(title_text="Sentiment")
    fig.update_yaxes(title_text="Mean trades per day")
    out_path = OUT_DIR / "mean_trades_by_sentiment.png"
    fig.write_image(out_path)
    print(f"[INFO] Saved chart: {out_path}")


def plot_mean_trade_size_by_sentiment(perf_by_sent: pd.DataFrame):
    fig = px.bar(
        perf_by_sent,
        x="sentiment",
        y="mean_avg_trade_size",   # <- note: trade size column
        title="Mean trade size by market sentiment",
    )
    fig.update_xaxes(title_text="Sentiment")
    fig.update_yaxes(title_text="Mean trade size")
    out_path = OUT_DIR / "mean_trade_size_by_sentiment.png"
    fig.write_image(out_path)
    print(f"[INFO] Saved chart: {out_path}")



def plot_segment_pnl_by_sentiment(seg_perf: pd.DataFrame):
    fig = px.bar(
        seg_perf,
        x="sentiment",
        y="mean_daily_pnl",
        color="lev_segment",
        barmode="group",
        title="Mean daily PnL by sentiment and leverage segment",
    )
    fig.update_xaxes(title_text="Sentiment")
    fig.update_yaxes(title_text="Mean daily PnL")
    out_path = OUT_DIR / "mean_pnl_by_sentiment_segment.png"
    fig.write_image(out_path)
    print(f"[INFO] Saved chart: {out_path}")


# ------------- Main pipeline -------------

def main():
    # Load
    fear_df, trades_df = load_datasets()

    # Sentiment prep
    fear_prepped = prepare_sentiment(fear_df)

    # Trades prep + metrics
    trades_prepped, acct_col = prepare_trades(trades_df)
    daily_metrics = compute_daily_metrics(trades_prepped, acct_col)

    # Merge & aggregates
    merged = merge_with_sentiment(daily_metrics, fear_prepped)
    perf_by_sent = performance_by_sentiment(merged)
    seg_perf = segment_high_low_leverage(daily_metrics, merged, acct_col)

    # ---- PLOTS (use ONLY these four lines) ----
    plot_mean_pnl_by_sentiment(perf_by_sent)
    plot_mean_trades_by_sentiment(perf_by_sent)
    plot_mean_trade_size_by_sentiment(perf_by_sent)   # <- new function
    plot_segment_pnl_by_sentiment(seg_perf)

    print("[INFO] Pipeline complete. Check 'outputs/' for CSVs and charts.")


    print("[INFO] Pipeline complete. Check 'outputs/' for CSVs and charts.")


if __name__ == "__main__":
    main()
