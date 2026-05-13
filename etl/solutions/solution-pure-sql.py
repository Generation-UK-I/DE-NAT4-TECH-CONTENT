#########################
#
# See the README.md file!
#
#########################

# Notes on the information/insights they should see from the data transformations:
# 2194 - low frequency spends, large amounts, buys the same product each time
# 5632 - medium frequency spends, medium amounts, buys three products
# 7365 - high frequency spends, small amounts, buys a different product each time

import csv
from sql_utils import *
file_name = 'sales_data.csv'

def extract_and_clean_sales_data():
    print(f'extract_and_clean_sales_data: loading {file_name} ...')
    sales_data = []

    try:
        with open(file_name, 'r') as file:
            source_file = csv.DictReader(file, fieldnames=['customer_id', 'purchase_date', 'purchase_amount', 'product_id'], delimiter=',')
            next(source_file) # ignore the header row
            for row in source_file:
                if '' not in row.values():
                    sales_data.append(row)
    except Exception as error:
        print("An error occurred: " + str(error))

    print(f'extract_and_clean_sales_data: loaded {len(sales_data)} rows')
    return sales_data

def insert_sales_data(cleaned_sales_data, cursor, connection):
    print(f'insert_sales_data: starting...')

    data_row_insert_sql = """
        INSERT INTO
        sales_data(customer_id, purchase_date, purchase_amount, product_id)
        VALUES(%s, %s, %s, %s)
    """
    for data_row in cleaned_sales_data:
        cursor.execute(data_row_insert_sql,
                    (data_row['customer_id'], data_row['purchase_date'], data_row['purchase_amount'], data_row['product_id']))

    connection.commit()
    print(f'insert_sales_data: ...done')

def calculate_customer_spend(cursor, connection):
    print(f'calculate_customer_spend: starting...')

    customer_spend_sql = """
        INSERT INTO customer_spend
        SELECT customer_id, AVG(purchase_amount), SUM(purchase_amount)
        FROM sales_data
        WHERE purchase_date between '2020-12-01' and '2020-12-05'
        GROUP BY customer_id
    """
    cursor.execute(customer_spend_sql)
    connection.commit()
    print(f'calculate_customer_spend: ...done')

def calculate_product_quantities(cursor, connection):
    print(f'calculate_product_quantities: starting...')

    customer_product_sql = """
        INSERT INTO customer_products
        SELECT customer_id, product_id, count(*)
        FROM sales_data
        WHERE purchase_date between '2020-12-01' and '2020-12-05'
        GROUP BY customer_id, product_id
        ORDER BY customer_id
    """
    cursor.execute(customer_product_sql)
    connection.commit()
    print(f'calculate_product_quantities: ...done')

# Get DB connection
conn, curr = setup_db_connection()

# Extract and clean the data
cleaned_sales_data = extract_and_clean_sales_data()

# Load the cleaned raw data
insert_sales_data(cleaned_sales_data, curr, conn)

# Get the spend values
calculate_customer_spend(curr, conn)

# Get the product quantity values
calculate_product_quantities(curr, conn)

# Tidy up
curr.close()
conn.close()
