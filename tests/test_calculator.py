"""Tests for the Calculator facade and REPL."""

import builtins
import pytest
from app.calculator import Calculator, calculator_repl, build_help_menu
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


@pytest.fixture
def config(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    return CalculatorConfig()


@pytest.fixture
def repl_env(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))


def feed(monkeypatch, inputs):
    """Replace input() with a scripted sequence of answers."""
    it = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda *a, **k: next(it))


# ---------- Facade tests ----------

@pytest.mark.parametrize("op, a, b, expected", [
    ("add", "2", "3", 5),
    ("power", "2", "3", 8),
    ("int_divide", "7", "2", 3),
    ("percent", "50", "200", 25),
    ("abs_diff", "3", "8", 5),
])
def test_perform_operation(config, op, a, b, expected):
    assert Calculator(config).perform_operation(op, a, b) == expected


def test_invalid_input(config):
    with pytest.raises(ValidationError):
        Calculator(config).perform_operation("add", "abc", "3")


def test_undo_redo(config):
    calc = Calculator(config)
    calc.perform_operation("add", "1", "1")
    assert calc.undo() is True
    assert calc.history_manager.is_empty()
    assert calc.redo() is True
    assert not calc.history_manager.is_empty()


def test_undo_nothing(config):
    assert Calculator(config).undo() is False


def test_redo_nothing(config):
    assert Calculator(config).redo() is False


def test_clear(config):
    calc = Calculator(config)
    calc.perform_operation("add", "1", "1")
    calc.clear()
    assert calc.history_manager.is_empty()


def test_save_load(config):
    calc = Calculator(config)
    calc.perform_operation("add", "1", "1")
    calc.save()
    calc.clear()
    calc.load()
    assert len(calc.history_manager.get_history()) == 1


def test_no_autosave(config):
    config.auto_save = False
    calc = Calculator(config)
    assert len(calc.history_manager._observers) == 1


def test_help_menu_contains_everything():
    menu = build_help_menu()
    for word in ["power", "percent", "abs_diff", "undo", "history", "exit"]:
        assert word in menu


# ---------- REPL tests ----------

@pytest.mark.parametrize("inputs, expected", [
    (["exit"], "Goodbye"),
    (["help", "exit"], "Available commands"),
    (["add", "5", "3", "exit"], "Result: 8"),
    (["history", "exit"], "No calculations yet"),
    (["add", "2", "2", "history", "exit"], "add(2.0, 2.0)"),
    (["clear", "exit"], "History cleared"),
    (["add", "1", "1", "undo", "exit"], "Undo successful"),
    (["undo", "exit"], "Nothing to undo"),
    (["add", "1", "1", "undo", "redo", "exit"], "Redo successful"),
    (["redo", "exit"], "Nothing to redo"),
    (["add", "1", "1", "save", "exit"], "History saved"),
    (["add", "1", "1", "save", "load", "exit"], "History loaded"),
    (["load", "exit"], "Error"),
    (["banana", "exit"], "Invalid command"),
    (["divide", "5", "0", "exit"], "Cannot divide by zero"),
    (["add", "abc", "3", "exit"], "Invalid number"),
])
def test_repl_commands(monkeypatch, capsys, repl_env, inputs, expected):
    feed(monkeypatch, inputs)
    calculator_repl()
    assert expected in capsys.readouterr().out



# ---------- Precision, observers, and logging levels ----------

def read_log(config):
    with open(config.log_file, encoding="utf-8") as f:
        return f.read()


def test_precision_rounds_results(config):
    config.precision = 2
    assert Calculator(config).perform_operation("divide", "1", "3") == 0.33


def test_add_observer_registers_with_calculator(config):
    class Spy:
        def __init__(self):
            self.seen = []

        def update(self, calculation):
            self.seen.append(calculation)

    calc = Calculator(config)
    spy = Spy()
    calc.add_observer(spy)
    calc.perform_operation("add", "1", "2")
    assert len(spy.seen) == 1


def test_error_is_logged(config):
    calc = Calculator(config)
    with pytest.raises(Exception):
        calc.perform_operation("divide", "5", "0")
    assert "ERROR" in read_log(config)


def test_warning_is_logged(config):
    calc = Calculator(config)
    calc.undo()
    assert "WARNING" in read_log(config)


def test_load_failure_is_logged(config):
    calc = Calculator(config)
    with pytest.raises(Exception):
        calc.load()
    assert "Loading history failed" in read_log(config)


def test_invalid_command_logs_warning(monkeypatch, repl_env, tmp_path):
    feed(monkeypatch, ["banana", "exit"])
    calculator_repl()
    with open(tmp_path / "logs" / "calculator.log", encoding="utf-8") as f:
        assert "Invalid command entered: banana" in f.read()


def test_help_menu_order():
    menu = build_help_menu()
    assert menu.index("history") < menu.index("exit")