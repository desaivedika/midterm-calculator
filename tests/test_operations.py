"""Tests for arithmetic operations and the Factory."""

import pytest
from app.operations import (
    OperationFactory, Addition, Subtraction, Multiplication, Division,
    Power, Root, Modulus, IntegerDivision, Percentage, AbsoluteDifference,
)
from app.exceptions import OperationError


@pytest.mark.parametrize("op_class, a, b, expected", [
    (Addition, 2, 3, 5),
    (Subtraction, 5, 3, 2),
    (Multiplication, 3, 4, 12),
    (Division, 10, 2, 5),
    (Power, 2, 3, 8),
    (Power, 2, -1, 0.5),
    (Root, 9, 2, 3),
    (Modulus, 10, 3, 1),
    (IntegerDivision, 7, 2, 3),
    (Percentage, 50, 200, 25),
    (AbsoluteDifference, 3, 8, 5),
])
def test_operations(op_class, a, b, expected):
    assert op_class().execute(a, b) == expected


@pytest.mark.parametrize("op_class, a, b", [
    (Division, 5, 0),
    (Modulus, 5, 0),
    (IntegerDivision, 5, 0),
    (Percentage, 5, 0),
    (Root, 5, 0),
])
def test_zero_errors(op_class, a, b):
    with pytest.raises(OperationError):
        op_class().execute(a, b)


def test_root_negative():
    with pytest.raises(OperationError):
        Root().execute(-4, 2)


def test_factory_creates():
    assert isinstance(OperationFactory.create("add"), Addition)
    assert isinstance(OperationFactory.create("abs_diff"), AbsoluteDifference)


def test_factory_unknown():
    with pytest.raises(OperationError):
        OperationFactory.create("unknown")


def test_available_operations():
    ops = OperationFactory.available_operations()
    assert "power" in ops and "percent" in ops and len(ops) == 10


def test_operation_str():
    assert str(Addition()) == "Addition"