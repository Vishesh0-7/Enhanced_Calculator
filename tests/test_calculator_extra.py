import os
import tempfile
from app.calculator import Calculator
from app.calculator_config import Config
from app.exceptions import OperationError


def test_constructor_no_autosave(tmp_path):
    cfg = Config()
    cfg.auto_save = False
    calc = Calculator(cfg)
    # autosave observer should not be attached; still works
    assert hasattr(calc, "history")


def test_apply_operation_wraps_exceptions():
    calc = Calculator()
    try:
        calc.apply_operation("divide", 1, 0)
    except OperationError:
        assert True
    else:
        assert False, "Expected OperationError for divide by zero"


def test_history_clear_and_undo_noop():
    calc = Calculator()
    calc.history.clear()
    # undo when no undo available should not raise
    calc.history.undo()
    calc.history.redo()
