import os
from app.calculator_config import Config


def test_config_defaults(monkeypatch):
    # Ensure defaults are read when env not set
    monkeypatch.delenv("CALCULATOR_LOG_DIR", raising=False)
    monkeypatch.delenv("CALCULATOR_HISTORY_DIR", raising=False)
    cfg = Config()
    assert isinstance(cfg.log_dir, str)
    assert isinstance(cfg.history_dir, str)
    assert cfg.max_history_size >= 1
