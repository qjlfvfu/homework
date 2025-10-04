import unittest
from unittest.mock import patch

from src.masks import get_mask_account, get_mask_card_number
from src.widget import get_date, mask_account_card


class TestGetDate(unittest.TestCase):
    def test_date_with_milliseconds(self):
        """Тест даты с миллисекундами"""
        date_str = "2023-12-31T23:59:59.999"
        result = get_date(date_str)
        self.assertEqual(result, "31.12.2023")

    def test_date_without_milliseconds(self):
        """Тест даты без миллисекунд"""
        date_str = "2023-12-31T23:59:59"
        result = get_date(date_str)
        self.assertEqual(result, "31.12.2023")

    def test_date_only(self):
        """Тест только даты (без времени)"""
        date_str = "2023-12-31"
        result = get_date(date_str)
        self.assertEqual(result, "31.12.2023")

    def test_empty_string(self):
        """Тест пустой строки"""
        result = get_date("")
        self.assertEqual(result, "")

    def test_none_input(self):
        """Тест None на входе"""
        result = get_date(None)
        self.assertEqual(result, None)

    def test_invalid_date_format(self):
        """Тест некорректного формата даты"""
        date_str = "31/12/2023"  # Неподдерживаемый формат
        result = get_date(date_str)
        self.assertEqual(result, "31/12/2023")

    def test_partial_date_string(self):
        """Тест неполной строки даты"""
        date_str = "2023-12"  # Неполная дата
        result = get_date(date_str)
        self.assertEqual(result, "2023-12")

    def test_whitespace_string(self):
        """Тест строки с пробелами"""
        date_str = "  2023-12-31  "
        result = get_date(date_str)
        self.assertEqual(result, "  2023-12-31  ")

    def test_different_valid_formats(self):
        """Тест разных валидных форматов"""
        test_cases = [
            ("2024-01-15T10:30:45.123", "15.01.2024"),
            ("2024-01-15T10:30:45", "15.01.2024"),
            ("2024-01-15", "15.01.2024"),
        ]

        for input_date, expected in test_cases:
            with self.subTest(input_date=input_date):
                result = get_date(input_date)
                self.assertEqual(result, expected)


class TestMaskAccountCard(unittest.TestCase):
    def test_mask_account_lowercase(self):
        """Тест маскировки счета (нижний регистр)"""
        account_info = "счет 1234567890123456"
        result = mask_account_card(account_info)
        expected = get_mask_account(account_info)
        self.assertEqual(result, expected)

    def test_mask_account_uppercase(self):
        """Тест маскировки счета (верхний регистр)"""
        account_info = "СЧЕТ 1234567890123456"
        result = mask_account_card(account_info)
        expected = get_mask_account(account_info)
        self.assertEqual(result, expected)

    def test_mask_account_mixed_case(self):
        """Тест маскировки счета (смешанный регистр)"""
        account_info = "СчЕт 1234567890123456"
        result = mask_account_card(account_info)
        expected = get_mask_account(account_info)
        self.assertEqual(result, expected)

    def test_mask_account_starts_with(self):
        """Тест маскировки счета (начинается с 'счет')"""
        account_info = "счет1234567890123456"
        result = mask_account_card(account_info)
        expected = get_mask_account(account_info)
        self.assertEqual(result, expected)

    def test_mask_card_number(self):
        """Тест маскировки номера карты"""
        account_info = "Visa Platinum 1234567890123456"
        result = mask_account_card(account_info)
        expected = get_mask_card_number(account_info)
        self.assertEqual(result, expected)

    def test_mask_card_number_with_spaces(self):
        """Тест маскировки номера карты с пробелами"""
        account_info = "MasterCard 1234 5678 9012 3456"
        result = mask_account_card(account_info)
        expected = get_mask_card_number(account_info)
        self.assertEqual(result, expected)

    def test_mask_card_special_characters(self):
        """Тест маскировки карты со специальными символами"""
        account_info = "Visa-1234567890123456"
        result = mask_account_card(account_info)
        expected = get_mask_card_number(account_info)
        self.assertEqual(result, expected)

    def test_empty_string(self):
        """Тест пустой строки"""
        account_info = ""
        try:
            result = mask_account_card(account_info)
            self.assertIsInstance(result, str)
        except Exception as e:
            self.fail(f"Функция упала на пустой строке: {e}")

    def test_only_word_account(self):
        """Тест только слова 'счет'"""
        account_info = "счет"
        result = mask_account_card(account_info)
        expected = get_mask_account(account_info)
        self.assertEqual(result, expected)

    def test_only_word_card(self):
        """Тест только названия карты"""
        account_info = "Visa"
        result = mask_account_card(account_info)
        expected = get_mask_card_number(account_info)
        self.assertEqual(result, expected)

    def test_whitespace_handling(self):
        """Тест обработки пробелов"""
        test_cases = [
            ("  счет 1234567890123456  ", get_mask_account),
            ("счет  1234567890123456", get_mask_account),
            ("  Visa  1234567890123456  ", get_mask_card_number),
        ]

        for account_info, expected_function in test_cases:
            with self.subTest(account_info=account_info):
                result = mask_account_card(account_info)
                expected = expected_function(account_info)
                self.assertEqual(result, expected)


class TestIntegration(unittest.TestCase):
    def test_multiple_account_types(self):
        """Интеграционный тест разных типов счетов/карт"""
        test_cases = [
            ("счет 1234567890123456", get_mask_account),
            ("Счет 9876543210987654", get_mask_account),
            ("Visa Platinum 1234567890123456", get_mask_card_number),
            ("MasterCard 1234 5678 9012 3456", get_mask_card_number),
            ("Maestro 1234567890123456", get_mask_card_number),
            ("МИР 1234567890123456", get_mask_card_number),
        ]

        for account_info, expected_function in test_cases:
            with self.subTest(account_info=account_info):
                result = mask_account_card(account_info)
                expected = expected_function(account_info)
                self.assertEqual(result, expected)


class TestEdgeCases(unittest.TestCase):
    def test_none_input_mask_function(self):
        """Тест None на входе функции маскировки"""
        try:
            result = mask_account_card(None)
            self.assertIsInstance(result, str)
        except Exception as e:
            self.fail(f"Функция упала на None: {e}")

    def test_very_long_account_number(self):
        """Тест очень длинного номера счета"""
        account_info = "счет " + "1" * 50
        result = mask_account_card(account_info)
        expected = get_mask_account(account_info)
        self.assertEqual(result, expected)

    def test_very_long_card_number(self):
        """Тест очень длинного номера карты"""
        account_info = "Visa " + "1" * 50
        result = mask_account_card(account_info)
        expected = get_mask_card_number(account_info)
        self.assertEqual(result, expected)

    def test_special_characters_in_account_name(self):
        """Тест специальных символов в названии счета/карты"""
        test_cases = [
            ("счёт 1234567890123456", get_mask_card_number),
            ("account 1234567890123456", get_mask_card_number),
            ("карта 1234567890123456", get_mask_card_number),
        ]

        for account_info, expected_function in test_cases:
            with self.subTest(account_info=account_info):
                result = mask_account_card(account_info)
                expected = expected_function(account_info)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
