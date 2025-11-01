import os
import pandas as pd
from app.history import History
from app.calculation import Calculation


def test_add_and_list(tmp_path):
    h = History(max_size=10)
    c1 = Calculation.create("add", [1, 2], 3)
    h.add(c1)
    assert len(h.list()) == 1


def test_undo_redo():
    h = History(max_size=10)
    c1 = Calculation.create("add", [1, 2], 3)
    c2 = Calculation.create("multiply", [2, 3], 6)
    h.add(c1)
    h.add(c2)
    assert len(h.list()) == 2
    h.undo()
    assert len(h.list()) == 1
    h.redo()
    assert len(h.list()) == 2


def test_save_load_csv(tmp_path):
    h = History(max_size=10)
    c1 = Calculation.create("add", [1, 2], 3)
    h.add(c1)
    path = tmp_path / "out.csv"
    h.save_csv(str(path))
    assert os.path.exists(str(path))
    h2 = History(max_size=10)
    h2.load_csv(str(path))
    assert len(h2.list()) == 1


def test_attach_detach_and_observer_exceptions(tmp_path):
    h = History(max_size=10)

    called = {"ok": False}

    def good_observer(event, data):
        called["ok"] = True

    def bad_observer(event, data):
        raise RuntimeError("observer failure")

    h.attach(good_observer)
    h.attach(bad_observer)
    c = Calculation.create("add", [1, 2], 3)
    # bad_observer raising should not stop history.add
    h.add(c)
    assert called["ok"] is True
    # detach and ensure not called again
    h.detach(good_observer)
    called["ok"] = False
    h.add(Calculation.create("add", [2, 3], 5))
    assert called["ok"] is False


def test_load_missing_file_raises(tmp_path):
    h = History()
    missing = tmp_path / "nope.csv"
    try:
        h.load_csv(str(missing))
    except Exception as e:
        from app.exceptions import PersistenceError

        assert isinstance(e, PersistenceError)
    else:
        assert False, "Expected PersistenceError"
