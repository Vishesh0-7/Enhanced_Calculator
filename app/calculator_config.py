"""Configuration loader for the calculator using python-dotenv."""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    log_dir: str = os.getenv("CALCULATOR_LOG_DIR", "./logs")
    log_file: str = os.getenv("CALCULATOR_LOG_FILE", "calculator.log")
    history_dir: str = os.getenv("CALCULATOR_HISTORY_DIR", "./data")
    history_file: str = os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")
    max_history_size: int = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
    auto_save: bool = os.getenv("CALCULATOR_AUTO_SAVE", "True").lower() in ("1", "true", "yes")
    precision: int = int(os.getenv("CALCULATOR_PRECISION", "6"))
    max_input_value: float = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", str(1e12)))
    default_encoding: str = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")


__all__ = ["Config"]
