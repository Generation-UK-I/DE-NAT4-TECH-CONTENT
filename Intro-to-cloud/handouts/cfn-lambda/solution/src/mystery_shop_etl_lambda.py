from utils import s3_utils

import etl
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def lambda_handler(event, context):
    LOGGER.info('lambda_handler: starting')
    file_path = 'NOT_SET'  # makes the exception handler compile

    try:
        bucket_name, file_path = s3_utils.get_file_info(event)

        csv_text = s3_utils.load_file(bucket_name, file_path)

        data = etl.extract(csv_text)

        transformed_data = etl.transform(data)
        # One would not normally log the data directly!!
        # ...there could be loads and it could have PID in it!!
        LOGGER.warn(f'lambda_handler: transformed_data={transformed_data}')

        LOGGER.info(f'lambda_handler: done, file={file_path}')

    except Exception as err:
        LOGGER.error(f'lambda_handler: failure: error={err}, file={file_path}')
        raise err
