"""Centralized logging configuration for the calculator."""

import logging
import os


class Logger:
    """Sets up and provides a logger that writes to a configured log file."""

    _counter = 0

    def __init__(self, log_file: str = "logs/calculator.log"):
        self.log_file = log_file
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        # Unique logger name per instance so each writes to its own file
        Logger._counter += 1
        self.logger = logging.getLogger(f"calculator_{Logger._counter}")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message: str) -> None:
        self.logger.info(message)
        for h in self.logger.handlers:
            h.flush()

    def warning(self, message: str) -> None:
        self.logger.warning(message)
        for h in self.logger.handlers:
            h.flush()

    def error(self, message: str) -> None:
        self.logger.error(message)
        for h in self.logger.handlers:
            h.flush()