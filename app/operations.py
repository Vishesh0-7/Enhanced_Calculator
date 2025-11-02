"""Operation implementations using a factory/registry (Factory Pattern).

Each operation registers itself in OP_REGISTRY via the @operation decorator.
"""
from __future__ import annotations
from typing import Callable, Dict, Tuple, Any
import math

OP_REGISTRY: Dict[str, Callable[..., "Operation"]] = {}


def operation(name: str, help_text: str = ""):
    """Decorator to register an operation class under a name.

    The decorated class must implement execute(a, b).
    """

    def _decorator(cls):
        cls.name = name
        cls.help_text = help_text
        OP_REGISTRY[name] = cls
        return cls

    return _decorator


class Operation:
    """Base class for operations."""

    name: str = "op"
    help_text: str = ""

    def __init__(self, precision: int = 6):
        self.precision = precision

    def execute(self, a: float, b: float) -> float:  # pragma: no cover - overridden
        raise NotImplementedError()

    def fmt(self, v: float) -> float:
        return round(v, self.precision)


@operation("add", "Add two numbers")
class Add(Operation):
    def execute(self, a, b):
        return self.fmt(a + b)


@operation("subtract", "Subtract b from a")
class Subtract(Operation):
    def execute(self, a, b):
        return self.fmt(a - b)


@operation("multiply", "Multiply two numbers")
class Multiply(Operation):
    def execute(self, a, b):
        return self.fmt(a * b)


@operation("divide", "Divide a by b")
class Divide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return self.fmt(a / b)


@operation("power", "Power a^b")
class Power(Operation):
    def execute(self, a, b):
        return self.fmt(math.pow(a, b))


@operation("root", "b-th root of a")
class Root(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Zero-degree root")
        if a < 0 and int(b) % 2 == 0:
            raise ValueError("Even root of negative number")
        return self.fmt(math.copysign(abs(a) ** (1.0 / b), a))


@operation("modulus", "a mod b")
class Modulus(Operation):
    def execute(self, a, b):
        return self.fmt(a % b)


@operation("int_divide", "Integer division a // b")
class IntDivide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Integer division by zero")
        return self.fmt(a // b)


@operation("percent", "Percent of a with respect to b ((a/b)*100)")
class Percent(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Percentage with respect to zero")
        return self.fmt((a / b) * 100.0)


@operation("abs_diff", "Absolute difference between a and b")
class AbsDiff(Operation):
    def execute(self, a, b):
        return self.fmt(abs(a - b))


def get_operation(name: str, precision: int = 6) -> Operation:
    cls = OP_REGISTRY.get(name)
    if not cls:
        raise KeyError(f"Unknown operation '{name}'")
    return cls(precision=precision)


__all__ = ["get_operation", "OP_REGISTRY", "Operation"]
