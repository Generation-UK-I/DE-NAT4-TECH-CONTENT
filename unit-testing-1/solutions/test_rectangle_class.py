from rectangle_class import Rectangle
import pytest

# The test functions to be executed by PyTest

def test_can_calc_area():
    rectangle = Rectangle(2, 3)
    assert rectangle.get_area() == 6, "incorrect area"

# edge case
def test_can_calc_area_for_big_numbers():
    rectangle = Rectangle(20000, 30000)
    assert rectangle.get_area() == 600000000, "incorrect area for big numbers"

def test_can_calc_area_after_width_change():
    rectangle = Rectangle(2, 3)
    rectangle.width = 10
    assert rectangle.get_area() == 30, "incorrect area after width change"

def test_type_error_for_non_int_arg():
    with pytest.raises(TypeError):
        Rectangle('1', 2)

def test_type_error_for_non_positive_arg():
    with pytest.raises(ValueError):
        Rectangle(-1, 2)
