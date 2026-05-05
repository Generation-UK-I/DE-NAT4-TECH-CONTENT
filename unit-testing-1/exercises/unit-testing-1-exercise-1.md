# Add Two Numbers

You have been asked to write and test a python function named `add_two_numbers` with the following requirements:

1. Put your `add_two_numbers` function in one file e.g. `add_two_numbers.py`
1. Put the tests in another file e.g. `test_add_two_numbers.py`
1. Your function should receive two numeric arguments and return the mathematical addition of them. Your first iteration of the function would have no "active" code, like this:

    ```python
    def add_two_numbers(a, b):
    pass
    ```

1. If a non-numeric arg has been passed to the function it should return the string `Invalid Input`
1. It should be robust (not crash) for all of these scenarios:
   - `adds two whole numbers`
   - `adds a positive whole number to a negative whole number`
   - `adds two floating point numbers`
   - `adds a string to a whole number` should return the string `Invalid Input`
   - `adds two strings` should return the string `Invalid Input`
1. You should define the code in one file and the test cases in another

_Note: you may find you need to iteratively improve your function to cater for all scenarios listed._
