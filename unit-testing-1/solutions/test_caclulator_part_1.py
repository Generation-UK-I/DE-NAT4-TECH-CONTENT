
from calculator_part_1 import calculator

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
