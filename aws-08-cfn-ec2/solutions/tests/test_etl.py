from src import etl


def test_extract():
    test_data = [
        'StoreID,StoreName,MysteryShopperID,MysteryShopperName,StoreType,NumberOfStoreEmployees,VisitDate,StartTime,EndTime,OverallScore',
        '1487,Leeds,22,Rory Gilmore,Free Standing,"12",13/03/2024,10:05,10:30,3',
        '1456,Edinburgh,48,Lane Kim,Mall,"6",21/03/2024,13:45,15:00,2'
    ]

    extracted = etl.extract(test_data)
    row = extracted[0]

    assert len(extracted) == 2

    assert row['store_id'] == '1487'
    assert row['store_name'] == 'Leeds'
    assert row['mystery_shopper_id'] == '22'
    assert row['mystery_shopper_name'] == 'Rory Gilmore'
    assert row['store_type'] == 'Free Standing'
    assert row['number_of_store_employees'] == '12'
    assert row['visit_date'] == '13/03/2024'
    assert row['start_time'] == '10:05'
    assert row['end_time'] == '10:30'
    assert row['overall_score'] == '3'


def test_remove_sensitive_information():
    test_data = [
        {
            'store_id': '1487',
            'mystery_shopper_id': '22',
            'mystery_shopper_name': 'Rory Gilmore',
        },
        {
            'store_id': '1456',
            'mystery_shopper_id': '48',
            'mystery_shopper_name': 'Lane Kim',
        },
    ]

    cleansed = etl.remove_sensitive_information(test_data)
    mystery_shop = cleansed[0]

    assert len(cleansed) == 2
    assert 'mystery_shopper_name' not in mystery_shop


def test_reformat_number_of_store_employees():
    test_data = [
        {'store_id': '1456', 'number_of_store_employees': '"6"'},
        {'store_id': '1456', 'number_of_store_employees': '"12"'},
    ]

    cleansed = etl.reformat_number_of_store_employees(test_data)

    mystery_shop = cleansed[0]

    assert len(cleansed) == 2
    assert mystery_shop['number_of_store_employees'] == 6


def test_reformat_visit_date():
    test_data = [
        {
            'store_id': '1487',
            'visit_date': '13/03/2024',
        },
        {
            'store_id': '1456',
            'visit_date': '21/03/2024',
        },
    ]

    cleansed = etl.reformat_visit_date(test_data)
    mystery_shop = cleansed[0]

    assert len(cleansed) == 2
    assert mystery_shop['visit_date'] == '2024-03-13'

