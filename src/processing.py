from collections import Counter
from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтр списка операций по статусу"""
    if not operations:
        return []

    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате.
    Args:
        data: Список словарей с операциями
        reverse: Если True - сортировка по убыванию, False - по возрастанию
    Returns:
        List[Dict[str, Any]]: Отсортированный список операций
    """
    if not data:
        return []

    def get_date_key(operation: Dict[str, Any]) -> datetime:
        """Извлекает дату из операции и преобразует в datetime объект"""
        date_str = operation.get("date", "")
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            # Если дата в неправильном формате, возвращаем минимальную дату
            return datetime.min

    # Сортируем операции по дате
    sorted_data = sorted(data, key=get_date_key, reverse=reverse)

    return sorted_data


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчет операций по категориям"""
    if not data or not categories:
        return {}

    # Собираем все описания
    descriptions = [op.get("description", "").lower() for op in data]

    # Считаем вхождения каждой категории
    category_counts = {}
    for category in categories:
        category_lower = category.lower()
        count = sum(1 for desc in descriptions if category_lower in desc)
        category_counts[category] = count

    return category_counts
