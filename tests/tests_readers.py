import pytest
import pandas as pd
import os
from unittest.mock import patch, Mock
from src.reader_scv_xlsx_files import reader_csv,reader_excel
from src.decorators import log, write_log,close_html_log,init_html_log


@log(filename="log_file_readers_test.html")
def test_files_exist():
    """Проверка существования файлов"""
    assert os.path.exists("transactions.csv"), "Файл transactions.csv не найден"
    assert os.path.exists("transactions_excel.xlsx"), "Файл transactions_excel.xlsx не найден"
    return "Файлы существуют"

@log(filename="log_file_readers_test.html")
def test_reader_csv():
    df=reader_csv()
    print(df)


@log(filename="log_file_readers_test.html")
def test_reader_xlsx():
    with patch('src.external_api.pd.read_excel') as mock_read_excel:
        mock_df = Mock()
        mock_read_excel.return_value = mock_df
        result = reader_excel()
        # Проверяем вызов
        mock_read_excel.assert_called_once_with("transactions_excel.xlsx")

        return "Тест пройден успешно"


@log(filename="log_file_readers_test.html")
def test_reader_xlsx():
    result=reader_excel()
    try:
        return result
    except Exception as e:
        print(f"Ошибка {e}")

@log(filename="log_file_readers_test.html")
def test_reader_excel_print_output():
    """Тест проверяет, что функция выводит DataFrame"""
    with patch('pandas.read_excel') as mock_read_excel, \
            patch('builtins.print') as mock_print:
        # Создаем mock DataFrame
        mock_df = Mock()
        mock_read_excel.return_value = mock_df

        # Вызываем функцию
        reader_excel()

        # Проверяем вызовы
        mock_read_excel.assert_called_once_with("transactions_excel.xlsx")
        mock_print.assert_called_once_with(mock_df)


if __name__ == "__main__":
    # Инициализируем HTML лог
    init_html_log("test_file_readers_test.html")
    print("Запуск тестов с логированием...")