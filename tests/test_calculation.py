"""Tests for the Calculation model."""

import pytest
from app.calculation import Calculation


@pytest.mark.parametrize("op, a, b, expected", [
    ("add", 2, 3, 5),
    ("power", 2, 4, 16),
    ("modulus", 10, 3, 1),
])
def test_calculation_result(op, a, b, expected):
    assert Calculation(op, a, b).result == expected


def test_to_dict():
    calc = Calculation("add", 1, 2)
    d = calc.to_dict()
    assert d["operation"] == "add"
    assert d["operand1"] == 1
    assert d["operand2"] == 2
    assert d["result"] == 3
    assert "timestamp" in d


def test_from_dict():
    data = {"operation": "multiply", "operand1": "3", "operand2": "4",
            "result": 12, "timestamp": "2024-01-01T00:00:00"}
    assert Calculation.from_dict(data).result == 12


def test_str():
    assert str(Calculation("add", 1, 2)) == "add(1, 2) = 3"



def test_from_dict_keeps_timestamp():
    data = {"operation": "add", "operand1": "1", "operand2": "2",
            "result": 3, "timestamp": "2024-05-01T10:30:00"}
    assert Calculation.from_dict(data).timestamp.isoformat() == "2024-05-01T10:30:00"