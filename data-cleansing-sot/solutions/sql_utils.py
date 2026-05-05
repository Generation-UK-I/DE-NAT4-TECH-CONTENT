import psycopg2
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

    print(f'setup_db_connection: connecting to {host_name}:{database_name}...')
    connection = psycopg2.connect(f"""
        host={host_name}
        dbname={database_name}
        user={user_name}
        password={user_password}
        """)
    cursor = connection.cursor()
    return connection, cursor

def insert_students(connection, cursor, student_list):
    # For the table definition see ./db-scripts/01_students_schema.sql
    sql = """
        INSERT INTO students (id, name, age, branch, teacher, start_date, tel)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    print(f'insert_students: inserting {len(student_list)} rows...')

    for student in student_list:
        row = (student['id'], student['name'],
            student['age'], student['branch'],
            student['teacher'], student['start_date'],
            student['tel'])
        cursor.execute(sql, row)

    connection.commit()
    print(f'insert_students: {len(student_list)} rows inserted.')
