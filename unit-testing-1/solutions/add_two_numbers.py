def add_two_numbers(a, b):
    if (not isinstance(a, int) and \
        not isinstance(a, float)) or \
        (not isinstance(b, int) and \
        not isinstance(b, float)):
        return "Invalid Input"
    return a + b
