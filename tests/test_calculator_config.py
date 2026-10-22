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