# Enhanced Calculator Command-Line Application

A modular command-line calculator built in Python. It supports ten arithmetic operations, an interactive REPL, undo/redo, calculation history saved to CSV with pandas, logging, and configuration through a `.env` file. The tests cover over 90% of the code, and GitHub Actions runs them on every push.

## Features

- Ten operations: add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff
- Interactive REPL with the commands history, clear, undo, redo, save, load, help and exit
- Undo and redo of calculations
- History saved to and loaded from CSV using pandas
- Logging of calculations, warnings and errors to a log file
- Results rounded to a configurable number of decimal places
- Configuration through a `.env` file, with default values
- Custom exceptions and input validation, so bad input never crashes the app
- Color-coded output (optional feature)
- Help menu generated automatically with the Decorator pattern (optional feature)
- Every request runs as a command object, and commands can be queued and run as a batch, using the Command pattern (optional feature)

## Design Patterns

- **Factory**: `OperationFactory` creates the right operation object from its name.
- **Memento**: `Memento` and `Caretaker` save snapshots of the history for undo and redo.
- **Observer**: `LoggingObserver` logs each calculation and `AutoSaveObserver` saves the history to CSV after each calculation. Observers are registered with the `Calculator` through `add_observer()`.
- **Facade**: the `Calculator` class gives one simple interface to all the parts above.
- **Decorator** (optional feature): `@help_entry` registers commands, and the help menu also lists every operation from the factory, so adding a new operation updates the menu automatically.
 - **Command** (optional feature): `app/commands.py` wraps each request (calculations, undo, redo, clear, save, load) in a command object. The REPL runs every request through a `CommandInvoker`, which records executed commands and can queue commands with `add_to_queue()` and run them later with `run_queue()`.

## Installation

1. Clone the repository:
   ~~~
   git clone git@github.com:desaivedika/midterm-calculator.git
   cd midterm-calculator
   ~~~

2. Create and activate a virtual environment:
   ~~~
   python -m venv venv
   source venv/Scripts/activate     # Windows (Git Bash)
   source venv/bin/activate         # macOS / Linux
   ~~~

3. Install the dependencies:
   ~~~
   pip install -r requirements.txt
   ~~~

## Configuration

Settings are loaded from a `.env` file in the project root using `python-dotenv`. If a setting is missing, a default value is used.

~~~
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1000000000000000
CALCULATOR_DEFAULT_ENCODING=utf-8
~~~

| Variable | Purpose | Default |
|---|---|---|
| CALCULATOR_LOG_DIR | Folder for the log file | logs |
| CALCULATOR_HISTORY_DIR | Folder for the history CSV | history |
| CALCULATOR_MAX_HISTORY_SIZE | Maximum number of history entries kept | 100 |
| CALCULATOR_AUTO_SAVE | Save history after every calculation (true/false) | true |
| CALCULATOR_PRECISION | Decimal places results are rounded to | 10 |
| CALCULATOR_MAX_INPUT_VALUE | Largest number allowed as input | 1e15 |
| CALCULATOR_DEFAULT_ENCODING | Encoding for file operations | utf-8 |
| CALCULATOR_LOG_FILE | Full path of the log file (optional) | logs/calculator.log |
| CALCULATOR_HISTORY_FILE | Full path of the history CSV (optional) | history/calculator_history.csv |

The configuration is checked when the app starts, and invalid values raise a `ConfigurationError`.

### Logging

Logs are written to the file set by `CALCULATOR_LOG_FILE` (default `<CALCULATOR_LOG_DIR>/calculator.log`) using Python's `logging` module. INFO records each calculation and actions such as undo, save and load. WARNING records invalid commands and undo/redo requests with nothing to undo or redo. ERROR records failed calculations and failed history loads.

Example log output:
~~~
2026-10-22 17:11:38 - INFO - Calculator initialized
2026-10-22 17:11:38 - INFO - Calculation: divide(1.0, 3.0) = 0.3333333333
2026-10-22 17:11:39 - WARNING - Invalid command entered: banana
2026-10-22 17:11:39 - WARNING - Undo requested but there is nothing to undo
2026-10-22 17:11:40 - ERROR - divide failed with inputs (5, 0): Cannot divide by zero
~~~

### History file

History is saved to the file set by `CALCULATOR_HISTORY_FILE` (default `<CALCULATOR_HISTORY_DIR>/calculator_history.csv`) with the columns operation, operand1, operand2, result and timestamp. A missing file, an empty file, or a file with the wrong columns produces a clear error message instead of a crash, and the current history is kept.

## Usage

Start the calculator:
~~~
python main.py
~~~

| Command | What it does |
|---|---|
| add, subtract, multiply, divide | Basic arithmetic on two numbers |
| power | Raises the first number to the power of the second |
| root | Takes the nth root (second number) of the first number |
| modulus | Remainder of the first number divided by the second |
| int_divide | Division with the fractional part discarded |
| percent | (a / b) * 100 |
| abs_diff | Absolute difference between the two numbers |
| history | Shows the calculation history |
| clear | Clears the history |
| undo / redo | Undoes or redoes the last change |
| save / load | Saves the history to CSV or loads it back |
| help | Shows the command menu |
| exit | Quits the calculator |

Example session:
~~~
>>> power
Enter first number: 2
Enter second number: 10
Result: 1024.0
>>> divide
Enter first number: 5
Enter second number: 0
Error: Cannot divide by zero
>>> exit
Goodbye!
~~~

## Testing

Run all tests with a coverage report:
~~~
python -m pytest --cov=app --cov-report=term-missing
~~~

Check the 90% coverage threshold, as the CI pipeline does:
~~~
python -m pytest --cov=app --cov-fail-under=90
~~~

The tests use parameterized cases and cover edge cases such as division by zero, negative exponents, roots of negative numbers, invalid input, invalid configuration, precision rounding, logging levels, and missing or malformed history files.

## CI/CD

GitHub Actions (`.github/workflows/python-app.yml`) runs on every push and pull request to `main`. It checks out the code, sets up Python, installs the dependencies, and runs pytest with coverage. The build fails if any test fails or if coverage drops below 90%.

## Project Structure

~~~
midterm-calculator/
├── app/
│   ├── __init__.py
│   ├── calculator.py           # Facade, REPL, help menu, color output
│   ├── calculation.py          # Calculation model
│   ├── calculator_config.py    # Configuration
│   ├── calculator_memento.py   # Memento pattern (undo/redo)
│   ├── exceptions.py           # Custom exceptions
│   ├── history.py              # History, Observer pattern, pandas CSV
│   ├── input_validators.py     # Input validation
│   ├── logger.py               # Logging setup
│   └── operations.py           # Operations and Factory pattern
│   ├── commands.py             # Command pattern and invoker
├── tests/
│   ├── __init__.py
│   ├── test_calculation.py
│   ├── test_calculator.py
│   ├── test_calculator_config.py
│   ├── test_calculator_memento.py
│   ├── test_exceptions.py
│   ├── test_history.py
│   ├── test_input_validators.py
│   ├── test_logger.py
│   └── test_operations.py
│   ├── test_commands.py
├── .env
├── main.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .github/workflows/python-app.yml
~~~