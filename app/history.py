"""History management with the Observer pattern and pandas persistence."""

import os
from abc import ABC, abstractmethod

import pandas as pd

from app.calculation import Calculation
from app.exceptions import OperationError
from app.logger import Logger


class HistoryObserver(ABC):
    """Abstract observer notified when a calculation occurs."""

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """React to a new calculation."""


class LoggingObserver(HistoryObserver):
    """Observer that logs each calculation to the log file."""

    def __init__(self, logger: Logger):
        self.logger = logger

    def update(self, calculation: Calculation) -> None:
        self.logger.info(
            f"Calculation: {calculation.operation_name}("
            f"{calculation.a}, {calculation.b}) = {calculation.result}"
        )


class AutoSaveObserver(HistoryObserver):
    """Observer that auto-saves history to CSV after each calculation."""

    def __init__(self, history_manager):
        self.history_manager = history_manager

    def update(self, calculation: Calculation) -> None:
        self.history_manager.save()


class HistoryManager:
    """Manages the list of calculations and persists them with pandas."""

    COLUMNS = ["operation", "operand1", "operand2", "result", "timestamp"]

    def __init__(self, history_file: str = "history/calculator_history.csv",
                 max_size: int = 100, encoding: str = "utf-8"):
        self.history_file = history_file
        self.max_size = max_size
        self.encoding = encoding
        self._history = []
        self._observers = []
        history_dir = os.path.dirname(history_file)
        if history_dir:
            os.makedirs(history_dir, exist_ok=True)

    def add_observer(self, observer: HistoryObserver) -> None:
        self._observers.append(observer)

    def notify(self, calculation: Calculation) -> None:
        for observer in self._observers:
            observer.update(calculation)

    def add_calculation(self, calculation: Calculation) -> None:
        self._history.append(calculation)
        if len(self._history) > self.max_size:
            self._history.pop(0)
        self.notify(calculation)

    def get_history(self) -> list:
        return self._history

    def is_empty(self) -> bool:
        return len(self._history) == 0

    def clear(self) -> None:
        self._history = []

    def to_dataframe(self) -> pd.DataFrame:
        rows = [calc.to_dict() for calc in self._history]
        return pd.DataFrame(rows, columns=self.COLUMNS)

    def save(self) -> None:
        """Serialize history to CSV using pandas."""
        try:
            df = self.to_dataframe()
            df.to_csv(self.history_file, index=False, encoding=self.encoding)
        except OSError as e:
            raise OperationError(f"Failed to save history: {e}")

    def load(self) -> None:
        """Deserialize history from CSV using pandas."""
        if not os.path.exists(self.history_file):
            raise OperationError("No history file found to load")
        try:
            df = pd.read_csv(self.history_file, encoding=self.encoding)
        except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            raise OperationError(f"History file is malformed: {e}")

        try:
            loaded = [Calculation.from_dict(row.to_dict()) for _, row in df.iterrows()]
        except (KeyError, ValueError, TypeError, OperationError) as e:
            raise OperationError(f"History file is malformed: {e}")
        self._history = loaded