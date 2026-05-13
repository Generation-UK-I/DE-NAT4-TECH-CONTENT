## ETL Exercise

The ETL Process will be used to carry out the following exercise in Data Analysis.

We have a set of customer sales data that we want to extract information from.

The full exercise is in three main parts - write Extract code (load a CSV), write Transform code (of the CSV data), and Load (to save the data in Postgres). This is designed to bring together the building-blocks of several previous sessions.

There is also a fourth part to do some analysis of the acquired data.

## Prep

> Important!
>
> Follow the steps in [../handouts/README.md](../handouts/README.md) to get a Postgres container running with the database tables ready in it, and a `venv` ready with your requirements.

## Task

Write a python script that executes the below steps.

Make sure work in the file `solution_start.py` which sets up the database connection.

The SQL of the target tables is in the `handouts/db-scripts/01_sales_schema.sql` file.

### Task 1 - Extract

1. Extract all the data from the `sales_data.csv` file.
    - The columns for the csv are `customer_id`, `purchase_date`, `purchase_amount` and `product_id`.

### Task 2 - Transform

For the transformation you can make SQL queries and run them using the `psycopg` library.

2. Clean that data (minimum requirement is to remove any rows that contain null cells).
3. Filter data for the period 1 December 2020 - 5 December 2020
4. Calculate each customer's total spend
5. Calculate each customer's average spend
6. Calculate how many times each customer has purchased a specific item

### Task 3 - Load

7. Load the results into the database table that is set up by `handouts/db-scripts/01_sales_schema.sql`
    - Have a look at the DB schema file to work out your queries

### Task 4 - Analyse

8. What does the data in the tables tell you about the different customers purchasing habits?
