import os
from typing import Any

import requests
from retry import retry

API_KEY = os.getenv("API_KEY")


@retry(exceptions=(ValueError, ConnectionError), tries=4, delay=2)
def convert_currency(amount: float, from_currency: str, to_currency: str) -> Any:
    """
    Конвертирует сумму из одной валюты в другую через API.

    Args:
        amount (float): сумма для конвертации
        from_currency (str): исходная валюта (например, 'USD', 'EUR', 'RUB')
        to_currency (str): целевая валюта (например, 'RUB', 'USD', 'EUR')

    Returns:
        float: конвертированная сумма
    """

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"

    payload: dict[str, Any] = {}
    headers = {"apikey": "dRqlRls7sqb8Qtbmqo8abG2skNv6gwwt"}

    try:
        response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()

        result = response.json()

        if result.get("success", False):
            return float(result["result"])
        else:
            print(f"Ошибка API: {result.get('error', {}).get('info', 'Unknown error')}")
            return float(amount)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return float(amount)


def convert_from_rub(amount: float, to_currency: str) -> Any:
    """
    Конвертирует сумму из рублей в указанную валюту через API.

    Args:
        amount (float): сумма в рублях для конвертации
        to_currency (str): целевая валюта ('USD', 'EUR')

    Returns:
        float: конвертированная сумма
    """
    if to_currency not in ["USD", "EUR"]:
        print(f"Валюта {to_currency} не поддерживается для конвертации из RUB")
        return float(amount)

    return convert_currency(amount, "RUB", to_currency)


def convert_to_rub(transaction: Any) -> Any:
    """
    Конвертирует сумму транзакции в рубли.
    """
    amount = transaction["amount"]
    currency = transaction["currency"]

    if currency == "RUB":
        return float(amount)

    if currency in ["USD", "EUR"]:
        return convert_currency(amount, currency, "RUB")

    return float(amount)
