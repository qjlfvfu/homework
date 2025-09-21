import os
from typing import Any, Optional

import requests
from dotenv import load_dotenv

# Загрузка API ключа
load_dotenv(".env")
API_KEY = os.getenv("API_KEY")


def convert_currency(from_curr: str, to_currs: Any, date: Optional[str] = None) -> Any:
    """
    Конвертирует валюту
    :param amount: сумма вводимая пользователем
    :param from_curr: из валюты (RUB)
    :param to_currs: в валюты вводимую пользователем (USD, EUR)
    :param date: дата (опционально)
    """
    url = "https://api.apilayer.com/currency_data/convert"
    headers = {"apikey": API_KEY}
    try:
        amount = float(input("Введите сумму которую хотите конвертировать в Рублях"))
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        return None

    params = {"amount": amount, "from": from_curr, "to": to_currs}

    if date:
        params["date"] = date

    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None
