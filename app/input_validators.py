"""Input validation helpers."""
from .exceptions import ValidationError


def to_number(value):
    try:
        return float(value)
    except Exception:
        raise ValidationError(f"Not a number: {value}")


def check_limits(value: float, max_value: float):
    if abs(value) > max_value:
        raise ValidationError(f"Value {value} exceeds allowed maximum of {max_value}")
