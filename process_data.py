import pandas as pd
from pathlib import Path
import argparse
import glob

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"  # RAW_DIR points to the raw data directory
OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"  # OUT_DIR points to the processed data directory
OUT_DIR.mkdir(parents=True, exist_ok=True)  # Creates the directory if it doesn't exist

def read_csv_with_real_header(path):
    # Detect the header row containing 'Close'
    with open(path, 'r') as f:
        for i, line in enumerate(f):
            if 'Close' in line:
                header_row = i
                break

    df = pd.read_csv(path, header=header_row, parse_dates=[0])
    df.columns = df.columns.str.strip().str.lower()
    return df

def process_file(path):
    # Skip the first 2 rows to get to actual data
    df = pd.read_csv(path, header=2)
    
    # Rename columns to standard names
    df.columns = ['date', 'close', 'high', 'low', 'open', 'volume']
    
    # Drop any rows where 'date' is invalid
    df = df[pd.to_datetime(df['date'], errors='coerce').notna()]
    
    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Now 'close' column is guaranteed to exist
    print(f"Processed file: {path}")
    print(df.head())
    
    return df



def process_all():
  files = glob.glob(str(RAW_DIR / "*.csv"))
  if not files:
    print("No raw data files to process. Running fetch_data.py first is recommended.")
    return
  for file in files:
    process_file(file)

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