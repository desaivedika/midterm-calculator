"""Configuration management using environment variables and dotenv."""

import os
from dotenv import load_dotenv

from app.exceptions import ConfigurationError

load_dotenv()


class CalculatorConfig:
    """Loads and validates calculator configuration from the environment."""

    def __init__(self):
        self.log_dir = os.getenv("CALCULATOR_LOG_DIR", "logs")
        self.history_dir = os.getenv("CALCULATOR_HISTORY_DIR", "history")
        self.max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
        self.auto_save = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
        self.precision = int(os.getenv("CALCULATOR_PRECISION", "10"))
        self.max_input_value = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e15"))
        self.default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")
        self.log_file = os.getenv(
            "CALCULATOR_LOG_FILE", os.path.join(self.log_dir, "calculator.log")
        )
        self.history_file = os.getenv(
            "CALCULATOR_HISTORY_FILE",
            os.path.join(self.history_dir, "calculator_history.csv"),
        )
        self.validate()

    def validate(self):
        """Validate configuration values."""
        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")
        if self.precision < 0:
            raise ConfigurationError("precision cannot be negative")
        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")