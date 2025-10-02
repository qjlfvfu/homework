from typing import Any, Dict, List
from collections import Counter

def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтр списка операций по статусу"""
    if not operations:
        return []

    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(get_date: Any, sorting: Any = "убывание") -> Any:
    """Сортировка списка дат по убыванию\возрастанию с выводом нового списка дат"""
    sorted_date = [""]
    if "убывание" in sorting:
        sorted_date = get_date.sort(reverse=True)
    else:
        sorted_date = get_date.sort()
    return sorted_date


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчет операций по категориям"""
    if not data or not categories:
        return {}

    # Собираем все описания
    descriptions = [op.get('description', '').lower() for op in data]

    # Считаем вхождения каждой категории
    category_counts = {}
    for category in categories:
        category_lower = category.lower()
        count = sum(1 for desc in descriptions if category_lower in desc)
        category_counts[category] = count

    return category_counts