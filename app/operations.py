"""Arithmetic operations implemented with the Factory design pattern."""

from abc import ABC, abstractmethod

from app.exceptions import OperationError


class Operation(ABC):
    """Abstract base class for all arithmetic operations."""

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Perform the operation on operands a and b."""

    def __str__(self) -> str:
        return self.__class__.__name__


class Addition(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b


class Subtraction(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b


class Multiplication(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b


class Division(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot divide by zero")
        return a / b


class Power(Operation):
    def execute(self, a: float, b: float) -> float:
        return a ** b


class Root(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot take the zeroth root")
        if a < 0:
            raise OperationError("Cannot take the root of a negative number")
        return a ** (1 / b)


class Modulus(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot take modulus with zero divisor")
        return a % b


class IntegerDivision(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot divide by zero")
        return a // b


class Percentage(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot compute percentage with zero divisor")
        return (a / b) * 100


class AbsoluteDifference(Operation):
    def execute(self, a: float, b: float) -> float:
        return abs(a - b)


class OperationFactory:
    """Factory that creates operation instances based on a name."""

    _operations = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "int_divide": IntegerDivision,
        "percent": Percentage,
        "abs_diff": AbsoluteDifference,
    }

    @classmethod
    def create(cls, operation_name: str) -> Operation:
        """Return an operation instance for the given name."""
        operation_class = cls._operations.get(operation_name)
        if operation_class is None:
            raise OperationError(f"Unknown operation: {operation_name}")
        return operation_class()

    @classmethod
    def available_operations(cls):
        """Return the list of supported operation names."""
        return list(cls._operations.keys())