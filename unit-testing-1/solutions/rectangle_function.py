
def get_rectangle_area(width, length):

    if not isinstance(width, int) or not isinstance(length, int):
        raise TypeError('Invalid Type Entered, Int type Expected')

    if (isinstance(width, int) and width <= 0) or \
        (isinstance(length, int) and length <= 0):
        raise ValueError('Invalid Value Entered, Value greater than 0 Expected')

    return width * length
