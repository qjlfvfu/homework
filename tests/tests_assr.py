import pytest
from datetime import datetime
from typing import List, Dict, Any, Tuple
from src.masks import get_mask_card_number
from src.masks import get_mask_account
from src.widget import get_date
from src.processing import filter_by_state


def test_get_mask_card_number():
    assert get_mask_card_number ( '1234567891011126' ) == '1234 56** **** 1126'


def test_get_mask_account():
    assert get_mask_account('Счет 12345678900987') == ('Счет **0987')


def test_get_date(valid_dates):
    """Тест форматирования даты с фикстурой"""
    for date_input, expected_output in valid_dates:
        result = get_date(date_input)
        assert result == expected_output
def test_get_date_valid_formats(valid_date_formats: List[Tuple[str, str]]):
    """Тестирование валидных форматов дат с фикстурой"""
    for date_input, expected_output in valid_date_formats:
        result = get_date(date_input)
        assert result == expected_output, f"Ошибка для {date_input}: ожидалось {expected_output}, получено {result}"

def test_get_date_edge_cases(edge_case_dates: List[Tuple[str, str]]):
    """Тестирование пограничных случаев с фикстурой"""
    for date_input, expected_output in edge_case_dates:
         result = get_date(date_input)
         assert result == expected_output, f"Ошибка для {date_input}: ожидалось {expected_output}, получено {result}"

def test_get_date_invalid_formats(invalid_dates: List[str]):
     """Тестирование невалидных форматов с фикстурой"""
     for date_input in invalid_dates:
        result = get_date(date_input)
        # Для невалидных форматов должна возвращаться исходная строка
        assert result == date_input, f"Для невалидной даты {date_input} ожидалось {date_input}, получено {result}"

def test_get_date_datetime_formats(datetime_formats: List[Tuple[str, str]]):
    """Тестирование разных форматов datetime с фикстурой"""
    for date_input, expected_output in datetime_formats:
        result = get_date(date_input)
        assert result == expected_output, f"Ошибка для {date_input}: ожидалось {expected_output}, получено {result}"

def test_get_date_empty_string():
    """Тест с пустой строкой"""
    assert get_date('') == ''

def test_get_date_none_input():
     """Тест с None входом"""
    # Ожидаем, что функция вернет None или выбросит исключение
     try:
         result = get_date(None)
         # Если функция обрабатывает None, проверяем результат
         if result is not None:
            assert isinstance(result, str)
     except (ValueError, TypeError):
         # Исключение - допустимое поведение
         pass


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтр списка операций по статусу"""
    if not operations:
        return []

    return [operation for operation in operations if operation.get('state') == state]


def test_filter_by_state_empty_list():
    """Тестирование с пустым списком операций"""
    result = filter_by_state([])
    assert result == []


def test_filter_by_state_operations_without_state(operations_without_state):
    """Тестирование операций без поля state с фикстурой"""
    result = filter_by_state(operations_without_state, 'EXECUTED')
    assert len(result) == 1
    assert result[0]['id'] == 2

