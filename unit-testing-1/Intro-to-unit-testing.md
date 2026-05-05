# Unit Testing

A "unit" of code is considered to be the smallest testable chunk of software which performs a very specific job or task, such as a function, method or class. They can be tested in isolation, away from the rest of the system.

The goal of unit testing to verify that each unit behaves as expected.

What is the expected behaviour of the below function, and how can we verify it?

```py
def add_two_numbers(a, b):
    return a + b
```

## What is Unit Testing?

Unit Testing is the process of executing this unit of code in isolation under various conditions and scenarios to test it's behaviour.

```py
add_two_numbers(1, 1) # Expected 2
add_two_numbers(-1, 0) # Expected -1
add_two_numbers(1.00234, 0.3456) # Expected 1.34794
add_two_numbers("test", 1) # Expected Error
add_two_numbers("string 1", "string 2") # Expected "String 1String 2" - invalid output
```

Are there any other tests for this function you can think of?

<details><summary>Reveal</summary>Examples could be:

- What if we pass variables or other objects?  
- What about two strings?</details>

Given the following function, what could some unit tests be?

```py
def is_even(n):
    return n % 2 == 0
```

<details>
<summary>Reveal</summary>Examples could be:

- is_even(4) # Expected True
- is_even(5) # Expected False
- is_even(-2) # Expected True
- is_even(0) # Expected True
- is_even(3.5) # Exception / False
- is_even("string") # Exception / False

</details>

>In Python, the built-in unittest framework and third-party libraries like pytest are commonly used.

It is particularly important to perform comprehensive unit testing before making a change to current application code to avoid `regression bugs`, which is when new code accidentally breaks existing functionality.

### Why is it Important?

A good testing strategy outlines the operational envelope of our software; Failing tests indicate where we need to improve our software; Passing tests are an indicator of software quality and robustness.

>Robust_software == happy_users == happy_employer

Good testing basically outlines how well your software is going to run!

If you test over a given set of parameters you can say with 100 percent confidence that this code is working fine within these conditions.

If someone comes and try to push it beyond its limitations then you can say that it's not the how this code is supposed to work, and then you can decide how you want to handle that.

### Unit Testing Vs. Debugging

It is easy to confuse these two activities, the key differences are:

|Unit Testing|Debugging|
|---|---|
|Confirms code works|Finds why code broke|
|Preventative|Reactive|
|Automated|Usually manual|

Unit testing and debugging are both important, but they're completely different steps during the application development process.

## Testing Pathways

When testing we refer to our test scenarios as following two distinct paths:

- **The Happy Path**: Valid inputs, expecting successful outcomes.

```py
add_two_numbers(1, 1) # Expected 2
add_two_numbers(-1, 0) # Expected -1
add_two_numbers(1.00234, 0.3456) # Expected 1.34794
```

- The Unhappy Path: Invalid inputs or scenarios, expecting unsuccessful or invalid outcomes.

```py
add_two_numbers("test", 1) # Expected Error
add_two_numbers("string 1", "string 2") # Expected "String 1String 2" - invalid output
```

### Test Cases

We can also define certain _test cases_ when we test:

- Common Case
- Edge Case
- Corner Case

#### Common Case

Common cases occurs at normal operating parameters

```python
add_two_numbers(100, 100)
```

#### Edge Case

Edge cases occur at an extreme (maximum or minimum) operating parameter.

```python
add_two_numbers(0, 10**10000)
```

#### Corner Case

Corner cases occur outside of normal operating parameters, specifically when multiple environmental variables or conditions are simultaneously at extreme levels, even though each parameter is within the specified range.

```python
add_two_numbers("text", 10**10000)
```

## Writing Tests

Python includes two main modules for running unit tests: `unittest` and `pytest`.

`Assert` is a built-in Python statement that checks if a condition is True. If it's True, nothing happens. If it's False, it raises an AssertionError. Both `unittest` and `pytest` implement assert in different ways.

- **Unittest**: A testing framework included in the standard Python library. Unittest is class based, with a number of 'special methods' to apply assert conditions. Some examples include:

```py
class TestExample(unittest.TestCase):
    def test_assertions(self):
        # Basic
        self.assertEqual(a, b)
        self.assertNotEqual(a, b)
        self.assertTrue(x)
        self.assertFalse(x)
        
        # Identity
        self.assertIs(a, b)
        self.assertIsNot(a, b)
        self.assertIsNone(x)
        self.assertIsNotNone(x)
        
        # Collections
        self.assertIn(item, container)
        self.assertNotIn(item, container)
        self.assertListEqual(list1, list2)
        self.assertDictEqual(dict1, dict2)
        self.assertSetEqual(set1, set2)
        
        # Numeric
        self.assertAlmostEqual(a, b, places=7)
        self.assertGreater(a, b)
        self.assertLess(a, b)
        
        # Exception
        self.assertRaises(ValueError, func, arg1, arg2)

        # All of the "self.assert..." statements are repetitive boilerplate, one reason developers prefer pytest
```

- `pytest`: Considered the industry standard testing framework and preferred by most developers; Plain assert statements are embedded into functions, followed by the conditional logic to be tested `assert <expression>`. Python evaluates if the expression is `True`. If it's `False`, the test fails.

    Pytest is developed and maintained by third parties and the community, it therefore has an extensive library of plugins available to extend its' functionality.

Here's a brief comparison of the two:

|Feature|`unittest` (Built-in)|`pytest` (Third-party)|
|---|---|---|
|Boilerplate|High. Requires classes and specific methods (see above).|Low. Just write a function starting with `test_.`|
|Assertions|Requires special methods like `self.assertEqual()`.|Uses the standard Python `assert` keyword.|
|Learning Curve|Higher (Object-Oriented focus).|Lower (Functional focus).|
|Features|Basic.|Advanced (Fixtures, Parameterisation, Plugins).|

### My First `pytest` Test

>pytest will run all files of the form `test_*.py` or `*_test.py` in the current directory and its subdirectories.

1. In a new working directory create a file called `test_sample.py` and open it in VSC.
2. Install the pytest library with `pip install -U pytest` (_Optional: create a virtual environment first_.)
3. Add the following code, save and run:

```py
import pytest

def add_two_numbers(a, b):
    return a + b

# No class needed (but can use)
def test_answer():
    assert add_two_numbers(3, 5) == 8
```

4. Nothing happens!

    The default method of pressing the 'run' button doesn't initialise pytest. To run our test we can run: `pytest test_sample.py` from the Terminal.
5. We can also use VSCs built in testing interface. Down the left hand side select the Testing option (conical flask - sciency!)
6. Select 'Choose a Testing Framework' then in the Quick Access bar choose pytest.
7. Once loaded you should see a line representing your working directory, if you drill down you'll see your `test_sample.py` file, and down again to see the `test_answer` function which was created, and recognised by pytest.

IMAGE

In our case there is only one `test_*.py` file, and only one `test_*` function, but if we had multiple we could run the individual tests, all the tests in a file, or all `test_*.py` files in a directory from here.

If you run the test above the output should be like this:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
rootdir: g:\downloads\generation\courses\DE\DE-NAT4\dev
collected 1 item

test_sample.py .                                                         [100%]

============================== 1 passed in 0.01s ==============================
Finished running tests!
```

Now change the assertion to a false value (i.e. change the 8 to something else). Then we get an output similar to this:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
rootdir: g:\downloads\generation\courses\DE\DE-NAT4\dev
collected 1 item

test_sample.py F                                                         [100%]

================================== FAILURES ===================================
_________________________________ test_answer _________________________________

    def test_answer():
>       assert add_two_numbers(3, 5) == 5
E       assert 8 == 5
E        +  where 8 = add_two_numbers(3, 5)

test_sample.py:35: AssertionError
=========================== short test summary info ===========================
FAILED test_sample.py::test_answer - assert 8 == 5
============================== 1 failed in 0.05s ==============================
Finished running tests!
```

The `100%` means that all defined tests ran, then we have the test report.

In this case it says: `FAILED test_sample.py::test_answer - assert 8 == 5` indicating that, in my case, 8 == 5 is False. For other failure cases pytest can:

- Shows you exactly where string characters differ.
- Highlight the missing or extra items in Lists/Dicts.
- Show the actual vs. expected value of numbers.

### PyTest Key Points

- **Naming**: Always name your test files test_*.py.
- **Functions**: Always name your test functions test_*.
- **Assertion**: Use assert <condition> for almost everything.
- **Execution**: Run `pytest` in the terminal, or use VSC's testing panel to see the test report.

## Test-Driven Development

Test-Driven Development (TDD) is a software development process that flips the traditional coding workflow on its head. Instead of writing code and then writing tests to see if it works, you write the test first, watch it fail (known as the **Red Phase**), and then write the minimum amount of code necessary to make it pass (the **Green Phase**).

>There is also a **Blue Phase** in which we refactor our code i.e. remove duplication, improve variable names, and optimize logic. Because you have a passing test, you can change the code confidently knowing the test will catch you if you break something. We're not aiming to become software developers, so this is a can of worms you can open by yourself if you wish.

### TDD vs. Traditional Development

In traditional development, testing is often an afterthought (or skipped entirely when deadlines loom).

|Feature|Traditional (Test-Last)|TDD (Test-First)|
|---|---|---|
|Code Quality|Often cluttered; harder to test later.|Naturally modular and "testable."|
|Confidence|High anxiety when changing old code.|High confidence; tests act as a safety net.|
|Documentation|Requires separate docs/comments.|The tests are the documentation.|
|Debugging|Hours spent hunting for bugs in large blocks.|Bugs are caught instantly in tiny increments.|

TDD encourages you to write just enough code to meet the objectives.

**Step 1**: The Red Phase

We create a file `test_validator.py` and write a test for a function that doesn't exist.

```py
from validator import is_valid_length

def test_password_is_too_short():
    # We expect this to return False for a 5-letter password
    assert is_valid_length("abc12") is False
```

Running pytest results in an ImportError or NameError. *Test is **Red***.

2. The Green Phase:

We create `validator.py` and write the bare minimum to pass.

```py
# validator.py
def is_valid_length(password):
    return len(password) >= 8
```

Running pytest now passes. *Test is **Green***.

3. Expanding the Requirements

Add a new test for a valid password.

```py
def test_password_is_long_enough():
    assert is_valid_length("securepassword123") is True
```

Is our status now **Red** or **Green**?

<details><summary>Reveal</summary>Green - our existing test covers this requirement, so we could move onto the next one.</details>
