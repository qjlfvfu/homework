import os
import sys
import unittest
from typing import Any, Dict, List
from unittest.mock import mock_open, patch

import pytest

# Добавляем путь к корневой директории проекта для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем функции из src.main
from src.main import main, process_bank_operations
from src.process_bank_search import process_bank_search
from src.processing import filter_by_state, sort_by_date
from src.reader_scv_xlsx_files import reader_csv, reader_excel
from src.utils import load_transactions


# Тесты для функции process_bank_operations
class TestProcessBankOperations(unittest.TestCase):

    def test_process_bank_operations_basic(self):
        """Тест базовой функциональности подсчета операций по категориям"""
        transactions = [
            {"description": "Перевод денег", "amount": 100},
            {"description": "Оплата услуг", "amount": 200},
            {"description": "Покупка товаров", "amount": 300},
        ]

        categories = ["перевод", "оплата", "покупка"]
        result = process_bank_operations(transactions, categories)

        expected = {"перевод": 1, "оплата": 1, "покупка": 1}
        self.assertEqual(result, expected)

    def test_process_bank_operations_partial_matching(self):
        """Тест частичного совпадения слов"""
        data = [
            {"description": "Денежный перевод", "amount": 100},
            {"description": "Перевод между счетами", "amount": 200},
            {"description": "Оплата заказа", "amount": 300},
            {"description": "Оплата услуг", "amount": 400},
        ]

        categories = ["перевод", "оплата"]
        result = process_bank_operations(data, categories)

        expected = {"перевод": 2, "оплата": 2}
        self.assertEqual(result, expected)

    def test_process_bank_operations_case_insensitive(self):
        """Тест регистронезависимого поиска"""
        data = [
            {"description": "ПЕРЕВОД денег", "amount": 100},
            {"description": "денежный перевод", "amount": 200},
            {"description": "оплата счета", "amount": 300},
            {"description": "ОПЛАТА услуг", "amount": 400},
        ]

        categories = ["перевод", "оплата"]
        result = process_bank_operations(data, categories)

        expected = {"перевод": 2, "оплата": 2}
        self.assertEqual(result, expected)

    def test_process_bank_operations_empty_description(self):
        """Тест с пустыми описаниями"""
        data = [
            {"description": "", "amount": 100},
            {"description": "   ", "amount": 200},
            {"description": "Оплата услуг", "amount": 300},
        ]

        categories = ["перевод", "оплата"]
        result = process_bank_operations(data, categories)

        expected = {"оплата": 1, "другие": 2}
        self.assertEqual(result, expected)

    def test_process_bank_operations_no_description_key(self):
        """Тест транзакций без ключа description"""
        data = [
            {"amount": 100},
            {"description": "Оплата услуг", "amount": 200},
            {"amount": 300},
        ]

        categories = ["оплата"]
        result = process_bank_operations(data, categories)

        expected = {"оплата": 1, "другие": 2}
        self.assertEqual(result, expected)

    def test_process_bank_operations_all_other(self):
        """Тест когда все транзакции попадают в 'другие'"""
        data = [
            {"description": "Неизвестная операция", "amount": 100},
            {"description": "Другая операция", "amount": 200},
        ]

        categories = ["перевод", "оплата"]
        result = process_bank_operations(data, categories)

        expected = {"другие": 2}
        self.assertEqual(result, expected)

    def test_process_bank_operations_multiple_keywords(self):
        """Тест нескольких ключевых слов для одной категории"""
        data = [
            {"description": "Bank transfer", "amount": 100},
            {"description": "Перечисление средств", "amount": 200},
            {"description": "Международный перевод", "amount": 300},
        ]

        categories = ["перевод"]
        result = process_bank_operations(data, categories)

        expected = {"перевод": 3}
        self.assertEqual(result, expected)

    def test_process_bank_operations_special_characters(self):
        """Тест со специальными символами в описании"""
        data = [
            {"description": "Перевод!@#$%", "amount": 100},
            {"description": "Оплата-услуг", "amount": 200},
            {"description": "Покупка_товара", "amount": 300},
        ]

        categories = ["перевод", "оплата", "покупка"]
        result = process_bank_operations(data, categories)

        expected = {"перевод": 1, "оплата": 1, "покупка": 1}
        self.assertEqual(result, expected)


# Тесты для функции main с моками
class TestMainFunction(unittest.TestCase):

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_json_choice(self, mock_load, mock_input):
        """Тест выбора JSON файла"""
        # Мокируем ввод пользователя
        mock_input.side_effect = ["1", "EXECUTED", "нет", "нет", "нет"]

        # Мокируем загрузку данных
        mock_load.return_value = [
            {"date": "2024-01-01", "description": "Test", "amount": 100, "currency": "RUB", "state": "EXECUTED"}
        ]

        # Запускаем функцию
        main()

        # Проверяем вызовы
        mock_load.assert_called_once_with("operations.json")

    @patch("builtins.input")
    @patch("src.main.reader_csv")
    def test_main_csv_choice(self, mock_reader, mock_input):
        """Тест выбора CSV файла"""
        mock_input.side_effect = ["2", "EXECUTED", "нет", "нет", "нет"]
        mock_reader.return_value = [
            {"date": "2024-01-01", "description": "Test", "amount": 100, "currency": "RUB", "state": "EXECUTED"}
        ]

        main()
        mock_reader.assert_called_once_with("transactions.csv")

    @patch("builtins.input")
    @patch("src.main.reader_excel")
    def test_main_excel_choice(self, mock_reader, mock_input):
        """Тест выбора Excel файла"""
        mock_input.side_effect = ["3", "EXECUTED", "нет", "нет", "нет"]
        mock_reader.return_value = [
            {"date": "2024-01-01", "description": "Test", "amount": 100, "currency": "RUB", "state": "EXECUTED"}
        ]

        main()
        mock_reader.assert_called_once_with("transactions.xlsx")

    @patch("builtins.input")
    def test_main_invalid_choice(self, mock_input):
        """Тест неверного выбора файла"""
        mock_input.return_value = "5"  # Неверный выбор

        # Должен завершиться без ошибок
        main()

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_empty_result(self, mock_load, mock_input):
        """Тест пустого результата загрузки"""
        mock_input.return_value = "1"
        mock_load.return_value = []  # Пустой результат

        # Должен завершиться без ошибок
        main()

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_state_filtering(self, mock_load, mock_input):
        """Тест фильтрации по статусу"""
        mock_input.side_effect = ["1", "PENDING", "нет", "нет", "нет"]

        mock_load.return_value = [
            {"date": "2024-01-01", "description": "Test1", "amount": 100, "currency": "RUB", "state": "PENDING"},
            {"date": "2024-01-02", "description": "Test2", "amount": 200, "currency": "USD", "state": "EXECUTED"},
        ]

        main()

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_no_matching_state(self, mock_load, mock_input):
        """Тест когда нет операций с выбранным статусом"""
        mock_input.side_effect = ["1", "CANCELED", "нет", "нет", "нет"]

        mock_load.return_value = [
            {"date": "2024-01-01", "description": "Test", "amount": 100, "currency": "RUB", "state": "EXECUTED"}
        ]

        # Должен завершиться без ошибок
        main()

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_sort_ascending(self, mock_load, mock_input):
        """Тест сортировки по возрастанию"""
        mock_input.side_effect = ["1", "EXECUTED", "да", "по возрастанию", "нет", "нет"]

        mock_load.return_value = [
            {"date": "2024-01-02", "description": "Test2", "amount": 200, "currency": "RUB", "state": "EXECUTED"},
            {"date": "2024-01-01", "description": "Test1", "amount": 100, "currency": "RUB", "state": "EXECUTED"},
        ]

        main()

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_sort_descending(self, mock_load, mock_input):
        """Тест сортировки по убыванию"""
        mock_input.side_effect = ["1", "EXECUTED", "да", "по убыванию", "нет", "нет"]

        mock_load.return_value = [
            {"date": "2024-01-01", "description": "Test1", "amount": 100, "currency": "RUB", "state": "EXECUTED"},
            {"date": "2024-01-02", "description": "Test2", "amount": 200, "currency": "RUB", "state": "EXECUTED"},
        ]

        main()

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_rub_filter(self, mock_load, mock_input):
        """Тест фильтрации рублевых транзакций"""
        mock_input.side_effect = ["1", "EXECUTED", "нет", "да", "нет"]

        mock_load.return_value = [
            {"date": "2024-01-01", "description": "Test1", "amount": 100, "currency": "RUB", "state": "EXECUTED"},
            {"date": "2024-01-02", "description": "Test2", "amount": 200, "currency": "USD", "state": "EXECUTED"},
        ]

        main()

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_no_rub_transactions(self, mock_load, mock_input):
        """Тест когда нет рублевых транзакций"""
        mock_input.side_effect = ["1", "EXECUTED", "нет", "да"]

        mock_load.return_value = [
            {"date": "2024-01-01", "description": "Test", "amount": 100, "currency": "USD", "state": "EXECUTED"}
        ]

        # Должен завершиться без ошибок
        main()

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    @patch("src.main.process_bank_search")
    def test_main_word_search(self, mock_search, mock_load, mock_input):
        """Тест поиска по слову"""
        mock_input.side_effect = ["1", "EXECUTED", "нет", "нет", "да", "перевод"]

        mock_load.return_value = [
            {"date": "2024-01-01", "description": "Test", "amount": 100, "currency": "RUB", "state": "EXECUTED"}
        ]

        mock_search.return_value = [
            {
                "date": "2024-01-01",
                "description": "Денежный перевод",
                "amount": 100,
                "currency": "RUB",
                "state": "EXECUTED",
            }
        ]

        main()
        mock_search.assert_called_once()

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_empty_word_search(self, mock_load, mock_input):
        """Тест поиска с пустым словом"""
        mock_input.side_effect = ["1", "EXECUTED", "нет", "нет", "да", ""]

        mock_load.return_value = [
            {"date": "2024-01-01", "description": "Test", "amount": 100, "currency": "RUB", "state": "EXECUTED"}
        ]

        main()

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_no_transactions_after_filters(self, mock_load, mock_input):
        """Тест когда после фильтров не осталось транзакций"""
        mock_input.side_effect = ["1", "EXECUTED", "нет", "нет", "да", "несуществующееслово"]

        mock_load.return_value = [
            {"date": "2024-01-01", "description": "Test", "amount": 100, "currency": "RUB", "state": "EXECUTED"}
        ]

        # Должен завершиться без ошибок
        main()


# Тесты для обработки исключений
class TestMainExceptions(unittest.TestCase):

    @patch("builtins.input")
    @patch("src.main.load_transactions")
    def test_main_exception_handling(self, mock_load, mock_input):
        """Тест обработки исключений при загрузке данных"""
        mock_input.return_value = "1"
        mock_load.side_effect = Exception("File not found")

        # Должен обработать исключение и завершиться
        main()


# Тесты для edge cases категорий
class TestCategoryEdgeCases(unittest.TestCase):

    def test_process_bank_operations_mixed_categories(self):
        """Тест смешанных категорий в одном описании"""
        data = [
            {"description": "Перевод для оплаты услуг", "amount": 100},
            {"description": "Оплата перевода", "amount": 200},
        ]

        categories = ["перевод", "оплата"]
        result = process_bank_operations(data, categories)

        # Должна быть найдена только первая категория (перевод)
        expected = {"перевод": 2}
        self.assertEqual(result, expected)

    def test_process_bank_operations_none_values(self):
        """Тест с None значениями"""
        data = [
            {"description": None, "amount": 100},
            {"description": "Оплата услуг", "amount": 200},
        ]

        categories = ["оплата"]
        result = process_bank_operations(data, categories)

        expected = {"оплата": 1, "другие": 1}
        self.assertEqual(result, expected)


# Тесты для полного покрытия process_bank_operations
class TestFullCoverage(unittest.TestCase):

    def test_process_bank_operations_all_categories(self):
        """Тест всех доступных категорий"""
        data = [
            {"description": "перевод", "amount": 100},
            {"description": "оплата", "amount": 200},
            {"description": "покупка", "amount": 300},
            {"description": "снятие", "amount": 400},
            {"description": "пополнение", "amount": 500},
            {"description": "возврат", "amount": 600},
            {"description": "другая операция", "amount": 700},
        ]

        categories = ["перевод", "оплата", "покупка", "снятие", "пополнение", "возврат"]
        result = process_bank_operations(data, categories)

        expected = {"перевод": 1, "оплата": 1, "покупка": 1, "снятие": 1, "пополнение": 1, "возврат": 1, "другие": 1}
        self.assertEqual(result, expected)


# Запуск всех тестов
if __name__ == "__main__":
    unittest.main()
