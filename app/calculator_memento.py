"""Memento implementation for history snapshots."""
from typing import List
from .calculation import Calculation


class CalculatorMemento:
    """A simple memento storing a copy of the history list."""

    def __init__(self, state: List[Calculation]):
        # shallow copy of the list (Calculation is immutable-ish)
        self._state = list(state)

    def get_state(self) -> List[Calculation]:
        return list(self._state)


class Caretaker:
    """Stores mementos for undo/redo.

    This caretaker keeps two stacks: undo and redo.
    """

    def __init__(self):
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

    def save(self, state: List[Calculation]):
        self.undo_stack.append(CalculatorMemento(state))
        self.redo_stack.clear()

    def can_undo(self) -> bool:
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0

    def undo(self, current_state: List[Calculation]):
        if not self.can_undo():
            return current_state
        m = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(current_state))
        return m.get_state()

    def redo(self, current_state: List[Calculation]):
        if not self.can_redo():
            return current_state
        m = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(current_state))
        return m.get_state()
