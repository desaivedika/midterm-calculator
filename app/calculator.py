"""Calculator facade and REPL interface.

Implements the Facade pattern (Calculator wraps all subsystems) and,
as optional features, a Decorator-pattern dynamic help menu and
color-coded output via colorama.
"""

from colorama import Fore, Style, init as colorama_init

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import Caretaker
from app.exceptions import CalculatorError
from app.history import HistoryManager, LoggingObserver, AutoSaveObserver
from app.input_validators import InputValidator
from app.logger import Logger
from app.operations import OperationFactory

colorama_init(autoreset=True)


# ----- Decorator pattern: dynamic help menu -----

_help_registry = []


def help_entry(command: str, description: str):
    """Decorator that registers a command and its description for the help menu."""
    def decorator(func):
        _help_registry.append((command, description))
        return func
    return decorator


def build_help_menu() -> str:
    """Dynamically build the help menu from registered entries + operations."""
    lines = [f"{Fore.CYAN}Available commands:{Style.RESET_ALL}"]
    for op in OperationFactory.available_operations():
        lines.append(f"  {Fore.GREEN}{op}{Style.RESET_ALL} - perform {op} on two numbers")
    # Decorators register bottom-up, so reverse to show them in written order
    for command, description in reversed(_help_registry):
        lines.append(f"  {Fore.GREEN}{command}{Style.RESET_ALL} - {description}")
    return "\n".join(lines)


@help_entry("history", "display calculation history")
@help_entry("clear", "clear calculation history")
@help_entry("undo", "undo the last calculation")
@help_entry("redo", "redo the last undone calculation")
@help_entry("save", "save history to CSV")
@help_entry("load", "load history from CSV")
@help_entry("help", "show this help menu")
@help_entry("exit", "exit the application")
def _register_commands():
    """Placeholder carrying the help registrations."""
    return None  # pragma: no cover


class Calculator:
    """Facade providing a simple interface to all calculator subsystems."""

    def __init__(self, config: CalculatorConfig = None):
        self.config = config or CalculatorConfig()
        self.logger = Logger(self.config.log_file)
        self.history_manager = HistoryManager(
            self.config.history_file,
            self.config.max_history_size,
            self.config.default_encoding,
        )
        self.caretaker = Caretaker()
        self.validator = InputValidator()

        self.add_observer(LoggingObserver(self.logger))
        if self.config.auto_save:
            self.add_observer(AutoSaveObserver(self.history_manager))
        self.logger.info("Calculator initialized")

    def add_observer(self, observer) -> None:
        """Register an observer with the calculator."""
        self.history_manager.add_observer(observer)

    def perform_operation(self, operation_name: str, a, b) -> float:
        """Validate inputs, run the operation, record it, return the result."""
        try:
            num_a = self.validator.validate_number(a, self.config.max_input_value)
            num_b = self.validator.validate_number(b, self.config.max_input_value)
            calculation = Calculation(operation_name, num_a, num_b)
        except CalculatorError as e:
            self.logger.error(f"{operation_name} failed with inputs ({a}, {b}): {e}")
            raise

        calculation.result = round(calculation.result, self.config.precision)
        self.caretaker.save_state(self.history_manager.get_history())
        self.history_manager.add_calculation(calculation)
        return calculation.result

    def undo(self) -> bool:
        state = self.caretaker.undo(self.history_manager.get_history())
        if state is None:
            self.logger.warning("Undo requested but there is nothing to undo")
            return False
        self.history_manager._history = state
        self.logger.info("Undo performed")
        return True

    def redo(self) -> bool:
        state = self.caretaker.redo(self.history_manager.get_history())
        if state is None:
            self.logger.warning("Redo requested but there is nothing to redo")
            return False
        self.history_manager._history = state
        self.logger.info("Redo performed")
        return True

    def clear(self) -> None:
        self.caretaker.save_state(self.history_manager.get_history())
        self.history_manager.clear()
        self.logger.info("History cleared")

    def save(self) -> None:
        try:
            self.history_manager.save()
        except CalculatorError as e:  # pragma: no cover
            self.logger.error(f"Saving history failed: {e}")
            raise
        self.logger.info(f"History saved to {self.config.history_file}")

    def load(self) -> None:
        try:
            self.history_manager.load()
        except CalculatorError as e:
            self.logger.error(f"Loading history failed: {e}")
            raise
        self.logger.info(f"History loaded from {self.config.history_file}")


def calculator_repl():
    """Run the Read-Eval-Print Loop."""
    calculator = Calculator()
    print(f"{Fore.CYAN}Welcome to the Enhanced Calculator!{Style.RESET_ALL}")
    print(build_help_menu())

    while True:
        command = input(f"{Fore.YELLOW}>>> {Style.RESET_ALL}").strip().lower()

        if command == "exit":
            calculator.logger.info("Application exited")
            print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
            break

        if command == "help":
            print(build_help_menu())
            continue

        if command == "history":
            if calculator.history_manager.is_empty():
                print("No calculations yet.")
            else:
                for calc in calculator.history_manager.get_history():
                    print(f"  {calc}")
            continue

        if command == "clear":
            calculator.clear()
            print(f"{Fore.GREEN}History cleared.{Style.RESET_ALL}")
            continue

        if command == "undo":
            print(f"{Fore.GREEN}Undo successful." if calculator.undo()
                  else f"{Fore.RED}Nothing to undo.")
            continue

        if command == "redo":
            print(f"{Fore.GREEN}Redo successful." if calculator.redo()
                  else f"{Fore.RED}Nothing to redo.")
            continue

        if command == "save":
            try:
                calculator.save()
                print(f"{Fore.GREEN}History saved.{Style.RESET_ALL}")
            except CalculatorError as e:  # pragma: no cover
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            continue

        if command == "load":
            try:
                calculator.load()
                print(f"{Fore.GREEN}History loaded.{Style.RESET_ALL}")
            except CalculatorError as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            continue

        # LBYL: check the command is a known operation before proceeding
        if command not in OperationFactory.available_operations():
            calculator.logger.warning(f"Invalid command entered: {command}")
            print(f"{Fore.RED}Invalid command. Type 'help' for options.{Style.RESET_ALL}")
            continue

        # EAFP: try to read numbers and perform the operation
        try:
            a = input("Enter first number: ")
            b = input("Enter second number: ")
            result = calculator.perform_operation(command, a, b)
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except CalculatorError as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")