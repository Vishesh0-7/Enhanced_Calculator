"""Custom exceptions for the calculator application."""
from typing import Optional


class CalculatorError(Exception):
    """Base class for calculator errors."""


class OperationError(CalculatorError):
    """Raised when an operation cannot be performed."""


class ValidationError(CalculatorError):
    """Raised when user input fails validation."""


class PersistenceError(CalculatorError):
    """Raised when save/load operations fail."""
