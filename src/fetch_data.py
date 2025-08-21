import yfinance as yf
import pandas as pd
from pathlib import Path
import argparse
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" # DATA_DIR points to the raw data directory
DATA_DIR.mkdir(parents=True, exist_ok=True) # Creates the directory if it doesn't exist

# Fetches historical stock data for a given ticker symbol using yfinance.
def fetch_ticker(ticker, period="1y", interval="1d"):
  print(f"Fetching {ticker} for period={period}, interval={interval}")
  df = yf.download(ticker, period=period, interval=interval, progress=False)
  if df.empty:
    raise RuntimeError("No data returned for ticker: " + ticker)
  filename = DATA_DIR / f"{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
  df.to_csv(filename)
  print(f"Saved raw data to {filename}")
  return filename

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ticker", default="^GSPC")
  parser.add_argument("--period", default="6mo")
  parser.add_argument("--interval", default="1d")
  args = parser.parse_args()
  fetch_ticker(args.ticker, period=args.period, interval=args.interval)