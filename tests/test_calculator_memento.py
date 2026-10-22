"""Tests for the Memento pattern (undo/redo)."""

from app.calculator_memento import Caretaker, Memento


def test_memento_copy():
    state = [1, 2, 3]
    m = Memento(state)
    state.append(4)
    assert m.get_state() == [1, 2, 3]


def test_undo_redo():
    c = Caretaker()
    c.save_state(["a"])
    assert c.undo(["b"]) == ["a"]
    assert c.redo(["a"]) == ["b"]


def test_undo_empty():
    assert Caretaker().undo(["x"]) is None


def test_redo_empty():
    assert Caretaker().redo(["x"]) is None


def test_save_clears_redo():
    c = Caretaker()
    c.save_state(["a"])
    c.undo(["b"])
    c.save_state(["c"])
    assert c.redo(["d"]) is None