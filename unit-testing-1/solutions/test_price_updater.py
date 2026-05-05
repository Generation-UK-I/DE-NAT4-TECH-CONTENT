
from price_updater import price_updater, price_updater_with_errors
import pytest

#
# Run this file with `python3 -m pytest`
#

def test_price_updater_common_case():
    test_prices = [2.5, 5.2]
    test_increase_rate = 0.25
    expected = [3.125, 6.5]

    result = price_updater(test_prices, test_increase_rate)

    assert expected == result

def test_price_updater_common_case_two():
    test_prices = [3.5, 5.0, 4.1]
    test_increase_rate = 0.25
    expected = [4.375, 6.25, 5.125]

    result = price_updater(test_prices, test_increase_rate)

    assert expected == result


def test_price_updater_price_not_float():
    test_prices = ['five', 5.0, 4.1]
    test_increase_rate = 0.25
    expected = 'Incorrect Price Detected!'

    result = price_updater(test_prices, test_increase_rate)

    assert expected == result


def test_price_updater_price_out_of_range():
    test_prices = [150000.5, 5.0, 4.1]
    test_increase_rate = 0.25
    expected = 'Price out of range!'

    result = price_updater(test_prices, test_increase_rate)

    assert expected == result


def test_price_updater_increase_factor_out_of_range():
    test_prices = [2.5, 5.2]
    test_increase_rate = 2.4
    expected = 'Increase factor out of range!'

    result = price_updater(test_prices, test_increase_rate)

    assert expected == result

# Changed this unit test to use new logic of a raised Exception
# Uses different function price_updater_with_errors
def test_price_updater_increase_factor_out_of_range_with_pytest():
    test_prices = [2.5, 5.2]
    test_increase_rate = 2.4

    with pytest.raises(ValueError):
        price_updater_with_errors(test_prices, test_increase_rate)

# New unit test for increase rate type
def test_price_updater_increase_factor_not_numeric_with_pytest():
    test_prices = [2.5, 5.2]
    test_increase_rate = '0.7'

    with pytest.raises(TypeError):
        price_updater(test_prices, test_increase_rate)
