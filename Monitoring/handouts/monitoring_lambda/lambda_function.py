import logging
from random import randint, random
from time import sleep, perf_counter
from cloudwatch_logging import CloudwatchLogging, Filters

coffee_items = [
    {
        "name": "Latte with Oat Milk",
        "price": 1.75
    },
    {
        "name": "Americano with Nutmeg",
        "price": 1.50
    },
    {
        "name": "Hot Chocolate with sprinkles",
        "price": 2.25
    },

]

def lambda_handler(event, context):
    logger = CloudwatchLogging.create_logger(__name__, appender=None, filter=None)
    logger.setLevel(logging.INFO)
    logger.propagate = False  # disable Lambda runtime default logger from double logging lines sent to this logger
    logger.addFilter(CloudwatchLogging.LogFilter(Filters.COST_EFFECTIVE))

    # Create 100 logs
    for _ in range(100):
        # Record runtime
        start_time = perf_counter()

        # Pick a random length of time between 1 and 5 seconds
        sleep_time = random()
        sleep(sleep_time)

        # Choose success / failure randomly
        success = randint(0, 1)
        status_code = 200 if success else 500

        salesItem = coffee_items[randint(0, 2)]

        json_log = {
            'statusCode': status_code,
            'executionTime': perf_counter() - start_time,
            'sales_data' : salesItem
        }

        if success:
            logger.info(json_log)
        else:
            logger.error(json_log)
