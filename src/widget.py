from datetime import datetime
from typing import Callable

from src.masks import get_mask_account, get_mask_card_number


def get_date(date_str: str) -> str:
    """Функция форматирования даты с поддержкой разных форматов"""
    if not date_str:
        return date_str
    # Список поддерживаемых форматов
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",  # Формат с миллисекундами: 2023-12-31T23:59:59.999
        "%Y-%m-%dT%H:%M:%S",  # Формат без миллисекунд: 2023-12-31T23:59:59
        "%Y-%m-%d",  # Только дата: 2023-12-31
    ]
    # Пробуем распарсить дату в каждом формате
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            continue
    # Если ни один формат не подошел, возвращаем исходную строку
    return date_str


def mask_account_card(account_info: str) -> str | Callable[[str], str]:
    """Функция считывает информацию о счете\карте маскируя их по разному"""
    if "счет" in account_info.lower() or account_info.lower().startswith("счет"):
        # Используем функцию для маскировки счета
        return get_mask_account(account_info)
    else:
        return get_mask_card_number
