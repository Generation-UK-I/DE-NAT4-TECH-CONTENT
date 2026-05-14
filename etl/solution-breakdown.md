# Solution Breakdown

There are numerous different approaches to this challenge, you may have discovered different libraries, necessitating different methods, but broadly the logic should be the same.

The solution is broken down piece by piece below, and the whole app is combined at the end.

## Configure Environment

```py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

host_name = os.environ.get("POSTGRES_HOST")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")
```

Hopefully this part is familiar by now:

- `import...`: the `psycopg2` and `os` libraries, and just the `load_dotenv` function from the `dotenv` library are all imported for use within our code.
- `load_dotenv()`: the function we just imported, this will export the variables contained in the .env file into the system's environment variables.
- `...os.environ.get...`: our DB connection details are in the `.env` file and exported as environment variables by `load_env()`, this line then calls those environment variables, and assigns them to new variables for use in our code `host_name`, `database_name`, etc.

### Setup the Connection to DB

```py
try:
    ### SETUP THE DATABASE CONNECTION
    print('Opening connection...')
    conn_string = f'host={host_name} dbname={database_name} user={user_name} password={user_password}'

    with psycopg2.connect(conn_string) as connection:

        print('Opening cursor...')
        cursor = connection.cursor()
```

For this example ETL job most of the application code is contained within a try-except block; this isn't best practice, but works for now, it means that the connection is opened with a context, and will always be closed if the code fails.

- `try`: opens the try-except block
- `conn_string = ...`: builds an f-string by concatenating the required variables
- `with psycopg2.connect...`: uses the psycopg2.connect() method to create a connection object, using the credentials in the conn_string variable; with opens the connection with a context, i.e. it is only open within the try-except block, and immediately closes if the code fails.
- `cursor = connection.cursor()`: The connection object has access to psycopg2's connection methods, in this case, we create a cursor object which opens a cursor against our Postgres DB, allowing us to enter our SQL commands.

---

### Create Tables

```py
cursor.execute("""
        CREATE TEMP TABLE staging_sales (
            customer_id text,
            purchase_date text,
            purchase_amount text,
            product_id text
        );

... # omitted code

        CREATE TABLE IF NOT EXISTS customer_products (
            customer_id int NOT NULL,
            product_id varchar(10),
            quantity int
        );
    """)
```

There are different approaches to completing this task, in this case, we're going to use a temporary SQL table, often called a **staging table**, to hold the data prior to transformation, then export it into our permanent table.

- `cursor.execute()`: opens the execute() method with our cursor object, enabling us to enter the necessary SQL statements to manage the DB
- `CREATE TEMP TABLE`: a temporary table is used to store data which is only required temporarily, typically during data transformations, to ensure the primary tables are not affected. It is automatically automatically deleted when a transaction or session is ended.

One final point - with this statement we created all of our required tables first, with one statement. For this reason it is important to plan your solution in advance.

## Extract

```py
with open('sales_data.csv', 'r') as f:
        next(f)  # Skip header
        cursor.copy_from(f, 'staging_sales', sep=',', null='')
```

We've used code similar to this a few times, particularly in our data persistence module, so it should be familiar, with just one new point...

- `with open('sales_data.csv', 'r') as f:`: opens the file in read only, aliased as f; With ensures the file will be closed again once done.
- `cursor.copy_from(f, 'staging_sales', sep=',', null='')`: use the cursor object's `.copy_from()` method to extract the data directly from the CSV into the **staging_sales** table we created above.
  - The syntax of copy_from is: `copy_from(source_file, target_table, seperator_character, null_character)`
    - more arguments are available
  - In this case our file's data is in `f`, our target table is `staging_sales`, the separator between different values is `','` and null values are an empty string `''`

---

```py
    cursor.execute("""
        DELETE FROM staging_sales 
        WHERE customer_id IS NULL 
        OR customer_id = ''
        OR purchase_amount IS NULL 
        OR purchase_amount = '';
    """)
```

## Transform

Our first transformatio is to again use the cursor object's `execute()` method to run a SQL statement, in this case to meet the requirement of deleting records with `NULL` values. This is done against the data in the staging table, we'll prepare it before committing to the permanent table(s), so it only contains cleaned and transformed data.

```py
    # 3. Filter data for the period 1 December 2020 - 5 December 2020
    cursor.execute("""
        DELETE FROM staging_sales 
        WHERE TO_DATE(purchase_date, 'YYYY-MM-DD') 
            NOT BETWEEN '2020-12-01' AND '2020-12-05';
    """)
```

Our requirements are to only extract records between the specified dates. To handle date values correctly in SQL we can use `TO_DATE`, we provide it with the field containing date values, and the format of the values ie. `YYYY-MM-DD`. Our command deletes all values that fall outside of the date range we're interested in.

>`TO_DATE` will only provide the correct output if the date values have been formatted consistently during data cleansing.

## Load

>Note: There can technically be a bit of overlap, in this case some of our transformations are being done during the load phase.

```py
# 7. Load the transformed data to the created tables
cursor.execute("""
        INSERT INTO sales_data (customer_id, purchase_date, purchase_amount, product_id)
        SELECT 
            customer_id::int,
            TO_DATE(purchase_date, 'YYYY-MM-DD'),
            purchase_amount::decimal(19,2),
            NULLIF(product_id, '')
        FROM staging_sales
        WHERE product_id IS NOT NULL AND product_id != '';
    """)
```

This code has some familiar commands, but it's getting a bit complicated, because we're doing a few things at once, for a start we're both `INSERT`ing and `SELECT`ing

- `INSERT INTO...`: defines our target table and fields
- `SELECT...`: we select the data from one table (**staging_sales**) that we want to insert into the other (**sales_data**)
  - `customer_id::int,`: Selects the `customer_id` field from **staging_sales**, but converts the values to integers - which matches the data type we defined when creating the **sales_data** table.
  - `TO_DATE(purchase_date, 'YYYY-MM-DD'),`: We select the `purchase_date` field, but the `TO_DATE` function again converts the values to the SQL **date** data type, and in the specified format.
  - `purchase_amount::decimal(19,2)`: Converts the `purchase_amount` values into fixed‑precision decimals (19 digits, 2 after the decimal).
  - `NULLIF(product_id, '')`: Turns empty strings into NULL. Perhaps unnecessary since we already dropped nulls, but this prevents inserting meaningless empty values.

---

```py
# 4. Calculate each customer's total spend
# 5. Calculate each customer's average spend
cursor.execute("""
        INSERT INTO customer_spend (customer_id, average_spend, total_spend)
        SELECT 
            customer_id,
            ROUND(AVG(purchase_amount), 2) as average_spend,
            ROUND(SUM(purchase_amount), 2) as total_spend
        FROM sales_data
        GROUP BY customer_id
        ORDER BY customer_id;
    """)
```

Again, we've just got an `INSERT` statement which will populate the `customer_spend` table, and a `SELECT` statement extracting records from `sales_data`, but the `SELECT` is doing some extra stuff.

The logic of SELECT is sometimes hard to follow. In this case:

1. The records in the sales_data table are grouped by `customer_id`, so all records for each unique `customer_id` will be grouped, then ordered by `customer_id`
2. We utilise SQL's built in mathematical functions to apply the necessary calculations to generate the new data
   - `ROUND(AVG(purchase_amount), 2) as average_spend`: since sales_data was grouped by customer, this line will calculate the average spend for each customer, and round it to 2 decimal places. The calculated values are aliased as `average_spend` to match the target field in the `customer_spend` table
   - `ROUND(SUM(purchase_amount), 2) as total_spend`: Same as above, but it calculates each customer's total purchases, and aliases it as `total_spend`
3. Once all of the new data has been calculated, and aliased, SQL goes back to the beginning of the statement to INSERT the data into the equivalently named fields.

---

```py
# 6. Calculate how many times each customer has purchased a specific item
cursor.execute("""
    INSERT INTO customer_products (customer_id, product_id, quantity)
    SELECT 
        customer_id,
        product_id,
        COUNT(*) as quantity
    FROM sales_data
    WHERE product_id IS NOT NULL
    GROUP BY customer_id, product_id
    ORDER BY customer_id, product_id;
""")
```

Once again we're INSERTing and SELECTing, this time from the `sales_data` table and into `customer_products`.

- The records in the `sales_data` table in which the `product_id` field is not **null** are selected
- `GROUP BY...`: Groups the rows by each unique combination of `customer_id` and `product_id`
- `customer_id` and `product_id` are selected, along with `COUNT(*)` which returns the number of rows in each group, aliased as `quantity`.
- `customer_id`, `product_id`, and `quantity` are all inserted into the target table.

---

```py
    connection.commit()

    print('Closing cursor...')
    # Closes the cursor so will be unusable from this point
    cursor.close()
    
    print('Closing connection...')
    
    # The connection will automatically close here 
except Exception as ex:
    print('Failed to:', ex)

# Leave this line here!
print('All done!')
```

This last section just cleans up.

- `connection.commit()`: Commits our changes to the database so that they persist
- `cursor.close()`: Closes our cursor object
- `except Exception as ex:`: closes our try-except block, which will close our connection once everything has finished, or if the code fails at any earlier time. If it fails any info about the exceptions will be printed out.

Remember, the temporary table will be deleted automatically when we close our session - we didn't need to drop it.

---

The final code is below.

```py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

host_name = os.environ.get("POSTGRES_HOST")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")

try:
    ### SETUP THE DATABASE CONNECTION
    print('Opening connection...')
    conn_string = f'host={host_name} dbname={database_name} user={user_name} password={user_password}'
    # Establish a database connection
    with psycopg2.connect(conn_string) as connection:

        print('Opening cursor...')
        cursor = connection.cursor()

    # Create tables including staging_table 
    cursor.execute("""
        CREATE TEMP TABLE staging_sales (
            customer_id text,
            purchase_date text,
            purchase_amount text,
            product_id text
        );
        
        CREATE TABLE IF NOT EXISTS sales_data (
            customer_id int NOT NULL,
            purchase_date date,
            purchase_amount decimal(19,2),
            product_id varchar(10)
        );

        CREATE TABLE IF NOT EXISTS customer_spend (
            customer_id int NOT NULL,
            average_spend decimal(19,2),
            total_spend decimal(19,2)
        );

        CREATE TABLE IF NOT EXISTS customer_products (
            customer_id int NOT NULL,
            product_id varchar(10),
            quantity int
        );
    """)
    
    ### Task 1.1 - EXTRACT
    # 1. Read the sales_data.csv 
    # Load CSV into staging
    with open('sales_data.csv', 'r') as f:
        next(f)  # Skip header
        cursor.copy_from(f, 'staging_sales', sep=',', null='')
    
    # 2. Clean that data
    cursor.execute("""
        DELETE FROM staging_sales 
        WHERE customer_id IS NULL 
        OR customer_id = ''
        OR purchase_amount IS NULL 
        OR purchase_amount = '';
    """)
    
    # 3. Filter data for the period 1 December 2020 - 5 December 2020
    cursor.execute("""
        DELETE FROM staging_sales 
        WHERE TO_DATE(purchase_date, 'YYYY-MM-DD') 
            NOT BETWEEN '2020-12-01' AND '2020-12-05';
    """)

    # 7. Load the transformed data to the created tables
    cursor.execute("""
        INSERT INTO sales_data (customer_id, purchase_date, purchase_amount, product_id)
        SELECT 
            customer_id::int,
            TO_DATE(purchase_date, 'YYYY-MM-DD'),
            purchase_amount::decimal(19,2),
            NULLIF(product_id, '')
        FROM staging_sales
        WHERE product_id IS NOT NULL AND product_id != '';
    """)

    # 4. Calculate each customer's total spend
    # 5. Calculate each customer's average spend
    cursor.execute("""
        INSERT INTO customer_spend (customer_id, average_spend, total_spend)
        SELECT 
            customer_id,
            ROUND(AVG(purchase_amount), 2) as average_spend,
            ROUND(SUM(purchase_amount), 2) as total_spend
        FROM sales_data
        GROUP BY customer_id
        ORDER BY customer_id;
    """)
    
    # 6. Calculate how many times each customer has purchased a specific item
    cursor.execute("""
        INSERT INTO customer_products (customer_id, product_id, quantity)
        SELECT 
            customer_id,
            product_id,
            COUNT(*) as quantity
        FROM sales_data
        WHERE product_id IS NOT NULL
        GROUP BY customer_id, product_id
        ORDER BY customer_id, product_id;
    """)

    connection.commit()

    print('Closing cursor...')
    # Closes the cursor so will be unusable from this point
    cursor.close()
    
    print('Closing connection...')
    
    # The connection will automatically close here 
except Exception as ex:
    print('Failed to:', ex)

# Leave this line here!
print('All done!')
```
