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
