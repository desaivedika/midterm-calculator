"""Tests for history management (Observer pattern + pandas)."""

import os
import pytest
from app.history import HistoryManager, LoggingObserver, AutoSaveObserver
from app.calculation import Calculation
from app.logger import Logger
from app.exceptions import OperationError


def make_manager(tmp_path):
    return HistoryManager(str(tmp_path / "hist.csv"), max_size=100)


def test_add_and_get(tmp_path):
    m = make_manager(tmp_path)
    assert m.is_empty()
    m.add_calculation(Calculation("add", 1, 2))
    assert not m.is_empty()
    assert len(m.get_history()) == 1


def test_clear(tmp_path):
    m = make_manager(tmp_path)
    m.add_calculation(Calculation("add", 1, 2))
    m.clear()
    assert m.is_empty()


def test_max_size(tmp_path):
    m = HistoryManager(str(tmp_path / "hist.csv"), max_size=2)
    for i in range(5):
        m.add_calculation(Calculation("add", i, 1))
    assert len(m.get_history()) == 2


def test_logging_observer(tmp_path):
    m = make_manager(tmp_path)
    log_file = str(tmp_path / "log.log")
    m.add_observer(LoggingObserver(Logger(log_file)))
    m.add_calculation(Calculation("add", 1, 2))
    with open(log_file, encoding="utf-8") as f:
        assert "add(1, 2) = 3" in f.read()


def test_autosave_observer(tmp_path):
    m = make_manager(tmp_path)
    m.add_observer(AutoSaveObserver(m))
    m.add_calculation(Calculation("add", 1, 2))
    assert os.path.exists(m.history_file)


def test_save_and_load(tmp_path):
    m = make_manager(tmp_path)
    m.add_calculation(Calculation("add", 1, 2))
    m.save()
    m2 = make_manager(tmp_path)
    m2.load()
    assert len(m2.get_history()) == 1


def test_load_missing(tmp_path):
    m = HistoryManager(str(tmp_path / "nope.csv"))
    with pytest.raises(OperationError):
        m.load()


def test_load_malformed(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("", encoding="utf-8")
    m = HistoryManager(str(bad))
    with pytest.raises(OperationError):
        m.load()


def test_to_dataframe(tmp_path):
    m = make_manager(tmp_path)
    m.add_calculation(Calculation("add", 1, 2))
    df = m.to_dataframe()
    assert list(df.columns) == HistoryManager.COLUMNS
    assert len(df) == 1