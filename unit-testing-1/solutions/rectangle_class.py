
class Rectangle:

    def __init__(self, width, length):
        if not isinstance(width, int) or not isinstance(length, int):
            raise TypeError('Invalid Type Entered, Int type Expected')
        if (isinstance(width, int) and width <= 0) or \
            (isinstance(length, int) and length <= 0):
            raise ValueError('Invalid Value Entered, Value greater than 0 Expected')
        self.width = width
        self.length = length

    def get_area(self):
        return self.width * self.length
