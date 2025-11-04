from pathlib import Path
from typing import Optional
import yfinance as yf
import pandas as pd
from .config import DATA_DIRECTORY
from .utils import setup_logger


logger = setup_logger("data_fetch")
class DataFetcher:
    def __init__(self, data_dir: Path = DATA_DIRECTORY):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents = True, exist_ok = True)

    def fetch_close_series(self, ticker: str, start: str, end: str, auto_adjust: bool = False) -> Optional[pd.Series]:
        """
        Download Close price series
        Return pandas Series named by ticker.
        Caches downloaded CSV under data_dir/{ticker}.csv
        """
        path = self.data_dir / f"{ticker}.csv"

        try:
            logger.info("Downloading %s %s -> %s", ticker, start, end)

            df = yf.download(ticker, start = start, end = end, progress = False, auto_adjust = auto_adjust)

            if df is None or df.empty:
                logger.warning("No data found for %s", ticker)
                return None
            
            series = df["Close"].copy()
            series.name = ticker

            # Save to cache
            series.to_csv(path)
            logger.info("Saved %s", Path)

            return series
        
        except Exception as e:
            logger.exception("Failed fetching %s %s", ticker ,e)
            return None

    def load_series_from_csv(self, ticker: str) -> Optional[pd.Series]:
        path = self.data_dir / f"{ticker}.csv"
        
        if not path.exists:
            logger.warning("Cache not found for %s", ticker)
            return None
        
        serie = pd.read_csv(path, index_col = 0, parse_dates = True).iloc[:, 0]
        serie.name = ticker

        return serie
