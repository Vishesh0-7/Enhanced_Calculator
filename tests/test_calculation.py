from app.calculation import Calculation


def test_create_and_to_dict():
    calc = Calculation.create("add", [1, 2], 3)
    d = calc.to_dict()
    assert d["operation"] == "add"
    assert d["operands"] == "1;2"
    assert "timestamp" in d
