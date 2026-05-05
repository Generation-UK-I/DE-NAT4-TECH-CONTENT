# Bonus Exercise

You could do this as either a procedural function or an OO class. Solutions are provided for both.

## Get rectangle area

You have been asked to write a function called `get_rectangle_area` with the following requirements:

1. It should receive two positive integer arguments (width, length).
1. When called, it should return the area of rectangle (width * length).
1. If a non-numeric arg has been used for width or length, it should throw `TypeError`.
1. If any numeric arg rather than a positive integer has been used for width or length, it should throw `ValueError`.

Given the requirements, do the following:

- Put your Rectangle code in a file named `rectangle.py`
- Put your tests in a file named `test_rectangle.py`
- Use `python3 -m pytest` (MacOS / Unix) `py -m pytest` (Windows) to run your test cases.
