"""Tests for configuration management."""

import pytest
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_defaults(monkeypatch):
    for var in ["CALCULATOR_MAX_HISTORY_SIZE", "CALCULATOR_PRECISION",
                "CALCULATOR_MAX_INPUT_VALUE"]:
        monkeypatch.delenv(var, raising=False)
    config = CalculatorConfig()
    assert config.max_history_size == 100
    assert config.precision == 10


def test_auto_save_flag(monkeypatch):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    assert CalculatorConfig().auto_save is False


def test_invalid_history_size(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "0")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_invalid_precision(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "100")
    monkeypatch.setenv("CALCULATOR_PRECISION", "-1")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_invalid_max_input(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "100")
    monkeypatch.setenv("CALCULATOR_PRECISION", "10")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "0")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()



def test_file_paths_from_env(monkeypatch, tmp_path):
    log_file = str(tmp_path / "custom.log")
    history_file = str(tmp_path / "custom.csv")
    monkeypatch.setenv("CALCULATOR_LOG_FILE", log_file)
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", history_file)
    config = CalculatorConfig()
    assert config.log_file == log_file
    assert config.history_file == history_file


def test_file_paths_default_to_dirs(monkeypatch):
    monkeypatch.delenv("CALCULATOR_LOG_FILE", raising=False)
    monkeypatch.delenv("CALCULATOR_HISTORY_FILE", raising=False)
    monkeypatch.setenv("CALCULATOR_LOG_DIR", "mylogs")
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", "myhistory")
    config = CalculatorConfig()
    assert config.log_file.startswith("mylogs")
    assert config.history_file.startswith("myhistory")