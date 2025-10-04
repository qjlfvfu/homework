from typing import Any, Dict, List


def count_operations_by_category_extended(
    data: List[Dict[str, Any]], default_category: str = "other"
) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям с расширенной логикой.

    Args:
        data: Список словарей с данными о банковских операциях
        default_category: Категория для операций без указанной категории

    Returns:
        Dict[str, int]: Словарь с количеством операций по категориям
    """
    if not data:
        return {}

    category_count = {}

    for operation in data:
        category = operation.get("category")

        # Если категория не указана, используем категорию по умолчанию
        if category is None or category == "":
            category = default_category

        category_count[category] = category_count.get(category, 0) + 1

    return category_count
