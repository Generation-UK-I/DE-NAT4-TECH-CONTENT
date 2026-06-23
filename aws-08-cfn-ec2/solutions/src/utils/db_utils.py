# This file exists to separate the direct use of psycopg2 from functions that only
# care about the Connection and Cursor - this makes those easier to unit test.

import psycopg2 as psy
import boto3
import logging
import json

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

ssm_client = boto3.client('ssm')


# Get the SSM Param from AWS and turn it into JSON
# Don't log the password!
def get_ssm_param(param_name):
    LOGGER.info(f'get_ssm_param: getting param_name={param_name}')
    parameter_details = ssm_client.get_parameter(Name=param_name)
    redshift_details = json.loads(parameter_details['Parameter']['Value'])

    host = redshift_details['host']
    user = redshift_details['user']
    db = redshift_details['database-name']
    LOGGER.info(f'get_ssm_param: loaded for db={db}, user={user}, host={host}')
    return redshift_details


# Use the redshift details json to connect
def open_sql_database_connection_and_cursor(redshift_details):
    try:
        LOGGER.info('open_sql_database_connection_and_cursor: opening connection...')
        db_connection = psy.connect(
            host=redshift_details['host'],
            database=redshift_details['database-name'],
            user=redshift_details['user'],
            password=redshift_details['password'],
            port=redshift_details['port'],
        )
        cursor = db_connection.cursor()
        LOGGER.info('open_sql_database_connection_and_cursor: connection ready')
        return db_connection, cursor
    except ConnectionError as ex:
        LOGGER.info(f'open_sql_database_connection_and_cursor: failed to open connection: {ex}')
        raise ex
