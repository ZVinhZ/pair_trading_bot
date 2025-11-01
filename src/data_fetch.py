import yfinance as yf
import pandas as pd
from pathlib import Path

# Set the folder where data files will be stored
DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
# create the folder if it doesn't exist and don't give error if it's already there
DATA_DIRECTORY.mkdir(exist_ok = True) 

def fetch_close_series(ticker: str, start: str, end: str) -> pd.Series:
    """
    Download historical Close prices for a stock using yfinance
    """
    df = yf.download(ticker, start = start, end = end, progress = False, auto_adjust= False)

    if df.empty:
        print(f"No data found for {ticker}")
        return None
    
    series = df["Close"]
    series.name = ticker
    return series

def save_series_to_csv(series: pd.Series, filename: str):
    """
    Save a price series as a CSV inside the /data folder.
    """
    filepath = DATA_DIRECTORY / filename
    series.to_csv(filepath)
    return filepath
