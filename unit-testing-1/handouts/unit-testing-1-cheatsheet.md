# Unit Testing 1 cheatsheet

## Naming guidance

- Your main code should be in a suitably named file e.g. `utility_functions.py`
- Your test code should in a file prefixed or suffixed with `test_`, e.g. `test_utility_functions.py` or `utility_functions_test.py`
- Function names should begin with `test_`. So for instance: `test_example`
- If tests are defined as methods on a class, the class name should start with `Test`, as in `TestExample`

## Testing

- The `assert` keyword validates if an expression is `True`, and takes an optional message argument

E.g.:

```python
# `utility_functions.py`
def add_two_numbers(a, b):
    return a + b
```

And

```python
# `test_utility_functions.py` or `utility_functions_test.py`
def test_add_two_numbers():
    # Arrange
    a = 5
    b = 5
    expected = 10

    # Act
    actual = add_two_numbers(a, b)

    # Assert - pass
    assert expected == actual, f'Expected result to be "{expected}" but was "{actual}".'
```

## Pytest

Installation (should be in a venv).

```sh
# Mac/Unix
$ python3 -m pip install pytest
# or on Windows
$ py -m pip install pytest
```

1. You can run `python3 -m pytest --collect-only` (MacOS / Unix) `py -m pytest --collect-only` (Windows) to see which tests `pytest` will discover, without running them

### Have a go

Copy the above code into a pair of Python files, and run `python3 -m pytest` (MacOS / Unix) `py -m pytest` (Windows) and watch the output.

Hopefully you should see some information about 1 test passing.

### Testing Terms and Definitions

- `Unit`: The smallest testable chunk of code.
- `TDD`: Test Driven Development. The process of writing tests first.
- `Happy Path`: Successful test scenarios.
- `Unhappy Path`: Unsuccessful test scenarios.
- `Corner Case`: Outside normal parameters.
- `Edge Case`: Extreme min/max parameters.
