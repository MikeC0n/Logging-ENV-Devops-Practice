""" tests/test_main.py """
import sys
from io import StringIO
from app.main import calculator


# Helper function to capture print statements
def run_calculator_with_input(monkeypatch, inputs):
    """
    Simulates user input and captures output from the calculator REPL.
    
    :param monkeypatch: pytest fixture to simulate user input
    :param inputs: list of inputs to simulate
    :return: captured output as a string
    """
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    # Capture the output of the calculator
    captured_output = StringIO()
    sys.stdout = captured_output
    calculator()
    sys.stdout = sys.__stdout__  # Reset stdout
    return captured_output.getvalue()


# Positive Tests
def test_addition(monkeypatch):
    """Test addition operation in REPL."""
    inputs = ["add 2 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output


def test_subtraction(monkeypatch):
    """Test subtraction operation in REPL."""
    inputs = ["subtract 5 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 3.0" in output


def test_multiplication(monkeypatch):
    """Test multiplication operation in REPL."""
    inputs = ["multiply 4 5", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 20.0" in output


def test_division(monkeypatch):
    """Test division operation in REPL."""
    inputs = ["divide 10 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output


# Negative Tests
def test_invalid_operation(monkeypatch):
    """Test invalid operation in REPL."""
    inputs = ["modulus 5 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Unknown operation" in output


def test_invalid_input_format(monkeypatch):
    """Test invalid input format in REPL."""
    inputs = ["add two three", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Please enter a valid operation and two numbers." in output


def test_division_by_zero(monkeypatch):
    """Test division by zero in REPL."""
    inputs = ["divide 5 0", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Division by zero is not allowed" in output  # Modify based on actual error message


# Additional Tests for REPL Commands
def test_list_history_empty(monkeypatch):
    """Test listing history when empty in REPL."""
    inputs = ["list", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "No calculations in history." in output


def test_list_history_with_operations(monkeypatch):
    """Test listing history after performing an operation."""
    inputs = ["add 1 2", "list", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "1.0 addition 2.0 = 3.0" in output  # Check if the operation appears in history


def test_clear_history(monkeypatch):
    """Test clearing history in REPL."""
    inputs = ["add 1 2", "clear", "list", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "History cleared." in output
    assert "No calculations in history." in output  # Confirm history is cleared
