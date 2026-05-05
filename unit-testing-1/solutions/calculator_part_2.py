
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
