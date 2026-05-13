############################################################
#
# ETL example start
#
############################################################

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
host_name = os.environ.get("POSTGRES_HOST")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")

try:

    ### Task 1.1 - EXTRACT

    # 1. Read the sales_data.csv
    # TODO - put code here to load the file

    ### Task 1.2 - TRANSFORM

    # TODO - put code here for the steps below
    # 2. Clean that data (minimum requirement is to remove any rows that contain null cells).

    # Optional / Stretch goals
    # 3. Filter data for the period 1 December 2020 - 5 December 2020
    # 4. Calculate each customer's total spend
    # 5. Calculate each customer's average spend
    # 6. Calculate how many times each customer has purchased a specific item


    ### SETUP THE DATABASE CONNECTION
    print('Opening connection...')
    conn_string = f'host={host_name} dbname={database_name} user={user_name} password={user_password}'
    # Establish a database connection
    with psycopg2.connect(conn_string) as connection:

        print('Opening cursor...')
        cursor = connection.cursor()

        ### Task 1.3 - LOAD
        # 7. Load the transformed data to the created tables
        # TODO - put code here to insert into the tables

        print('Closing cursor...')
        # Closes the cursor so will be unusable from this point
        cursor.close()

        # The connection will automatically close here
except Exception as ex:
    print('Failed to:', ex)

# Leave this line here!
print('All done!')
