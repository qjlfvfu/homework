import os
import re
from typing import Any

from src.process_bank_search import process_bank_search
from src.processing import filter_by_state, sort_by_date
from src.reader_scv_xlsx_files import reader_csv, reader_excel
from src.utils import load_transactions


def process_bank_operations(transactions: list, categories: list) -> dict:
    """
    Подсчитывает операции по категориям на основе ключевых слов в описании.

    Args:
        transactions: Список транзакций
        categories: Список категорий для поиска

    Returns:
        dict: Статистика по категориям
    """
    # Инициализируем статистику для всех категорий и "другие"
    category_stats = {category: 0 for category in categories}
    category_stats["другие"] = 0

    category_keywords = {
        "перевод": ["перевод", "transfer", "перечисление"],
        "оплата": ["оплата", "payment", "платеж"],
        "покупка": ["покупка", "purchase", "buy", "купить"],
        "снятие": ["снятие", "withdrawal", "cash", "наличные"],
        "пополнение": ["пополнение", "deposit", "пополнить"],
        "возврат": ["возврат", "refund", "возврат средств"],
    }

    for transaction in transactions:
        description = transaction.get("description", "")
        if not isinstance(description, str) or not description.strip():
            category_stats["другие"] += 1
            continue

        description = description.lower()
        category_found = False

        for category, keywords in category_keywords.items():
            if any(keyword in description for keyword in keywords):
                category_stats[category] += 1
                category_found = True
                break

        if not category_found:
            category_stats["другие"] += 1

    # Убираем категории с нулевым количеством операций
    return {k: v for k, v in category_stats.items() if v > 0}


def main():
    """Основная функция программы для работы с банковскими транзакциями"""
    print(
        """
    Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.
    Выберите пункт меню:
    1. Получить информацию о транзакциях из JSON-файла
    2. Получить информацию о транзакциях из CSV-файла
    3. Получить информацию о транзакциях из XLSX-файла
    """
    )

    # Выбираем тип файла для транзакции
    choice = input("Выберите пункт меню: ")
    result = None

    if choice not in ["1", "2", "3"]:
        print("Неверный ввод. Завершение программы.")
        return
    try:
        if choice == "1":
            result = load_transactions("operations.json")  # в корне проекта
        elif choice == "2":
            result = reader_csv("transactions.csv")  # в корне проекта
        elif choice == "3":
            result = reader_excel("transactions.xlsx")  # в корне проекта
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return

    # Проверяем результат
    if not result:
        print("Программа: Не удалось загрузить данные или файл пуст.")
        return

    print(f"Загружено операций: {len(result)}")

    # Фильтруем операции по статусу
    states = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print(
            """
    Введите статус, по которому необходимо выполнить фильтрацию.
    Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING
        """
        )
        state_input = input("Статус: ").upper()

        if state_input in states:
            print(f"Операции отфильтрованы по статусу '{state_input}'")
            break
        else:
            print(f"Статус операции '{state_input}' недоступен.")

    # Фильтруем по статусу
    filtered_state = filter_by_state(result, state=state_input)

    if not filtered_state:
        print("Нет операций с выбранным статусом.")
        return

    print(f"Найдено операций с статусом '{state_input}': {len(filtered_state)}")

    # Уточняем фильтрацию
    final_transactions = filtered_state.copy()

    # Сортировка по дате
    while True:
        print("\nОтсортировать операции по дате? Да/Нет")
        date_input = input("Да/Нет: ").upper()

        if date_input in ["ДА", "YES", "Y", "НЕТ", "NO", "N"]:
            break
        print("Пожалуйста введите Да или Нет")

    if date_input in ["ДА", "YES", "Y"]:
        while True:
            print("\nОтсортировать по возрастанию или по убыванию?")
            sorting_input = input("по возрастанию/по убыванию: ").lower()

            if sorting_input in ["по возрастанию", "по убыванию"]:
                break
            print("Пожалуйста введите 'по возрастанию' или 'по убыванию'")

        reverse = sorting_input == "по убыванию"
        final_transactions = sort_by_date(final_transactions, reverse)
        order = "убыванию" if reverse else "возрастанию"
        print(f"Операции отсортированы по дате в порядке {order}")

    # Фильтрация по валюте
    while True:
        print("\nВыводить только рублевые транзакции? Да/Нет")
        transaction_input = input("Да/Нет: ").upper()

        if transaction_input in ["ДА", "YES", "Y", "НЕТ", "NO", "N"]:
            break
        print("Пожалуйста введите Да или Нет")

    if transaction_input in ["ДА", "YES", "Y"]:
        rub_transactions = [t for t in final_transactions if t.get("currency") == "RUB"]
        if not rub_transactions:
            print("Не найдено рублевых транзакций.")
            return
        final_transactions = rub_transactions
        print(f"Оставлено рублевых транзакций: {len(final_transactions)}")

    # Фильтрация по слову с использованием process_bank_search
    while True:
        print("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет")
        transaction_word_input = input("Да/Нет: ").upper()

        if transaction_word_input in ["ДА", "YES", "Y", "НЕТ", "NO", "N"]:
            break
        print("Пожалуйста введите Да или Нет")

    if transaction_word_input in ["ДА", "YES", "Y"]:
        print("\nВведите слово для поиска в описании:")
        filter_word = input("Слово: ").strip()

        if filter_word:
            # Используем функцию process_bank_search с регулярными выражениями
            searched_transactions = process_bank_search(final_transactions, filter_word)

            if not searched_transactions:
                print(f"Не найдено транзакций со словом '{filter_word}' в описании.")
                return

            final_transactions = searched_transactions
            print(f"Найдено транзакций с словом '{filter_word}': {len(final_transactions)}")
        else:
            print("Слово для поиска не введено.")

    # Подсчет категорий операций
    print("\n" + "=" * 50)
    print("ПОДСЧЕТ ОПЕРАЦИЙ ПО КАТЕГОРИЯМ")
    print("=" * 50)

    categories = ["перевод", "оплата", "покупка", "снятие", "пополнение", "возврат"]
    category_stats = process_bank_operations(final_transactions, categories)

    if category_stats:
        print("Статистика по категориям операций:")
        for category, count in category_stats.items():
            print(f"  {category.capitalize()}: {count} операций")
    else:
        print("Не удалось определить категории операций")

    # Вывод финальных результатов
    print("\n" + "=" * 50)
    print("ИТОГОВЫЙ СПИСОК ТРАНЗАКЦИЙ")
    print("=" * 50)

    if not final_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(final_transactions)}\n")

        for i, transaction in enumerate(final_transactions, 1):
            date = transaction.get("date", "Дата не указана")
            description = transaction.get("description", "Описание отсутствует")
            amount = transaction.get("amount", "")
            currency = transaction.get("currency", "")
            status = transaction.get("state", "")

            print(f"{i}. {date} - {description}")
            print(f"   Сумма: {amount} {currency}")
            if status:
                print(f"   Статус: {status}")
            print()


if __name__ == "__main__":
    main()
