# ETL Solutions

The target database schema can be seen in file [./db-scripts/01_sales_schema.sql](./db-scripts/01_sales_schema.sql).

### To run the solutions

- First use the database setup scripts for podman/docker in the [../handouts/](../handouts/) folder as per [../handouts/README.md](../handouts/README.md)
- Then
    - open a terminal in hte `solutions` folder
    - run `python3 solution-in-memory.py`
    - or `python3 solution-pure-sel.py`
    - Some users may need to run `python` or `py` instead of `python3` as appropriate

## Solution 1 - transform in memory

File [./solution-in-memory.py](./solution-in-memory.py)

- This solves the exercise by loading the data into memory
- Then in-memory working out the solutions required
- Then saves the data in database tables (`sales_data`, `customer_spend`, and `customer_products`)
- The functions in this file are written in a very "Jupyter Notebooks" style, i.e everything is global variable

## Solution 2 - transform in sql tables

File [./solution-pure-sql.py](./solution-pure-sql.py)

- This file solves the exercise by using a sequence of sql tables
- It first loads the all the data into the `sales_data` table
- Then uses a sequence of `INSERT/SELECT` statements to aggregate into the `customer_spend` and `customer_products` tables

## Data trends that we can see

Notes on the information/insights they should see from the data transformations:

- `2194` - low frequency spends, large amounts, buys the same product each time
- `5632` - medium frequency spends, medium amounts, buys three products
- `7365` - high frequency spends, small amounts, buys a different product each time
