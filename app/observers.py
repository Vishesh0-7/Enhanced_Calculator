"""Observers for logging and autosave (Observer Pattern)."""
from typing import Any
import os
import logging
import pandas as pd
from .calculation import Calculation
from .exceptions import PersistenceError


class LoggingObserver:
    """Observer that logs calculation events to a file using logging module."""

    def __init__(self, log_path: str):
        os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
        self.logger = logging.getLogger(f"calculator_logger_{log_path}")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            fh = logging.FileHandler(log_path)
            fmt = logging.Formatter("%(asctime)s - %(message)s")
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)

    def __call__(self, event_type: str, data: Any):
        if event_type == "calculation_added" and isinstance(data, Calculation):
            self.logger.info(f"{data.timestamp} | {data.operation} | {data.operands} => {data.result}")
        else:
            self.logger.info(f"event={event_type} data={data}")


class AutoSaveObserver:
    """Observer that automatically saves history to CSV whenever a calculation is added.

    Expects to be provided with a function history.save_csv path or similar; but for simplicity,
    it accepts a history instance and a path to write to.
    """

    def __init__(self, history, save_path: str, encoding: str = "utf-8"):
        self.history = history
        self.path = save_path
        self.encoding = encoding

    def __call__(self, event_type: str, data: Any):
        if event_type == "calculation_added":
            try:
                self.history.save_csv(self.path, encoding=self.encoding)
            except Exception as e:
                # Do not raise to the subject
                raise PersistenceError(str(e))
