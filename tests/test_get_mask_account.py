from src.masks import get_mask_account


def test_get_mask_account() -> None:
    """Тест маскировки счета"""
    result = get_mask_account('Счет 1234567890123456')
    assert result == 'Счет **3456'


def test_get_mask_account_short() -> None:
    """Тест маскировки короткого счета"""
    result = get_mask_account('Счет 123')
    assert result == 'Счет **3'


def test_get_mask_account_empty() -> None:
    """Тест маскировки пустой строки"""
    result = get_mask_account('')
    assert result == ''
