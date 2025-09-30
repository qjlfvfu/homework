import re
from typing import List, Dict, Any


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Фильтрует список банковских операций по строке поиска в описании.
    Использует регулярные выражения для поиска подстроки в описании.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка для поиска в описании операций

    Returns:
        List[Dict[str, Any]]: Отфильтрованный список операций,
                             где в описании найдена строка поиска
    """
    if not data or not search:
        return []

    filtered_operations = []

    for operation in data:
        description = operation.get('description')
        if isinstance(description, str):
            if re.findall(search, description, re.IGNORECASE):
                filtered_operations.append(operation)

    return filtered_operations