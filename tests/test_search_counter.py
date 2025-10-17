import re
import unittest
from unittest.mock import patch

from src.search_counter import count_operations_by_category_extended


class TestCountOperationsByCategoryExtended(unittest.TestCase):

    def test_basic_category_counting(self):
        """Тест базового подсчета по категориям"""
        data = [
            {"category": "food", "amount": 100},
            {"category": "transport", "amount": 200},
            {"category": "food", "amount": 300},
            {"category": "entertainment", "amount": 400},
        ]

        result = count_operations_by_category_extended(data)

        expected = {"food": 2, "transport": 1, "entertainment": 1}
        self.assertEqual(result, expected)

    def test_empty_data_list(self):
        """Тест с пустым списком данных"""
        result = count_operations_by_category_extended([])
        self.assertEqual(result, {})

    def test_operations_without_category(self):
        """Тест операций без поля category"""
        data = [
            {"amount": 100},
            {"category": "food", "amount": 200},
            {"currency": "USD"},
            {"category": "", "amount": 300},
        ]

        result = count_operations_by_category_extended(data)

        expected = {"food": 1, "other": 3}
        self.assertEqual(result, expected)

    def test_default_category_usage(self):
        """Тест использования категории по умолчанию"""
        data = [{"amount": 100}, {"category": "food", "amount": 200}, {"category": "", "amount": 300}]

        result = count_operations_by_category_extended(data, default_category="other")

        expected = {"food": 1, "other": 2}
        self.assertEqual(result, expected)

    def test_case_sensitivity(self):
        """Тест чувствительности к регистру категорий"""
        data = [
            {"category": "FOOD", "amount": 100},
            {"category": "food", "amount": 200},
            {"category": "Food", "amount": 300},
        ]

        result = count_operations_by_category_extended(data)

        expected = {"FOOD": 1, "food": 1, "Food": 1}
        self.assertEqual(result, expected)

    def test_none_category_values(self):
        """Тест с None значениями категорий"""
        data = [
            {"category": None, "amount": 100},
            {"category": "food", "amount": 200},
            {"category": "transport", "amount": 300},
        ]

        result = count_operations_by_category_extended(data)

        # None категории попадают в "other" по умолчанию
        expected = {"food": 1, "transport": 1, "other": 1}
        self.assertEqual(result, expected)

    def test_single_category_all_operations(self):
        """Тест когда все операции одной категории"""
        data = [
            {"category": "food", "amount": 100},
            {"category": "food", "amount": 200},
            {"category": "food", "amount": 300},
        ]

        result = count_operations_by_category_extended(data)

        expected = {"food": 3}
        self.assertEqual(result, expected)

    def test_mixed_data_types_in_category(self):
        """Тест с разными типами данных в поле category"""
        data = [
            {"category": "food", "amount": 100},
            {"category": "123", "amount": 200},
            {"category": "", "amount": 300},
            {"category": None, "amount": 400},
        ]

        result = count_operations_by_category_extended(data, default_category="other")

        # Число 123 конвертируется в строку "123"
        expected = {"food": 1, "123": 1, "other": 2}
        self.assertEqual(result, expected)

    def test_special_characters_in_category(self):
        """Тест специальных символов в категориях"""
        data = [
            {"category": "food & drinks", "amount": 100},
            {"category": "transport-urban", "amount": 200},
            {"category": "shopping@online", "amount": 300},
        ]

        result = count_operations_by_category_extended(data)

        expected = {"food & drinks": 1, "transport-urban": 1, "shopping@online": 1}
        self.assertEqual(result, expected)

    def test_unicode_characters_in_category(self):
        """Тест Unicode символов в категориях"""
        data = [
            {"category": "еда", "amount": 100},
            {"category": "транспорт", "amount": 200},
            {"category": "развлечения", "amount": 300},
        ]

        result = count_operations_by_category_extended(data)

        expected = {"еда": 1, "транспорт": 1, "развлечения": 1}
        self.assertEqual(result, expected)

    def test_empty_string_default_category(self):
        """Тест с пустой строкой как категорией по умолчанию"""
        data = [
            {"amount": 100},
            {"category": "food", "amount": 200},
        ]

        result = count_operations_by_category_extended(data, default_category="")

        expected = {"": 1, "food": 1}
        self.assertEqual(result, expected)

    def test_large_dataset_performance(self):
        """Тест производительности с большим объемом данных"""
        # Создаем 1000 операций с разными категориями
        data = []
        categories = ["food", "transport", "entertainment", "shopping", "utilities"]

        for i in range(1000):
            category = categories[i % len(categories)]
            data.append({"category": category, "amount": i})

        result = count_operations_by_category_extended(data)

        # Каждая категория должна встречаться 200 раз (1000 / 5)
        expected_counts = {category: 200 for category in categories}
        self.assertEqual(result, expected_counts)

    def test_complex_operations_structure(self):
        """Тест со сложной структурой операций"""
        data = [
            {"category": "food", "amount": 100, "currency": "USD", "date": "2024-01-01"},
            {"category": "transport", "amount": 200.50, "description": "Bus ticket"},
            {"category": "food", "amount": 300, "metadata": {"type": "restaurant"}},
            {"amount": 400, "notes": "No category provided"},
        ]

        result = count_operations_by_category_extended(data, default_category="uncategorized")

        expected = {"food": 2, "transport": 1, "uncategorized": 1}
        self.assertEqual(result, expected)

    def test_no_default_category_parameter(self):
        """Тест без указания default_category параметра"""
        data = [{"category": "food", "amount": 100}, {"amount": 200}]

        result = count_operations_by_category_extended(data)

        expected = {"food": 1, "other": 1}
        self.assertEqual(result, expected)


class TestCountOperationsByCategoryExtendedEdgeCases(unittest.TestCase):

    def test_only_operations_without_category(self):
        """Тест когда ни у одной операции нет категории"""
        data = [
            {"amount": 100},
            {"description": "Test", "amount": 200},
            {"currency": "USD", "amount": 300},
        ]

        result = count_operations_by_category_extended(data)
        self.assertEqual(result, {"other": 3})

    def test_only_operations_with_empty_category(self):
        """Тест когда у всех операций пустая категория"""
        data = [
            {"category": "", "amount": 100},
            {"category": "", "amount": 200},
            {"category": "", "amount": 300},
        ]

        result = count_operations_by_category_extended(data)
        self.assertEqual(result, {"other": 3})

    def test_mixed_none_and_empty_category(self):
        """Тест смеси None и пустых категорий"""
        data = [
            {"category": None, "amount": 100},
            {"category": "", "amount": 200},
            {"category": "food", "amount": 300},
        ]

        result = count_operations_by_category_extended(data)
        expected = {"food": 1, "other": 2}
        self.assertEqual(result, expected)

    def test_very_long_category_names(self):
        """Тест очень длинных названий категорий"""
        long_category = "Очень длинное название категории " * 10
        data = [
            {"category": long_category, "amount": 100},
            {"category": "short", "amount": 200},
        ]

        result = count_operations_by_category_extended(data)
        expected = {long_category: 1, "short": 1}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    # Запуск всех тестов
    unittest.main(verbosity=2)
