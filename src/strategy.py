# This dataclasses package is used to create classes that primarily store data using decorator
from dataclasses import dataclass
import pandas as pd
import numpy as np
from .utils import setup_logger

logger = setup_logger("strategy")

# Decorator in Python to automatically generate special methods like __init__()
@dataclass
class Signal:
    timestamp: pd.Timestamp
    side: str # "enter_long_spread", "enter_short_spread", "exit"
    price_x: float
    price_y: float
    zscore: float

class PairStrategy:
    def __init__(self, beta: float, lookback: int = 20, entry_zscore: float = 2.0, exit_zscore: float = 0.5):
        self.beta = beta
        self.lookback = lookback
        self.entry_zscore = entry_zscore
        self.exit_zscore = exit_zscore

    def compute_spread(self, series_x: pd.Series, series_y: pd.Series) -> pd.Series:
        """
        Compute spread series: spread = price_y - beta * price_x
        """
        df = pd.concat([series_x, series_y], axis = 1).dropna()
        spread = df.iloc[:, 1] - self.beta * df.iloc[:, 0]
        spread.name = "spread"
        return spread
    
    def zscore(self, spread: pd.Series) -> pd.Series:
        """
        Compute rolling z-score of the spread series
        zscore = (spread - rolling_mean) / rolling_std
        """
        rolling_mean = spread.rolling(window = self.lookback).mean()
        rolling_std = spread.rolling(window = self.lookback).std()

        zscore_spread = (spread - rolling_mean) / rolling_std
        zscore_spread.name = "zscore_spread"
        return zscore_spread