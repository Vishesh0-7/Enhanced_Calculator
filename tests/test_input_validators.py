import pytest
from app.input_validators import to_number, check_limits
from app.exceptions import ValidationError


def test_to_number_success():
    assert to_number("3.14") == 3.14


def test_to_number_failure():
    with pytest.raises(ValidationError):
        to_number("not_a_number")


def test_check_limits_ok():
    check_limits(10, 100)


def test_check_limits_exceed():
    with pytest.raises(ValidationError):
        check_limits(1e9, 1e3)
