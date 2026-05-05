# Test-Driven Development Exercise

## Objectives

Create a function fizzbuzz(number) that:

- Returns `Fizz` if the number is divisible by **3**.
- Returns `Buzz` if the number is divisible by **5**.
- Returns `FizzBuzz` if divisible by both.
- Returns `BuzzFizz` if divisible by neither.

## Task

1. Create a file called `test_fizzbuzz.py` and add the following first test.

```py
from fizzbuzz import *

def test_returns_fizz_when_divisible_by_three():
    assert fizzbuzz(3) == "Fizz"
```

2. Run the test using VSC's built-in test interface, it will fail, so your code is in **red phase**; fix it by creating the `fizzbuzz.py` file, and create a function which will pass the test.

3. Once your code is in green, add the following new test to `test_fizzbuzz.py`.

```py
def test_returns_buzz_when_divisible_by_five():
    assert fizzbuzz(5) == "Buzz"
```

4. Your code is now red again; Update your function to pass the test.

5. Add your own test for BuzzFizz and update your code to pass it.

### Stretch and Challenge

Refactor your code.
