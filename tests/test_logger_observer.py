import os
from app.observers import LoggingObserver, AutoSaveObserver
from app.history import History
from app.calculation import Calculation


def test_logging_observer(tmp_path):
    path = tmp_path / "calc.log"
    obs = LoggingObserver(str(path))
    h = History()
    h.attach(obs)
    c = Calculation.create("add", [1, 2], 3)
    h.add(c)
    assert os.path.exists(str(path))


def test_autosave_observer(tmp_path):
    path = tmp_path / "history.csv"
    h = History()
    obs = AutoSaveObserver(h, str(path))
    h.attach(obs)
    c = Calculation.create("add", [1, 2], 3)
    h.add(c)
    assert os.path.exists(str(path))
