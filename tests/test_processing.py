import unittest
from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, process_bank_operations, sort_by_date


def test_filter_by_state(test_operations: List[Dict[str, Any]]) -> None:
    """Тест фильтрации операций по статусу EXECUTED"""
    result = filter_by_state(test_operations, "EXECUTED")
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


def test_filter_by_state_pending(test_operations: List[Dict[str, Any]]) -> None:
    """Тест фильтрации операций по статусу PENDING"""
    result = filter_by_state(test_operations, "PENDING")
    assert len(result) == 1
    assert result[0]["state"] == "PENDING"


def test_filter_by_state_unknown(test_operations: List[Dict[str, Any]]) -> None:
    """Тест фильтрации по несуществующему статусу"""
    result = filter_by_state(test_operations, "UNKNOWN")
    assert len(result) == 0


def test_filter_by_state_default(test_operations: List[Dict[str, Any]]) -> None:
    """Тест фильтрации со значением по умолчанию"""
    result = filter_by_state(test_operations)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


class TestSortByDate(unittest.TestCase):

    def test_invalid_date_format(self):
        """Тест с некорректным форматом даты"""
        data = [
            {"date": "2024-01-15", "amount": 100},
            {"date": "invalid-date", "amount": 200},
            {"date": "2024-01-10", "amount": 300},
        ]

        result = sort_by_date(data)

        # Текущая реализация: 'invalid-date' считается как строка и идет ПЕРВОЙ
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["date"], "invalid-date")  # Некорректная дата первая (как строка)
        self.assertEqual(result[1]["date"], "2024-01-10")  # Затем валидные даты
        self.assertEqual(result[2]["date"], "2024-01-15")

    def test_mixed_date_formats(self):
        """Тест с разными форматами дат"""
        data = [
            {"date": "15.01.2024", "amount": 100},  # другой формат
            {"date": "2024-01-10", "amount": 200},
            {"date": "2024-01-20", "amount": 300},
        ]

        result = sort_by_date(data)

        # Текущая реализация: '15.01.2024' считается как строка и идет ПЕРВОЙ
        self.assertEqual(result[0]["date"], "15.01.2024")  # Другой формат первый (как строка)
        self.assertEqual(result[1]["date"], "2024-01-10")  # Затем валидные даты
        self.assertEqual(result[2]["date"], "2024-01-20")

    def test_operations_without_date(self):
        """Тест операций без даты"""
        data = [
            {"amount": 100},  # нет date
            {"date": "2024-01-15", "amount": 200},
            {"amount": 300},  # нет date
        ]

        result = sort_by_date(data)

        # Текущая реализация: операции без даты идут ПЕРВЫМИ (None < any string)
        self.assertEqual(len(result), 3)
        self.assertNotIn("date", result[0])  # Первый элемент без даты
        self.assertNotIn("date", result[1])  # Второй элемент без даты
        self.assertEqual(result[2]["date"], "2024-01-15")  # Элемент с датой ПОСЛЕДНИЙ

    def test_sort_string_dates(self):
        """Тест сортировки дат как строк"""
        data = [
            {"date": "2024-02-01", "amount": 100},
            {"date": "2024-01-15", "amount": 200},
            {"date": "2023-12-01", "amount": 300},
        ]

        result = sort_by_date(data)

        # Текущая реализация: сортировка как строк (лексикографическая)
        self.assertEqual(result[0]["date"], "2023-12-01")  # Первая по алфавиту
        self.assertEqual(result[1]["date"], "2024-01-15")
        self.assertEqual(result[2]["date"], "2024-02-01")


class TestProcessBankOperations(unittest.TestCase):

    def test_partial_word_matching(self):
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

    def test_case_insensitive_partial_matching(self):
        """Тест регистронезависимого совпадения"""
        data = [
            {"description": "ПЕРЕВОД денег", "amount": 100},
            {"description": "денежный перевод", "amount": 200},
            {"description": "оплата счета", "amount": 300},
            {"description": "ОПЛАТА услуг", "amount": 400},
        ]

        categories = ["перевод", "оплата"]
        result = process_bank_operations(data, categories)

        # Текущая реализация регистронезависимости
        expected = {"перевод": 2, "оплата": 2}
        self.assertEqual(result, expected)
