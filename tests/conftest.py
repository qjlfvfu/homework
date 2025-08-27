import pytest
from datetime import datetime
from typing import List, Dict, Any, Tuple
# ФИКСТУРЫ

@pytest.fixture
def valid_date_formats() -> List[Tuple[str, str]]:
    """Фикстура с валидными датами разных форматов"""
    return [
        # (input_date, expected_output)
        ('2023-12-31', '31.12.2023'),
        ('2023-12-31T23:59:59.999', '31.12.2023'),
        ('2023-12-31T14:30:45', '31.12.2023'),
        ('1970-01-01', '01.01.1970'),
        ('2024-02-29T12:00:00.000', '29.02.2024'),  # Високосный год
        ('1999-12-31T00:00:00.000', '31.12.1999')
    ]

@pytest.fixture
def edge_case_dates() -> List[Tuple[str, str]]:
    """Фикстура с пограничными случаями дат"""
    return [
        ('2000-01-01T00:00:00.000', '01.01.2000'),  # Начало тысячелетия
        ('2100-12-31T23:59:59.999', '31.12.2100'),  # Будущая дата
        ('1900-01-01T12:30:45.123', '01.01.1900')   # Историческая дата
    ]

@pytest.fixture
def invalid_dates() -> List[str]:
    """Фикстура с невалидными датами"""
    return [
        'invalid-date-format',
        '2023-13-45',  # Несуществующая дата
        '2023/12/31',  # Неправильный разделитель
        '31.12.2023',  # Уже в целевом формате
        '2023-12-31T25:61:61.999',  # Неверное время
        '',
        '12345'
    ]

@pytest.fixture
def datetime_formats() -> List[Tuple[str, str]]:
    """Фикстура с разными форматами datetime"""
    return [
        ('2023-01-15T14:30:00.123456', '15.01.2023'),  # Микросекунды
        ('2023-01-15T14:30:00.123', '15.01.2023'),     # Миллисекунды
        ('2023-01-15T14:30:00', '15.01.2023'),         # Без миллисекунд
        ('2023-01-15', '15.01.2023')                   # Только дата
    ]
@pytest.fixture
def test_operations():
    """Фикстура с тестовыми данными операций"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01', 'amount': 100, 'description': 'Payment 1'},
        {'id': 2, 'state': 'PENDING', 'date': '2023-01-02', 'amount': 200, 'description': 'Payment 2'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-01-03', 'amount': 300, 'description': 'Payment 3'},
        {'id': 4, 'state': 'CANCELED', 'date': '2023-01-04', 'amount': 400, 'description': 'Payment 4'},
        {'id': 5, 'state': 'EXECUTED', 'date': '2023-01-05', 'amount': 500, 'description': 'Payment 5'}
    ]

@pytest.fixture
def operations_without_state():
    """Фикстура с операциями без поля state"""
    return [
        {'id': 1, 'date': '2023-01-01', 'amount': 100},
        {'id': 2, 'state': 'EXECUTED', 'date': '2023-01-02', 'amount': 200},
        {'id': 3, 'date': '2023-01-03', 'amount': 300}
    ]


@pytest.fixture
def operations_with_case():
    """Фикстура с операциями с разным регистром"""
    return [
        {'id': 1, 'state': 'executed', 'amount': 100},
        {'id': 2, 'state': 'EXECUTED', 'amount': 200},
        {'id': 3, 'state': 'Executed', 'amount': 300}
    ]

@pytest.mark.parametrize('state, expected_ids', [
    ('EXECUTED', [1, 3, 5]),
    ('PENDING', [2]),
    ('CANCELED', [4]),
    ('UNKNOWN', []),
    ('', []),
])

@pytest.fixture
def valid_dates():
    """Фикстура с валидными датами"""
    return [
        ('2023-12-31', '31.12.2023'),
        ('2023-12-31T23:59:59.999', '31.12.2023'),
        ('1970-01-01', '01.01.1970')
    ]

@pytest.fixture
def test_operations():
    """Фикстура с тестовыми операциями"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01', 'amount': 100},
        {'id': 2, 'state': 'PENDING', 'date': '2023-01-02', 'amount': 200},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-01-03', 'amount': 300}
    ]

@pytest.fixture
def account_data():
    """Фикстура с данными счетов"""
    return [
        'Счет 1234567890123456',
        'Счет 9876543210987654',
        'Visa 1234567812345678'
    ]