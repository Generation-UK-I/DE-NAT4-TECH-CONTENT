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
from datetime import datetime
import pprint
from sql_utils import *

pp = pprint.PrettyPrinter(indent=2)
customer_spend = {}
customer_sales = {}
sales_data = []
sales_data_filtered = []
date1 = datetime.strptime('2020-12-01', '%Y-%m-%d')
date2 = datetime.strptime('2020-12-05', '%Y-%m-%d')
file_name = 'sales_data.csv'

def extract_and_clean_sales_data():
    try:
        print(f'extract_and_clean_sales_data: Loading file {file_name}...')
        with open(file_name, 'r') as file:
            source_file = csv.DictReader(file, fieldnames=['customer_id', 'purchase_date', 'purchase_amount', 'product_id'], delimiter=',')
            next(source_file) #ignore the header row

            for row in source_file:
                if '' not in row.values(): # do not add record if data is missing
                    date = datetime.strptime(row['purchase_date'], '%Y-%m-%d')
                    if date1 <= date <= date2:
                        sales_data_filtered.append(row)
                        if row['customer_id'] not in customer_spend: # add new customer to customer_spend
                            customer_spend[row['customer_id']] = { 'avg_spend': 0, 'total_spend': 0, 'no_of_purchases': 0 }

                        if row['customer_id'] not in customer_sales: # add new customer to customer_sales
                            customer_sales[row['customer_id']] = { 'products': { } }

                    sales_data.append(row)

        print(f'extract_and_clean_sales_data: Loaded {len(sales_data)} rows from file {file_name}.')

    except Exception as error:
        print("An error occurred: " + str(error))
    return sales_data

# get avg and total spend for each customer
def calculate_customer_spend():
    print('calculate_customer_spend: starting...')
    for customer_id, spend_data in customer_spend.items():
        for sale in sales_data_filtered:
            if customer_id == sale['customer_id']:
                spend_data['total_spend'] += float(sale['purchase_amount'])
                spend_data['no_of_purchases'] += 1

        spend_data['total_spend'] = round(spend_data['total_spend'], 2) # round total spend to 2 decimal places
        avg_spend = spend_data['total_spend'] / spend_data['no_of_purchases']
        spend_data['avg_spend'] = round(avg_spend, 2)

    print(f'calculate_customer_spend: calculated {len(spend_data)} rows')

# get number of purchases per product for each customer
def calculate_customer_sales():
    print(f'calculate_customer_sales: starting...')
    for customer_id, product_data in customer_sales.items():
        for sale in sales_data_filtered:
            if customer_id == sale['customer_id']:
                if sale['product_id'] not in product_data['products']:
                    product_data['products'][sale['product_id']] = 1
                else:
                    product_data['products'][sale['product_id']] += 1

    print(f'calculate_customer_sales: calculated {len(product_data)} rows')

def insert_sales_data(conn, cursor):
    print('insert_sales_data: starting...')
    sql = \
        '''
            INSERT INTO sales_data (customer_id, purchase_date, purchase_amount, product_id)
            VALUES (%s, DATE(%s), %s, %s)
        '''

    for sale in sales_data:
        cursor.execute(sql, (int(sale['customer_id']), sale['purchase_date'], float(sale['purchase_amount']), sale['product_id']))

    conn.commit()
    print('insert_sales_data: ...done')

def insert_customer_spend(conn, cursor):
    print('insert_customer_spend: starting...')
    sql = \
        '''
            INSERT INTO customer_spend (customer_id, average_spend, total_spend)
            VALUES (%s, %s, %s)
        '''

    for customer_id, spend_data in customer_spend.items():
        cursor.execute(sql, (customer_id, spend_data['avg_spend'], spend_data['total_spend']))

    conn.commit()
    print('insert_customer_spend: ...done')

def insert_customer_sales(conn, cursor):
    print('insert_customer_sales: starting...')
    sql = \
        '''
            INSERT INTO customer_products (customer_id, product_id, quantity)
            VALUES (%s, %s, %s)
        '''

    for customer_id, products in customer_sales.items():
        for product_data in products.values():
            for product_id, quantity in product_data.items():
                cursor.execute(sql, (customer_id, product_id, quantity))

    conn.commit()
    print('insert_customer_sales: ...done')

# Get DB connection
connection, cursor = setup_db_connection()

extract_and_clean_sales_data()
calculate_customer_spend()
calculate_customer_sales()
insert_sales_data(connection, cursor)
insert_customer_spend(connection, cursor)
insert_customer_sales(connection, cursor)
cursor.close()
connection.close()
