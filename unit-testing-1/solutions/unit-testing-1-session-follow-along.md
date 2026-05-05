## Unit Testing 1 - Session Follow-along Solution

### Part 1

Create two new scripts called `price_updater.py` and `test_price_updater.py`.

```py
def price_updater(prices: list[float], increase_rate: float) -> list[float]:
    if increase_rate < 0 or increase_rate > 1:
        return 'Increase factor out of range!'

    increased_prices = []

    for price in prices:
        if type(price) != float:
            return 'Incorrect Price Detected!'

        elif price < 0 or price > 100000:
            return 'Price out of range!'

        else:
            new_price = price * (1 + increase_rate)
            increased_prices.append(new_price)

    return increased_prices

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

test_price_updater_common_case()
test_price_updater_common_case_two()
test_price_updater_price_not_float()
test_price_updater_price_out_of_range()
test_price_updater_increase_factor_out_of_range()
```

### Part 2

Use `pytest` to run the unit tests now - remove the 5 function calls from end of the python script from Part 1.

```py
# Updated same function with additional requirements
def price_updater(prices: list[float], increase_rate: float) -> list[float]:
    if not isinstance(increase_rate, float) and not isinstance(increase_rate, int):
        raise TypeError('Increase rate is not a numeric type!')

    if increase_rate < 0 or increase_rate > 1:
        raise ValueError('Increase rate out of range!')

    increased_prices = []

    for price in prices:
        if type(price) != float:
            return 'Incorrect Price Detected!'

        elif price < 0 or price > 100000:
            return 'Price out of range!'

        else:
            new_price = price * (1 + increase_rate)
            increased_prices.append(new_price)

    return increased_prices

# Changed this unit test to use new logic of a raised Exception
def test_price_updater_increase_factor_out_of_range():
    test_prices = [2.5, 5.2]
    test_increase_rate = 2.4

    with pytest.raises(ValueError):
        price_updater(test_prices, test_increase_rate)

# New unit test for increase rate type
def test_price_updater_increase_factor_not_numeric():
    test_prices = [2.5, 5.2]
    test_increase_rate = '0.7'

    with pytest.raises(TypeError):
        price_updater(test_prices, test_increase_rate)
```

Run the unit tests with the following command:

```sh
# Mac/Unix
$ python3 -m pytest -v test_price_updater.py
# or on Windows
$ py -m pytest -v test_price_updater.py
```
