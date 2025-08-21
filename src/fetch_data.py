import yfinance as yf
import pandas as pd
from pathlib import Path
import argparse
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" # DATA_DIR points to the raw data directory
DATA_DIR.mkdir(parents=True, exist_ok=True) # Creates the directory if it doesn't exist