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

def price_updater_with_errors(prices: list[float], increase_rate: float) -> list[float]:
    if increase_rate < 0 or increase_rate > 1:
        raise ValueError

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
