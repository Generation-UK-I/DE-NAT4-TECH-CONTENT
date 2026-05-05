# Calculator

You can do this as either an OO Class or a procedural function. Solutions are provided for both.

## Part 1

You have been asked to write and test a python function named `calculator` with the following requirements:

1. It should receive two numeric arguments, and another argument for which mathematical operator to run on them (add, subtract, multiply, or divide)
1. It should return the result of applying the chosen operator to the two numbers (e.g. 5.3 + 4)

Given the requirements, do the following:

- Put your `calculator` function in a file named `calculator.py`
- Put your tests in a file named `test_calculator.py`
- Use `python3 -m pytest` (MacOS / Unix) `py -m pytest` (Windows) to run your test cases.

## Part 2

Extend your `calculator` function and test cases with the following criteria:

1. If a non-numeric argument is given for one of the two numbers, it should throw `TypeError`
1. If any operator other than the four listed above is given it should return the string `'That is an incorrect operator'`
1. The numeric arguments should be within -100,000 and 100,000, otherwise the function should throw `ValueError`
