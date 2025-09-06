from generators.transaction_descriptions import transaction_descriptions
from typing import List,Dict,Any

transactions = [
    {
        "id": 939719570,
        "transaction":" ",
        "operationAmount": {
            "currency": {"code": "USD"}
        }
    },
    {
        "id": 142264268,
        "transaction":"обед деда",
        "operationAmount": {
            "currency": {"code": "USD"}
        }
    },
    {
        "id": 873106923,
        "transaction":"Перечисления банка",
        "operationAmount": {
            "currency": {"code": "RUB"}
        }
    }
]


def test_transaction_work():
    descriptions = transaction_descriptions(transactions)
    for _ in range(3):
        print(next(descriptions))
