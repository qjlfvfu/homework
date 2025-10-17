from src.utils import load_transactions


def test_utils_work():
    if __name__ == "__main__":
        # Загрузка транзакций из файла
        transactions = load_transactions("data/operations.json")
        print(f"Загружено транзакций: {len(transactions)}")


def test_utils_load():
    if __name__ == "__main__":
        transactions = load_transactions("data/operations.json")
        print(f" Первые 3 транзакции:{transactions[:3]}")
