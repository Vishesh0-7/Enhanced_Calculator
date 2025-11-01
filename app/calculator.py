"""Main Calculator CLI with REPL, integrates operations, history, observers, and config."""
from typing import List
import os
import shlex
from colorama import Fore, Style, init as colorama_init
from .calculator_config import Config
from .operations import get_operation, OP_REGISTRY
from .calculation import Calculation
from .history import History
from .observers import LoggingObserver, AutoSaveObserver
from .logger import setup_app_logger
from .input_validators import to_number, check_limits
from .exceptions import OperationError, ValidationError

colorama_init(autoreset=True)


class Calculator:
    """Calculator ties together operations, history, observers, and provides a REPL."""

    def __init__(self, cfg: Config = None):
        self.cfg = cfg or Config()
        self.history = History(max_size=self.cfg.max_history_size)
        log_path = setup_app_logger(self.cfg)
        self.log_observer = LoggingObserver(log_path)
        self.history.attach(self.log_observer)
        if self.cfg.auto_save:
            autosave_path = os.path.join(self.cfg.history_dir, self.cfg.history_file)
            self.autosave_observer = AutoSaveObserver(self.history, autosave_path, encoding=self.cfg.default_encoding)
            self.history.attach(self.autosave_observer)

    def apply_operation(self, name: str, a: float, b: float):
        check_limits(a, self.cfg.max_input_value)
        check_limits(b, self.cfg.max_input_value)
        try:
            op = get_operation(name, precision=self.cfg.precision)
            result = op.execute(a, b)
            calc = Calculation.create(name, [a, b], result)
            self.history.add(calc)
            return result
        except KeyError:
            raise OperationError(f"Unknown operation: {name}")
        except Exception as e:
            raise OperationError(str(e))

    def list_operations(self) -> List[str]:
        return sorted(OP_REGISTRY.keys())

    def help_text(self) -> str:
        lines = []
        for name, cls in sorted(OP_REGISTRY.items()):
            lines.append(f"{name}: {getattr(cls, 'help_text', '')}")
        return "\n".join(lines)

    def repl(self):  # pragma: no cover
        # The interactive REPL requires user input; exclude from automated coverage
        # as it's exercised manually.
        print(Fore.CYAN + "Advanced Calculator REPL. Type 'help' for commands.")
        while True:
            try:
                raw = input(Fore.CYAN + "> ")
            except (KeyboardInterrupt, EOFError):
                print()
                break
            parts = shlex.split(raw)
            if not parts:
                continue
            cmd = parts[0].lower()
            args = parts[1:]
            try:
                if cmd in self.list_operations():
                    if len(args) < 2:
                        print(Fore.YELLOW + "Please provide two numeric operands")
                        continue
                    a = to_number(args[0])
                    b = to_number(args[1])
                    res = self.apply_operation(cmd, a, b)
                    print(Fore.GREEN + f"Result: {res}")
                elif cmd == "history":
                    for i, c in enumerate(self.history.list()):
                        print(Fore.CYAN + f"{i+1}. {c.operation} {c.operands} => {c.result} @ {c.timestamp}")
                elif cmd == "clear":
                    self.history.clear()
                    print(Fore.YELLOW + "History cleared")
                elif cmd == "undo":
                    self.history.undo()
                    print(Fore.YELLOW + "Undo performed")
                elif cmd == "redo":
                    self.history.redo()
                    print(Fore.YELLOW + "Redo performed")
                elif cmd == "save":
                    path = args[0] if args else os.path.join(self.cfg.history_dir, self.cfg.history_file)
                    self.history.save_csv(path, encoding=self.cfg.default_encoding)
                    print(Fore.GREEN + f"Saved to {path}")
                elif cmd == "load":
                    path = args[0] if args else os.path.join(self.cfg.history_dir, self.cfg.history_file)
                    self.history.load_csv(path, encoding=self.cfg.default_encoding)
                    print(Fore.GREEN + f"Loaded from {path}")
                elif cmd == "help":
                    print(Fore.CYAN + self.help_text())
                    print(Fore.CYAN + "Additional commands: history, clear, undo, redo, save [path], load [path], help, exit")
                elif cmd == "exit":
                    break
                else:
                    print(Fore.RED + f"Unknown command: {cmd}")
            except ValidationError as e:
                print(Fore.RED + f"Validation error: {e}")
            except OperationError as e:
                print(Fore.RED + f"Operation error: {e}")
            except Exception as e:
                print(Fore.RED + f"Error: {e}")
