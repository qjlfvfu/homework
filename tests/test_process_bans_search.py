from src.decorators import init_html_log, log
from src.process_bank_search import process_bank_search


@log(filename="log_file_search_bank.html")
def test_process_bank_search_basic():
    """Тест базового поиска подстроки в описании"""
    test_data = [
        {"amount": 100, "currency": "USD", "description": "Coffee shop purchase"},
        {"amount": 200, "currency": "EUR", "description": "Grocery store"},
        {"amount": 50, "currency": "GBP", "description": "Coffee with friends"},
    ]

    result = process_bank_search(test_data, "coffee")

    # Проверяем что найдено 2 операции с 'coffee' в описании
    assert len(result) == 2
    # Проверяем что все найденные операции содержат 'coffee' (без учета регистра)
    assert all("coffee" in op["description"].lower() for op in result)
    # Проверяем суммы найденных операций
    assert {op["amount"] for op in result} == {100, 50}


@log(filename="log_file_search_bank.html")
def test_process_bank_search_case_insensitive():
    """Тест поиска без учета регистра"""
    test_data = [
        {"amount": 100, "description": "COFFEE SHOP"},
        {"amount": 200, "description": "coffee machine"},
        {"amount": 300, "description": "Café"},
    ]

    result = process_bank_search(test_data, "Coffee")

    # Должны найти обе операции с разным регистром
    assert len(result) == 2
    assert {op["amount"] for op in result} == {100, 200}


@log(filename="log_file_search_bank.html")
def test_process_bank_search_no_matches():
    """Тест когда нет совпадений"""
    test_data = [
        {"amount": 100, "description": "Restaurant bill"},
        {"amount": 200, "description": "Supermarket shopping"},
        {"amount": 300, "description": "Gas station"},
    ]

    result = process_bank_search(test_data, "coffee")

    # Не должно быть найдено ни одной операции
    assert result == []


@log(filename="log_file_search_bank.html")
def test_process_bank_search_with_regex_pattern():
    """Тест поиска с использованием регулярных выражений"""
    test_data = [
        {"amount": 100, "description": "Payment #12345 completed"},
        {"amount": 200, "description": "Transfer #ABCDE failed"},
        {"amount": 300, "description": "Refund #67890 processed"},
    ]

    # Ищем операции с номерами (цифры после #)
    result = process_bank_search(test_data, r"#\d+")

    # Должны найти только операции с цифрами после #
    assert len(result) == 2
    assert {op["amount"] for op in result} == {100, 300}
    # Проверяем что описания содержат цифры после #
    assert all(
        "#" in op["description"] and any(char.isdigit() for char in op["description"].split("#")[1]) for op in result
    )


if __name__ == "__main__":
    # Инициализируем HTML лог
    init_html_log("log_file_search_bank.html")
    print("Запуск тестов с логированием...")
