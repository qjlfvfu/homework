from typing import Any, Dict, Generator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency_code: str
) -> Generator[Dict[str, Any], None, None]:
    """
    Генератор, который фильтрует транзакции по коду валюты.
    Поочередно выдает транзакции, где валюта операции соответствует заданной.
    """
    for transaction in transactions:
        # Получаем валюту операции из вложенной структуры
        operation_amount = transaction.get("operationAmount", {})
        currency = operation_amount.get("currency", {})

        # Проверяем соответствие кода валюты
        if currency.get("code") == currency_code:
            yield transaction
