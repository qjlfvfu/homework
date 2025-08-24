from typing import List, Dict, Any


def filter_by_state(
    operations: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """Фильтр списка по операциям
    Args:
    operations: Список
    словарей сданными операций state: Статус для фильтрации(по умолчанию' EXECUTED ')

    Returns:
    operation_list: Отфильтрованный список операций"""
    operation_list: List[Dict[str, Any]] = []
    if not operations:
        return operation_list
    for operation in operations:
        if state == "EXECUTED":
            operation_list.append(operation)
    return operation_list


def sort_by_date(get_date, sorting: str = "убывание"):
    """Сортировка списка дат по убыванию\возрастанию с выводом нового списка дат"""
    sorted_date = []
    if "убывание" in sorting:
        sorted_date = get_date.sort(reverse=True)
    else:
        sorted_date = get_date.sort()
    return sorted_date
