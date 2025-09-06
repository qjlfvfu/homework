from typing import List,Dict,Any


def transaction_descriptions(transactions: List[Dict[str,Any]]) ->  Any:
    """Фильтр списка по описанию транзакции"""
    for transaction in transactions:
        transactions=[{"id":"id","transaction":transaction,"currency":"currency"}]
        description=transaction.get("transaction",transaction)
        yield description