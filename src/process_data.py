# src/process_data.py
import pandas as pd
from pathlib import Path
import argparse
import glob

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def process_file(path):
    # Read file (skip first 2 metadata rows, then enforce proper column names)
    df = pd.read_csv(path, header=2)
    df.columns = ["date", "close", "high", "low", "open", "volume"]

    # Drop any rows where 'date' is not valid
    df = df[pd.to_datetime(df["date"], errors="coerce").notna()]
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").set_index("date")

    # Calculate daily return
    df["daily_return"] = df["close"].pct_change()

    # Calculate moving averages
    df["sma_10"] = df["close"].rolling(window=10).mean()
    df["sma_50"] = df["close"].rolling(window=50).mean()

    # Calculate annualized volatility (20-day rolling window)
    df["vol_20"] = df["daily_return"].rolling(window=20).std() * (252 ** 0.5)

    # Save processed file
    out_path = OUT_DIR / (Path(path).stem + "_processed.csv")
    df.to_csv(out_path)
    print(f"Processed and saved to {out_path}")

    return out_path

def process_all():
    files = glob.glob(str(RAW_DIR / "*.csv"))
    if not files:
        print("No raw files to process. Run fetch_data first.")
        return
    for f in files:
        process_file(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--file", help="path to raw csv")
    args = parser.parse_args()
    if args.all:
        process_all()
    elif args.file:
        process_file(args.file)
    else:
        process_all()
