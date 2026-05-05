import csv
from datetime import datetime
from sql_utils import setup_db_connection, insert_students

def read_csv_to_list(filename):
    print(f'read_csv_to_list: opening {filename}...')
    with open(filename, newline='') as file:
        return list(csv.DictReader(file, delimiter=','))


def convert_all_dates(list_of_dicts, date_cols,
                      current_format='%d/%m/%Y',
                      expected_format='%Y-%m-%d'):
    print(f'convert_all_dates...')
    # Uniformity
    for dict in list_of_dicts:
        for col in date_cols:
            try:
                str_to_date = datetime.strptime(dict[col], current_format)
                date_to_str = datetime.strftime(str_to_date, expected_format)
                dict[col] = date_to_str
            except ValueError as e:
                print(f"convert_all_dates: Error parsing value '{dict[col]}' in column '{col}': {e}")
                dict[col] = None

    return list_of_dicts


def check_integer_columns(list_of_dicts, int_cols):
    print(f'check_integer_columns...')
    # Validity
    for dict in list_of_dicts:
        for col in int_cols:
            try:
                dict[col] = int(dict[col])
            except ValueError as e:
                print(f"check_integer_columns: Error parsing value '{dict[col]}' in column '{col}': {e}")
                dict[col] = None
    return list_of_dicts


def check_values_in_valid_list(list_of_dicts, valid_items, col_name):
    print(f'check_values_in_valid_list...')
    # Validity
    for dict in list_of_dicts:
        if dict[col_name] in valid_items:
            continue
        else:
            dict[col_name] = None
    return list_of_dicts


def drop_duplicate_ids(list_of_dicts):
    print(f'drop_duplicate_ids...')
    # Validity
    id_list = []
    list_with_unique_ids = []
    for dict in list_of_dicts:
        if dict['id'] not in id_list:
            id_list.append(dict['id'])
            list_with_unique_ids.append(dict)
    return list_with_unique_ids


def drop_rows_with_null(list_of_dicts):
    print(f'drop_rows_with_null...')
    # Validity / Completeness
    list_with_no_nulls = []
    for dict in list_of_dicts:
        if None not in dict.values() and '' not in dict.values():
            list_with_no_nulls.append(dict)
    return list_with_no_nulls


if __name__ == '__main__':

    data_list = read_csv_to_list('messy-data.csv')

    data_list = convert_all_dates(data_list, ['start_date'])
    data_list = check_integer_columns(data_list, ['id', 'age'])

    teacher_list = ['Mrs. X', 'Ms. Smith', 'Mr. G']
    data_list = check_values_in_valid_list(data_list, teacher_list, 'teacher')

    data_list = drop_duplicate_ids(data_list)
    data_list = drop_rows_with_null(data_list)

    connection, cursor = setup_db_connection()
    insert_students(connection, cursor, data_list)

    cursor.close()
    connection.close()
