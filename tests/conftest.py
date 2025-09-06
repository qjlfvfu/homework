from typing import Any, Dict, List, Tuple

import pytest


@pytest.fixture
def valid_date_formats() -> List[Tuple[str, str]]:
    """Фикстура с валидными датами разных форматов"""
    return [
        ("2023-12-31", "31.12.2023"),
        ("2023-12-31T23:59:59.999", "31.12.2023"),
        ("2023-12-31T14:30:45", "31.12.2023"),
        ("1970-01-01", "01.01.1970"),
        ("2024-02-29T12:00:00.000", "29.02.2024"),
    ]


@pytest.fixture
def edge_case_dates() -> List[Tuple[str, str]]:
    """Фикстура с пограничными случаями дат"""
    return [
        ("2000-01-01T00:00:00.000", "01.01.2000"),
        ("2100-12-31T23:59:59.999", "31.12.2100"),
        ("1900-01-01T12:30:45.123", "01.01.1900"),
    ]


@pytest.fixture
def invalid_dates() -> List[str]:
    """Фикстура с невалидными датами"""
    return ["invalid-date-format", "2023-13-45", "2023/12/31", "31.12.2023", "2023-12-31T25:61:61.999", "", "12345"]


@pytest.fixture
def datetime_formats() -> List[Tuple[str, str]]:
    """Фикстура с разными форматами datetime"""
    return [
        ("2023-01-15T14:30:00.123456", "15.01.2023"),
        ("2023-01-15T14:30:00.123", "15.01.2023"),
        ("2023-01-15T14:30:00", "15.01.2023"),
        ("2023-01-15", "15.01.2023"),
    ]


@pytest.fixture
def test_operations() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми операциями"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "amount": 100},
        {"id": 2, "state": "PENDING", "date": "2023-01-02", "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03", "amount": 300},
        {"id": 4, "state": "CANCELED", "date": "2023-01-04", "amount": 400},
    ]


@pytest.fixture
def account_data() -> List[str]:
    """Фикстура с данными счетов"""
    return ["Счет 1234567890123456", "Счет 9876543210987654", "Visa 1234567812345678"]

@pytest.fixture
def transaction()->List[Dict[str,Any]]:
    transactions = [
        [
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702"
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188"
            },
            {
                "id": 873106923,
                "state": "EXECUTED",
                "date": "2019-03-23T01:09:46.296404",
                "operationAmount": {
                    "amount": "43318.34",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 44812258784861134719",
                "to": "Счет 74489636417521191160"
            },
            {
                "id": 895315941,
                "state": "EXECUTED",
                "date": "2018-08-19T04:27:37.904916",
                "operationAmount": {
                    "amount": "56883.54",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод с карты на карту",
                "from": "Visa Classic 6831982476737658",
                "to": "Visa Platinum 8990922113665229"
            },
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
                "operationAmount": {
                    "amount": "67314.70",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "from": "Visa Platinum 1246377376343588",
                "to": "Счет 14211924144426031657"
            }
        ]
    ]
