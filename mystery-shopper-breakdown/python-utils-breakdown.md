# ETL Pipeline Utils

First recall the file structure for our ETL pipeline resources:

```text
[app_dir]
    |-[src]
    |   |-[utils]
    |   |    |- db_utils.py
    |   |    |- s3_utils.py
    |   |    |- sql_utils.py
    |   |- etl.py # DONE
    |   |- mystery_shop_etl_lambda.py # DONE
    |- deployment-bucket-stack.yml # DONE
    |- deploy.sh # DONE
    |- etl-stack-packaged.yml # DONE
    |- etl-stack.yml # DONE
    |- requirements-lambda.txt # Libraries to import to Lambda
    |- requirements-test.txt # Libraries to import for testing purposes - outside of our scope.
```

If you haven't been through them already:

- The `deploy.sh` file has been explored in [mystery-shopper-breakdown](./mystery-shopper-breakdown.md)
- The `deployment-bucket-stack.yml` and `etl-stack.yml` have been covered in [CF-templates-breakdown](./CF-templates-breakdown.md)
- `mystery_shop_etl_lambda.py` and `etl.py` are in [python-files-breadown](./python-files-breakdown.md).

You can see that we only have our utils modules to review:

Although there are three separate files, they're quite short, and with a bit of repetition with what we've already covered, or learned previously, so it should be pretty straightforward.

## S3_utils.py

This is a short file, with just two functions:

```py
import boto3
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

s3_client = boto3.client('s3')


def get_file_info(event):
    LOGGER.info('get_file_info: starting')
    first_record = event['Records'][0]
    bucket_name = first_record['s3']['bucket']['name']
    file_name = first_record['s3']['object']['key']

    LOGGER.info(f'get_file_info: file={file_name}, bucket_name={bucket_name}')
    return bucket_name, file_name


def load_file(bucket_name, s3_key):
    LOGGER.info(f'load_file: loading s3_key={s3_key} from bucket_name={bucket_name}')
    response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
    body_text = response['Body'].read().decode('utf-8').split('\n')

    LOGGER.info(f'load_file: done: s3_key={s3_key} result_chars={len(body_text)}')
    return body_text
```

As with previous examples we'll omit the LOGGER statements, as we went through it in the `mystery_shop_etl_lambda.py` file in the [python-files-breakdown](./python-files-breakdown.md) guide, and it works the same way here.

```py
import boto3
...
s3_client = boto3.client('s3')
```

- `import boto3`: Boto3 is the official AWS SDK for Python, i.e. it is a Python library containing functions and methods for interacting with AWS.
  - If using it locally you may need to install boto3 with `pip` before you can import it, because it's not part of the _Python Standard Library_.
- `s3_client = boto3.client('s3')`: boto3 allows you create 'clients', which are interfaces for AWS services. In this case we create an s3 client (called `s3_client`) which we can then use to call s3 APIs.

```py
def get_file_info(event):
    ...
    first_record = event['Records'][0]
    bucket_name = first_record['s3']['bucket']['name']
    file_name = first_record['s3']['object']['key']

    ...
    return bucket_name, file_name
```

When we reviewed the `lambda_handler()` function we saw that an `event` is the data passed to the function when it is triggered. 

Typically this is a JSON object, but lambda returns it as a dictionary, allowing us to use Python dictionary syntax to access the event.

---

Here is an example of an AWS event created when s3 triggers a lambda:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "my-bucket" },
        "object": { "key": "data/file.csv" }
      }
    }
  ]
}
```

Although this is JSON, it's the same as python list and dictionary syntax, so you should be able to follow the logic in the examples below to understand where the values are coming from.

---

- `first_record = event['Records'][0]`: the first key in the dictionary is `"Records"`, it's value is a list `[...]`. The first item in our list (_index[0]_) is the `"s3"` key.

  This `"s3"` key and it's associated dictionary (containing `bucket` and `object` keys and values) are both assigned to the `first_record` object.
- `bucket_name = first_record['s3']['bucket']['name']`: this is simpler than it looks, just follow the keys. In brief, `bucket_name` is the value of a key, that is two keys/dictionaries deep `"s3"` > `"bucket"` > `"name"`
- `file_name = first_record['s3']['object']['key']`: this is the same as the previous statement, except we retrieve the object key (the path and name to a specific object).

```py
return bucket_name, file_name
```

The two values we extracted from the `event` record are returned.

```py
def load_file(bucket_name, s3_key):
    ...
    response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
    body_text = response['Body'].read().decode('utf-8').split('\n')
    ...
    return body_text
```

This function loads the raw csv from the bucket, using the bucket_name and s3_key values returned by the previous function.

>For clarity, the previous function doesn't pass the values through straight through to this one. They're linked by the main `mystery_shop_etl_lambda.py` file, it receives the `bucket_name` and `s3_key` from the first function, then passes them through to this one.

- `response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)`: recall, we created an `s3_client` object at the top of the file, so we use it's `.get_object()` function, taking the `bucket_name` and `s3_key` to load the relevant object into our new `response` object.

  The response object is actually a dictionary containing many different key value pairs, basically containing all of the uploaded files metadata. Most of the data isn't relevant to us at this time, but as examples there are values for _LastModified_, _ContentType_, the most important one for us is __body__ which will contain the actual contents of the file.
- `body_text = response['Body'].read().decode('utf-8').split('\n')`: here we take the contents from the Body key of our response object and do a few things to it:
  - `.read()`: reads the data from the body, as raw bytes
  - `.decode('utf-8')`: converts the raw bytes into strings by encoding them with the `utf-8` standard.
  - `.split('\n')`: Splits the decoded string into a list of lines wherever the newline characters (`/n`) are encountered.

  Data is extracted from the csv and decoded like this "Line1Line2Line3..." and is split into a list like this ["Line1", "Line2", "Line3"...]
- `return body_text`: the `body_text` object, a list of the lines in the csv, is returned.

These are the only two functions in the `s3_utils.py` file, so let's move onto the final two, `sql_utils.py`, and `db_utils.py`.

## Database Utils

We have various functions for interacting with our DB, but they've been separated into two files:

- `sql_utils` contains the functions which just use the database `connection` and `cursor` objects (Review our databases module if you don't know what these are).
- `db_utils` contains functions which use the `psycopg` and `boto3` libraries. This separation allows for easier testing.

### sql_utils.py

```py
# This file exists to separate the direct use of psycopg2 in 'connect_to_db.py'
# from functions here that only care about the Connection and Cursor - this makes these easier to unit test.

import uuid
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def create_db_tables(connection, cursor):
    LOGGER.info('create_db_tables: started')
    try:

        LOGGER.info('create_db_tables: creating mystery_shop_visit table')
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS mystery_shop_visit (
                visit_id VARCHAR(255) PRIMARY KEY,
                store_id INT NOT NULL,
                mystery_shopper_id  INT NOT NULL,
                store_type VARCHAR(50) NOT NULL,
                store_name VARCHAR(50) NOT NULL,
                number_of_store_employees INT NOT NULL,
                visit_date DATE NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                overall_score INT NOT NULL
            );
            '''
        )

        LOGGER.info('create_db_tables: committing')
        connection.commit()

        LOGGER.info('create_db_tables: done')
    except Exception as ex:
        LOGGER.info(f'create_db_tables: failed to run sql: {ex}')
        raise ex

def create_guid():
    return str(uuid.uuid4())
# Use a generated GUID for the db table IDs as this is better in high-concurrency systems

def save_data_in_db(connection, cursor, bucket_name, file_path, data):
    LOGGER.info(f'save_data_in_db: started: file_path={file_path}, rows={len(data)}')

    try:
        columns = ', '.join(data[0].keys())
        columns = 'visit_id, ' + columns
        sql_insert_template = f'INSERT INTO mystery_shop_visit ({columns}) VALUES '

        # do len(data[0] + 1) to get length including visit_id for (%s, ?s ...)
        values_placeholder = ', '.join(['%s'] * (len(data[0]) + 1))

        LOGGER.info(
            f'save_data_in_db: columns={columns}, sql_insert_template={sql_insert_template}, values_placeholder={values_placeholder}'
        )

        for row in data:
            visit_id = create_guid()
            values = list(row.values())
            values.insert(0, visit_id)

            cursor.execute(sql_insert_template + f'({values_placeholder})', values)

        connection.commit()

        LOGGER.info(f'save_data_in_db: done: file_path={file_path}, rows={len(data)}')
    except Exception as ex:
        LOGGER.info(f'save_data_in_db: error: ex={ex}, file_path={file_path}')
        raise ex
```

As always, we'll omit things that are repeating what we've already covered, or learned earlier in our program to make things easier to read.

```py
import uuid
```

This is a module from the Standard Library which generates universally unique identifiers `uuid`s which comply with an international standard format.

```py
def create_db_tables(connection, cursor):
    ...
    try:
        ...
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS mystery_shop_visit (
                visit_id VARCHAR(255) PRIMARY KEY,
                ... # Additional fields omitted
            );
            '''
        )
        ...
        connection.commit()
        ...
    except Exception as ex:
        ...
        raise ex
```

Once it's been trimmed down, this function should be quite familiar, you've used very similar examples several times.

- `cursor.execute('''CREATE TABLE IF NOT EXISTS...);`: notice connection and cursor objects are passed through when calling the function (_they're created by a function in db_utils_), so we use the `cursor.execute()` function to enter our SQL statements, and `connection.commit()` to save our changes.

  Notice our cursor and connection are within a try-except block to ensure it fails closed.

```py
def create_guid():
    return str(uuid.uuid4())
```

This little function simply returns a UUID, it will be called later when such a value is required.

```py
def save_data_in_db(connection, cursor, bucket_name, file_path, data):
    try:
        columns = ', '.join(data[0].keys())
        columns = 'visit_id, ' + columns
        sql_insert_template = f'INSERT INTO mystery_shop_visit ({columns}) VALUES '

        # do len(data[0] + 1) to get length including visit_id for (%s, ?s ...)
        values_placeholder = ', '.join(['%s'] * (len(data[0]) + 1))

        for row in data:
            visit_id = create_guid()
            values = list(row.values())
            values.insert(0, visit_id)

            cursor.execute(sql_insert_template + f'({values_placeholder})', values)

        connection.commit()

    except Exception as ex:
        raise ex
```

As you may guess from the function name, this is the L part of ETL, so it's important, and a bit tricky.

First look at the function definition and notice all of the parameters

```py
def save_data_in_db(connection, cursor, bucket_name, file_path, data):
```

We have our `connection` and `cursor` objects, the `bucket_name` and `file_path` to the object in s3, and the data from the file, which by this point has been cleaned by passing through all of the transform functions.

