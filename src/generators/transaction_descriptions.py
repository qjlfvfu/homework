from typing import Any, Dict, Generator, List, Optional


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[Optional[str], None, None]:
    """Фильтр списка по описанию транзакции"""
    try:
        for transaction in transactions:
            description = transaction.get("description")
            yield description
    except Exception as e:
        print(f"Ошибка при обработке транзакций: {e}")
        # Генератор автоматически вызовет StopIteration при выходе из функции
