import pytest
from app.operations import get_operation


@pytest.mark.parametrize(
    "name,a,b,expected",
    [
        ("add", 1, 2, 3),
        ("subtract", 5, 3, 2),
        ("multiply", 2, 3, 6),
        ("divide", 7, 2, 3.5),
        ("power", 2, 3, 8),
        ("root", 27, 3, 3),
        ("modulus", 10, 3, 1),
        ("int_divide", 7, 2, 3.0),
        ("percent", 20, 200, 10),
        ("abs_diff", 5, 9, 4),
    ],
)
def test_operations(name, a, b, expected):
    op = get_operation(name, precision=6)
    res = op.execute(a, b)
    assert pytest.approx(res, rel=1e-9) == expected


def test_divide_by_zero():
    op = get_operation("divide")
    with pytest.raises(ZeroDivisionError):
        op.execute(1, 0)
