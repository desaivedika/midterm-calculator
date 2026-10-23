"""Tests for the Command pattern."""

import pytest
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.commands import (
    CommandInvoker, CalculateCommand, UndoCommand, RedoCommand,
    ClearCommand, SaveCommand, LoadCommand,
)
from app.exceptions import OperationError


@pytest.fixture
def calc(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    return Calculator(CalculatorConfig())


@pytest.mark.parametrize("op, a, b, expected", [
    ("add", "2", "3", 5),
    ("modulus", "10", "3", 1),
    ("root", "27", "3", 3),
])
def test_calculate_command(calc, op, a, b, expected):
    assert CommandInvoker().execute(CalculateCommand(calc, op, a, b)) == pytest.approx(expected)


def test_calculate_command_error(calc):
    with pytest.raises(OperationError):
        CommandInvoker().execute(CalculateCommand(calc, "divide", "5", "0"))


def test_calculate_command_str(calc):
    assert str(CalculateCommand(calc, "add", 1, 2)) == "CalculateCommand(add, 1, 2)"


def test_undo_redo_commands(calc):
    invoker = CommandInvoker()
    invoker.execute(CalculateCommand(calc, "add", "1", "1"))
    assert invoker.execute(UndoCommand(calc)) is True
    assert calc.history_manager.is_empty()
    assert invoker.execute(RedoCommand(calc)) is True
    assert not calc.history_manager.is_empty()


def test_clear_save_load_commands(calc):
    invoker = CommandInvoker()
    invoker.execute(CalculateCommand(calc, "add", "1", "1"))
    invoker.execute(SaveCommand(calc))
    invoker.execute(ClearCommand(calc))
    assert calc.history_manager.is_empty()
    invoker.execute(LoadCommand(calc))
    assert len(calc.history_manager.get_history()) == 1


def test_invoker_records_executed_commands(calc):
    invoker = CommandInvoker()
    invoker.execute(CalculateCommand(calc, "add", "1", "1"))
    invoker.execute(UndoCommand(calc))
    assert len(invoker.executed) == 2


def test_command_queue(calc):
    invoker = CommandInvoker()
    invoker.add_to_queue(CalculateCommand(calc, "add", "1", "2"))
    invoker.add_to_queue(CalculateCommand(calc, "power", "2", "5"))
    invoker.add_to_queue(CalculateCommand(calc, "abs_diff", "3", "10"))
    assert invoker.queue_size() == 3
    assert calc.history_manager.is_empty()  # nothing runs until the queue is executed

    results = invoker.run_queue()

    assert results == [3, 32, 7]
    assert invoker.queue_size() == 0
    assert len(calc.history_manager.get_history()) == 3