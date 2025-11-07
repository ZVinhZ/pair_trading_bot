from abc import ABC, abstractmethod
from typing import Dict, Any
from .utils import setup_logger

logger = setup_logger("executor")

class Executor(ABC):
    @abstractmethod
    def submit_order(self, symbol: str, side: str, quantity: int) -> Dict[str, Any]:
        pass

class PaperExecutor(Executor):
    def __init__(self):
        self.trades = []

    def submit_order(self, symbol: str, side: str, quantity: int) -> Dict[str, Any]:
        """Simulate order submission by logging the trade details.
        """
        trade = {"symbol": symbol, "side": side, "quantity": quantity}
        self.trades.append(trade)
        logger.info("Paper order submitted: %s", trade)
        
        return {"status": "submitted", "trade": trade}