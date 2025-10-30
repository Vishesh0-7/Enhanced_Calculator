"""Launcher for the Advanced Calculator CLI.

Run this file after creating and activating a virtual environment.
"""
from app.calculator import Calculator
from app.calculator_config import Config


def main():
    cfg = Config()
    calc = Calculator(cfg)
    try:
        calc.repl()
    except KeyboardInterrupt:
        print('\nExiting calculator.')


if __name__ == "__main__":
    main()
