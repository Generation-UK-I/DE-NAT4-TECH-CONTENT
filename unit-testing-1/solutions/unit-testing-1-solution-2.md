## Unit Testing 1 - Exercise 2 Solution

### Part 1

```python
# calculator.py
def calculator(a, b, operator):
    if operator == 'add':
        return a + b
    elif operator == 'subtract':
        return a - b
    elif operator == 'multiply':
        return a * b
    elif operator == 'divide':
        return a / b

# test_calculator.py
from calc import calculator

def test_calculator_add():
    a = 10
    b = 2
    operator = 'add'

    expected = 12

    actual = calculator(a, b, operator)

    assert expected == actual

def test_calculator_subtract():
    a = 10
    b = 2
    operator = 'subtract'

    expected = 8

    actual = calculator(a, b, operator)

    assert expected == actual

def test_calculator_multiply():
    a = 10
    b = 2
    operator = 'multiply'

    expected = 20

    actual = calculator(a, b, operator)

    assert expected == actual

def test_calculator_divide():
    a = 10
    b = 2
    operator = 'divide'

    expected = 5

    actual = calculator(a, b, operator)

    assert expected == actual
```

### Part 2

```python
# calculator.py
def calculator(a, b, operator):
    if (not isinstance(a, int) and not isinstance(a, float)) or \
        (not isinstance(b, int) and not isinstance(b, float)):
        raise TypeError('You entered an invalid type')
    if (a < -100000 or a > 100000) or \
        (b < -100000 or b > 100000):
        raise ValueError('Number out of range')
    if operator == 'add':
        return a + b
    elif operator == 'subtract':
        return a - b
    elif operator == 'multiply':
        return a * b
    elif operator == 'divide':
        return a / b
    else:
        return 'That is an incorrect operator'

# test_calculator.py
import pytest
from calculator import calculator

def test_calculator_add():
    a = 10
    b = 2
    operator = 'add'

    expected = 12

    actual = calculator(a, b, operator)

    assert expected == actual

def test_calculator_subtract():
    a = 10
    b = 2
    operator = 'subtract'

    expected = 8

    actual = calculator(a, b, operator)

    assert expected == actual

def test_calculator_multiply():
    a = 10
    b = 2
    operator = 'multiply'

    expected = 20

    actual = calculator(a, b, operator)

    assert expected == actual

def test_calculator_divide():
    a = 10
    b = 2
    operator = 'divide'

    expected = 5

    actual = calculator(a, b, operator)

    assert expected == actual

def test_calculator_wrong_number_type():
    a = 'ten'
    b = 2
    operator = 'add'

    with pytest.raises(TypeError):
        calculator(a, b, operator)

def test_calculator_wrong_operator():
    a = 10
    b = 2
    operator = 'addition'

    expected = 'That is an incorrect operator'

    actual = calculator(a, b, operator)

    assert expected == actual

def test_calculator_number_out_of_range():
    a = 50000
    b = 190000
    operator = 'add'

    with pytest.raises(ValueError):
        calculator(a, b, operator)
```
