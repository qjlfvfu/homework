# src/processing.py
from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтр списка операций по статусу"""
    if not operations:
        return []

    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(get_date: Any, sorting: Any = "убывание") -> List[Any]:
    """Сортировка списка дат по убыванию\возрастанию с выводом нового списка дат"""
    sorted_date = []
    if "убывание" in sorting:
        sorted_date = get_date.sort(reverse=True)
    else:
        sorted_date = get_date.sort()
    return sorted_date
