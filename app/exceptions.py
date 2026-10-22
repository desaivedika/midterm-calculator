"""Custom exceptions for the calculator application."""


class CalculatorError(Exception):
    """Base exception for all calculator errors."""


class OperationError(CalculatorError):
    """Raised when an arithmetic operation fails."""


class ValidationError(CalculatorError):
    """Raised when user input fails validation."""


class ConfigurationError(CalculatorError):
    """Raised when configuration is invalid."""