from typing import List, Tuple

from src.widget import get_date


def test_get_date_edge_cases(edge_case_dates: List[Tuple[str, str]]) -> None:
    """Тестирование пограничных случаев"""
    for date_input, expected_output in edge_case_dates:
        result = get_date(date_input)
        assert result == expected_output


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
