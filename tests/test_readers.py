from unittest.mock import Mock, patch
import pandas as pd
import pytest
import sys
import os

# Добавляем путь к src в sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.reader_scv_xlsx_files import reader_csv, reader_excel
from src.decorators import init_html_log, log


class TestReaderFunctions:
    """Тесты для функций чтения CSV и Excel"""

    def test_reader_csv_basic(self):
        """Базовый тест reader_csv"""
        with patch('src.reader_scv_xlsx_files.pd.read_csv') as mock_read_csv:
            # Создаем mock DataFrame
            mock_df = Mock()
            mock_df.to_dict.return_value = [
                {"amount": 100.50, "currency": "USD", "description": "Purchase"},
                {"amount": 2500.00, "currency": "RUB", "description": "Payment"},
            ]
            mock_read_csv.return_value = mock_df

            # Вызываем функцию
            result = reader_csv("transactions.csv")

            # Проверяем вызовы
            mock_read_csv.assert_called_once_with("transactions.csv")
            mock_df.to_dict.assert_called_once_with("records")

            # Проверяем результат
            expected = [
                {"amount": 100.50, "currency": "USD", "description": "Purchase"},
                {"amount": 2500.00, "currency": "RUB", "description": "Payment"},
            ]
            assert result == expected

    def test_reader_csv_empty(self):
        """Тест reader_csv с пустым файлом"""
        with patch('src.reader_scv_xlsx_files.pd.read_csv') as mock_read_csv:
            mock_df = Mock()
            mock_df.to_dict.return_value = []
            mock_read_csv.return_value = mock_df

            result = reader_csv("empty.csv")

            assert result == []
            assert isinstance(result, list)

    def test_reader_excel_basic(self):
        """Базовый тест reader_excel"""
        with patch('src.reader_scv_xlsx_files.pd.read_excel') as mock_read_excel:
            mock_df = Mock()
            mock_df.to_dict.return_value = [
                {"amount": 50.00, "currency": "EUR", "description": "Coffee"},
                {"amount": 150.75, "currency": "USD", "description": "Lunch"},
            ]
            mock_read_excel.return_value = mock_df

            result = reader_excel("transactions.xlsx")

            mock_read_excel.assert_called_once_with("transactions.xlsx")
            mock_df.to_dict.assert_called_once_with("records")

            expected = [
                {"amount": 50.00, "currency": "EUR", "description": "Coffee"},
                {"amount": 150.75, "currency": "USD", "description": "Lunch"},
            ]
            assert result == expected

    def test_reader_csv_with_real_dataframe(self):
        """Тест с реальным DataFrame"""
        with patch('src.reader_scv_xlsx_files.pd.read_csv') as mock_read_csv:
            # Создаем реальный DataFrame
            test_df = pd.DataFrame({
                'amount': [100.50, 200.75],
                'currency': ['USD', 'EUR'],
                'description': ['Item1', 'Item2']
            })
            mock_read_csv.return_value = test_df

            result = reader_csv("test.csv")

            expected = [
                {'amount': 100.50, 'currency': 'USD', 'description': 'Item1'},
                {'amount': 200.75, 'currency': 'EUR', 'description': 'Item2'}
            ]
            assert result == expected

    def test_reader_excel_multiple_rows(self):
        """Тест reader_excel с несколькими строками"""
        with patch('src.reader_scv_xlsx_files.pd.read_excel') as mock_read_excel:
            mock_df = Mock()
            mock_df.to_dict.return_value = [
                {"amount": 10.0, "currency": "USD"},
                {"amount": 20.0, "currency": "EUR"},
                {"amount": 30.0, "currency": "GBP"},
                {"amount": 40.0, "currency": "RUB"},
            ]
            mock_read_excel.return_value = mock_df

            result = reader_excel("multiple.xlsx")

            assert len(result) == 4
            assert all("amount" in item for item in result)
            assert all("currency" in item for item in result)


class TestReaderFunctionsWithLogging:
    """Тесты с логированием"""

    @log(filename="log_file_readers_test.html")
    def test_reader_csv_with_logging(self):
        """Тест reader_csv с логированием"""
        with patch('src.reader_scv_xlsx_files.pd.read_csv') as mock_read_csv:
            mock_df = Mock()
            mock_df.to_dict.return_value = [
                {'amount': 100.50, 'currency': 'USD', 'description': 'Purchase'}
            ]
            mock_read_csv.return_value = mock_df

            result = reader_csv("transactions.csv")

            mock_read_csv.assert_called_once_with("transactions.csv")
            assert len(result) == 1
            return "Тест reader_csv с логированием пройден"

    @log(filename="log_file_readers_test.html")
    def test_reader_excel_with_logging(self):
        """Тест reader_excel с логированием"""
        with patch('src.reader_scv_xlsx_files.pd.read_excel') as mock_read_excel:
            mock_df = Mock()
            mock_df.to_dict.return_value = [
                {'amount': 200.75, 'currency': 'EUR', 'description': 'Coffee'}
            ]
            mock_read_excel.return_value = mock_df

            result = reader_excel("transactions.xlsx")

            mock_read_excel.assert_called_once_with("transactions.xlsx")
            assert len(result) == 1
            return "Тест reader_excel с логированием пройден"


def run_simple_test():
    """Простой тест для быстрой проверки"""
    with patch('src.reader_scv_xlsx_files.pd.read_csv') as mock_read:
        mock_df = Mock()
        mock_df.to_dict.return_value = [{'test': 'data'}]
        mock_read.return_value = mock_df

        result = reader_csv("test.csv")
        print("✓ reader_csv работает")

    with patch('src.reader_scv_xlsx_files.pd.read_excel') as mock_read:
        mock_df = Mock()
        mock_df.to_dict.return_value = [{'test': 'data'}]
        mock_read.return_value = mock_df

        result = reader_excel("test.xlsx")
        print("✓ reader_excel работает")


if __name__ == "__main__":
    # Для быстрой проверки
    run_simple_test()

    # Для запуска с логированием
    init_html_log("test_file_readers_test.html")
    print("Запуск тестов с логированием...")

    # Создаем экземпляр и запускаем тесты с логированием
    test_class = TestReaderFunctionsWithLogging()
    test_class.test_reader_csv_with_logging()
    test_class.test_reader_excel_with_logging()

    print("Тесты завершены!")