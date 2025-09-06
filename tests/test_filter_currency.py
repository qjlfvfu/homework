import pytest
from generators.filter_by_currency  import filter_by_currency


# Тестовые данные
transactions = [
    {
        "id": 939719570,
        "operationAmount": {
            "currency": {"code": "USD"}
        }
    },
    {
        "id": 142264268,
        "operationAmount": {
            "currency": {"code": "USD"}
        }
    },
    {
        "id": 873106923,
        "operationAmount": {
            "currency": {"code": "RUB"}
        }
    }
]


def test_filter_by_currency_usd_transactions():
    """Тест 1: Фильтрация USD транзакций через next()"""
    usd_transactions = filter_by_currency(transactions, "USD")

    transaction1 = next(usd_transactions)
    transaction2 = next(usd_transactions)

    assert transaction1["id"] == 939719570
    assert transaction2["id"] == 142264268
    assert transaction1["operationAmount"]["currency"]["code"] == "USD"
    assert transaction2["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_no_more_transactions():
    """Тест 2: Проверка остановки генератора"""
    usd_transactions = filter_by_currency(transactions, "USD")

    transaction1 = next(usd_transactions)
    transaction2 = next(usd_transactions)

    with pytest.raises(StopIteration):
        next(usd_transactions)



