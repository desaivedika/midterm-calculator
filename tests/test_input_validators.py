"""Tests for input validation."""

import pytest
from app.input_validators import InputValidator
from app.exceptions import ValidationError


@pytest.mark.parametrize("value, expected", [("5", 5.0), ("3.14", 3.14), ("-2", -2.0)])
def test_valid(value, expected):
    assert InputValidator.validate_number(value) == expected


@pytest.mark.parametrize("value", ["abc", "", None])
def test_invalid(value):
    with pytest.raises(ValidationError):
        InputValidator.validate_number(value)


def test_exceeds_max():
    with pytest.raises(ValidationError):
        InputValidator.validate_number("1000", max_input_value=100)