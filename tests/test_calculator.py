""" tests/test_calculator.py """
import sys
from io import StringIO
from app.calculator import calculator


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


# Tests for valid operations
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


# Tests for invalid inputs and errors
def test_invalid_input_format(monkeypatch):
    """Test invalid input format in REPL."""
    inputs = ["add two three", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Please follow the format: <operation> <num1> <num2>" in output


def test_division_by_zero(monkeypatch):
    """Test division by zero in REPL."""
    inputs = ["divide 5 0", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Error: Improper Inputs" in output


def test_unknown_operation(monkeypatch):
    """Test unknown operation in REPL."""
    inputs = ["modulus 5 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert (
        "Unknown operation 'modulus'. Supported operations: add, subtract, multiply, divide."
        in output
    )

def test_exit_command(monkeypatch):
    """Test exit command to quit REPL."""
    inputs = ["exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Exiting calculator..." in output
