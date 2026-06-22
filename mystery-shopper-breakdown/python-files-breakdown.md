# Mystery Shopper ETL

## Project Files Overview

Although maddeningly complex pipelines are in use in the real world, considering our starting point, our ETL function is still pretty hard to decipher.

At the top of our [mystery-shopper-breakdown](./CF-templates-breakdown.md) we looked at the structure for the whole project, as per below.

```text
[app_dir]
    |-[src]
    |   |-[utils]
    |   |    |- db_utils.py
    |   |    |- s3_utils.py
    |   |    |- sql_utils.py
    |   |- etl.py
    |   |- mystery_shop_etl_lambda.py
    |- deployment-bucket-stack.yml
    |- deploy.sh
    |- etl-stack-packaged.yml
    |- etl-stack.yml
    |- requirements-lambda.txt
    |- requirements-test.txt
```

- The `deploy.sh` file has been explored in [mystery-shopper-breakdown](./mystery-shopper-breakdown.md)
- The `deployment-bucket-stack.yml` and `etl-stack.yml` have been covered in [CF-templates-breakdown](./CF-templates-breakdown.md)
  - We saw that `etl-stack-packaged.yml` is almost the same as `etl-stack.yml` but with S3 links to all artifacts.

So let's update our progress:

```text
[app_dir]
    |-[src]
    |   |-[utils]
    |   |    |- db_utils.py
    |   |    |- s3_utils.py
    |   |    |- sql_utils.py
    |   |- etl.py
    |   |- mystery_shop_etl_lambda.py
    |- deployment-bucket-stack.yml # DONE
    |- deploy.sh # DONE
    |- etl-stack-packaged.yml # DONE
    |- etl-stack.yml # DONE
    |- requirements-lambda.txt # Libraries to import to Lambda
    |- requirements-test.txt # Libraries to import for testing purposes - outside of our scope.
```

We're now going to start pulling apart the Python files, conveniently, they're all organised in the `./src` directory which looks like this, so we're focused upon this part of the file structure.

```text
[src]
  |-[utils]
  |    |- db_utils.py
  |    |- s3_utils.py
  |    |- sql_utils.py
  |- etl.py
  |- mystery_shop_etl_lambda.py
```

We'll start by breaking down the `mystery_shop_etl_lambda.py` file, since this runs when our function is invoked (by an upload to the raw data bucket).

## mystery_shop_etl_lambda.py

```py
from utils import s3_utils, sql_utils, db_utils

import etl
import logging
import os

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

SSM_ENV_VAR_NAME = 'SSM_PARAMETER_NAME'


def lambda_handler(event, context):
    LOGGER.info('lambda_handler: starting')
    file_path = 'NOT_SET'  # makes the exception handler compile

    try:
        bucket_name, file_path = s3_utils.get_file_info(event)

        csv_text = s3_utils.load_file(bucket_name, file_path)

        data = etl.extract(csv_text)

        transformed_data = etl.transform(data)
        # One would not normally log the data directly!!
        # ...there could be loads and it could have PID in it!!
        LOGGER.warning(f'lambda_handler: transformed_data={transformed_data}')

        ssm_param_name = os.environ.get(SSM_ENV_VAR_NAME, 'NOT_SET')
        LOGGER.info(f'lambda_handler: ssm_param_name={ssm_param_name} from ssm_env_var_name={SSM_ENV_VAR_NAME}')
        redshift_details = db_utils.get_ssm_param(ssm_param_name)
        conn, cur = db_utils.open_sql_database_connection_and_cursor(redshift_details)

        sql_utils.create_db_tables(conn, cur)
        sql_utils.save_data_in_db(conn, cur, bucket_name, file_path, transformed_data)
        cur.close()
        conn.close()

        LOGGER.info(f'lambda_handler: done, file={file_path}')

    except Exception as err:
        LOGGER.error(f'lambda_handler: failure: error={err}, file={file_path}')
        raise err
```

Our ETL code is very modular, which means our main code file is quite short, with all of the functions we need being imported from our modules.

```py
from utils import s3_utils, sql_utils, db_utils

import etl
import logging
import os
```

Review the file structure again, notice our `s3`/`sql`/`db_utils` are all in a `utils` directory, so first they're all imported. Next our `etl.py` file is imported, we'll come back to this, but in brief it contains the functions to E, T, and L our data.

Finally, `logging` and `os` are imported, which are both part of the Python Standard Library.

- `os` contains various functions for interacting with the operating system. We previously used it to access environment variables in our OS, and it works exactly the same way to access environment variables we create in Lambda.
- `Logging` is a module which simplifies the creation of log files, which are important for recording what is happening in your app.

```py
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

SSM_ENV_VAR_NAME = 'SSM_PARAMETER_NAME'
```

- `LOGGER = logging.getLogger()`: This can be a little confusing, but we declare a `LOGGER` object, which calls the __logger__ from the logging module (a bit like creating a _cursor_ from a _connection_ object when working with DBs). The Logging module allows us to create a __logger__, which is the agent that monitors the activity in your app, and generates the logs you define.

---

### Python Logging Library

>The application code provided for you is closer to production ready than other code we've provided. You will see many upcoming examples of how developers generate logs throughout their code using the built in functions of the logging library.

Logs provide insight into what's happening in your app, however how much detail should you log?

There are five standard logging levels which represent the severity of the logged activity.

|Level|Syntax|Description|
|---|---|---|
|DEBUG|`logging.debug()`|Logs providing a granular level of detail to the developer about activity within the app (e.g. connection established).|
|INFO|`logging.info()`|Provides information about more significant but likely still normal activity (e.g. someone successfully logged in).|
|WARNING|`logging.warning()`|Logs which could indicate a problem, but not likely to impact operations imminently.|
|ERROR|`logging.error()`|Alerts you to an issue with an important function, but not likely to bring the system down (e.g. a DB connection request is timing out).|
|CRITICAL|`logging.critical()`|A serious problem has occurred and may have crashed your app.|

It is ultimately up to the developer to define what log-level different outcomes in their code will generate logs at

---

Back to our code snippet...

- `LOGGER.setLevel(logging.INFO)`: This tells our __logger__ to capture all log messages of level `INFO` or higher
- `SSM_ENV_VAR_NAME = 'SSM_PARAMETER_NAME'`: This value is the System Center Parameter Store parameter, which is created by the cloudformation template that deploys your lambda function (see [cf-templates-breakdown.md](./CF-templates-breakdown.md)).

>The parameter in Parameter Store has been created for you, it is a JSON object containing all of the database connection details, including database-name, connection endpoint, port, user, and password.

```py
def lambda_handler(event, context):
    LOGGER.info('lambda_handler: starting')
    file_path = 'NOT_SET'  # makes the exception handler compile

    try:
        bucket_name, file_path = s3_utils.get_file_info(event)

        csv_text = s3_utils.load_file(bucket_name, file_path)

        data = etl.extract(csv_text)

        transformed_data = etl.transform(data)

        LOGGER.warning(f'lambda_handler: transformed_data={transformed_data}')
```

- `def lambda_handler(event, context):` - The lambda_handler is the entry point to your code when your Lambda function is called. Lambda doesn't run your code like VSC, where you can just press the play button, instead it imports your code, and then looks for the `myapp.lambda_handler(event, context)` function to execute.
  - `event`: this is the data passed to the function when it is triggered. The event could be an API Gateway request, an object being added to a bucket, or a message to an SQS queue, a scheduled event, pretty much anything.

    The data passed through is usually in a Python dictionary, so we can access it using our dictionary methods.
  - `Context`: provides methods which allow you to access information from the lambda environment, such as `context.function_name`, `context.function_name`, `context.get_remaining_time_in_millis()`* and more.

    *This is a particularly useful one for investigating timeout failures

- `LOGGER.info('lambda_handler: starting')`: This instructs our LOGGER object to create an `INFO` log message containing the provided string.
  - As you read through the code you will see lots of these, at different severity levels, so we won't bother repeating each one in our breakdowns.
- `try:`: opens a try-except block for error handling and cleanly closing any DB connections
- `bucket_name, file_path = s3_utils.get_file_info(event)`: declares two variables, and assigns values to them which are returned by the `.get_file_info()` function, in the `s3_utils` module.
  - The next 3 lines, like the one above just call functions from other modules. We will explore these modules separately, so we'll skip them for now.

```py
ssm_param_name = os.environ.get(SSM_ENV_VAR_NAME, 'NOT_SET')
    ...
    redshift_details = db_utils.get_ssm_param(ssm_param_name)
    conn, cur = db_utils.open_sql_database_connection_and_cursor(redshift_details)
```

Our cloudformation template __etl-stack.yml__, when creating this lambda function, also creates a lambda environment variable called `SSM_PARAMETER_NAME`, which is imported at the top of this file.

- `ssm_param_name = os.environ.get(SSM_ENV_VAR_NAME, 'NOT_SET')`: uses the `os` library to get the Systems Manager parameter name from the lambda environment variables.
- `redshift_details = db_utils.get_ssm_param(ssm_param_name)`: populates the redshift_details variable, with the value returned by the `.get_ssm_param()` function, from within the `db_utils` module.
  - We'll review these modules elsewhere
- `conn, cur = db_utils.open_sql_database_connection_and_cursor(redshift_details)`: creates `conn` and `cur` objects for connecting to and interacting with a database.

```py
sql_utils.create_db_tables(conn, cur)
sql_utils.save_data_in_db(conn, cur, bucket_name, file_path, transformed_data)
cur.close()
conn.close()
```

- `sql_utils.create_db_tables(conn, cur)`: calls the `.create_db_tables()` function, passing the `conn` and `cur` objects to facilitate connecting to the database and inserting the relevant SQL statements.
- `sql_utils.save_data_in_db(conn, cur, bucket_name, file_path, transformed_data)`: call the `.save_data_in_db()` function, passing multiple arguments through to it.
- `cur.close()` / `conn.close()`: close the cursor and connection.

```py
except Exception as err:
    ...
    raise err
```

Finally we close out our try-except block.

---

Recall our file structure from the beginning, we've broken down the `mystery_shop_etl_lambda.py` file, so now let's do the `etl.py` file, then move onto the `utils`.

```text
[src]
  |-[utils]
  |    |- db_utils.py
  |    |- s3_utils.py
  |    |- sql_utils.py
  |- etl.py
  |- mystery_shop_etl_lambda.py # DONE
```

## etl.py

Below is the etl.py code, a few things to note first.

- Again the Python Logging library is used, but it works the same as the previous example, so we'll omit them.
- The `mystery_shop_etl_lambda.py` file contained some new concepts like the lambda_handler, logging library, redshift, and SSM. Much of this next file is simply applying Python features and logic you should already be familiar with - so it should be easier/quicker.

```py
import csv
from datetime import datetime
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

MYSTERY_SHOPPER_FIELDS = [
            'store_id',
            'store_name',
            'mystery_shopper_id',
            'mystery_shopper_name',
            'store_type',
            'number_of_store_employees',
            'visit_date',
            'start_time',
            'end_time',
            'overall_score',
        ]

def extract(body_text):
    LOGGER.info('extract: starting')
    reader = csv.DictReader(
        body_text,
        fieldnames=MYSTERY_SHOPPER_FIELDS,
        delimiter=',',
    )

    # skip header row
    next(reader)

    data = [row for row in reader]

    LOGGER.info(f'extract: done: rows={len(data)}')
    return data

def remove_sensitive_information(data):
    LOGGER.info(f'remove_sensitive_information: processing rows={len(data)}')
    return [
        {k: v for k, v in item.items() if k != 'mystery_shopper_name'} for item in data
    ]

def reformat_number_of_store_employees(data):
    LOGGER.info(f'reformat_number_of_store_employees: starting')
    updated_data = []
    for item in data:
        updated_item = item.copy()
        updated_item['number_of_store_employees'] = int(
            updated_item['number_of_store_employees'].strip('"')
        )
        updated_data.append(updated_item)

    LOGGER.info(f'reformat_number_of_store_employees: done: rows={len(updated_data)}')
    return updated_data

def reformat_visit_date(data):
    LOGGER.info('reformat_visit_date: starting')
    updated_data = []
    for item in data:
        updated_item = item.copy()
        input_format_string = '%d/%m/%Y'
        dt = datetime.strptime(updated_item['visit_date'], input_format_string)
        new_datetime = dt.strftime('%Y-%m-%d')
        updated_item['visit_date'] = new_datetime
        updated_data.append(updated_item)

    LOGGER.info(f'reformat_visit_date: done: rows={len(updated_data)}')
    return updated_data

def transform(data):
    LOGGER.info('transform: starting')
    data = remove_sensitive_information(data)
    data = reformat_number_of_store_employees(data)
    data = reformat_visit_date(data)

    LOGGER.info(f'transform: done: rows={len(data)}')
    return data
```

Again, repetitive info will be omitted, but we start by importing some libraries, `csv` and `datetime` in this case. Additionally, we'll skip simple actions were a sufficient comment exists.

```py
import csv
from datetime import datetime
...

MYSTERY_SHOPPER_FIELDS = [
            ...
        ]
```

- `csv` provides functions and methods for working with csv files. You have used this with your first DE project.
- `datetime` provides functions and methods for working with date and time data types, such as arithemitic, and time zones.
- `MYSTERY_SHOPPER_FIELDS = [...]`: A Python list containing strings that represent the column headings in our raw csv

```py
def extract(body_text):
    ...
    reader = csv.DictReader(
        body_text,
        fieldnames=MYSTERY_SHOPPER_FIELDS,
        delimiter=',',
    )

    # skip header row
    next(reader)

    data = [row for row in reader]
    ...
    return data
```

- `def extract(body_text):`: defines our __extract__ function
  - Remember, we don't run this file directly, these functions are called from the `mystery_shop_etl_lambda.py` file.
  - `body_text` is passed through when calling the function; in this case the data is first captured from the csv file when it is uploaded to S3, then passed through to this extract function.
    - We'll see how this happens when we break down the `s3_utils.py` file.
  - `reader = csv.DictReader(body_text, fieldnames=MYSTERY_SHOPPER_FIELDS, delimiter=',',)`: (NOTE: formatting changed to put on one line) here we use the `csv.DictReader()` function to extract the body text from the data passed from the uploaded csv, each row will be a new Python dictionary.
    - `filesnames`: references the list of field names created earlier
    - `delimiters`: tells the Reader that a comma separates the fields on each row of the csv.
- `data = [row for row in reader]`: each of the individual dictionaries extracted by the reader is now appended to a list called data, which is returned by the function for use elsewhere.

---

The next function in the `etl.py` file is `remove_sensitive_information()`, but if we review the `mystery_shop_etl_lambda.py` file again we'll see that it's not the next one to actually run. After getting the file from S3 and extracting the data, the `etl.transform()` function is run next, and that calls additional functions for us, so let's look at the transform one first.

```py
def transform(data):
    ...
    data = remove_sensitive_information(data)
    data = reformat_number_of_store_employees(data)
    data = reformat_visit_date(data)
    ...
    return data
```

- `def transform(data):`: Again, the `mystery_shop_etl_lambda.py` file connects everything together, so after the data is extracted by the `extract()` function, it is then immediately passed into the `transform()` function.
- `data = remove_sensitive_information(data)`
- `data = reformat_number_of_store_employees(data)`
- `data = reformat_visit_date(data)`
  - Each of the above simply passes the data through different function automatically, to clean it in various ways.
- `return data`: The cleaned data is returned.

Now let's look at the three different functions called by the `transform()` function.

```py
def remove_sensitive_information(data):
    ...
    return [
        {k: v for k, v in item.items() if k != 'mystery_shopper_name'} for item in data
    ]
```

The name of the function makes it clear what is happening, but the logic is a little tricky. The goal is to return a version of the mystery shopper data with the names removed.

- `return [...]`: The function will return a list, but the list is created by the expression within...
- `{k: v for k, v in item.items() if k != 'mystery_shopper_name'} for item in data`: Lets split this one up
  - Start at the end `for item in data`, so something is going to happen to each item in the `data` object (which is a list of dictionaries)
  - `{...}`: the big expression is within curly brackets, therefore it's building a dictionary
  - `k: v`: these represent the key and value in the new dictionary (call these k1 and v1 for clarity)
  - `for k, v in item.items()`: loop through the key and value of each item (dictionary) from `data`, each k and v, is assigned to k1 and v1 in turn, building a new dictionary. This is repeated for each dictionary in `data`.
  - `if k != 'mystery_shopper_name'`: only do the previous step if the key (k) is not equal to 'mystery_shopper_name'.

Once these steps have completed the function returns a new list of dictionaries, except the mystery_shopper_name field has been removed (cleaned).

```py
def reformat_number_of_store_employees(data):
    ...
    updated_data = []
    for item in data:
        updated_item = item.copy()
        updated_item['number_of_store_employees'] = int(
            updated_item['number_of_store_employees'].strip('"')
        )
        updated_data.append(updated_item)
    ...
    return updated_data
```

This function is pretty straightforward; if you review the sample csv you can see that the "NumberOfStoreEmployees" field (we renamed it to `number_of_store_employees` during extraction) is a string e.g. "8" (including the quotation marks), and we want it to be an integer suitable for data analysis.

- `updated_data = []`: After defining the function and passing `data` through, create an empty dictionary
  - Remember, at this point the data has already been passed through the `remove_sensitive_information()` function
- `for item in data:`: Loop through each item (dictionary) in `data`
- `updated_item = item.copy()`: create an updated_item object, and make it a copy of the current item in the for loop.
- `updated_item['number_of_store_employees'] = int(updated_item['number_of_store_employees'].strip('"'))`: a long statement, so let's break it in half
  - `updated_item['number_of_store_employees'] = `: the updated_item is a dictionary, so this is going to reassign the value for the key of `number_of_store_employees` to...
  - `int(updated_item['number_of_store_employees'].strip('"'))`: find the current value for the `number_of_store_employees` key, use `.strip('"')` to remove the speech marks, and convert the value to an `int()`.
- `updated_data.append(updated_item)`: the new dictionary item is appended to our updated_data list.

By the end of the for loop we have an `updated_data` list containing our dictionaries, but with the `number_of_store_employees` value transformed to an integer. This object is then returned.

```py
def reformat_visit_date(data):
    ...
    updated_data = []
    for item in data:
        updated_item = item.copy()
        input_format_string = '%d/%m/%Y'
        dt = datetime.strptime(updated_item['visit_date'], input_format_string)
        new_datetime = dt.strftime('%Y-%m-%d')
        updated_item['visit_date'] = new_datetime
        updated_data.append(updated_item)
    ...
    return updated_data
```

The last function in our `etl.py` file utilises the datetime library we imported at the top to reformat the `visit_date` value from "DD/MM/YYYY" to "YYYY-MM-DD", likely to ensure formatting is consistent with other data sources for easier comparative analysis.

This function is identical to the previous one up to `updated_item = item.copy()`, so we'll start on the next line.

- `input_format_string = '%d/%m/%Y'`: this string uses datetime format codes to define the original date format
- `dt = datetime.strptime(updated_item['visit_date'], input_format_string)`: we'll break this down a little further, but first note that in our dictionaries, the value for `visit_date` is currently a string.
  - `dt = `: make an object called `dt`, it's value is...
  - `datetime.strptime()`: uses the `strptime` (string parse time) function from the datetime library to create a datetime object. strptime requires two parameters, the original value, and a format string.
  - `updated_item['visit_date']`: retrieves the original value for the key `visit_date` from the current `updated_item` dictionary.
  - `input_format_string`: we declared this in the previous step, it contains the format codes which instruct `strptime` what the current date format is, i.e. tells it which value is day/month/year.

  Remember, this new datetime object is assigned to the `dt` object.
- `new_datetime = dt.strftime('%Y-%m-%d')`: use the `strftime()` (string format time) function against the current `dt` object, to remake it in the specified format `'%Y-%m-%d'`

---

A few datetime format code examples:

|code|meaning|
|---|---|
|`%d`|numerical day of the month (0-31)|
|`%a`|short weekday name (Sun, Mon, Tue...)|
|`%b`|short month name (Jan, Feb, Mar...)|
|`%m`|numerical month of the year (0-12)|
|`%y`|year 2-digit|
|`%Y`|year 4-digit|

---

- `updated_item['visit_date'] = new_datetime`: assign `new_datetime` object, as the value for the key `visit_date`, in the dictionary `updated_item`.
- `updated_data.append(updated_item)`: the new dictionary is appended to our `updated_data` list.

---

Review our structure:

```text
[src]
  |-[utils]
  |    |- db_utils.py
  |    |- s3_utils.py
  |    |- sql_utils.py
  |- etl.py # DONE
  |- mystery_shop_etl_lambda.py # DONE
```

At this point we know:

- How our deployment and ETL CloudFormation stacks have been created and are deployed.
- How our lambda function works
- How the data is extracted from the csv
- How the data is transformed:
  1. Personal data is removed
  1. number_of_store_employees is changed to integers
  1. The visit_date has been formatted correctly

We still have to unpack our utils directory, but we'll do that in a different file to keep things organised.

[Utils Breakdown](./python-utils-breakdown.md)