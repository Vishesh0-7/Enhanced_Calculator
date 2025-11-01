from app.calculator import Calculator
from app.calculator_config import Config
from app.exceptions import OperationError


def test_apply_operation():
    cfg = Config()
    calc = Calculator(cfg)
    res = calc.apply_operation("add", 1, 2)
    assert res == 3


def test_unknown_operation():
    calc = Calculator()
    try:
        calc.apply_operation("unknown_op", 1, 2)
    except OperationError:
        assert True
    else:
        assert False, "Expected OperationError"


def test_list_and_help():
    calc = Calculator()
    ops = calc.list_operations()
    assert "add" in ops
    help_text = calc.help_text()
    assert "add:" in help_text
