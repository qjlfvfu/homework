from typing import List, Dict, Any
from src.processing import filter_by_state

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