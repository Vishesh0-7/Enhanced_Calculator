"""History manager that stores calculations and notifies observers."""
from typing import List, Callable, Any
import os
import pandas as pd
from .calculation import Calculation
from .calculator_memento import Caretaker
from .exceptions import PersistenceError


class History:
    """Keeps an ordered list of Calculation objects, supports undo/redo and persistence."""

    def __init__(self, max_size: int = 100):
        self._items: List[Calculation] = []
        self.max_size = max_size
        self._observers: List[Callable[[str, Any], None]] = []
        self._caretaker = Caretaker()

    def attach(self, observer: Callable[[str, Any], None]):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Callable[[str, Any], None]):
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify(self, event_type: str, data: Any):
        for obs in list(self._observers):
            try:
                obs(event_type, data)
            except Exception:
                # observers must not break history
                pass

    def add(self, calculation: Calculation):
        # Save snapshot before change
        self._caretaker.save(self._items)
        self._items.append(calculation)
        if len(self._items) > self.max_size:
            self._items = self._items[-self.max_size :]
        self._notify("calculation_added", calculation)

    def list(self) -> List[Calculation]:
        return list(self._items)

    def clear(self):
        self._caretaker.save(self._items)
        self._items.clear()
        self._notify("cleared", None)

    def undo(self):
        new_state = self._caretaker.undo(self._items)
        self._items = new_state
        self._notify("undo", None)

    def redo(self):
        new_state = self._caretaker.redo(self._items)
        self._items = new_state
        self._notify("redo", None)

    def save_csv(self, path: str, encoding: str = "utf-8"):
        try:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            df = pd.DataFrame([c.to_dict() for c in self._items])
            df.to_csv(path, index=False, encoding=encoding)
            self._notify("saved", path)
        except Exception as e:
            raise PersistenceError(str(e))

    def load_csv(self, path: str, encoding: str = "utf-8"):
        try:
            df = pd.read_csv(path, encoding=encoding)
            items: List[Calculation] = []
            for _, row in df.iterrows():
                ops = [float(x) for x in str(row["operands"]).split(";") if x != ""]
                calc = Calculation(operation=str(row["operation"]), operands=ops, result=float(row["result"]), timestamp=str(row.get("timestamp", "")))
                items.append(calc)
            self._caretaker.save(self._items)
            self._items = items
            self._notify("loaded", path)
        except FileNotFoundError:
            raise PersistenceError(f"File not found: {path}")
        except Exception as e:
            raise PersistenceError(str(e))
