"""Tests for custom exceptions."""

import pytest
from app.exceptions import (
    CalculatorError, OperationError, ValidationError, ConfigurationError,
)


@pytest.mark.parametrize("exc", [OperationError, ValidationError, ConfigurationError])
def test_subclass(exc):
    assert issubclass(exc, CalculatorError)


def test_raise():
    with pytest.raises(OperationError, match="boom"):
        raise OperationError("boom")