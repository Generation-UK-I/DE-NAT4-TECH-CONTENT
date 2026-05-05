from maths_example import add_numbers, calculator
import pytest
import re

# test the maths function

def test_happy_add_two_numbers_adds_two_integers():
    # arrange some test data
    number1 = 12
    number2 = 30
    expected = 42

    # act on our function
    result = add_numbers(number1, number2)

    # assert the result was correct
    assert result == expected, f'Expected {expected} but was {result}'


def test_happy_add_two_numbers_with_zeros():
    # arrange some test data
    number1 = 0
    number2 = 0
    expected = 0

    # act on our function
    result = add_numbers(number1, number2)

    # assert the result was correct
    assert result == expected, f'Expected {expected} but was {result}'

def test_happy_add_two_numbers_with_decimals():
    # arrange some test data
    number1 = 1.2
    number2 = 3.4
    expected = 4.6

    # act on our function
    result = add_numbers(number1, number2)

    # assert the result was correct
    assert result == expected, f'Expected {expected} but was {result}'

def test_happy_add_two_numbers_with_zero_and_big_number():
    # arrange some test data
    number1 = 0
    number2 = 999999999
    expected = 999999999

    # act on our function
    result = add_numbers(number1, number2)

    # assert the result was correct
    assert result == expected, f'Expected {expected} but was {result}'



def test_happy_add_two_numbers_with_negatives():
    # arrange some test data
    number1 = -1
    number2 = -2
    expected = -3

    # act on our function
    result = add_numbers(number1, number2)

    # assert the result was correct
    assert result == expected, f'Expected {expected} but was {result}'
    # assert (thing is true), "message if not true"


def test_unhappy_add_two_numbers_with_none_arg():
    number1 = None
    number2 = 42
    expected_message = re.escape(
        r"unsupported operand type(s) for +: 'NoneType' and 'int'")

    with pytest.raises(TypeError, match=expected_message):
        add_numbers(number1, number2)


def test_unhappy_add_two_numbers_with_string_and_number():
    # arrange some test data
    number1 = 12
    number2 = "cat"
    expected_message = "unsupported operand type(s) for +: 'int' and 'str'"

    # act on our function
    try:
        add_numbers(number1, number2)
        assert False, 'Should have been a TypeError but was not'
    except TypeError as expected:
        #TypeError: unsupported operand type(s) for +: 'int' and 'str'
        assert f'{expected}' == expected_message, 'Error message was not as expected'
    except Exception as whoopsy:
        assert False, f'Expected a TypeError but got "{whoopsy}"'


def test_calculator_will_add_two_numbers():
    # arrange
    num1 = 12
    num2 = 34
    operation = "add"
    expected_result = 46

    # act
    result = calculator(num1, num2, operation)

    # assert
    assert result == expected_result, f'Expected {expected_result} but was {result}'


def test_calculator_will_subtract_two_numbers():
    # arrange
    num1 = 12
    num2 = 34
    operation = "subtract"
    expected_result = -22

    # act
    result = calculator(num1, num2, operation)

    # assert
    assert result == expected_result, f'Expected {expected_result} but was {result}'

