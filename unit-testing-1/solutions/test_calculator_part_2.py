import pytest
from calculator_part_2 import calculator

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
