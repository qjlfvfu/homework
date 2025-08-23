from datetime import datetime
from typing import Callable

from masks import get_mask_account , get_mask_card_number


def get_date(date_str):
    """Функция превращает вводимую дату в форматированную"""
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    # Форматируем datetime в строку с нужным форматом
    return dt.strftime("%d.%m.%Y")


def mask_account_card(account_info: str) -> str | Callable[[str], str]:
    """Функция считывает информацию о счете\карте маскируя их по разному"""
    if "счет" in account_info.lower() or account_info.lower().startswith("счет"):
        # Используем функцию для маскировки счета
        return get_mask_account(account_info)
    else:
        return get_mask_card_number
