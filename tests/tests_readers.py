from unittest.mock import Mock, patch

from src.decorators import init_html_log, log
from src.reader_scv_xlsx_files import reader_csv, reader_excel


@log(filename="log_file_readers_test.html")
def test_reader_csv_basic():
    """Базовый тест reader_csv"""
    with patch("pandas.read_csv") as mock_read_csv:
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


@log(filename="log_file_readers_test.html")
def test_reader_csv_empty():
    """Тест reader_csv с пустым файлом"""
    with patch("pandas.read_csv") as mock_read_csv:
        mock_df = Mock()
        mock_df.to_dict.return_value = []
        mock_read_csv.return_value = mock_df

        result = reader_csv("empty.csv")

        assert result == []
        assert isinstance(result, list)


@log(filename="log_file_readers_test.html")
def test_reader_excel_basic():
    """Базовый тест reader_excel"""
    with patch("pandas.read_excel") as mock_read_excel:
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


@log(filename="log_file_readers_test.html")
def test_reader_excel_different_columns():
    """Тест reader_excel с разными колонками"""
    with patch("pandas.read_excel") as mock_read_excel:
        mock_df = Mock()
        mock_df.to_dict.return_value = [
            {"sum": 100, "curr": "USD", "date": "2024-01-01"},
            {"sum": 200, "curr": "EUR", "date": "2024-01-02"},
        ]
        mock_read_excel.return_value = mock_df

        result = reader_excel("different.xlsx")

        expected = [
            {"sum": 100, "curr": "USD", "date": "2024-01-01"},
            {"sum": 200, "curr": "EUR", "date": "2024-01-02"},
        ]
        assert result == expected


@log(filename="log_file_readers_test.html")
def test_reader_excel_multiple_rows():
    """Тест reader_excel с несколькими строками"""
    with patch("pandas.read_excel") as mock_read_excel:
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


if __name__ == "__main__":
    # Инициализируем HTML лог
    init_html_log("test_file_readers_test.html")
    print("Запуск тестов с логированием...")
