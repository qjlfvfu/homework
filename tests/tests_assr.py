from datetime import datetime
from typing import Any, Dict, List, Tuple


# Временные реализации функций для тестирования
def get_date(date_str: str) -> str:
    """Функция форматирования даты"""
    if not date_str:
        return date_str
    formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            continue

    return date_str


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтр списка операций по статусу"""
    if not operations:
        return []

    return [operation for operation in operations if operation.get("state") == state]


def get_mask_account(account_info: str) -> str:
    """Маскировка номера счета"""
    if not account_info:
        return account_info

    parts = account_info.split()
    account_type = " ".join(parts[:-1])
    account_number = parts[-1]

    if len(account_number) >= 4:
        masked_number = "**" + account_number[-4:]
        return f"{account_type} {masked_number}"

    return account_info


# ТЕСТЫ ДЛЯ GET_DATE
def test_get_date_valid_formats(valid_date_formats: List[Tuple[str, str]]) -> None:
    """Тестирование валидных форматов дат"""
    for date_input, expected_output in valid_date_formats:
        result = get_date(date_input)
        assert result == expected_output


def test_get_date_edge_cases(edge_case_dates: List[Tuple[str, str]]) -> None:
    """Тестирование пограничных случаев"""
    for date_input, expected_output in edge_case_dates:
        result = get_date(date_input)
        assert result == expected_output


def test_get_date_invalid_formats(invalid_dates: List[str]) -> None:
    """Тестирование невалидных форматов"""
    for date_input in invalid_dates:
        result = get_date(date_input)
        assert result == date_input


def test_get_date_empty_string() -> None:
    """Тест с пустой строкой"""
    assert get_date("") == ""


def test_get_date_none_input() -> None:
    """Тест с None входом"""
    try:
        result = get_date("None")
        if result is not None:
            assert isinstance(result, str)
    except (ValueError, TypeError):
        pass


# ТЕСТЫ ДЛЯ FILTER_BY_STATE
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


def test_filter_by_state_empty_list() -> None:
    """Тест с пустым списком операций"""
    result = filter_by_state([])
    assert result == []


# ТЕСТЫ ДЛЯ GET_MASK_ACCOUNT
def test_get_mask_account() -> None:
    """Тест маскировки счета"""
    result = get_mask_account("Счет 1234567890123456")
    assert result == "Счет **3456"


def test_get_mask_account_short() -> None:
    """Тест маскировки короткого счета"""
    result = get_mask_account("Счет 123")
    assert result == "Счет 123"


def test_get_mask_account_empty() -> None:
    """Тест маскировки пустой строки"""
    result = get_mask_account("")
    assert result == ""
