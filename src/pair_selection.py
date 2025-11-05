from typing import Tuple, Optional
import pandas as pd
from statsmodels.tsa.stattools import coint
from sklearn.linear_model import LinearRegression
from .utils import setup_logger

logger = setup_logger("pair_selection")

class PairSelector:
    def __init__(self, pvalue_threshold: float = 0.05):
        self.pvalue_threshold = pvalue_threshold

    def test_cointegration(self, s1: pd.Series, s2: pd.Series) -> float:
        """
        Returns p-value of Engle-Granger cointegration test
        """

        df = pd.concat([s1, s2], axis = 1).dropna()
        if df.shape[0] < 50:
            logger.warning("Not enough data points for cointegration test %d", df.shape[0])

        _, pvalue, _ = coint(df.iloc[:, 0], df.iloc[:, 1])
        return pvalue
    
    def hedge_ratio(self, s1: pd.Series, s2: pd.Series) -> Optional[float]:
        """
        Returns hedge ration (beta) from linear regression of s1 ~ s2
        """
        df = pd.concat([s1, s2], axis = 1).dropna()
        if df.shape[0] < 2:
            logger.warning("Not enough data points for hedge ratio calculation %s", df.shape[0])
            return None

        # reshape to 2D array for sklearn, -1 means infer dimension from number of rows
        X = df.iloc[:, 1].values.reshape(-1, 1)
        y = df.iloc[:, 0].values

        model = LinearRegression()
        model.fit(X, y)

        return float(model.coef_[0])
        
    def select_pair(self, s1: pd.Series, s2: pd.Series) -> Optional[Tuple[float, float]]:
        """
        Test whether two series form a cointegrated pair.
        If yes, return hedge ratio and p-value.
        Otherwise, return None.
        """
        pvalue = self.test_cointegration(s1, s2)
        logger.info("Cointegration test p-value: %.4f", pvalue)
        if pvalue < self.pvalue_threshold:
            hedge_ratio = self.hedge_ratio(s1, s2)
            logger.info("Hedge ratio: %.4f", hedge_ratio)
            if hedge_ratio is None:
                return None
            return pvalue, hedge_ratio
        else:
            logger.info("Pair rejected due to high p-value %.4f", pvalue)
            return None
