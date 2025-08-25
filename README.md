# MiniProject2025
StockMarketDataPipeline

---
A small ETL (Extract-Transform-Load) pipeline that downloads historical stock data, computes simple indicators, and stores processed results for quick analysis.

## Quick start
In cmd:
cd <\PathToProjectRoot>
python -m venv .venv (If venv not already created)
.venv\Scripts\activate (Activates venv)

pip install -r requirements.txt (Install dependencies)
python src/fetch_data.py --ticker <\StockTicker> --period 1y (Retrieves raw data)
python src/process_data.py --file data/raw/<\fileName>.csv (Makes raw data readable)
OR python src/process_data.py --all 
jupyter notebook notebooks/quick_demo.ipynb (Run through each cell)

deactivate (After finished with use)