"""Calculation model representing a single computation."""

from datetime import datetime

from app.operations import OperationFactory


class Calculation:
    """Represents one calculation: operation, operands, result, timestamp."""

    def __init__(self, operation_name: str, a: float, b: float):
        self.operation_name = operation_name
        self.a = a
        self.b = b
        self.operation = OperationFactory.create(operation_name)
        self.result = self.operation.execute(a, b)
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        """Convert the calculation to a dictionary (for pandas/CSV)."""
        return {
            "operation": self.operation_name,
            "operand1": self.a,
            "operand2": self.b,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict) -> "Calculation":
        """Recreate a Calculation from a stored dictionary/row."""
        return Calculation(data["operation"], float(data["operand1"]), float(data["operand2"]))

    def __str__(self) -> str:
        return f"{self.operation_name}({self.a}, {self.b}) = {self.result}"