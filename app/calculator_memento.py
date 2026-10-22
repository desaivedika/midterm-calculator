"""Memento design pattern for undo/redo of calculation history."""

import copy


class Memento:
    """Stores a snapshot of the history list."""

    def __init__(self, state: list):
        self._state = copy.deepcopy(state)

    def get_state(self) -> list:
        return copy.deepcopy(self._state)


class Caretaker:
    """Manages undo and redo stacks of mementos."""

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def save_state(self, state: list) -> None:
        self._undo_stack.append(Memento(state))
        self._redo_stack.clear()

    def undo(self, current_state: list):
        if not self._undo_stack:
            return None
        self._redo_stack.append(Memento(current_state))
        return self._undo_stack.pop().get_state()

    def redo(self, current_state: list):
        if not self._redo_stack:
            return None
        self._undo_stack.append(Memento(current_state))
        return self._redo_stack.pop().get_state()