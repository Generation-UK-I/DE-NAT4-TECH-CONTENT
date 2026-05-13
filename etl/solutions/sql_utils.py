import psycopg2 as psycopg
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
HOST_NAME = os.environ.get("POSTGRES_HOST")
DATABASE_NAME = os.environ.get("POSTGRES_DB")
USER_NAME = os.environ.get("POSTGRES_USER")
USER_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

def setup_db_connection(host_name=HOST_NAME,
                        database_name=DATABASE_NAME,
                        user_name=USER_NAME,
                        user_password=USER_PASSWORD):

    conn_string = f'host={host_name} dbname={database_name} user={user_name} password={user_password}'
    # Establish a database connection
    connection = psycopg.connect(conn_string)
    cursor = connection.cursor()
    return connection, cursor
