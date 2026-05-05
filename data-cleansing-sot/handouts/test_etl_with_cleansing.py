from etl_with_cleansing import check_integer_columns, check_values_in_valid_list, \
                                drop_duplicate_ids, drop_rows_with_null


def test_check_integer_columns():
    dummy_data = [
        {'id': '5', 'animal': 'cat'},
        {'id': 'five', 'animal': 'dog'}
    ]

    expected = [
        {'id': 5, 'animal': 'cat'},
        {'id': None, 'animal': 'dog'}
    ]

    result = check_integer_columns(dummy_data, int_cols=['id'])

    assert result == expected


def test_check_values_in_valid_list():
    dummy_data = [
        {'id': '5', 'animal': 'cat'},
        {'id': 'five', 'animal': 'dog'},
        {'id': '3', 'animal': 'mouse'},
    ]

    expected = [
        {'id': '5', 'animal': 'cat'},
        {'id': 'five', 'animal': 'dog'},
        {'id': '3', 'animal': None}
    ]

    valid_items = ['cat', 'dog']

    result = check_values_in_valid_list(dummy_data, valid_items, col_name='animal')

    assert result == expected


def test_drop_duplicate_ids():
    dummy_data = [
        {'id': '5', 'animal': 'cat'},
        {'id': '6', 'animal': 'dog'},
        {'id': '6', 'animal': 'cat'},
    ]

    expected = [
        {'id': '5', 'animal': 'cat'},
        {'id': '6', 'animal': 'dog'}
    ]

    result = drop_duplicate_ids(dummy_data)

    assert result == expected


def test_drop_rows_with_null():
    dummy_data = [
        {'id': '5', 'animal': 'cat'},
        {'id': '6', 'animal': None},
        {'id': '7', 'animal': 'cat'},
        {'id': '8', 'animal': ''},
    ]

    expected = [
        {'id': '5', 'animal': 'cat'},
        {'id': '7', 'animal': 'cat'}
    ]

    result = drop_rows_with_null(dummy_data)

    assert result == expected
