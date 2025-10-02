import unittest
from unittest.mock import patch
import re
from src.search_counter import process_bank_search  # правильный импорт


class TestProcessBankSearch100Coverage(unittest.TestCase):

    def test_basic_search_success(self):
        """Тест базового успешного поиска - ИСПРАВЛЕННЫЙ"""
        data = [
            {'description': 'Кофе Starbucks', 'amount': 100},
            {'description': 'Обед в кафе', 'amount': 200},
            {'description': 'Покупка в магазине', 'amount': 300}
        ]

        # "кафе" есть только в 'Обед в кафе'
        result = process_bank_search(data, 'кафе')

        self.assertEqual(len(result), 1)  # ИСПРАВЛЕНО: был 2, теперь 1
        self.assertEqual(result[0]['description'], 'Обед в кафе')

    def test_case_insensitive_search(self):
        """Тест поиска без учета регистра"""
        data = [
            {'description': 'COFFEE SHOP', 'amount': 100},
            {'description': 'coffee machine', 'amount': 200},
            {'description': 'TEA HOUSE', 'amount': 300}
        ]

        result = process_bank_search(data, 'Coffee')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['description'], 'COFFEE SHOP')
        self.assertEqual(result[1]['description'], 'coffee machine')

    def test_regex_search(self):
        """Тест поиска с использованием регулярных выражений"""
        data = [
            {'description': 'Payment #12345', 'amount': 100},
            {'description': 'Transfer #ABCDE', 'amount': 200},
            {'description': 'Refund #67890', 'amount': 300}
        ]

        result = process_bank_search(data, r'#\d+')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['description'], 'Payment #12345')
        self.assertEqual(result[1]['description'], 'Refund #67890')

    def test_no_matches_found(self):
        """Тест когда совпадений не найдено"""
        data = [
            {'description': 'Ресторан', 'amount': 100},
            {'description': 'Супермаркет', 'amount': 200}
        ]

        result = process_bank_search(data, 'кофе')

        self.assertEqual(result, [])

    def test_empty_data_list(self):
        """Тест с пустым списком данных"""
        result = process_bank_search([], 'кофе')

        self.assertEqual(result, [])

    def test_empty_search_string(self):
        """Тест с пустой строкой поиска"""
        data = [
            {'description': 'Кофе', 'amount': 100}
        ]

        result = process_bank_search(data, '')

        self.assertEqual(result, [])

    def test_none_search_string(self):
        """Тест с None строкой поиска"""
        data = [
            {'description': 'Кофе', 'amount': 100}
        ]

        result = process_bank_search(data, None)

        self.assertEqual(result, [])

    def test_operations_without_description(self):
        """Тест операций без поля description"""
        data = [
            {'amount': 100},  # нет description
            {'description': 'Кофе', 'amount': 200},
            {'currency': 'USD'}  # нет description
        ]

        result = process_bank_search(data, 'кофе')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['description'], 'Кофе')

    def test_description_not_string(self):
        """Тест когда description не строка"""
        data = [
            {'description': 12345, 'amount': 100},  # число
            {'description': None, 'amount': 200},  # None
            {'description': ['кофе', 'кафе'], 'amount': 300},  # список
            {'description': 'Кофе Starbucks', 'amount': 400}  # строка
        ]

        result = process_bank_search(data, 'кофе')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['description'], 'Кофе Starbucks')

    def test_special_characters_in_search(self):
        """Тест специальных символов в поиске"""
        data = [
            {'description': 'Café Paris', 'amount': 100},
            {'description': 'Price $100.50', 'amount': 200},
            {'description': 'Order #123-ABC', 'amount': 300}
        ]

        result1 = process_bank_search(data, 'Café')
        result2 = process_bank_search(data, r'\$100\.50')
        result3 = process_bank_search(data, r'#123-ABC')

        self.assertEqual(len(result1), 1)
        self.assertEqual(len(result2), 1)
        self.assertEqual(len(result3), 1)

    def test_multiple_matches_in_description(self):
        """Тест когда слово 'кофе' есть в нескольких описаниях"""
        data = [
            {'description': 'Утренний кофе', 'amount': 100},
            {'description': 'Кофе с друзьями', 'amount': 200},
            {'description': 'Обед в кафе', 'amount': 300}  # тут "кафе", а не "кофе"
        ]

        result = process_bank_search(data, 'кофе')

        self.assertEqual(len(result), 2)  # Только первые две
        self.assertEqual(result[0]['description'], 'Утренний кофе')
        self.assertEqual(result[1]['description'], 'Кофе с друзьями')

    def test_exact_match_required(self):
        """Тест что поиск ищет подстроку, а не точное совпадение"""
        data = [
            {'description': 'Кофе Starbucks', 'amount': 100},
            {'description': 'Кофе', 'amount': 200},
            {'description': 'Кафешка', 'amount': 300}  # "кафе" != "кофе"
        ]

        result = process_bank_search(data, 'кофе')

        self.assertEqual(len(result), 2)  # Первые две
        self.assertEqual(result[0]['description'], 'Кофе Starbucks')
        self.assertEqual(result[1]['description'], 'Кофе')

    def test_mixed_data_types(self):
        """Тест с разными типами данных в операциях"""
        data = [
            {'description': 'Кофе', 'amount': 100, 'currency': 'RUB', 'date': '2024-01-01'},
            {'description': 'Обед', 'amount': 200.50, 'currency': 'USD', 'status': 'completed'},
            {'description': 'Ужин', 'amount': 300, 'metadata': {'type': 'food'}}
        ]

        result = process_bank_search(data, 'кофе')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['description'], 'Кофе')
        self.assertEqual(result[0]['amount'], 100)

    @patch('src.search_counter.re.search')
    def test_re_search_called_correctly(self, mock_search):
        """Тест что re.search вызывается правильно"""
        mock_search.return_value = True  # Всегда возвращаем True

        data = [{'description': 'Тест', 'amount': 100}]
        process_bank_search(data, 'тест')

        # Проверяем что re.search был вызван с правильными аргументами
        mock_search.assert_called_once_with('тест', 'Тест', re.IGNORECASE)

    def test_performance_with_large_data(self):
        """Тест производительности с большим объемом данных"""
        # Создаем 1000 операций
        data = [{'description': f'Операция {i}', 'amount': i} for i in range(1000)]
        # Добавляем несколько операций с искомым словом
        data.extend([
            {'description': 'Кофе утром', 'amount': 1001},
            {'description': 'Кофе вечером', 'amount': 1002}
        ])

        result = process_bank_search(data, 'кофе')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['description'], 'Кофе утром')
        self.assertEqual(result[1]['description'], 'Кофе вечером')


class TestProcessBankSearchEdgeCases(unittest.TestCase):

    def test_unicode_characters(self):
        """Тест Unicode символов"""
        data = [
            {'description': 'Café ☕', 'amount': 100},
            {'description': 'Ресторан 🍽️', 'amount': 200}
        ]

        result = process_bank_search(data, '☕')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['description'], 'Café ☕')

    def test_very_long_description(self):
        """Тест очень длинного описания"""
        long_description = 'Очень длинное описание операции ' * 10 + 'кофе в конце'
        data = [{'description': long_description, 'amount': 100}]

        result = process_bank_search(data, 'кофе')

        self.assertEqual(len(result), 1)

    def test_search_pattern_at_different_positions(self):
        """Тест поиска в разных позициях строки"""
        data = [
            {'description': 'кофе в начале', 'amount': 100},
            {'description': 'в середине кофе тоже', 'amount': 200},
            {'description': 'в конце кофе', 'amount': 300}
        ]

        result = process_bank_search(data, 'кофе')

        self.assertEqual(len(result), 3)

    def test_empty_string_description(self):
        """Тест с пустой строкой в description"""
        data = [
            {'description': '', 'amount': 100},
            {'description': 'Кофе', 'amount': 200}
        ]

        result = process_bank_search(data, 'кофе')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['description'], 'Кофе')


if __name__ == '__main__':
    # Запуск всех тестов
    unittest.main(verbosity=2)