"""High-level logging helper to configure the application logger."""
from .calculator_config import Config
import logging
import os


def setup_app_logger(cfg: Config, filename: str | None = None) -> str:
    os.makedirs(cfg.log_dir, exist_ok=True)
    log_name = filename or cfg.log_file
    path = os.path.join(cfg.log_dir, log_name)
    logger = logging.getLogger("advanced_calculator")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(path)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(fh)
    return path
