Advanced Calculator CLI
=======================

A modular, test-driven advanced calculator CLI showcasing several classic design patterns with robust configuration, history, logging, autosave, and a friendly REPL.

This project is intended as both a practical tool and a teaching reference for:
- Factory Pattern for arithmetic operations
- Memento Pattern for undo/redo history
- Observer Pattern for logging and autosave
- Decorator/registration for dynamic help and easy extensibility


## Project overview

The calculator provides advanced arithmetic operations and a full command-line REPL interface. Every calculation is recorded in a history that supports undo and redo. Observers can be attached dynamically to log calculations to a file and to autosave the history as a CSV file.

Highlights:
- Operations implemented as individual classes and registered via a factory/registry
- Persistence to CSV with pandas
- Logging via Python's logging module to a configurable directory
- Configurable precision, limits, and behavior from a `.env` file
- Colorized output for readability

Core commands available in REPL:
- Operations: `add`, `subtract`, `multiply`, `divide`, `power`, `root`, `modulus`, `int_divide`, `percent`, `abs_diff`
- Utilities: `history`, `clear`, `undo`, `redo`, `save [path]`, `load [path]`, `help`, `exit`

Key modules (in `app/`):
- `operations.py`: operation classes and factory registry
- `calculator.py`: main calculator and REPL
- `history.py`: history list, observers, persistence, undo/redo
- `calculator_memento.py`: Caretaker for memento stacks
- `observers.py`: `LoggingObserver`, `AutoSaveObserver`
- `calculator_config.py`: `.env` loading and defaults
- `logger.py`: logger setup helper
- `input_validators.py`: input checks with typed exceptions
- `calculation.py`: calculation record (dataclass)
- `exceptions.py`: `OperationError`, `ValidationError`, `PersistenceError`


## Setup + Installation

Requirements: Python 3.9+ (tested on Python 3.12)

1) Create and activate a virtual environment

```bash
cd /home/vishesh/is601/mid_proj
python3 -m venv .venv
. .venv/bin/activate
```

2) Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3) Run the calculator REPL

```bash
python main.py
```

Tip: If you want to exit the REPL, type `exit` or press Ctrl+C.


## Configuration (.env) example

Configuration is loaded from environment variables using `python-dotenv`. Defaults are provided if variables are missing. You can edit the provided `.env` at the project root.

Example `.env`:

```ini
# Where to write log files
CALCULATOR_LOG_DIR=./logs
CALCULATOR_LOG_FILE=calculator.log

# Where to write history CSV files
CALCULATOR_HISTORY_DIR=./data
CALCULATOR_HISTORY_FILE=history.csv

# Max in-memory history entries retained
CALCULATOR_MAX_HISTORY_SIZE=100

# Automatically save history to CSV on each new calculation
CALCULATOR_AUTO_SAVE=True

# Decimal places to round results to
CALCULATOR_PRECISION=6

# Maximum absolute allowed value for inputs
CALCULATOR_MAX_INPUT_VALUE=1e12

# Encoding used for CSV persistence
CALCULATOR_DEFAULT_ENCODING=utf-8
```


## CLI usage and commands

Start the REPL with `python main.py`. Then use commands in the form:

```text
<operation> <a> <b>
```

Examples:
- `add 1 2` → 3
- `divide 7 2` → 3.5
- `power 2 3` → 8
- `root 27 3` → 3
- `percent 200 10` → 20
- `abs_diff 5 9` → 4

Utility commands:
- `history` — list past calculations with timestamps
- `clear` — clear history (undo-able)
- `undo` — revert to previous history state
- `redo` — re-apply an undone state
- `save [path]` — persist current history as CSV (default path from config)
- `load [path]` — load history from CSV (replacing in-memory history)
- `help` — show dynamic help derived from registered operations
- `exit` — quit the REPL

Output is colorized via `colorama`:
- Success: green
- Warnings/info: yellow/cyan
- Errors: red

Error handling:
- Division by zero, invalid roots, non-numeric input, and values exceeding limits are reported clearly.
- Persistence issues raise a `PersistenceError` and are surfaced cleanly.


## Testing instructions

This project uses `pytest` and `pytest-cov` with an enforced minimum coverage of 90%.

Run the test suite:

```bash
. .venv/bin/activate
pytest --cov=app --cov-fail-under=90
```

What’s covered:
- Parameterized arithmetic operation tests
- Memento undo/redo behavior
- Observer side-effects (logging, autosave)
- Config loading and defaults
- Validation and error handling

Note: The interactive `repl()` is excluded from coverage by design since it requires user input.


## CI/CD workflow explanation

GitHub Actions workflow at `.github/workflows/python-app.yml` runs on pushes and PRs to `main`:
- Checks out the code
- Sets up Python 3.x
- Installs dependencies (from `requirements.txt`) and testing tools
- Runs `pytest` with coverage, enforcing `--cov-fail-under=90`

A failure occurs if tests fail or if total coverage is below 90%.


## Attribution for design patterns

- Factory Pattern: Each operation is its own class registered in a central registry (`OP_REGISTRY`) via a decorator. This makes adding new operations trivial—define a class, decorate it, and it appears in help and is available in the REPL.

- Memento Pattern: `CalculatorMemento` and `Caretaker` (`app/calculator_memento.py`) capture and restore `History` state for `undo`/`redo` without exposing internals.

- Observer Pattern: `History` acts as the subject; observers like `LoggingObserver` and `AutoSaveObserver` (`app/observers.py`) subscribe to events and react to changes (e.g., log entries, autosave CSV).

- Decorator/Registration: Operation classes are registered using a decorator in `operations.py`, enabling dynamic help generation in `Calculator.help_text()` and loose coupling between the REPL and concrete operations.


## Extending the calculator

To add a new operation:
1. Create a new class in `app/operations.py` implementing `execute(a, b)` and decorate it with `@operation("name", "Help text")`.
2. That’s it—`help` output updates automatically, and the REPL recognizes the new command.


## License

This project is provided for educational purposes. Adapt and extend as needed.

How to run
----------

1. Create and activate a virtual environment (recommended):

```bash
cd /home/vishesh/is601/mid_proj
python3 -m venv .venv
. .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov
```

3. Launch the calculator REPL:

```bash
python main.py
```

The REPL supports commands: `add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff`, and utility commands: `history, clear, undo, redo, save [path], load [path], help, exit`.

Notes
-----
- Configuration values come from `.env` (see file in repo) and have sensible defaults.
- The REPL is interactive; automated tests exercise the logic and persistency separately.

