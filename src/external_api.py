import os
from typing import Any, Optional
import requests


API_KEY = os.getenv("API_KEY")



def convert_currency(from_curr: str, to_currs: Any, date: Optional[str] = None) -> Any:
    """
    Конвертирует валюту
    :param amount: сумма вводимая пользователем
    :param from_curr: из валюты (RUB)
    :param to_currs: в валюты вводимую пользователем (USD, EUR)
    :param date: дата (опционально)
    """

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={from_curr}&from={to_currs}&amount=1"

    payload = {}
    headers = {
        "apikey": API_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    status_code = response.status_code
    result = response.text
    return result if status_code == 200 else status_code
