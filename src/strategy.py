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
    
    def generate_signals(self, series_x: pd.Series, series_y: pd.Series) -> pd.DataFrame:
        """
        Generate trading signals based on z-score thresholds
        Returns DataFrame of Signal dataclass instances
        """
        spread = self.compute_spread(series_x, series_y)
        zscore_spread = self.zscore(spread)

        df = pd.DataFrame({"series_x": series_x, "series_y": series_y, "spread": spread, "zscore_spread": zscore_spread}).dropna()
        signals = []
        position = 0 # 0 = flat, 1 = long spread (long y, short x), -1 = short spread

        for idx, row in df.iterrows():
            zscore_value = row["zscore_spread"]

            if position == 0:
                # if spread too high => short spread
                if zscore_value > self.entry_zscore:
                    # Enter short spread: short y, long x
                    signals.append(Signal(timestamp = idx, side = "enter_short_spread", price_x = row["series_x"], price_y = row["series_y"], zscore = zscore_value))
                    position = -1
                # if spread too low => long spread
                elif zscore_value < -self.entry_zscore:
                    # Enter long spread: long y, short x
                    signals.append(Signal(timestamp = idx, side = "enter_long_spread", price_x = row["series_x"], price_y = row["series_y"], zscore = zscore_value))
                    position = 1        
            elif position == 1:
                if abs(zscore_value) < self.exit_zscore:
                    # Exit long spread because z-score reverted from low value to neutral
                    signals.append(Signal(timestamp = idx, side = "exit", price_x = row["series_x"], price_y = row["series_y"], zscore = zscore_value))
                    position = 0
            elif position == -1:
                if abs(zscore_value) < self.exit_zscore:
                    # Exit short spread because z-score reverted from high value to neutral 
                    signals.append(Signal(timestamp = idx, side = "exit", price_x = row["series_x"], price_y = row["series_y"], zscore = zscore_value))
                    position = 0

        # return as DataFrame
        # s.__dict__ converts dataclass instance (variable) stored inside s to dictionary
    
        return pd.DataFrame([s.__dict__ for s in signals]).set_index("timestamp")