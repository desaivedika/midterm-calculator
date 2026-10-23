"""Command design pattern: each user request is wrapped in a command object.

Commands can be executed immediately through the CommandInvoker, or queued
and run later as a batch, which allows parameterization and queuing of
operations.
"""

from abc import ABC, abstractmethod


class Command(ABC):
    """Abstract base class for all commands."""

    @abstractmethod
    def execute(self):
        """Carry out the request and return its result."""


class CalculateCommand(Command):
    """Runs one arithmetic operation with two operands."""

    def __init__(self, calculator, operation_name: str, a, b):
        self.calculator = calculator
        self.operation_name = operation_name
        self.a = a
        self.b = b

    def execute(self):
        return self.calculator.perform_operation(self.operation_name, self.a, self.b)

    def __str__(self) -> str:
        return f"CalculateCommand({self.operation_name}, {self.a}, {self.b})"


class UndoCommand(Command):
    """Undoes the last change to the history."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        return self.calculator.undo()


class RedoCommand(Command):
    """Redoes the last undone change."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        return self.calculator.redo()


class ClearCommand(Command):
    """Clears the calculation history."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        return self.calculator.clear()


class SaveCommand(Command):
    """Saves the history to CSV."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        return self.calculator.save()


class LoadCommand(Command):
    """Loads the history from CSV."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        return self.calculator.load()


class CommandInvoker:
    """Executes commands, keeps a log of executed commands, and supports a queue."""

    def __init__(self):
        self.executed = []
        self._queue = []

    def execute(self, command: Command):
        """Execute a command immediately and record it."""
        result = command.execute()
        self.executed.append(command)
        return result

    def add_to_queue(self, command: Command) -> None:
        """Queue a command to be run later."""
        self._queue.append(command)

    def queue_size(self) -> int:
        return len(self._queue)

    def run_queue(self) -> list:
        """Execute all queued commands in order and return their results."""
        results = [self.execute(command) for command in self._queue]
        self._queue.clear()
        return results