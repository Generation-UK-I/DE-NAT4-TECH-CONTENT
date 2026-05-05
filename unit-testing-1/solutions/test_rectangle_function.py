from rectangle_function import get_rectangle_area
import pytest

# The test functions to be executed by PyTest

def test_can_calc_area():
    result_area = get_rectangle_area(2, 3)
    assert result_area == 6, "incorrect area"

# edge cases
def test_can_calc_area_for_big_numbers():
    result_area = get_rectangle_area(20000, 30000)
    assert result_area == 600000000, "incorrect area for big numbers"

def test_type_error_for_non_int_arg():
    with pytest.raises(TypeError):
        get_rectangle_area('1', 2)

def test_type_error_for_non_positive_arg():
    with pytest.raises(ValueError):
        get_rectangle_area(-1, 2)
